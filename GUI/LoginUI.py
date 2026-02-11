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
                                      corner_radius= 41
                                      )
        login_main_frame.place(x= 353, y=120)