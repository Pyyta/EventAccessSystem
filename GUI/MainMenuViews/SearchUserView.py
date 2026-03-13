import customtkinter as ctk
from tkinter import filedialog

class SearchUserView:
    # Phase ID -> phase name mapping
    PHASE_NAMES = {
        1: "Fase 1",
        2: "Fase 2",
        3: "Taquilla",
        4: "Invitación especial",
    }

    def __init__(self, parent_frame, main_menu):
        self.parent_frame = parent_frame
        self.main_menu = main_menu
        self.master = main_menu.master
        self.setup_ui()

    def setup_ui(self):
        # Search input
        self.search_entry = ctk.CTkEntry(master=self.parent_frame,
                                         fg_color="#FFFFFF",
                                         border_color="gray",
                                         text_color="#000000",
                                         placeholder_text="Ingrese el numero de cedula sin puntos (ej: 1021986523)",
                                         font=self.master.main_font)
        self.search_entry.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.08)

        # Search button
        self.btn_search = ctk.CTkButton(master=self.parent_frame,
                                        text="Buscar",
                                        fg_color=self.main_menu.header_color,
                                        hover_color=self.main_menu.sidebar_color,
                                        text_color="#FFFFFF",
                                        font=self.master.main_font,
                                        corner_radius=0,
                                        command=self.execute_user_search)
        self.btn_search.place(relx=0.35, rely=0.30, relwidth=0.3, relheight=0.08)

        # Results container (will be populated after a search)
        self.search_results_frame = ctk.CTkFrame(master=self.parent_frame,
                                                  fg_color="transparent")
        self.search_results_frame.place(relx=0.05, rely=0.45, relwidth=0.9, relheight=0.50)

    def execute_user_search(self):
        """Search for a user by document and display results with action buttons."""
        document = self.search_entry.get().strip()
        if not document:
            self.main_menu.show_popup("Ingrese un número de cédula")
            return

        # Validate document format
        if not self.master.controller.validate_document(document):
            self.main_menu.show_popup("Cédula inválida")
            return

        user_data = self.master.controller.get_user_by_document(document)

        # Clear previous results
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()

        if user_data is None:
            self.main_menu.show_popup("Usuario no encontrado")
            return

        # Unpack user data: (id, document, name, email, age, validated, date, token, phase_id)
        user_id, user_doc, user_name, user_email, user_age, user_validated, user_date, user_token, user_phase_id = user_data

        # Build a dict for ticket generation
        self._found_user = {
            "name": user_name,
            "document": user_doc,
            "email": user_email,
            "date": user_date,
            "token": user_token,
        }

        validated_text = "Sí" if user_validated else "No"
        phase_name = self.PHASE_NAMES.get(user_phase_id, "Desconocida")

        # --- User info labels ---
        info_font = ctk.CTkFont(family="Jaini Purva", size=20)

        info_lines = [
            f"Nombre:  {user_name}",
            f"Cédula:  {user_doc}",
            f"Correo:  {user_email}",
            f"Edad:  {user_age}",
            f"Etapa:  {phase_name}",
            f"Validado:  {validated_text}",
            f"Fecha de compra:  {user_date}",
        ]

        for i, line in enumerate(info_lines):
            lbl = ctk.CTkLabel(master=self.search_results_frame,
                               text=line,
                               font=info_font,
                               text_color="#000000",
                               anchor="w")
            lbl.place(relx=0.02, rely=0.02 + i * 0.11, relwidth=0.55, relheight=0.10)

        # --- Action buttons ---
        btn_width = 0.32
        btn_x = 0.65

        self.btn_reset_user = ctk.CTkButton(master=self.search_results_frame,
                                            text="Resetear usuario",
                                            fg_color="#2E6B6B",
                                            hover_color=self.main_menu.sidebar_color,
                                            text_color="#FFFFFF",
                                            font=self.master.main_font,
                                            corner_radius=6,
                                            command=lambda: self.action_reset_user(user_doc))
        self.btn_reset_user.place(relx=btn_x, rely=0.05, relwidth=btn_width, relheight=0.18)

        self.btn_delete_user = ctk.CTkButton(master=self.search_results_frame,
                                             text="Eliminar usuario",
                                             fg_color="#8B2020",
                                             hover_color="#A52A2A",
                                             text_color="#FFFFFF",
                                             font=self.master.main_font,
                                             corner_radius=6,
                                             command=lambda: self.action_delete_user(user_doc))
        self.btn_delete_user.place(relx=btn_x, rely=0.30, relwidth=btn_width, relheight=0.18)

        self.btn_save_ticket = ctk.CTkButton(master=self.search_results_frame,
                                             text="Guardar ticket\nlocalmente",
                                             fg_color=self.main_menu.header_color,
                                             hover_color=self.main_menu.sidebar_color,
                                             text_color="#FFFFFF",
                                             font=self.master.main_font,
                                             corner_radius=6,
                                             command=self.action_save_ticket_locally)
        self.btn_save_ticket.place(relx=btn_x, rely=0.55, relwidth=btn_width, relheight=0.18)

    def action_reset_user(self, document):
        """Reset (un-validate) the user."""
        success = self.master.controller.reset_one_user(document)
        if success:
            self.main_menu.show_popup("Usuario reseteado exitosamente")
            # Refresh search results
            self.execute_user_search()
        else:
            self.main_menu.show_popup("No se pudo resetear el usuario")

    def action_delete_user(self, document):
        """Delete the user from the database."""
        success = self.master.controller.delete_one_user(document)
        if success:
            self.main_menu.show_popup("Usuario eliminado exitosamente")
            # Clear results since user no longer exists
            for widget in self.search_results_frame.winfo_children():
                widget.destroy()
        else:
            self.main_menu.show_popup("No se pudo eliminar el usuario")

    def action_save_ticket_locally(self):
        """Save the ticket PDF to a user-chosen location via file dialog."""
        if not hasattr(self, '_found_user') or self._found_user is None:
            self.main_menu.show_popup("No hay usuario seleccionado")
            return

        file_path = filedialog.asksaveasfilename(
            title="Guardar ticket como",
            defaultextension=".pdf",
            filetypes=[("Archivo PDF", "*.pdf")],
            initialfile=f"{self._found_user['document']}_ticket.pdf"
        )

        if not file_path:
            return  # User cancelled the dialog

        result = self.master.controller.save_ticket_to_path(self._found_user, file_path)
        if result[0]:
            self.main_menu.show_popup(f"Ticket guardado exitosamente")
        else:
            self.main_menu.show_popup(f"Error al guardar el ticket:\n{result[1]}")
