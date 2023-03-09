import customtkinter as ct
from tkinterweb import htmlwidgets

class CourseContent(ct.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.message = htmlwidgets.HtmlFrame(self)
        self.message.on_link_click(self.load_link)

        self.__make_ui()