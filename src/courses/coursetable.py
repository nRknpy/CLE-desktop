import customtkinter as ct
import threading
import json
from collections import defaultdict

from api import get_courses

class CourseTable(ct.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.outframes = []
        self.make_ui()

    def make_ui(self):
        th = threading.Thread(target=self.__make_ui)
        th.setDaemon(True)
        th.start()

    def __make_ui(self):
        try:
            courses = get_courses()
        except:
            print('get courses error')
        print(courses)
        course_dict = self.classify(courses)
        for term, course_list in course_dict.items():
            for c in course_list:
                self.add_item(c['name'], c['teacher'], c['locale'])
    
    def classify(self, courses):
        d = defaultdict(list)
        for course in courses:
            try:
                description = json.loads(course['description'])
            except json.JSONDecodeError:
                continue
            d[course['name']].append({
                'name': course['displayName'],
                'teacher': description['lecturer'],
                'locale': description['timetable'][0]['locale'],
            })
        for k,v in d.items():
            d[k] = sorted(v, key=lambda x: x['name'])
        return d

    def add_item(self, name, teacher, locale):
        outframe = ct.CTkFrame(self, width=self.winfo_width())
        outframe.grid_columnconfigure(0, weight=1)
        name_label = ct.CTkLabel(outframe, text=name, font=(ct.CTkFont('MSゴシック'), 16), fg_color='transparent').grid(row=0, column=0, sticky="ew")
        info_label = ct.CTkLabel(outframe, text=f'{locale} | {teacher}', fg_color='transparent').grid(row=1, column=0, sticky="ew")
        outframe.grid(row=len(self.outframes), padx=1, pady=(0, 6), sticky="nsew")
        self.outframes.append(outframe)
