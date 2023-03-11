import customtkinter as ct

from const import CACHE_DIR

class Config(ct.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        
        self.darkmode_frame = ct.CTkFrame(self, corner_radius=10)
        self.darkmode_frame.grid_columnconfigure(1, weight=1)
        self.darkmode_label = ct.CTkLabel(self.darkmode_frame, text='ダークモード:', width=400, anchor='e')
        self.darkmode_label.grid(row=0, column=0, pady=15)
        self.darkmode_switch = ct.CTkSwitch(self.darkmode_frame, width=500, text='')
        self.darkmode_switch.grid(row=0, column=1, pady=15)
        self.darkmode_frame.grid(row=0, padx=1, pady=(0, 6), sticky="nsew")
        
        self.userinfo_frame = ct.CTkFrame(self, corner_radius=10)
        self.userinfo_frame.grid_columnconfigure(1, weight=1)
        self.userinfo_frame.grid_rowconfigure(4, weight=1)
        self.rightframe = ct.CTkFrame(self.userinfo_frame, fg_color='transparent')
        self.rightframe.grid_rowconfigure(1, weight=1)
        self.rightframe.grid_columnconfigure(0, weight=1)
        self.userinfo_label = ct.CTkLabel(self.userinfo_frame, text='ユーザー情報:', width=400, anchor='ne')
        self.userinfo_label.grid(row=0, column=0)
        self.userid_label = ct.CTkLabel(self.rightframe, text='大阪大学個人ID:', width=10, anchor='e')
        self.userid_label.grid(row=0, column=0, padx=10)
        self.userid_entry = ct.CTkEntry(self.rightframe, placeholder_text='未設定')
        self.userid_entry.grid(row=0, column=1)
        self.password_label = ct.CTkLabel(self.rightframe, text='パスワード:', width=10, anchor='e')
        self.password_label.grid(row=1, column=0, padx=10)
        self.password_entry = ct.CTkEntry(self.rightframe, placeholder_text='未設定')
        self.password_entry.grid(row=1, column=1)
        self.token_label = ct.CTkLabel(self.rightframe, text='トークン:', width=10, anchor='e')
        self.token_label.grid(row=2, column=0, padx=10)
        self.token_entry = ct.CTkEntry(self.rightframe, placeholder_text='未設定')
        self.token_entry.grid(row=2, column=1)
        self.tips_label = ct.CTkLabel(self.rightframe,
                                      text='「大阪大学個人ID」と「パスワード」を設定することで，ログイン時に自動的に入力されます．\n「トークン」を設定することで，ワンタイムパスワードの入力を自動化できます．')
        self.tips_label.grid(row=3, column=0, columnspan=2, pady=10)
        self.rightframe.grid(row=0, column=1, pady=15)
        self.userinfo_frame.grid(row=1, padx=1, pady=(0, 6), sticky="nsew")
        
        self.apply_button = ct.CTkButton(self, text='適用', command=self.apply_config)
        self.apply_button.grid(row=2, padx=(200, 0))
    
    def apply_config(self):
        darkmode_on = self.darkmode_switch.get()
        userid = None if not self.userid_entry.get() else self.userid_entry.get()
        password = None if not self.password_entry.get() else self.password_entry.get()
        token = None if not self.token_entry.get() else self.token_entry.get()
        print(darkmode_on, userid, password, token)
    
    def destroy_this(self):
        self.destroy()