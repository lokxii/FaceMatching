from tkinter import ttk, END


class Screens():
    def __init__(self, window, on_click_register, on_click_login, on_click_logout):
        print("Screens Init")

        # panel will not move
        # and is at the top of the screen
        self.panel = ttk.Label(window)
        self.panel.pack()

        self.register_button = ttk.Button(
                window,
                text="Register",
                command=on_click_register,
                )

        self.login_button = ttk.Button(
                window,
                text="Log in",
                command=on_click_login,
                )

        self.logout_button = ttk.Button(
                window,
                text="Log out",
                command=on_click_logout,
                )

        self.msg = ttk.Label(
                window,
                text="",
                )

        self.entry = ttk.Entry(window)
        self.entry_label = ttk.Label(
                window,
                text="User name:",
                )


    def set_panel_image(self, imgtk):
        self.panel.imgtk = imgtk
        self.panel.configure(image=imgtk)


    def __reset__(self):
        self.register_button.pack_forget()
        self.login_button.pack_forget()
        self.logout_button.pack_forget()
        self.msg.pack_forget()
        self.entry.pack_forget()
        self.entry_label.pack_forget()
        # self.clear_entry()

    def home_screen(self):
        self.__reset__()
        self.clear_entry()
        self.entry_label.pack()
        self.entry.pack()
        self.register_button.pack()
        self.login_button.pack()


    def registering_screen(self):
        self.__reset__()
        self.msg.pack()


    def update_msg_text(self, text):
        self.msg.configure(text=text)


    def logging_in_screen(self):
        self.__reset__()
        self.msg.configure(text="Matching...")
        self.msg.pack()


    def logged_in_screen(self):
        self.__reset__()
        self.msg.pack()
        self.logout_button.pack()


    def get_entry(self):
        return self.entry.get()


    def clear_entry(self):
        self.entry.delete(0, END)
