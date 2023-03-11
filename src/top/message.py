import customtkinter as ct
from tkinterweb import htmlwidgets
import webbrowser
import threading

from api import get_message

class MassageFrame(ct.CTkFrame):
    def __init__(self, master, threads_list, **kwargs):
        super().__init__(master, **kwargs)
        self.threads_list = threads_list
        self.grid_columnconfigure(0, weight=1)
        self.message = htmlwidgets.HtmlFrame(self)
        self.message.on_link_click(self.load_link)

        self.__make_ui()
        # th = threading.Thread(target=self.__make_ui)
        # th.setDaemon(True)
        # th.start()

    def __make_ui(self):
        try:
            message_html = get_message()
            print(message_html)
        except:
            print('get message error')
        # message = htmlwidgets.HtmlFrame(self, height=self.winfo_height())
        # message.on_link_click(self.load_link)
        credit_html = '<p><strong>【CLE Desktop】</strong></p><br><p>・開発: <a href=\"https://twitter.com/Ra_kn_c\">@Ra_kn_c (Twitter)</a> / バグ・要望等はDMへ</p>'
        self.message.load_html(message_html + credit_html)
        self.message.grid(row=0, column=0, padx=0, pady=0, sticky="ew")

    def load_link(self, url):
        webbrowser.open(url)
