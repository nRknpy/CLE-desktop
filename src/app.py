import customtkinter as ct
import os
from PIL import Image
import threading
import pickle

from login.login_window import LoginWindow
from top.top import Top
from courses.courses import Courses
from config.config import Config
from mfacode.mfacode import MFACode

from utils import isexists_login_info
from api import check_auth, login_save
from const import ASSET_DIR, CACHE_DIR, CONFIG_PATH


class App(ct.CTk):
    def __init__(self):
        super().__init__()
        self.logined = False
        self.login()

        self.title('CLE-desktop')
        self.geometry(f'{1400}x{800}+150+50')
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.logo_image = ct.CTkImage(light_image=Image.open(os.path.join(ASSET_DIR, 'CLELogo_light.png')),
                                      dark_image=Image.open(os.path.join(
                                          ASSET_DIR, 'CLELogo_dark.png')),
                                      size=(220, 32))

        self.navigation_frame = ct.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)
        self.logo = ct.CTkButton(self.navigation_frame,
                                 image=self.logo_image,
                                 text='',
                                 fg_color="transparent",
                                 hover=False,
                                 command=lambda: self.change_content('top'))
        self.logo.grid(row=0, column=0, padx=20, pady=20)
        self.home_button = ct.CTkButton(self.navigation_frame,
                                        corner_radius=0, height=40, border_spacing=10,
                                        text='ホーム', fg_color="transparent", text_color=("gray10", "gray90"),
                                        hover_color=("gray70", "gray30"),
                                        anchor="w",
                                        command=lambda: self.change_content('top'))
        self.home_button.grid(row=1, column=0, padx=20, pady=20)
        self.course_button = ct.CTkButton(self.navigation_frame,
                                          corner_radius=0, height=40, border_spacing=10,
                                          text='コース', fg_color="transparent", text_color=("gray10", "gray90"),
                                          hover_color=("gray70", "gray30"),
                                          anchor="w",
                                          command=lambda: self.change_content('courses'))
        self.course_button.grid(row=2, column=0, padx=20, pady=20)
        self.config_button = ct.CTkButton(self.navigation_frame,
                                          corner_radius=0, height=40, border_spacing=10,
                                          text='MFA認証コード', fg_color="transparent", text_color=("gray10", "gray90"),
                                          hover_color=("gray70", "gray30"),
                                          anchor="w",
                                          command=lambda: self.change_content('mfacode'))
        self.config_button.grid(row=3, column=0, padx=20, pady=20)
        self.config_button = ct.CTkButton(self.navigation_frame,
                                          corner_radius=0, height=40, border_spacing=10,
                                          text='設定', fg_color="transparent", text_color=("gray10", "gray90"),
                                          hover_color=("gray70", "gray30"),
                                          anchor="w",
                                          command=lambda: self.change_content('config'))
        self.config_button.grid(row=4, column=0, padx=20, pady=20)

        self.current = None
        self.change_content('top')

    def change_content(self, to):
        if self.current != None:
            th = threading.Thread(target=self.current.destroy_this)
            th.setDaemon(True)
            th.start()
        if to == 'top':
            top = Top(self, fg_color='transparent')
            top.tkraise()
            top.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
            self.current = top
            return
        if to == 'courses':
            courses = Courses(self, fg_color='transparent')
            courses.tkraise()
            courses.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
            self.current = courses
            return
        if to == 'config':
            config = Config(self, fg_color='transparent')
            config.tkraise()
            config.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
            self.current = config
            return
        if to == 'mfacode':
            mfacode = MFACode(
                self, change_content_fnc=self.change_content, fg_color='transparent')
            mfacode.tkraise()
            mfacode.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
            self.current = mfacode
            return

    def login(self):
        if isexists_login_info():
            if check_auth():
                return
        if os.path.exists(CONFIG_PATH):
            config = pickle.load(open(CONFIG_PATH, 'rb'))
            if config['userid'] and config['password'] and not config['token']:
                self.login_window = LoginWindow(
                    self, userid=config['userid'], password=config['password'])
                self.login_window.mainloop()
                return
            if config['userid'] and config['password'] and config['token']:
                login_save(config['userid'], config['password'],
                           config['token'], input_token=True)
                return
        self.login_window = LoginWindow(self)
        self.login_window.mainloop()

    def close_window(self):
        if os.path.exists(os.path.join(CACHE_DIR, 'courses.pkl')):
            os.remove(os.path.join(CACHE_DIR, 'courses.pkl'))
        self.destroy()


if __name__ == '__main__':
    if os.path.exists(CONFIG_PATH):
        config = pickle.load(open(CONFIG_PATH, 'rb'))
        if config['darkmode']:
            ct.set_appearance_mode('dark')
        else:
            ct.set_appearance_mode('light')
        ct.set_default_color_theme(config['theme'])
    else:
        ct.set_appearance_mode("system")
        ct.set_default_color_theme("blue")
    app = App()
    app.iconbitmap(bitmap=os.path.join(ASSET_DIR, 'icon.ico'))
    app.mainloop()
