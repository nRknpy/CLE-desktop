import customtkinter as ct

from .coursetable import CourseTable

from api import get_courses

class Courses(ct.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.coursetable = CourseTable(self, height=self.winfo_height(), corner_radius=10)
        self.coursetable.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="nsew")
        
        
