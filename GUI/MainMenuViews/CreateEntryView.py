import customtkinter as ctk
import threading

class CreateEntryView:
    # Maps the etapa combobox text to the Phases table id
    ETAPA_TO_PHASE_ID = {
        "Fase 1, $18000": 1,
        "Fase 2, $22000": 2,
        "Taquilla, $30000": 3,
        "Invitacion especial, $0": 4,
    }

    def __init__(self, parent_frame, main_menu):
        self.parent_frame = parent_frame
        self.main_menu = main_menu
        self.master = main_menu.master
        self.setup_ui()

    def setup_ui(self):
        self.nombre_entry = ctk.CTkEntry(master=self.parent_frame,
                                         fg_color="#FFFFFF",
                                         border_color="gray",
                                         text_color="#000000",
                                         placeholder_text="Nombre",
                                         font=self.master.main_font)
        self.nombre_entry.place(relx=0.05, rely=0.1, relwidth=0.50, relheight=0.08)

        self.edad_combo = ctk.CTkComboBox(master=self.parent_frame,
                                          values=[str(i) for i in range(18, 101)],
                                          fg_color="#FFFFFF",
                                          dropdown_fg_color="#FFFFFF",
                                          dropdown_hover_color="#E0E0E0",
                                          dropdown_text_color="#000000",
                                          border_color="gray",
                                          text_color="#000000",
                                          button_color="#FFFFFF",
                                          button_hover_color="#F0F0F0",
                                          font=self.master.main_font,
                                          state="readonly")
        self.edad_combo.set("Edad")
        self.edad_combo.place(relx=0.60, rely=0.1, relwidth=0.15, relheight=0.08)

        etapa_options = ["Fase 1, $18000", "Fase 2, $22000", "Taquilla, $30000", "Invitacion especial, $0"]
        self.etapa_combo = ctk.CTkComboBox(master=self.parent_frame,
                                           values=etapa_options,
                                           fg_color="#FFFFFF",
                                           dropdown_fg_color="#FFFFFF",
                                           dropdown_hover_color="#E0E0E0",
                                           dropdown_text_color="#000000",
                                           border_color="gray",
                                           text_color="#000000",
                                           button_color="#FFFFFF",
                                           button_hover_color="#F0F0F0",
                                           font=self.master.main_font,
                                           state="readonly")
        self.etapa_combo.set("Etapa")
        self.etapa_combo.place(relx=0.78, rely=0.1, relwidth=0.18, relheight=0.08)

        self.cedula_entry = ctk.CTkEntry(master=self.parent_frame,
                                         fg_color="#FFFFFF",
                                         border_color="gray",
                                         text_color="#000000",
                                         placeholder_text="Cédula",
                                         font=self.master.main_font)
        self.cedula_entry.place(relx=0.05, rely=0.25, relwidth=0.50, relheight=0.08)

        self.correo_entry = ctk.CTkEntry(master=self.parent_frame,
                                         fg_color="#FFFFFF",
                                         border_color="gray",
                                         text_color="#000000",
                                         placeholder_text="Correo",
                                         font=self.master.main_font)
        self.correo_entry.place(relx=0.05, rely=0.40, relwidth=0.50, relheight=0.08)

        self.send_email_var = ctk.BooleanVar(value=True)
        self.chk_send_email = ctk.CTkCheckBox(master=self.parent_frame,
                                              text="Enviar ticket por correo",
                                              text_color="#000000",
                                              fg_color=self.main_menu.header_color,
                                              hover_color=self.main_menu.sidebar_color,
                                              variable=self.send_email_var,
                                              font=self.master.main_font)
        self.chk_send_email.place(relx=0.05, rely=0.60, relwidth=0.45, relheight=0.08)

        self.btn_crear = ctk.CTkButton(master=self.parent_frame,
                                       text="Crear",
                                       fg_color=self.main_menu.header_color,
                                       hover_color=self.main_menu.sidebar_color,
                                       text_color="#FFFFFF",
                                       font=self.master.main_font,
                                       corner_radius=0,
                                       command=lambda: self.create_entry_action(validate=False))
        self.btn_crear.place(relx=0.55, rely=0.60, relwidth=0.30, relheight=0.08)

        self.btn_crear_validar = ctk.CTkButton(master=self.parent_frame,
                                               text="Crear y validar",
                                               fg_color=self.main_menu.header_color,
                                               hover_color=self.main_menu.sidebar_color,
                                               text_color="#FFFFFF",
                                               font=self.master.main_font,
                                               corner_radius=0,
                                               command=lambda: self.create_entry_action(validate=True))
        self.btn_crear_validar.place(relx=0.55, rely=0.72, relwidth=0.30, relheight=0.08)

    def create_entry_action(self, validate=False):
        if self.edad_combo.get() == "Edad" or self.etapa_combo.get() == "Etapa":
            self.main_menu.show_popup("Debes seleccionar la edad y/o etapa")
            return

        user = {
            "name": self.nombre_entry.get().strip(),
            "document": self.cedula_entry.get().strip(),
            "email": self.correo_entry.get().strip(),
            "age": int(self.edad_combo.get()),
            "phase_id": self.ETAPA_TO_PHASE_ID.get(self.etapa_combo.get()),
            "validated": 1 if validate else 0,
        }

        # Controller validates data and inserts into DB
        errors = self.master.controller.register_user(user)

        if not errors:
            # Disable buttons to prevent duplicate submissions
            self.btn_crear.configure(state="disabled")
            self.btn_crear_validar.configure(state="disabled")

            if self.send_email_var.get():
                # Show a loading popup while the email is being sent
                loading_popup = self._show_loading_popup("Enviando correo...")

                # Send ticket to user's email in a background thread
                def _send_email():
                    email_status = self.master.controller.send_ticket_to_email(user)
                    # Schedule the UI update back on the main thread
                    self.main_menu.container.after(0, lambda: self._on_email_sent(email_status, validate, loading_popup))

                thread = threading.Thread(target=_send_email, daemon=True)
                thread.start()
            else:
                msg = ("Entrada creada y validada exitosamente!\nSin envío de correo."
                       if validate
                       else "Entrada creada exitosamente!\nSin envío de correo.")
                self.main_menu.show_popup(msg)
                self.clear_create_entry_form()
                self.btn_crear.configure(state="normal")
                self.btn_crear_validar.configure(state="normal")
        else:
            error_messages = []
            for field, _status in errors.items():
                if field == "document used":
                    error_messages.append("La cédula ya está registrada")
                elif field == "document":
                    error_messages.append("Cédula inválida")
                elif field == "name":
                    error_messages.append("Nombre inválido")
                elif field == "email":
                    error_messages.append("Correo inválido")
            self.main_menu.show_popup("\n".join(error_messages))

    def clear_create_entry_form(self):
        self.nombre_entry.delete(0, "end")
        self.cedula_entry.delete(0, "end")
        self.correo_entry.delete(0, "end")
        self.edad_combo.set("Edad")
        self.etapa_combo.set("Etapa")

    def _show_loading_popup(self, message):
        """Show a non-blocking loading popup while an operation runs in the background."""
        popup = ctk.CTkToplevel(self.main_menu.container)
        popup.title("Procesando")
        popup.geometry("400x200")
        popup.transient(self.main_menu.container.winfo_toplevel())
        popup.grab_set()

        def _close_popup():
            try:
                popup.grab_release()
                popup.destroy()
            except Exception:
                pass
            self.btn_crear.configure(state="normal")
            self.btn_crear_validar.configure(state="normal")

        # Allow the user to close it to unblock the UI
        popup.protocol("WM_DELETE_WINDOW", _close_popup)

        label = ctk.CTkLabel(popup, text=message, font=self.master.main_font, text_color="#FFFFFF")
        label.pack(expand=True, pady=(20, 10))
        
        btn_close = ctk.CTkButton(popup, text="Cerrar / Continuar en fondo", 
                                  command=_close_popup, 
                                  fg_color=self.main_menu.header_color, 
                                  hover_color=self.main_menu.sidebar_color,
                                  font=self.master.main_font)
        btn_close.pack(pady=10)
        return popup

    def _on_email_sent(self, email_status, validate, loading_popup):
        """Called on the main thread after the email thread finishes."""
        # Close the loading popup
        try:
            loading_popup.grab_release()
            loading_popup.destroy()
        except Exception:
            pass

        # Re-enable the create buttons
        self.btn_crear.configure(state="normal")
        self.btn_crear_validar.configure(state="normal")

        if email_status[0]:
            msg = ("Entrada creada y validada exitosamente!\nTicket enviado al correo."
                   if validate
                   else "Entrada creada exitosamente!\nTicket enviado al correo.")
        else:
            msg = "Entrada creada pero no se pudo enviar el correo:\n" + email_status[1]
        self.main_menu.show_popup(msg)
        self.clear_create_entry_form()
