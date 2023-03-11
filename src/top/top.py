import customtkinter as ct

from .homeworks import Homeworks
from .message import MassageFrame

class Top(ct.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.threads = []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=3)

        self.homeworks = Homeworks(self, self.threads, height=500, corner_radius=10)
        self.homeworks.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.homework_label = ct.CTkLabel(self, text=f'課題 ({self.homeworks.get_date})', anchor='w', font=(ct.CTkFont('MSゴシック'), 20))
        self.homework_label.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.message_label = ct.CTkLabel(self, text='新着情報', anchor='w', font=(ct.CTkFont('MSゴシック'), 20))
        self.message_label.grid(row=2, column=0, padx=0, pady=(10, 0), sticky="nsew")
        self.message = MassageFrame(self, self.threads, height=200, corner_radius=10)
        self.message.grid(row=3, column=0, padx=0, pady=0, sticky="nsew")
    
    def destroy_this(self):
        for th in self.threads:
            th.join()
        self.destroy()
        print('top destroyed')
