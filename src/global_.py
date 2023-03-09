import customtkinter
from PIL import Image, ImageTk
import tkinter as tk
from time import sleep
import threading
import os

from const import ASSET_DIR

class Player(threading.Thread):
    def __init__(self, path, label):
        super().__init__(daemon=True)
        self._please_stop = False
        self.path = path
        self.label = label
        self.duration = []
        print(os.listdir(os.path.join(ASSET_DIR, 'wait')))
        self.frames = [customtkinter.CTkImage(Image.open(os.path.join(ASSET_DIR, 'wait', framename)), size=(48, 48)) for framename in os.listdir(os.path.join(ASSET_DIR, 'wait'))]
        self.last_frame_index = None

    def run(self):
        frame_index = 0
        while not self._please_stop:
            # configでフレーム変更
            self.label.configure(image=self.frames[frame_index])
            frame_index += 1
            # 最終フレームになったらフレームを０に戻す
            if frame_index >= len(self.frames):
                frame_index = 0
            # 次のフレームまでの秒数
            sleep(0.06)

    def stop(self):
        self._please_stop = True

class WaitLabel(customtkinter.CTkButton):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.frames = [customtkinter.CTkImage(Image.open(os.path.join(ASSET_DIR, 'wait', framename)), size=(48, 48)) for framename in os.listdir(os.path.join(ASSET_DIR, 'wait'))]
        # # self.configure(image=customtkinter.CTkImage(Image.open(os.path.join(ASSET_DIR, 'CLELogo.png')), size=(220, 32)))
        self._please_stop = False

    def play(self):
        frame_index = 1
        while not self._please_stop:
            # configでフレーム変更
            self.configure(image=self.frames[frame_index])
            frame_index += 1
            # 最終フレームになったらフレームを０に戻す
            if frame_index >= len(self.frames):
                frame_index = 0
            # 次のフレームまでの秒数
            sleep(0.06)

    def stop_loop(self):
        self._please_stop = True
