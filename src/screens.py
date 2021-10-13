from tkinter import ttk

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
        self.register_button.pack()

        self.login_button = ttk.Button(
                window,
                text="Log in",
                command=on_click_login,
                )
        self.login_button.pack()

        self.logout_button = ttk.Button(
                window,
                text="Log out",
                command=on_click_logout,
                )

        self.msg = ttk.Label(
                window,
                style='TLabel',
                text="")


    def set_panel_image(self, imgtk):
        self.panel.imgtk = imgtk
        self.panel.configure(image=imgtk)


    def home_screen(self):
        self.msg.pack_forget()
        self.logout_button.pack_forget()
        self.register_button.state(['!disabled'])
        self.login_button.state(['!disabled'])
        self.register_button.pack()
        self.login_button.pack()


    def registering_screen(self):
        self.register_button.pack_forget()
        self.login_button.pack_forget()
        self.logout_button.pack_forget()
        self.msg.pack()


    def update_msg_text(self, text):
        self.msg.configure(text=text)


    def logging_in_screen(self):
        # disable buttons
        self.logout_button.pack_forget()
        self.register_button.state(['disabled'])
        self.login_button.state(['disabled'])
        self.msg.configure(text="Matching...")
        self.msg.pack()


    def logged_in_screen(self):
        self.register_button.pack_forget()
        self.login_button.pack_forget()
        self.logout_button.pack()
