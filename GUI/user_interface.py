#author: Daniel Pita Romero (created without Copilot)

#libraries
import customtkinter as ctk
#main class
class MainMenu:
    def __init__(self, root):
        #initial settings
        self.root=root
        self.root.geometry("1280x720")
        self.root.minsize(800, 600)
        #self.root.iconbitmap("C:/Users/dpita/OneDrive/Documentos/proyectos python/Software entradas/iconbit.ico") #app logo 
        self.root.title("Validacion de boletas")
        
        #Creates and sets the ratios of the main Rows and Columns
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=15)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        
        #top and bottom menu
        self.top_menu=ctk.CTkFrame(self.root, fg_color="#011F26", corner_radius=0)
        self.top_menu.grid(row=0, column=1, sticky="nsew")
        self.bottom_menu=ctk.CTkFrame(self.root, fg_color="white")
        self.bottom_menu.grid(row=1, column=1, sticky="nsew")
        #top menu title
        self.title=ctk.CTkLabel(self.top_menu, font=("Jaini Purva", 64), text="SISTEMA DE VALIDACION DE BOLETAS")        
        self.title.pack(fill="x", expand=True)
        self.root.bind("<Configure>", self.font_resize)
        #left menu (where all the buttons are placed)
        self.left_menu=ctk.CTkFrame(self.root, fg_color="#014F61", corner_radius=0)
        self.left_menu.grid(row=0, column=0, rowspan=2, sticky="nsew")
        #buttons
        self.create_buttons()
    
    def create_buttons(self):
        
        self.validate_button=self.command_button("Validar", self.prueba)
        self.validate_button.pack(fill="x", expand=True, padx=40)
        self.create_button=self.command_button("Crear nueva entrada", self.prueba)
        self.create_button.pack(fill="x", expand=True, padx=40)
        self.services_button=self.command_button("Servicios/Productos", self.prueba)
        self.services_button.pack(fill="x", expand=True, padx=40)
        self.register_button=self.command_button("Ver Registro", self.prueba)
        self.register_button.pack(fill="x", expand=True, padx=40)
        self.gains_button=self.command_button("Ver ingresos generados", self.prueba)
        self.gains_button.pack(fill="x", expand=True, padx=40)

    def command_button(self, text, function):
        return ctk.CTkButton(master=self.left_menu, text=text, command=function, fg_color="#011F26", corner_radius=0, font=("Jaini Purva", 25), height=80)

    def prueba(self):
        print("ola, soy omelo chino")
    #make the font responsive
    def font_resize(self, event):
        if event.widget == self.root:   #run when something change in the main window (root), not when a child item changes
            new_title_size = min((event.width*0.05), 64)     # 64(original font size) / 1280(original app width) = 0.05 (ratio between font size and app width)
            self.title.configure(font=("Jaini Purva", new_title_size))
                
def main():
    root=ctk.CTk() #the CTK() creates one app
    app=MainMenu(root)     #the main menu is being created as an object
    root.mainloop()     #running the entire app
    
if __name__== "__main__":
    main()