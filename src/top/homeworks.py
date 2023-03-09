import customtkinter as ct
import webbrowser
import threading
from datetime import datetime, timezone, timedelta

from api import get_homeworks

class Homeworks(ct.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.get_date = datetime.now().strftime('%Y/%m/%d %H:%M')
        self.hw_outframes = []
        self.make_ui()

    def make_ui(self):
        th = threading.Thread(target=self.__make_ui)
        th.setDaemon(True)
        th.start()

    def __make_ui(self):
        try:
            homeworks = get_homeworks()
        except:
            print('get homework error')
        if not len(homeworks):
            outframe = ct.CTkFrame(self, width=self.winfo_width())
            ct.CTkLabel(outframe, text='現在，課題はありません．', width=outframe.winfo_width()).grid(row=0, column=0, sticky="nsew")
            outframe.grid(row=0, sticky="nsew")
            self.hw_outframes.append(outframe)
            return
        for homework in homeworks:
            self.add_item(homework['title'], homework['calendarNameLocalizable']['rawValue'], homework['endDate'],
                          homework['calendarId'], homework['itemSourceType'], homework['itemSourceId'])

    def add_item(self, homework_name, course_name, deadline, course_id, item_source_type, item_source_id):
        deadline = datetime.strptime(deadline + '+0000', '%Y-%m-%dT%H:%M:%S.%fZ%z').astimezone(timezone(timedelta(hours=+9))).strftime('%Y/%m/%d %H:%M')
        hw_outframe = ct.CTkFrame(self, width=self.winfo_width())
        hw_outframe.grid_columnconfigure(0, weight=1)
        hw_frame = ct.CTkFrame(hw_outframe)
        hw_frame.grid_columnconfigure(0, weight=1)
        hw_name_label = ct.CTkLabel(hw_frame, text=homework_name).grid(row=0, column=0, sticky="ew")
        course_name_label = ct.CTkLabel(hw_frame, text=course_name).grid(row=1, column=0, sticky="ew")
        deadline_label = ct.CTkLabel(hw_outframe, text=deadline,
                                                compound='left', padx=5, anchor='w',
                                                font=(ct.CTkFont('MSゴシック'), 15))
        button = ct.CTkButton(hw_outframe, text='詳細', width=100, height=24,
                                         command=lambda: webbrowser.open(
                                             'https://www.cle.osaka-u.ac.jp/ultra/courses/'
                                             + course_id
                                             + '/cl/outline?legacyUrl=~2Fwebapps~2Fcalendar~2Flaunch~2Fattempt~2F_'
                                             + item_source_type
                                             + '-'
                                             + item_source_id
                                         ))
        hw_frame.grid(row=0, column=0, padx=(2, 2), pady=(5, 5), sticky="nsew")
        deadline_label.grid(row=0, column=1, pady=(5, 5))
        button.grid(row=0, column=2, pady=(5, 5), padx=5)
        hw_outframe.grid(row=len(self.hw_outframes), padx=1, pady=(0, 3), sticky="nsew")
        self.hw_outframes.append(hw_outframe)
