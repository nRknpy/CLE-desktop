import customtkinter as ct
import tkinter as tk
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from subprocess import CREATE_NO_WINDOW
import requests
import pickle
import os
import threading

from const import COOKIES_PATH, CACHE_DIR
from api import get_userinfo

class LoginWindow(ct.CTkToplevel):
    def __init__(self, *args, userid=None, password=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.threads = []
        self.driver = None
        self.geometry("400x400")
        self.resizable(False, False)
        self.title('Login')
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.grid_rowconfigure(1, weight=1)

        self.login_label = ct.CTkLabel(self, text='ログイン', font=(ct.CTkFont('MSゴシック'), 20))
        self.login_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.frame = ct.CTkFrame(master=self, width=300, height=300)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.frame.grid_rowconfigure(5, weight=1)
        self.username_entry = ct.CTkEntry(master=self.frame, placeholder_text='大阪大学個人ID')
        self.username_entry.grid(row=0, column=0, padx=20, pady=5)
        self.password_entry = ct.CTkEntry(master=self.frame, placeholder_text='パスワード', show='*')
        self.password_entry.grid(row=1, column=0, padx=20, pady=5)
        self.totp_entry = ct.CTkEntry(master=self.frame, placeholder_text='認証コード')
        self.totp_entry.grid(row=2, column=0, padx=20, pady=5)
        self.message = ct.CTkLabel(self.frame, text='')
        self.message.grid(row=3, column=0, padx=20, pady=5)
        self.login_button = ct.CTkButton(master=self.frame, text='Login', command=self.login_button_click)
        self.login_button.bind("<Return>", lambda e: self.login_button_click())
        self.login_button.grid(row=4, column=0, padx=20, pady=10)
        
        if userid: self.username_entry.insert(tk.END, userid)
        if password: self.password_entry.insert(tk.END, password)
    
    def login_button_click(self):
        self.login_button.configure(state='disabled')
        username = self.username_entry.get()
        password = self.password_entry.get()
        totp = self.totp_entry.get()
        self.wait_bar = ct.CTkProgressBar(self, mode='indetermine', width=self.winfo_width())
        self.wait_bar.pack()
        self.wait_bar.start()
        res = [None]
        thread = threading.Thread(target=self.login_process, args=(username, password, totp, res))
        thread.setDaemon(True)
        self.threads.append(thread)
        thread.start()
        self.after_process(res)

    def login_process(self, username, password, totp, res):
        self.message.configure(text='ログイン処理中...', text_color=('black', 'white'))
        options = uc.ChromeOptions()
        options.add_argument('--headless=new')
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled" : False}
        options.add_experimental_option("prefs", prefs)
        self.driver = uc.Chrome(service_creationflags=CREATE_NO_WINDOW, options=options)
        self.driver.get("https://www.cle.osaka-u.ac.jp/")
        self.driver.find_element(By.XPATH, "//*[@id=\"loginsaml\"]").click()
        if (len(self.driver.find_elements(By.XPATH, "//*[@id=\"USER_ID\"]"))):
            self.driver.find_element(By.XPATH, "//*[@id=\"USER_ID\"]").send_keys(username)
            self.driver.find_element(By.XPATH, "//*[@id=\"USER_PASSWORD\"]").send_keys(password)
            self.driver.find_element(By.XPATH, "/html/body/table/tbody/tr[3]/td/table/tbody/tr[5]/td/table/tbody/tr/td[2]/div/input").click()
        if (len(self.driver.find_elements(By.XPATH, "/html/body/form/table/tbody/tr/td/div[2]/h1"))):
            res[0] = 'info-error'
            self.driver.quit()
            return
        if (len(self.driver.find_elements(By.XPATH, "//*[@id=\"OTP_CODE\"]"))):
            self.driver.find_element(By.XPATH, "//*[@id=\"OTP_CODE\"]").send_keys(totp)
            self.driver.find_element(By.XPATH, "//*[@id=\"STORE_OTP_AUTH_RESULT\"]").click()
            self.driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[3]/td/table/tbody/tr[7]/td/div/button").click()
        if (len(self.driver.find_elements(By.XPATH, "/html/body/form/table/tbody/tr/td/div[2]/h1"))):
            res[0] = 'totp-error'
            self.driver.quit()
            return
        if (len(self.driver.find_elements(By.XPATH, "/html/body/form/table[2]/tbody/tr[4]/td[1]/input"))):
            self.driver.find_element(By.XPATH, "/html/body/form/table[2]/tbody/tr[4]/td[1]/input").click()
            self.driver.find_element(By.XPATH, "//*[@id=\"ok\"]").click()
        os.makedirs(CACHE_DIR, exist_ok=True)
        pickle.dump(self.driver.get_cookies(), open(COOKIES_PATH, 'wb'))
        self.driver.quit()
        self.message.configure(text='ユーザー情報取得中...', text_color=('black', 'white'))
        user_id = get_userinfo()['id']
        self.message.configure(text='ユーザー情報保存中...', text_color=('black', 'white'))
        pickle.dump(user_id, open(os.path.join(CACHE_DIR, 'user-id.pkl'), 'wb'))
        res[0] = 'success'

    def after_process(self, res):
        if res[0] == 'success':
            self.quit()
            self.destroy()
            return
        if res[0] == 'info-error':
            self.message.configure(text='個人IDまたはパスワードに誤りがあります', text_color='red')
            self.login_button.configure(state='normal')
            self.wait_bar.destroy()
            return
        if res[0] == 'totp-error':
            self.message.configure(text='認証コードに誤りがあります', text_color='red')
            self.login_button.configure(state='normal')
            self.wait_bar.destroy()
            return
        self.after(10, self.after_process, res)

    def close_window(self):
        if self.driver != None:
            self.driver.quit()
        self.quit()
        self.destroy()
        if len(self.threads):
            for th in self.threads:
                th.join()
        os._exit(0)
