import customtkinter as ct
from tkinterweb import htmlwidgets
import webbrowser
import threading

from api import get_content_html

class CourseContent(ct.CTkFrame):
    def __init__(self, master, threads_list, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.threads_list = threads_list
        self.content = None

    def make_ui(self, course_id, latest_id):
        if self.content != None:
            self.content.destroy()
        self.bar = ct.CTkProgressBar(self, mode='indetermine', width=self.winfo_width())
        self.bar.grid(row=0, sticky="new")
        self.bar.start()
        flag, res = get_content_html(course_id)
        self.bar.stop()
        self.bar.destroy()
        if latest_id[0] != course_id: return
        self.content = htmlwidgets.HtmlFrame(self, height=self.winfo_height(), width=self.winfo_width(), messages_enabled = False)
        self.content.on_link_click(self.load_link)
        self.content.load_html(res)
        self.content.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

    def load_link(self, url):
        webbrowser.open(url)
