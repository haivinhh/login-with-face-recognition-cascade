import os.path
import datetime
import subprocess
from tkinter import messagebox
import tkinter as tk
import cv2
from PIL import Image, ImageTk

import util
face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt.xml")
class Facelogin:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Face Login")
        self.main_window.iconbitmap('Facelogin.ico')
        self.main_window.geometry("1200x520+350+100")

        self.title_label_main_window = tk.Label(self.main_window, text="Face Login Interface",  font=("Arial Bold", 20))
        self.title_label_main_window.place(x=790, y=10)
        self.title_label1_main_window = tk.Label(self.main_window, text="Nguyen Hai Vinh - DH51904906", font=("Arial Bold", 12))
        self.title_label1_main_window.place(x=810, y=50)

        self.login_button_main_window = util.get_button(self.main_window, 'LOGIN', 'cyan', self.login,fg='black')
        self.login_button_main_window.place(x=750, y=110)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'REGISTER', 'violet',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=250)

        self.quit_button_main_window = util.get_button(self.main_window, 'QUIT', 'red', self.quit)
        self.quit_button_main_window.place(x=750, y=396)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './database'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img_, cv2.COLOR_RGB2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img_, (x, y), (x + w, y + h), (0, 255, 0), 2)

        self.most_recent_capture_pil = Image.fromarray(img_)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = '.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-5]

        if name in 'unknown_person':
            util.msg_box('Sorry', 'Unknown user. Please register new user or try again.')
            with open(self.log_path, 'a') as f:
                f.write('{},{} login fail\n'.format(name, datetime.datetime.now()))
                f.close()
        elif name in 'no_persons_found':
            util.msg_box('Sorry', 'no_persons_found. Please register new user or try again.')
            with open(self.log_path, 'a') as f:
                f.write('{},{} login fail\n'.format(name, datetime.datetime.now()))
                f.close()
        else:
            util.msg_box('Welcome back!', 'Welcome, {}.'.format(name))
            with open (self.log_path, 'a') as f:
                f.write('{},{} login success\n'.format(name, datetime.datetime.now(),))
                f.close()
        os.remove(unknown_img_path)

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'ACCEPT', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.back_button_register_new_user_window = util.get_button(self.register_new_user_window, 'BACK', 'black', self.back_register_new_user, fg="white")
        self.back_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, input username')
        self.text_label_register_new_user.place(x=750, y=70)

    def back_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def quit(self):
        self.main_window.quit()
    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)
        util.msg_box('Success!', 'Succesfully !')

        self.register_new_user_window.destroy()

if __name__ == "__main__":
    app = Facelogin()
    app.start()