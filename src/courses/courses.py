import customtkinter as ct
import webbrowser

from .coursetable import CourseTable
from .course_content import CourseContent

class Courses(ct.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.threads = []

        # self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.coursetable = CourseTable(self, self.show_content, self.threads, width=600, corner_radius=10)
        self.coursetable.grid(row=0, column=0, padx=(0, 2), pady=0, sticky="nsew")

        self.content = None
        self.course_content = CourseContent(self, self.threads, width=500, height=self.winfo_height(), corner_radius=10)
        self.course_content.grid(row=0, column=1, padx=(2, 0), pady=0, sticky="nsew")

    def show_content(self, course_id, latest_id):
        self.course_content.make_ui(course_id, latest_id)

    def load_link(self, url):
        webbrowser.open(url)
    
    def destroy_this(self):
        for th in self.threads:
            th.join()
        self.destroy()
        print('courses destroyed')
