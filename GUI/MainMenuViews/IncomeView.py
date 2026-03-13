import customtkinter as ctk

class IncomeView:
    def __init__(self, parent_frame, main_menu):
        self.parent_frame = parent_frame
        self.main_menu = main_menu
        self.master = main_menu.master
        self.setup_ui()

    def setup_ui(self):
        # Fetch the income dictionary from the controller
        gains_data = self.master.controller.get_total_gains()
        
        # If there is no data or database error, use fallback values
        if gains_data is None:
            gains_data = {
                "earlier phases": 0,
                "sold at checkout": 0,
                "total accesories": 0,
                "total_gains": 0
            }

        title_label = ctk.CTkLabel(master=self.parent_frame,
                                   text="Ingresos Generados",
                                   font=self.master.title_font,
                                   text_color="#000000")
        title_label.place(relx=0.0, rely=0.1, relwidth=1.0)

        # Labels for displaying different income sources
        font_info = ctk.CTkFont(family="Jaini Purva", size=22)

        info_lines = [
            f"Fases anteriores: ${gains_data.get('earlier phases', 0):,.2f}",
            f"Taquilla: ${gains_data.get('sold at checkout', 0):,.2f}",
            f"Accesorios Totales: ${gains_data.get('total accesories', 0):,.2f}",
            "",
            f"Ingresos Totales: ${gains_data.get('total_gains', 0):,.2f}"
        ]

        for i, line in enumerate(info_lines):
            lbl = ctk.CTkLabel(master=self.parent_frame,
                               text=line,
                               font=font_info,
                               text_color="#000000",
                               anchor="center")
            lbl.place(relx=0.1, rely=0.3 + i * 0.1, relwidth=0.8)
