import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class SFEDIT(ctk.CTk):
    def __init__(self): 
        super().__init__()
        self.title("Sprocket FIle Editor")
        
        # Geometry fit to screen
        height, width = self.winfo_screenheight(), self.winfo_screenwidth()
        self.geometry("%dx%d+0+0" % (width, height))

        # Buttons section
        self.button = ctk.CTkButton(self, command=self.button_click, text="TEST")
        self.button.grid(row=0, column=0)

    def button_click(self):
        """
        Return a text that confirms the button was clicked.
        """
        print("button clicked")
        

sfe = SFEDIT()
sfe.mainloop()
