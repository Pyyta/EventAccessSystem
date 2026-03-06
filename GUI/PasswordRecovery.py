import customtkinter as ctk
import os
from PIL import Image

class PasswordRecovery: 
    def __init__(self, parent_container, master):
        self.container=parent_container
        self.master=master
        self.set_background_image()
        self.set_main_frame()
        self.update_timer()
        
    def set_background_image(self):
        bg_image_path= os.path.join(self.master.images_dir, "LoginBackground.png")
        bg_image= ctk.CTkImage(light_image= Image.open(bg_image_path),
                                       dark_image= Image.open(bg_image_path), 
                                       size= (1920, 1080))
        bg_image_label= ctk.CTkLabel(self.container, image= bg_image, text="")
        bg_image_label.pack(expand=True, fill= "both")
    
    def set_main_frame(self):
        self.main_frame=ctk.CTkFrame(master= self.container, 
                                      width= 560,
                                      height= 500,
                                      fg_color="#034040",
                                      )
        self.main_frame.place(relx= 0.25, rely=0.125, relheight=0.75, relwidth=0.5)

        title = ctk.CTkLabel(master=self.main_frame,
                             text="RECUPERAR CONTRASEÑA",
                             font=self.master.title_font,
                             text_color="#FFFFFF")
        title.place(relx=0.1, rely=0.05, relwidth=0.8)

        subtitle = ctk.CTkLabel(master=self.main_frame,
                                text="escribe el codigo temporal",
                                font=self.master.main_font,
                                text_color="#FFFFFF")
        subtitle.place(relx=0.1, rely=0.25, relwidth=0.8)

        vcmd = (self.main_frame.register(self.validate_numbers), '%P')
        self.code_field = ctk.CTkEntry(master= self.main_frame,
                                          placeholder_text= "Código",
                                          fg_color= "#FFFFFF",
                                          placeholder_text_color="#011A1A",
                                          text_color="#011A1A",
                                          font=self.master.main_font,
                                          validate="key", 
                                          validatecommand=vcmd)
        self.code_field.place(relx= 0.2, rely=0.4, relheight=0.1, relwidth=0.6)

        self.timer_label = ctk.CTkLabel(master=self.main_frame,
                                        text="Tiempo restante: 60s",
                                        font=self.master.main_font,
                                        text_color="#FFFFFF")
        self.timer_label.place(relx=0.1, rely=0.55, relwidth=0.8)

        self.resend_button = ctk.CTkButton(master=self.main_frame,
                                      text="enviar el codigo de nuevo",
                                      fg_color="#022A2A",
                                      hover_color="#011A1A",
                                      font=self.master.main_font,
                                      text_color="#FFFFFF",
                                      command=self.resend_code)

        self.back_button = ctk.CTkButton(master=self.main_frame,
                                         text="Volver",
                                         fg_color="#022A2A",
                                         hover_color="#011A1A",
                                         font=self.master.main_font,
                                         text_color="#FFFFFF",
                                         command=self.go_back)
        self.back_button.place(relx=0.05, rely=0.85, relheight=0.1, relwidth=0.3)

    def validate_numbers(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def update_timer(self):
        time_left = getattr(self.master, 'recovery_time_left', 0)
        if time_left > 0:
            self.timer_label.configure(text=f"Tiempo restante: {time_left}s")
            self.resend_button.place_forget()
        else:
            self.timer_label.configure(text="Tiempo expirado")
            self.show_resend_button()

    def show_resend_button(self):
        self.resend_button.place(relx=0.2, rely=0.7, relheight=0.12, relwidth=0.6)

    def resend_code(self):
        status, message = self.master.trigger_password_recovery_email()
        if status:
            self.update_timer()
        
    def go_back(self):
        self.master.show_login()
