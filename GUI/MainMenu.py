import customtkinter as ctk
import threading
from tkinter import filedialog

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
                                          anchor="center",
                                          command=self.show_validate_view)
        self.btn_validate.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.08)

        # 2. Create new entry
        self.btn_create = ctk.CTkButton(master=self.sidebar_frame,
                                        text="Crear nueva entrada",
                                        fg_color=self.button_idle_color,
                                        hover_color=self.button_idle_color,
                                        font=self.master.main_font,
                                        corner_radius=0,
                                        anchor="center",
                                        command=self.show_create_entry_view)
        self.btn_create.place(relx=0.1, rely=0.20, relwidth=0.8, relheight=0.08)

        # 3. Search User
        self.btn_search_user = ctk.CTkButton(master=self.sidebar_frame,
                                              text="Buscar usuario",
                                              fg_color=self.button_idle_color,
                                              hover_color=self.button_idle_color,
                                              font=self.master.main_font,
                                              corner_radius=0,
                                              anchor="center",
                                              command=self.show_search_user_view)
        self.btn_search_user.place(relx=0.1, rely=0.32, relwidth=0.8, relheight=0.08)

        self.btn_services = ctk.CTkButton(master=self.sidebar_frame,
                                            text="Servicios/Productos",
                                            fg_color=self.button_idle_color,
                                            hover_color=self.button_idle_color,
                                            font=self.master.main_font,
                                            corner_radius=0,
                                            anchor="center",
                                            command=self.show_services_view)
        self.btn_services.place(relx=0.1, rely=0.44, relwidth=0.8, relheight=0.08)

        # 5. View Registry
        self.btn_registry = ctk.CTkButton(master=self.sidebar_frame,
                                           text="Ver Registro",
                                           fg_color=self.button_idle_color,
                                           hover_color=self.button_idle_color,
                                           font=self.master.main_font,
                                           corner_radius=0,
                                           anchor="center",
                                           command=self.show_registry_view)
        self.btn_registry.place(relx=0.1, rely=0.56, relwidth=0.8, relheight=0.08)

        # 6. View generated income
        self.btn_income = ctk.CTkButton(master=self.sidebar_frame,
                                           text="Ver ingresos\ngenerados",
                                           fg_color=self.button_idle_color,
                                           hover_color=self.button_idle_color,
                                           font=self.master.main_font,
                                           corner_radius=0,
                                           anchor="center",
                                           command=self.show_income_view)
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

    def update_sidebar_buttons(self, active_btn):
        for btn in [self.btn_validate, self.btn_create, self.btn_search_user, self.btn_services, self.btn_registry, self.btn_income]:
            btn.configure(fg_color=self.button_idle_color)
        active_btn.configure(fg_color=self.button_active_color)

    def show_validate_view(self):
        # Clean current view
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.update_sidebar_buttons(self.btn_validate)

        from GUI.MainMenuViews.ValidateView import ValidateView
        self.current_view = ValidateView(parent_frame=self.content_frame, main_menu=self)

    def show_create_entry_view(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.update_sidebar_buttons(self.btn_create)

        from GUI.MainMenuViews.CreateEntryView import CreateEntryView
        self.current_view = CreateEntryView(parent_frame=self.content_frame, main_menu=self)

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

    # ========================== Search User View ==========================

    # Phase ID -> phase name mapping
    PHASE_NAMES = {
        1: "Fase 1",
        2: "Fase 2",
        3: "Taquilla",
        4: "Invitación especial",
    }

    def show_services_view(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.update_sidebar_buttons(self.btn_services)

        from GUI.MainMenuViews.ServicesView import ServicesView
        self.current_view = ServicesView(parent_frame=self.content_frame, main_menu=self)

    def show_registry_view(self):
        # Clean current view
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.update_sidebar_buttons(self.btn_registry)

        from GUI.MainMenuViews.RegistryView import RegistryView
        self.current_view = RegistryView(parent_frame=self.content_frame, main_menu=self)

    def show_income_view(self):
        # Clean current view
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.update_sidebar_buttons(self.btn_income)

        from GUI.MainMenuViews.IncomeView import IncomeView
        self.current_view = IncomeView(parent_frame=self.content_frame, main_menu=self)

    def show_search_user_view(self):
        """Display the search-by-document view."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.update_sidebar_buttons(self.btn_search_user)

        from GUI.MainMenuViews.SearchUserView import SearchUserView
        self.current_view = SearchUserView(parent_frame=self.content_frame, main_menu=self)