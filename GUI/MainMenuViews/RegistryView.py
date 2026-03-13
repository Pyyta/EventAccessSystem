import customtkinter as ctk
from tkinter import filedialog, messagebox

class RegistryView:
    def __init__(self, parent_frame, main_menu):
        self.parent_frame = parent_frame
        self.main_menu = main_menu
        self.master = main_menu.master
        self.setup_ui()

    def setup_ui(self):
        # We can add a label and a button to export
        self.title_label = ctk.CTkLabel(master=self.parent_frame,
                                        text="Exportar Registro de Usuarios",
                                        font=self.master.title_font,
                                        text_color="#000000")
        self.title_label.place(relx=0.0, rely=0.2, relwidth=1.0)
        
        self.btn_export = ctk.CTkButton(master=self.parent_frame,
                                        text="Exportar a Excel",
                                        fg_color=self.main_menu.header_color,
                                        hover_color=self.main_menu.sidebar_color,
                                        text_color="#FFFFFF",
                                        font=self.master.main_font,
                                        corner_radius=6,
                                        command=self.action_export_csv)
        self.btn_export.place(relx=0.2, rely=0.5, relwidth=0.25, relheight=0.1)

        self.btn_delete_all = ctk.CTkButton(master=self.parent_frame,
                                            text="Borrar registro",
                                            fg_color="#8B2020",
                                            hover_color="#A52A2A",
                                            text_color="#FFFFFF",
                                            font=self.master.main_font,
                                            corner_radius=6,
                                            command=self.action_delete_all_users)
        self.btn_delete_all.place(relx=0.55, rely=0.5, relwidth=0.25, relheight=0.1)

    def action_export_csv(self):
        file_path = filedialog.asksaveasfilename(
            title="Guardar registro como",
            defaultextension=".csv",
            filetypes=[("Archivo CSV", "*.csv")],
            initialfile="registro_usuarios.csv"
        )
        
        if not file_path:
            return  # User cancelled the dialog

        result = self.master.controller.export_all_users(file_path)
        if result is None:
            self.main_menu.show_popup("No hay usuarios para exportar")
        elif result is True:
            self.main_menu.show_popup("Registro exportado exitosamente")
        else:
            self.main_menu.show_popup("Error al exportar el registro")
            
    def action_delete_all_users(self):
        confirm = messagebox.askyesno(
            "Confirmar acción",
            "¿Estás seguro de que quieres borrar a TODOS los usuarios? Esta acción no se puede deshacer.",
            parent=self.main_menu.container.winfo_toplevel()
        )
        
        if confirm:
            success = self.master.controller.delete_all_users()
            if success:
                self.main_menu.show_popup("Todos los usuarios han sido eliminados.")
            else:
                self.main_menu.show_popup("Error al intentar eliminar los usuarios.")
