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
                                text="Revisa tu correo y escribe el código temporal",
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
        self.code_field.place(relx= 0.2, rely=0.38, relheight=0.1, relwidth=0.6)

        verify_button = ctk.CTkButton(master=self.main_frame,
                                      text="Verificar PIN",
                                      fg_color="#022A2A",
                                      hover_color="#011A1A",
                                      font=self.master.main_font,
                                      text_color="#FFFFFF",
                                      command=self.verify_pin)
        verify_button.place(relx=0.2, rely=0.52, relheight=0.1, relwidth=0.6)

        self.timer_label = ctk.CTkLabel(master=self.main_frame,
                                        text="Tiempo restante: 60s",
                                        font=self.master.main_font,
                                        text_color="#FFFFFF")
        self.timer_label.place(relx=0.1, rely=0.66, relwidth=0.8)

        # resend_button is NOT created here; it is built on-demand by create_resend_button()
        self.resend_button = None

        self.back_button = ctk.CTkButton(master=self.main_frame,
                                         text="Volver",
                                         fg_color="#022A2A",
                                         hover_color="#011A1A",
                                         font=self.master.main_font,
                                         text_color="#FFFFFF",
                                         command=self.go_back)
        self.back_button.place(relx=0.05, rely=0.88, relheight=0.1, relwidth=0.3)

    def validate_numbers(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def update_timer(self):
        time_left = getattr(self.master, 'recovery_time_left', 0)
        if time_left > 0:
            self.timer_label.configure(text=f"Tiempo restante: {time_left}s")
            # Hide and destroy the resend button if it was previously created
            if self.resend_button is not None:
                self.resend_button.destroy()
                self.resend_button = None
        else:
            self.timer_label.configure(text="Tiempo expirado")
            self.show_resend_button()

    def show_resend_button(self):
        # Only create the button if it doesn't already exist
        if self.resend_button is None:
            self.create_resend_button()

    def create_resend_button(self):
        """Dynamically creates and places the 'Volver a enviar correo' button
        when the countdown timer reaches zero."""
        self.resend_button = ctk.CTkButton(master=self.main_frame,
                                           text="Volver a enviar correo",
                                           fg_color="#022A2A",
                                           hover_color="#011A1A",
                                           font=self.master.main_font,
                                           text_color="#FFFFFF",
                                           command=self.resend_code)
        self.resend_button.place(relx=0.2, rely=0.78, relheight=0.1, relwidth=0.6)

    def resend_code(self):
        # Destroy the button immediately so the user can't click it twice
        if self.resend_button is not None:
            self.resend_button.destroy()
            self.resend_button = None

        status, message = self.master.trigger_password_recovery_email()
        if status:
            self.update_timer()

    def verify_pin(self):
        pin_attempt = self.code_field.get()
        status, message = self.master.controller.check_recovery_pin(pin_attempt)
        if status:
            self.show_new_password_setter()
        else:
            print("incorrect")

    def go_back(self):
        self.master.show_login()

    def show_new_password_setter(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(master=self.main_frame,
                             text="NUEVA CONTRASEÑA",
                             font=self.master.title_font,
                             text_color="#FFFFFF")
        title.place(relx=0.1, rely=0.05, relwidth=0.8)

        self.new_password_field = ctk.CTkEntry(master= self.main_frame,
                                          placeholder_text= "Nueva contraseña",
                                          fg_color= "#FFFFFF",
                                          placeholder_text_color="#011A1A",
                                          text_color="#011A1A",
                                          show="*",
                                          font=self.master.main_font)
        self.new_password_field.place(relx= 0.1, rely=0.25, relheight=0.1, relwidth=0.8)

        self.confirm_password_field = ctk.CTkEntry(master= self.main_frame,
                                          placeholder_text= "Confirmar contraseña",
                                          fg_color= "#FFFFFF",
                                          placeholder_text_color="#011A1A",
                                          text_color="#011A1A",
                                          show="*",
                                          font=self.master.main_font)
        self.confirm_password_field.place(relx= 0.1, rely=0.40, relheight=0.1, relwidth=0.8)

        set_password_button = ctk.CTkButton(master=self.main_frame,
                                      text="Establecer nueva contraseña",
                                      fg_color="#022A2A",
                                      hover_color="#011A1A",
                                      font=self.master.main_font,
                                      text_color="#FFFFFF",
                                      command=self.update_admin_password)
        set_password_button.place(relx=0.1, rely=0.55, relheight=0.1, relwidth=0.8)

        self.status_label = ctk.CTkLabel(master=self.main_frame,
                                        text="",
                                        font=self.master.main_font,
                                        text_color="#FFFFFF")
        self.status_label.place(relx=0.1, rely=0.70, relwidth=0.8)

        self.back_button = ctk.CTkButton(master=self.main_frame,
                                         text="Volver",
                                         fg_color="#022A2A",
                                         hover_color="#011A1A",
                                         font=self.master.main_font,
                                         text_color="#FFFFFF",
                                         command=self.go_back)
        self.back_button.place(relx=0.05, rely=0.88, relheight=0.1, relwidth=0.3)

    def update_admin_password(self):
        new_password = self.new_password_field.get()
        confirm_password = self.confirm_password_field.get()

        if new_password != confirm_password:
            self.status_label.configure(text="Las contraseñas no coinciden")
            return

        status, message = self.master.controller.update_admin_password(new_password)
        self.status_label.configure(text=message)
        
        if status:
            self.main_frame.after(1500, self.master.show_login)
