import customtkinter as ct
import pyotp
import os
import pickle
import pyperclip
import threading
import time

from const import CONFIG_PATH
from utils import now_second


class MFACode(ct.CTkFrame):
    def __init__(self, master, change_content_fnc, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.threads = []
        self.in_progress = True

        if os.path.exists(CONFIG_PATH):
            config = pickle.load(open(CONFIG_PATH, 'rb'))
            if config['token']:
                self.totp = pyotp.TOTP(config['token'])
                self.frame = ct.CTkFrame(self, corner_radius=10)
                self.frame.grid_columnconfigure(0, weight=1)
                self.code_frame = ct.CTkFrame(self.frame, corner_radius=10)
                self.code_frame.grid_rowconfigure(1, weight=1)
                self.timebar = ct.CTkProgressBar(
                    self.code_frame, width=self.code_frame.winfo_width())
                self.timebar.grid(row=0, column=0, columnspan=2, sticky="nsew")
                self.innerframe = ct.CTkFrame(self.code_frame, corner_radius=6)
                self.code = ct.CTkLabel(
                    self.innerframe, text='******', font=ct.CTkFont('Lucida Console', size=50))
                self.code.grid(row=0, column=0, padx=10, pady=7)
                self.innerframe.grid(row=1, column=0, padx=10, pady=5)
                self.copy_button = ct.CTkButton(
                    self.code_frame, text='コピー', command=lambda: pyperclip.copy(self.totpcode))
                self.copy_button.grid(row=1, column=1, padx=5, pady=5)
                self.code_frame.grid(row=0, padx=1, pady=(6, 6))
                self.frame.grid(row=0, padx=1, pady=(0, 6), sticky="ew")

                th = threading.Thread(target=self.thread_fnc)
                th.setDaemon(True)
                self.threads.append(th)
                th.start()
                return

        self.frame = ct.CTkFrame(self, corner_radius=10)
        self.frame.grid_columnconfigure(0, weight=1)
        self.tips = ct.CTkLabel(
            self.frame, text='この機能を利用するには，設定の「ユーザー情報」からトークンを設定してください')
        self.tips.grid(row=0, column=0, pady=6, sticky='ew')
        self.config_button = ct.CTkButton(
            self.frame, text='設定', width=80, command=lambda: change_content_fnc('config'))
        self.config_button.grid(row=1, column=0, padx=10)
        self.frame.grid(row=0, padx=1, pady=(0, 6), sticky="nsew")

    def update_code(self):
        self.totpcode = self.totp.now()
        s = now_second()
        bar_value = (30 - (s % 30)) / 30
        self.timebar.set(bar_value)
        self.code.configure(text=self.totpcode)

    def thread_fnc(self):
        time.sleep(0.5)
        while self.in_progress:
            self.update_code()

    def destroy_this(self):
        self.in_progress = False
        for th in self.threads:
            th.join()
        self.destroy()
