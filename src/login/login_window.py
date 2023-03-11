import customtkinter as ct
import tkinter as tk
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
        thread.start()
        self.after_process(res)

    def login_process(self, username, password, totp, res):
        self.message.configure(text='ログイン処理中...', text_color=('black', 'white'))
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-logging')
        options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service()
        service.creation_flags = CREATE_NO_WINDOW
        driver = webdriver.Chrome(options=options, service=service)
        driver.get("https://www.cle.osaka-u.ac.jp/")
        driver.find_element(By.XPATH, "//*[@id=\"loginsaml\"]").click()
        if (len(driver.find_elements(By.XPATH, "//*[@id=\"USER_ID\"]"))):
            driver.find_element(By.XPATH, "//*[@id=\"USER_ID\"]").send_keys(username)
            driver.find_element(By.XPATH, "//*[@id=\"USER_PASSWORD\"]").send_keys(password)
            driver.find_element(By.XPATH, "/html/body/table/tbody/tr[3]/td/table/tbody/tr[5]/td/table/tbody/tr/td[2]/div/input").click()
        if (len(driver.find_elements(By.XPATH, "/html/body/form/table/tbody/tr/td/div[2]/h1"))):
            res[0] = 'info-error'
            driver.quit()
            return
        if (len(driver.find_elements(By.XPATH, "//*[@id=\"OTP_CODE\"]"))):
            driver.find_element(By.XPATH, "//*[@id=\"OTP_CODE\"]").send_keys(totp)
            driver.find_element(By.XPATH, "//*[@id=\"STORE_OTP_AUTH_RESULT\"]").click()
            driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[3]/td/table/tbody/tr[7]/td/div/button").click()
        if (len(driver.find_elements(By.XPATH, "/html/body/form/table/tbody/tr/td/div[2]/h1"))):
            res[0] = 'totp-error'
            driver.quit()
            return
        if (len(driver.find_elements(By.XPATH, "/html/body/form/table[2]/tbody/tr[4]/td[1]/input"))):
            driver.find_element(By.XPATH, "/html/body/form/table[2]/tbody/tr[4]/td[1]/input").click()
            driver.find_element(By.XPATH, "//*[@id=\"ok\"]").click()
        os.makedirs(CACHE_DIR, exist_ok=True)
        pickle.dump(driver.get_cookies(), open(COOKIES_PATH, 'wb'))
        driver.quit()
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
        self.destroy()
        exit()
