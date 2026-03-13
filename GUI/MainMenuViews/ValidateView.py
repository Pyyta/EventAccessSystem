import customtkinter as ctk

class ValidateView:
    def __init__(self, parent_frame, main_menu):
        self.parent_frame = parent_frame
        self.main_menu = main_menu
        self.master = main_menu.master
        self.setup_ui()

    def setup_ui(self):
        # Validation Input
        self.validation_entry = ctk.CTkEntry(master=self.parent_frame,
                                               fg_color="#FFFFFF",
                                               border_color="gray",
                                               text_color="#000000",
                                               font=self.master.main_font)
        self.validation_entry.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.1)

        # Validation Button
        self.submit_button = ctk.CTkButton(master=self.parent_frame,
                                            text="Validar",
                                            fg_color=self.main_menu.header_color,
                                            hover_color=self.main_menu.sidebar_color,
                                            text_color="#FFFFFF",
                                            font=self.master.main_font,
                                            corner_radius=0,
                                            command=self.validate_ticket)
        self.submit_button.place(relx=0.15, rely=0.45, relwidth=0.3, relheight=0.08)

    def validate_ticket(self):
        token = self.validation_entry.get().strip()
        if not token:
            return

        status_name = self.master.controller.check_scanned_token(token)
        if status_name is True or isinstance(status_name, str):
            # The repository method check_scanned_token originally returns the user's name if Validated
            name = status_name if isinstance(status_name, str) else ""
            self.main_menu.show_popup("Ticket aceptado, Bienvenido!" + name)
            self.validation_entry.delete(0, 'end')
        elif status_name == False:
            self.main_menu.show_popup("Ticket ya validado!")
        elif status_name is None:
            self.main_menu.show_popup("No encontrado")
