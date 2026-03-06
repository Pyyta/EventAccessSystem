import customtkinter as ctk
import os
from pathlib import Path
from PIL import Image

class LoginUI: 
    def __init__(self, parent_container, master):
        self.container=parent_container
        self.master=master
        self.set_backgroung_image()
        self.set_login_main_frame()
        
    def set_backgroung_image(self):
        bg_image_path= os.path.join(self.master.images_dir, "LoginBackground.png")
        bg_image= ctk.CTkImage(light_image= Image.open(bg_image_path),
                                       dark_image= Image.open(bg_image_path), 
                                       size= (1920, 1080))
        bg_image_label= ctk.CTkLabel(self.container, image= bg_image, text="")
        bg_image_label.pack(expand=True, fill= "both")
    
    def set_login_main_frame(self):
        login_main_frame=ctk.CTkFrame(master= self.container, 
                                      width= 560,
                                      height= 500,
                                      fg_color="#034040",
                                      )
        login_main_frame.place(relx= 0.25, rely=0.125, relheight=0.75, relwidth=0.5)

        login_title = ctk.CTkLabel(master=login_main_frame,
                                   text="LOGIN",
                                   font=self.master.title_font,
                                   text_color="#FFFFFF")
        login_title.place(relx=0.1, rely=0.05, relwidth=0.8)
        self.username_field= ctk.CTkEntry(master= login_main_frame,
                                          placeholder_text= "Usuario",
                                          fg_color= "#FFFFFF",
                                          placeholder_text_color="#011A1A",
                                          text_color="#011A1A",
                                          font=self.master.main_font
                                          )
        self.username_field.place(relx= 0.2, rely=0.25, relheight=0.1, relwidth=0.6)
        self.password_field = ctk.CTkEntry(master= login_main_frame,
                                          placeholder_text= "Contraseña",
                                          fg_color= "#FFFFFF",
                                          placeholder_text_color="#011A1A",
                                          text_color="#011A1A",
                                          font=self.master.main_font,
                                          show="*"
                                          )
        self.password_field.place(relx= 0.2, rely=0.45, relheight=0.1, relwidth=0.6)

        login_button = ctk.CTkButton(master=login_main_frame,
                                     text="Entrar",
                                     fg_color="#022A2A",
                                     hover_color="#011A1A",
                                     font=self.master.main_font,
                                     text_color="#FFFFFF",
                                     command=self.login_callback)
        login_button.place(relx=0.05, rely=0.7, relheight=0.12, relwidth=0.4)

        forgot_password_button = ctk.CTkButton(master=login_main_frame,
                                              text="Olvide la contraseña",
                                              fg_color="#022A2A",
                                              hover_color="#011A1A",
                                              font=self.master.main_font,
                                              text_color="#FFFFFF",
                                              command=self.forgot_password_callback)
        forgot_password_button.place(relx=0.55, rely=0.7, relheight=0.12, relwidth=0.4)

    def forgot_password_callback(self):
        self.master.show_password_recovery()

    def login_callback(self):
        username = self.username_field.get()
        admin_pin = self.password_field.get()
        
        # Calling the controller's check function
        # result is a Tuple (bool, str) or (None, str)
        status, message = self.master.controller.check_admin_credentials(admin_pin, username)
        
        if status:
            print(f"Login successful: {message}")
        else:
            print(f"Login failed: {message}")
