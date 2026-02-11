#libraries
from pathlib import Path
import customtkinter as ctk
import os

#Calls to UI screens
from GUI import LoginUI

#Calls to logic files


class UserInterface:
    def __init__(self):
        self.__root=ctk.CTk()
        """
        Window initial settings 
        """
        self.__root.geometry("1280x720")
        self.__root.minsize(800, 600)
        self.__root.title("Validacion de boletas")

        #favicon
        self.images_dir= os.path.join(Path(__file__).parents[1], "Assets", "Images")
        iconbitmap_loc= os.path.join(self.images_dir, "iconbit.ico")
        self.__root.iconbitmap(iconbitmap_loc)

        self.container=ctk.CTkFrame(self.__root)
        self.container.pack(expand=True, fill="both")
        self.show_login()
        
    def show_login(self):
        login=LoginUI.LoginUI(parent_container= self.container,
                master= self)
        

    def run(self):
        self.__root.mainloop()
                