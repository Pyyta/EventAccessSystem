#libraries
from pathlib import Path
import customtkinter as ctk
import os
import threading
import ctypes
from ctypes import windll

#Calls to UI screens
from GUI import LoginUI

#Calls to logic files
from Logic import Controller


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

        #Font
        font_path = os.path.join(Path(__file__).parents[1], "Assets", "Fonts", "JainiPurva-Regular.ttf")
        
        # Register font on Windows
        if os.name == 'nt':
            windll.gdi32.AddFontResourceW(font_path)
            # Notify other apps that the font resource has changed
            # 0x1D is WM_FONTCHANGE
            # 0xFFFF is HWND_BROADCAST
            windll.user32.SendMessageW(0xFFFF, 0x1D, 0, 0)

        self.main_font = ctk.CTkFont(family="Jaini Purva", size=25)
        self.title_font = ctk.CTkFont(family="Jaini Purva", size=50)

        #Logic Initialization
        self.controller = Controller.Controller()

        self.recovery_time_left = 0
        self.recovery_timer_id = None
        self.current_view = None

        self.container=ctk.CTkFrame(self.__root)
        self.container.pack(expand=True, fill="both")
        self.show_login()
        
    def trigger_password_recovery_email(self):
        def _send():
            status, message = self.controller.admin_password_recovery()
            # Schedule UI update on the main thread
            self.container.after(0, lambda: self._on_recovery_email_sent(status, message))

        thread = threading.Thread(target=_send, daemon=True)
        thread.start()

    def _on_recovery_email_sent(self, status, message):
        """Called on the main thread after the recovery email thread finishes."""
        if status:
            self.start_recovery_timer()
        if hasattr(self, 'current_view') and hasattr(self.current_view, 'on_recovery_email_result'):
            self.current_view.on_recovery_email_result(status, message)

    def start_recovery_timer(self):
        if self.recovery_timer_id is not None:
            self.container.after_cancel(self.recovery_timer_id)
        self.recovery_time_left = 60
        self._tick_recovery_timer()

    def _tick_recovery_timer(self):
        if self.recovery_time_left > 0:
            self.recovery_time_left -= 1
            self.recovery_timer_id = self.container.after(1000, self._tick_recovery_timer)
            if hasattr(self, 'current_view') and hasattr(self.current_view, 'update_timer'):
                self.current_view.update_timer()
        else:
            self.recovery_timer_id = None
            if hasattr(self, 'current_view') and hasattr(self.current_view, 'update_timer'):
                self.current_view.update_timer()

    def show_login(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        self.current_view = LoginUI.LoginUI(parent_container= self.container, master= self)
                
    def show_password_recovery(self):
        if self.recovery_time_left == 0:
            self.trigger_password_recovery_email()
            
        for widget in self.container.winfo_children():
            widget.destroy()
        from GUI import PasswordRecovery
        self.current_view = PasswordRecovery.PasswordRecovery(parent_container=self.container, master=self)
        
    def show_main_menu(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        from GUI import MainMenu
        self.current_view = MainMenu.MainMenu(parent_container=self.container, master=self)

    def run(self):
        self.__root.mainloop()
                