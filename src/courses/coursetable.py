import customtkinter as ct
import threading
import json
from collections import defaultdict
import os
import pickle

from api import get_courses
from const import CACHE_DIR
from utils import dbstrlen

MAX_NAME_LEN = 47


class CourseTable(ct.CTkScrollableFrame):
    def __init__(self, master, callback, threads_list, **kwargs):
        super().__init__(master, **kwargs)
        self.callback = callback
        self.threads_list = []
        self.grid_columnconfigure(0, weight=1)

        self.row_cnt = 0
        self.outframes = []
        self.buttons = []
        self.ids = []

        self.latest_id = ['']
        self.current_idx = None

        self.make_ui()

    def make_ui(self):
        th = threading.Thread(target=self.__make_ui)
        th.setDaemon(True)
        self.threads_list.append(th)
        th.start()

    def __make_ui(self):
        bar = ct.CTkProgressBar(self, mode='indetermine',
                                width=self.winfo_width())
        bar.grid(row=0, sticky="nsew")
        bar.start()
        if os.path.exists(os.path.join(CACHE_DIR, 'courses.pkl')):
            courses = pickle.load(
                open(os.path.join(CACHE_DIR, 'courses.pkl'), 'rb'))
        else:
            try:
                courses = get_courses()
            except:
                print('get courses error')
        pickle.dump(courses, open(os.path.join(
            CACHE_DIR, 'courses.pkl'), 'wb'))
        course_dict = self.classify(courses)
        bar.stop()
        bar.destroy()
        for term, course_list in course_dict.items():
            termlabel = ct.CTkLabel(
                self, text='・ ' + term, fg_color='transparent', anchor='w', font=(ct.CTkFont('MSゴシック'), 16))
            termlabel.grid(row=self.row_cnt, padx=1,
                           pady=(2, 6), sticky='nsew')
            self.row_cnt += 1
            for c in course_list:
                self.add_item(**c)

    def classify(self, courses):
        d = defaultdict(list)
        for course in courses:
            try:
                description = json.loads(course['description'])
            except json.JSONDecodeError:
                print('JSONDecodeError', course)
                continue
            if not 'term' in course.keys():
                print('no term key')
                continue
            d[course['term']['name']].append({
                'name': course['displayName'],
                'teacher': description['lecturer'],
                'locale': description['timetable'][0]['locale'],
                'course_id': course['id'],
            })
        for k, v in d.items():
            d[k] = sorted(v, key=lambda x: x['name'])
        return d

    def add_item(self, name, teacher, locale, course_id):
        outframe = ct.CTkFrame(self, width=self.winfo_width())
        outframe.grid_columnconfigure(0, weight=1)
        if dbstrlen(name) > MAX_NAME_LEN:
            name = name[:MAX_NAME_LEN] + '...'
        innerframe = ct.CTkFrame(outframe, width=outframe.winfo_width())
        innerframe.grid_columnconfigure(0, weight=1)
        name_button = ct.CTkButton(innerframe, text=name,
                                   font=(ct.CTkFont('MSゴシック'), 16),
                                   text_color=("gray10", "gray90"),
                                   text_color_disabled=("gray70", "gray30"),
                                   fg_color='transparent',
                                   hover=False,
                                   anchor='w',
                                   command=lambda: self.click(outframe))
        name_button.grid(row=0, column=0, sticky="ew")
        info_label = ct.CTkLabel(innerframe, text=f'- {locale} | {teacher}', fg_color='transparent', anchor='w').grid(
            row=1, column=0, padx=(15, 0), sticky="ew")
        innerframe.grid(row=0, sticky='nsew')
        outframe.grid(row=self.row_cnt, padx=1,
                      pady=(0, 6), sticky="nsew")
        self.row_cnt += 1
        self.outframes.append(outframe)
        self.ids.append(course_id)
        self.buttons.append(name_button)

    def click(self, outframe):
        idx = self.outframes.index(outframe)
        course_id = self.ids[idx]
        if self.current_idx != None:
            self.buttons[self.current_idx].configure(state='normal')
        self.buttons[idx].configure(state='disabled')
        self.current_idx = idx
        self.latest_id[0] = course_id
        print(course_id)
        th = threading.Thread(
            target=lambda: self.callback(course_id, self.latest_id))
        th.setDaemon(True)
        self.threads_list.append(th)
        th.start()
