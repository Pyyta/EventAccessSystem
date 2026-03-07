import customtkinter as ctk

class MainMenu:
    def __init__(self, parent_container, master):
        self.container = parent_container
        self.master = master
        
        # Colors based on the UI theme
        self.sidebar_color = "#034040"
        self.header_color = "#011A1A"
        self.button_idle_color = "#011A1A"
        self.button_active_color = "transparent"
        self.bg_color = "#FFFFFF"

        self.setup_ui()

    def setup_ui(self):
        # Clean the container
        for widget in self.container.winfo_children():
            widget.destroy()

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(master=self.container, 
                                          fg_color=self.sidebar_color,
                                          corner_radius=0)
        self.sidebar_frame.place(relx=0, rely=0, relwidth=0.25, relheight=1.0)

        # Buttons in Sidebar
        # 1. Validate (Active initially)
        self.btn_validate = ctk.CTkButton(master=self.sidebar_frame,
                                          text="Validar",
                                          fg_color=self.button_active_color,
                                          hover_color=self.button_idle_color,
                                          font=self.master.main_font,
                                          corner_radius=0,
                                          anchor="center")
        self.btn_validate.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.08)

        # 2. Create new entry
        self.btn_create = ctk.CTkButton(master=self.sidebar_frame,
                                        text="Crear nueva entrada",
                                        fg_color=self.button_idle_color,
                                        hover_color=self.button_idle_color,
                                        font=self.master.main_font,
                                        corner_radius=0,
                                        anchor="center")
        self.btn_create.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.08)

        # 3. Services/Products
        self.btn_services = ctk.CTkButton(master=self.sidebar_frame,
                                            text="Servicios/Productos",
                                            fg_color=self.button_idle_color,
                                            hover_color=self.button_idle_color,
                                            font=self.master.main_font,
                                            corner_radius=0,
                                            anchor="center")
        self.btn_services.place(relx=0.1, rely=0.40, relwidth=0.8, relheight=0.08)

        # 4. View Registry
        self.btn_registry = ctk.CTkButton(master=self.sidebar_frame,
                                           text="Ver Registro",
                                           fg_color=self.button_idle_color,
                                           hover_color=self.button_idle_color,
                                           font=self.master.main_font,
                                           corner_radius=0,
                                           anchor="center")
        self.btn_registry.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.08)

        # 5. View generated income
        self.btn_income = ctk.CTkButton(master=self.sidebar_frame,
                                           text="Ver ingresos\ngenerados",
                                           fg_color=self.button_idle_color,
                                           hover_color=self.button_idle_color,
                                           font=self.master.main_font,
                                           corner_radius=0,
                                           anchor="center")
        self.btn_income.place(relx=0.1, rely=0.80, relwidth=0.8, relheight=0.12)

        # --- Header ---
        self.header_frame = ctk.CTkFrame(master=self.container,
                                          fg_color=self.header_color,
                                          corner_radius=0)
        self.header_frame.place(relx=0.25, rely=0, relwidth=0.75, relheight=0.15)

        self.title_label = ctk.CTkLabel(master=self.header_frame,
                                        text="SISTEMA DE TICKETES PARA BLADE & BASS",
                                        font=self.master.title_font,
                                        text_color="#FFFFFF")
        self.title_label.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        # --- Main Content Area ---
        self.content_frame = ctk.CTkFrame(master=self.container,
                                           fg_color=self.bg_color,
                                           corner_radius=0)
        self.content_frame.place(relx=0.25, rely=0.15, relwidth=0.75, relheight=0.85)

        # Initial View: Validate
        self.show_validate_view()

    def show_validate_view(self):
        # Clean current view
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Validation Input
        self.validation_entry = ctk.CTkEntry(master=self.content_frame,
                                               fg_color="#FFFFFF",
                                               border_color="gray",
                                               text_color="#000000",
                                               font=self.master.main_font)
        self.validation_entry.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.1)

        # Validation Button
        self.submit_button = ctk.CTkButton(master=self.content_frame,
                                            text="Validar",
                                            fg_color=self.header_color,
                                            hover_color=self.sidebar_color,
                                            text_color="#FFFFFF",
                                            font=self.master.main_font,
                                            corner_radius=0,
                                            command=self.validate_ticket)
        self.submit_button.place(relx=0.15, rely=0.45, relwidth=0.3, relheight=0.08)

    def validate_ticket(self):
        token = self.validation_entry.get().strip()
        if not token:
            return

        status = self.master.controller.check_scanned_token(token)
        
        if status == True:
            self.show_popup("Ticket aceptado, Bienvenido!")
            self.validation_entry.delete(0, 'end')
        elif status == False:
            self.show_popup("Ticket ya validado!")
        elif status is None:
            self.show_popup("No encontrado")

    def show_popup(self, message):
        popup = ctk.CTkToplevel(self.container)
        popup.title("Validación")
        popup.geometry("400x200")
        
        # Center relative to parent and make it modal
        popup.transient(self.container.winfo_toplevel())
        popup.grab_set()

        label = ctk.CTkLabel(popup, text=message, font=self.master.main_font, text_color="#FFFFFF")
        label.pack(expand=True, pady=(20, 10))

        btn_ok = ctk.CTkButton(popup, 
                               text="OK", 
                               font=self.master.main_font, 
                               fg_color=self.header_color,
                               hover_color=self.sidebar_color,
                               command=popup.destroy)
        btn_ok.pack(pady=(10, 20))