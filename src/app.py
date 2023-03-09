import customtkinter as ct
import os
from PIL import Image
import threading

from login.login_window import LoginWindow
from top.top import Top
from courses.courses import Courses

from utils import isexists_login_info
from api import get_courses, check_auth
from const import ASSET_DIR

class App(ct.CTk):
    def __init__(self):
        super().__init__()
        self.logined = False
        self.login()

        self.title('CLE-desktop')
        self.geometry(f'{1400}x{800}+150+50')
        self.focus()

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.logo_image = ct.CTkImage(Image.open(os.path.join(ASSET_DIR, 'CLELogo.png')), size=(220, 32))

        # navigation frame
        self.navigation_frame = ct.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.logo = ct.CTkButton(self.navigation_frame,
                                            image=self.logo_image,
                                            text='',
                                            fg_color="transparent",
                                            hover=False,
                                            command=self.click_logo).grid(row=0, column=0, padx=20, pady=20)
        self.course_button = ct.CTkButton(self.navigation_frame,
                                                     corner_radius=0, height=40, border_spacing=10,
                                                     text='コース', fg_color="transparent", text_color=("gray10", "gray90"),
                                                     hover_color=("gray70", "gray30"),
                                                     anchor="w",
                                                     command=self.click_course_button).grid(row=1, column=0, padx=20, pady=20)

        self.current = None
        self.change_content('Top')

    def change_content(self, to):
        # if self.current != None:
        #     self.current.destroy()
        if to == 'Top':
            top = Top(self, fg_color='transparent')
            top.tkraise()
            top.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
            self.current = top
            return
        if to == 'Courses':
            courses = Courses(self)
            courses.tkraise()
            courses.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
            self.current = courses
            return

    def login(self):
        if isexists_login_info():
            if check_auth():
                return
        self.login_window = LoginWindow(self)
        self.login_window.mainloop()

    def click_logo(self):
        print('logo')
        self.change_content('Top')

    def click_course_button(self):
        print('course')
        self.change_content('Courses')


if __name__ == '__main__':
    ct.set_appearance_mode("dark")
    app = App()
    app.mainloop()
