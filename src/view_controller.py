from tkinter import Tk
import cv2
from PIL import Image, ImageTk
from src.authenticator import *
from src.screens import Screens
from threading import Timer, Thread


class ViewController():
    def __init__(self):
        print("View Controller Init")

        self.window = Tk()

        self.window.title("Face ID")
        self.window.geometry("600x800")
        self.window.configure(
                background="white",
                cursor="arrow",
                )

        self.screens = Screens(
                self.window,
                self.on_click_register,
                self.on_click_login,
                self.on_click_logout)

        self.camera = cv2.VideoCapture(0)

        self.recording = False
        self.batch_size = 64
        self.auth = Authenticator(
                self.batch_size,
                0.382887,
                "./2021-07-31-10_22_13.pt")


    def on_click_register(self):
        print("Clicked Register")

        self.recording = True
        self.recording_frames = []

        self.screens.registering_screen()

    def on_complete_recording(self):
        print("Finshed registering")
        self.recording = False
        self.auth.register("Austin", self.recording_frames)
        self.recording_frames = []

        self.screens.home_screen()

    def match(self):
        if self.auth.can_match():
            success = self.auth.match(self.image)
            print(f"Match: {success}")
            return success
        return False


    def on_click_login(self):
        print("Clicked Login")

        self.screens.logging_in_screen()

        if self.match():
            self.screens.update_msg_text(
                    text="Logged in as {}".format(
                        self.auth.get_user_id()))

            self.screens.logged_in_screen()

        else:
            self.screens.home_screen()


    def on_click_logout(self):
        print("Clicked logout")

        self.auth.logout()
        self.screens.home_screen()


    def video_loop(self):
        success, frame = self.camera.read()
        if not success:
            return

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        image = crop_square(Image.fromarray(image))
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
        imgtk = ImageTk.PhotoImage(image=image)

        self.image = image
        self.screens.set_panel_image(imgtk)

        self.window.after(20, self.video_loop)

        if self.recording:
            self.recording_frames.append(image)
            print(f"Recording Frame: {len(self.recording_frames)}")
            # show progress, update text
            self.screens.update_msg_text(
                    "Registering... {}/{}".format(
                        len(self.recording_frames),
                        self.batch_size
                ))

            if (len(self.recording_frames) == self.batch_size):
                self.on_complete_recording()


    def start(self):
        print("View Controller Starts")

        self.video_loop()
        self.window.mainloop()
        self.camera.release()
        cv2.destroyAllWindows()


def crop_square(image):
    width, height = image.size
    magnify_ratio = 0.55
    square_length = min(width, height) * magnify_ratio
    left = (width - square_length) / 2
    right = (width + square_length) / 2
    top = (height - square_length) / 2
    bottom = (height + square_length) / 2
    return image.crop((left, top, right, bottom))
