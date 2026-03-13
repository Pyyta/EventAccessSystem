import customtkinter as ctk

class ServicesView:
    def __init__(self, parent_frame, main_menu):
        self.parent_frame = parent_frame
        self.main_menu = main_menu
        self.master = main_menu.master
        self.setup_ui()

    def setup_ui(self):
        # --- Search Area ---
        self.search_entry = ctk.CTkEntry(master=self.parent_frame,
                                         fg_color="#FFFFFF",
                                         border_color="gray",
                                         text_color="#000000",
                                         placeholder_text="Escriba el numero de documento",
                                         font=self.master.main_font)
        self.search_entry.place(relx=0.1, rely=0.1, relwidth=0.6, relheight=0.08)

        self.btn_search = ctk.CTkButton(master=self.parent_frame,
                                        text="Buscar",
                                        fg_color=self.main_menu.header_color,
                                        hover_color=self.main_menu.sidebar_color,
                                        text_color="#FFFFFF",
                                        font=self.master.main_font,
                                        corner_radius=0,
                                        command=self.search_user)
        self.btn_search.place(relx=0.75, rely=0.1, relwidth=0.15, relheight=0.08)

        # Status Label (El sr/sra {name})
        self.lbl_status = ctk.CTkLabel(master=self.parent_frame,
                                       text="",
                                       font=self.master.main_font,
                                       text_color="#000000",
                                       anchor="w")
        self.lbl_status.place(relx=0.1, rely=0.2, relwidth=0.6, relheight=0.05)

        # --- Accesories Area ---
        # Combobox for accessory
        self.asset_options = ["Locker, $8000", "Bandana, $4000"]
        self.asset_combo = ctk.CTkComboBox(master=self.parent_frame,
                                           values=self.asset_options,
                                           fg_color="#FFFFFF",
                                           dropdown_fg_color="#FFFFFF",
                                           dropdown_hover_color="#E0E0E0",
                                           dropdown_text_color="#000000",
                                           border_color="gray",
                                           text_color="#000000",
                                           button_color="#FFFFFF",
                                           button_hover_color="#F0F0F0",
                                           font=self.master.main_font,
                                           state="readonly",
                                           command=self.on_asset_changed)
        self.asset_combo.set("Seleccione el accesorio")
        self.asset_combo.place(relx=0.1, rely=0.35, relwidth=0.4, relheight=0.08)

        # Locker entry (only visible when Locker is selected)
        self.locker_entry = ctk.CTkEntry(master=self.parent_frame,
                                         fg_color="#FFFFFF",
                                         border_color="gray",
                                         text_color="#000000",
                                         placeholder_text="Escriba el numero de locker",
                                         font=self.master.main_font)
        # We start with it hidden or disabled depending on the mockup.
        # It's better to just place it but make it invisible initially, or we could just 
        # keep it empty. Let's make it visible when Locker is selected.
        

        # --- Footer Buttons ---
        self.btn_finalize = ctk.CTkButton(master=self.parent_frame,
                                          text="Finalizar",
                                          fg_color=self.main_menu.header_color,
                                          hover_color=self.main_menu.sidebar_color,
                                          text_color="#FFFFFF",
                                          font=self.master.main_font,
                                          corner_radius=0,
                                          command=self.action_finalize)
        self.btn_finalize.place(relx=0.1, rely=0.7, relwidth=0.3, relheight=0.08)

        self.btn_view_lockers = ctk.CTkButton(master=self.parent_frame,
                                              text="Ver lockers asignados",
                                              fg_color=self.main_menu.header_color,
                                              hover_color=self.main_menu.sidebar_color,
                                              text_color="#FFFFFF",
                                              font=self.master.main_font,
                                              corner_radius=0,
                                              command=self.action_view_lockers)
        self.btn_view_lockers.place(relx=0.5, rely=0.7, relwidth=0.4, relheight=0.08)

    def search_user(self):
        document = self.search_entry.get().strip()
        if not document:
            self.lbl_status.configure(text="Ingrese número de documento")
            return

        if not self.master.controller.validate_document(document):
            self.lbl_status.configure(text="Cédula inválida")
            return

        user_data = self.master.controller.get_user_by_document(document)
        if user_data:
            user_name = user_data[2]  # Unpack based on previous logic (id, doc, name...)
            self.lbl_status.configure(text=f"El sr/sra {user_name}")
        else:
            self.lbl_status.configure(text="No encontrado")

    def on_asset_changed(self, choice):
        if choice == "Locker, $8000":
            self.locker_entry.place(relx=0.6, rely=0.35, relwidth=0.3, relheight=0.08)
        else:
            self.locker_entry.place_forget()

    def action_finalize(self):
        document = self.search_entry.get().strip()
        asset_choice = self.asset_combo.get()
        num_locker = self.locker_entry.get().strip() if asset_choice == "Locker, $8000" else ""

        if "El sr/sra" not in self.lbl_status.cget("text"):
            self.main_menu.show_popup("Primero debe buscar y seleccionar un usuario válido.")
            return

        if asset_choice == "Seleccione el accesorio":
            self.main_menu.show_popup("Debe seleccionar un accesorio.")
            return

        if asset_choice == "Locker, $8000" and not num_locker:
            self.main_menu.show_popup("Debe ingresar un número de locker.")
            return

        id_asset = 1 if asset_choice == "Locker, $8000" else 2

        asset_data = {
            "document": document,
            "id_asset": id_asset,
            "num_locker": num_locker
        }

        success = self.master.controller.buy_accessory(asset_data)
        if success:
            self.main_menu.show_popup("Accesorio comprado exitosamente.")
            # Clear fields
            self.search_entry.delete(0, 'end')
            self.lbl_status.configure(text="")
            self.asset_combo.set("Seleccione el accesorio")
            self.locker_entry.delete(0, 'end')
            self.locker_entry.place_forget()
        else:
            self.main_menu.show_popup("No se pudo realizar la compra. Ya tiene este accesorio o el usuario no existe.")

    def action_view_lockers(self):
        lockers = self.master.controller.get_lockers()
        
        popup = ctk.CTkToplevel(self.main_menu.container)
        popup.title("Lockers Asignados")
        popup.geometry("500x400")
        popup.transient(self.main_menu.container.winfo_toplevel())
        popup.grab_set()

        title_lbl = ctk.CTkLabel(popup, text="Listado de Lockers", font=self.master.title_font)
        title_lbl.pack(pady=10)

        # Scrollable frame for lockers
        scroll_frame = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        scroll_frame.pack(expand=True, fill="both", padx=20, pady=10)

        if not lockers:
            lbl = ctk.CTkLabel(scroll_frame, text="No hay lockers asignados aún.", font=self.master.main_font)
            lbl.pack(pady=10)
        else:
            for locker_data in lockers:
                # Based on query: SELECT Users.document, name, num_locker
                doc, name, num_locker = locker_data
                text_info = f"Locker {num_locker} - {name} ({doc})"
                lbl = ctk.CTkLabel(scroll_frame, text=text_info, font=self.master.main_font, anchor="w")
                lbl.pack(fill="x", pady=2)

        btn_close = ctk.CTkButton(popup, 
                                  text="Cerrar", 
                                  font=self.master.main_font, 
                                  fg_color=self.main_menu.header_color,
                                  hover_color=self.main_menu.sidebar_color,
                                  command=popup.destroy)
        btn_close.pack(pady=10)
