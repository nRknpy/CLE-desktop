import customtkinter as ct
import tkinter as tk
import threading
import pickle
import os
import sys
import webbrowser

from const import CACHE_DIR, CONFIG_PATH
from api import login_save


class Config(ct.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.threads = []
        self.grid_columnconfigure(0, weight=1)

        self.darkmode_frame = ct.CTkFrame(self, corner_radius=10)
        self.darkmode_frame.grid_columnconfigure(1, weight=1)
        self.darkmode_label = ct.CTkLabel(
            self.darkmode_frame, text='ダークモード:', width=400, anchor='e')
        self.darkmode_label.grid(row=0, column=0, pady=15)
        self.darkmode_switch = ct.CTkSwitch(
            self.darkmode_frame, width=500, text='')
        self.darkmode_switch.grid(row=0, column=1, pady=15)
        self.darkmode_frame.grid(row=0, padx=1, pady=(0, 6), sticky="nsew")

        self.theme_frame = ct.CTkFrame(self, corner_radius=10)
        self.theme_frame.grid_columnconfigure(1, weight=1)
        self.theme_label = ct.CTkLabel(
            self.theme_frame, text='カラーテーマ:', width=400, anchor='e')
        self.theme_label.grid(row=0, column=0, pady=15)
        self.theme_segbutton = ct.CTkSegmentedButton(self.theme_frame, width=500,
                                                     values=[
                                                         'blue', 'dark-blue', 'green'],
                                                     variable=ct.StringVar(value='blue'))
        self.theme_segbutton.grid(
            row=0, column=1, padx=40, pady=15, sticky='ew')
        self.theme_tips = ct.CTkLabel(self.theme_frame, width=500,
                                      text='テーマを変更するには，適用後にアプリの再起動が必要です')
        self.theme_tips.grid(row=1, column=1, padx=40, pady=15, sticky='ew')
        self.theme_frame.grid(row=1, padx=1, pady=(0, 6), sticky="nsew")

        self.userinfo_frame = ct.CTkFrame(self, corner_radius=10)
        self.userinfo_frame.grid_columnconfigure(1, weight=1)
        self.userinfo_frame.grid_rowconfigure(4, weight=1)
        self.rightframe = ct.CTkFrame(
            self.userinfo_frame, fg_color='transparent')
        self.rightframe.grid_rowconfigure(1, weight=1)
        self.rightframe.grid_columnconfigure(0, weight=1)
        self.userinfo_label = ct.CTkLabel(
            self.userinfo_frame, text='ユーザー情報:', width=400, anchor='ne')
        self.userinfo_label.grid(row=0, column=0)
        self.userid_label = ct.CTkLabel(
            self.rightframe, text='大阪大学個人ID:', width=10, anchor='e')
        self.userid_label.grid(row=0, column=0, padx=10)
        self.userid_entry = ct.CTkEntry(
            self.rightframe, placeholder_text='未設定')
        self.userid_entry.grid(row=0, column=1)
        self.password_label = ct.CTkLabel(
            self.rightframe, text='パスワード:', width=10, anchor='e')
        self.password_label.grid(row=1, column=0, padx=10)
        self.password_entry = ct.CTkEntry(
            self.rightframe, placeholder_text='未設定', show='*')
        self.password_entry.grid(row=1, column=1)
        self.token_label = ct.CTkLabel(
            self.rightframe, text='トークン:', width=10, anchor='e')
        self.token_label.grid(row=2, column=0, padx=10)
        self.token_entry = ct.CTkEntry(self.rightframe, placeholder_text='未設定')
        self.token_entry.grid(row=2, column=1)
        self.error_label = ct.CTkLabel(self.rightframe, text='')
        self.error_label.grid(row=3, column=0, columnspan=2, pady=5)
        self.tips_label = ct.CTkLabel(self.rightframe,
                                      text='「大阪大学個人ID」と「パスワード」を設定することで，ログイン時に自動的に入力されます．\n「トークン」を設定することで，ログイン作業を自動化できます．\n「トークン」は，下のボタンからMFAの再登録を行い，\n表示される「手動入力コード」を入力してください．')
        self.tips_label.grid(row=4, column=0, columnspan=2, pady=10)
        self.mfa_regist_button = ct.CTkButton(self.rightframe, text='MFA再登録', command=lambda: webbrowser.open(
            'https://auth-mfa.auth.osaka-u.ac.jp/AttributeRegistSite/MfaInfoServlet'))
        self.mfa_regist_button.grid(row=5, column=1, padx=5, sticky='e')
        self.rightframe.grid(row=0, column=1, pady=15)
        self.userinfo_frame.grid(row=2, padx=1, pady=(0, 6), sticky="nsew")

        self.buttons_frame = ct.CTkFrame(self, fg_color='transparent')
        self.default_button = ct.CTkButton(
            self.buttons_frame, text='リセット', width=80, command=self.set_default)
        self.default_button.grid(row=2, column=1, padx=10, sticky='e')
        self.apply_button = ct.CTkButton(
            self.buttons_frame, text='適用', width=80, command=self.apply_config)
        self.apply_button.grid(row=2, column=2, padx=10, sticky='e')
        self.buttons_frame.grid(row=3, padx=10, sticky='e')

        if os.path.exists(CONFIG_PATH):
            nowconfig = pickle.load(open(CONFIG_PATH, 'rb'))
            if nowconfig['darkmode']:
                self.darkmode_switch.select()
            else:
                self.darkmode_switch.deselect()

            self.theme_segbutton.set(nowconfig['theme'])

            if nowconfig['userid']:
                self.userid_entry.delete(0, tk.END)
                self.userid_entry.insert(tk.END, nowconfig['userid'])
            if nowconfig['password']:
                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(tk.END, nowconfig['password'])
            if nowconfig['token']:
                self.token_entry.delete(0, tk.END)
                self.token_entry.insert(tk.END, nowconfig['token'])

    def get_config(self):
        return dict(
            darkmode=self.darkmode_switch.get(),
            theme=self.theme_segbutton.get(),
            userid=None if not self.userid_entry.get() else self.userid_entry.get(),
            password=None if not self.password_entry.get() else self.password_entry.get(),
            token=None if not self.token_entry.get() else self.token_entry.get()
        )

    def apply_config(self):
        self.apply_button.configure(state='disabled', text='適用中...')
        newconfig = self.get_config()
        nowconfig = None
        if os.path.exists(CONFIG_PATH):
            nowconfig = pickle.load(open(CONFIG_PATH, 'rb'))
            if nowconfig == newconfig:
                self.apply_button.configure(state='normal', text='適用')
                return
            if (nowconfig['userid'], nowconfig['password'], nowconfig['token']) == (newconfig['userid'], newconfig['password'], newconfig['token']):
                if nowconfig['darkmode'] != newconfig['darkmode']:
                    ct.set_appearance_mode(
                        'dark' if newconfig['darkmode'] else 'light')
                if nowconfig['theme'] != newconfig['theme']:
                    ct.set_default_color_theme(newconfig['theme'])
                self.apply_button.configure(state='normal', text='適用')
                self.error_label.configure(text='')
                pickle.dump(newconfig, open(CONFIG_PATH, 'wb'))
                return
        th = threading.Thread(
            target=lambda: self.__apply_config(newconfig, nowconfig))
        th.setDaemon(True)
        self.threads.append(th)
        th.start()

    def __apply_config(self, newconfig, nowconfig):
        ct.set_appearance_mode('dark' if newconfig['darkmode'] else 'light')
        if not (newconfig['userid'] or newconfig['password'] or newconfig['token']):
            self.error_label.configure(text='')
            pickle.dump(newconfig, open(CONFIG_PATH, 'wb'))
            self.apply_button.configure(state='normal', text='適用')
            return
        if newconfig['userid'] and newconfig['password'] and not newconfig['token']:
            res = login_save(newconfig['userid'], newconfig['password'], '')
            if res == 'totp-error':
                self.error_label.configure(text='')
                pickle.dump(newconfig, open(CONFIG_PATH, 'wb'))
                self.apply_button.configure(state='normal', text='適用')
                return
            else:
                self.error_label.configure(
                    text='個人IDまたはパスワードに誤りがあります', text_color='red')
                pickle.dump(nowconfig, open(CONFIG_PATH, 'wb'))
                self.apply_button.configure(state='normal', text='適用')
                return
        if newconfig['userid'] and newconfig['password'] and newconfig['token']:
            res = login_save(
                newconfig['userid'], newconfig['password'], newconfig['token'], input_token=True)
            if res == 'success':
                self.error_label.configure(text='')
                pickle.dump(newconfig, open(CONFIG_PATH, 'wb'))
                self.apply_button.configure(state='normal', text='適用')
                return
            if res == 'info-error':
                self.error_label.configure(
                    text='個人IDまたはパスワードに誤りがあります', text_color='red')
                self.apply_button.configure(state='normal', text='適用')
            if res == 'totp-error':
                self.error_label.configure(
                    text='トークンに誤りがあります', text_color='red')
                self.apply_button.configure(state='normal', text='適用')
            nowconfig['darkmode'] = newconfig['darkmode']
            pickle.dump(nowconfig, open(CONFIG_PATH, 'wb'))
            return
        self.error_label.configure(
            text='『「大阪大学個人ID」と「パスワード」』，もしくは\n『「大阪大学個人ID」と「パスワード」と「トークン」』を入力してください', text_color='red')
        nowconfig['darkmode'] = newconfig['darkmode']
        pickle.dump(nowconfig, open(CONFIG_PATH, 'wb'))
        self.apply_button.configure(state='normal', text='適用')
        return

    def set_default(self):
        self.darkmode_switch.deselect()
        self.theme_segbutton.set('blue')
        self.userid_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.token_entry.delete(0, tk.END)

    def destroy_this(self):
        for th in self.threads:
            th.join()
        self.destroy()
