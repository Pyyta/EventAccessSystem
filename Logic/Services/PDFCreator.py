#PDF Creator: create Ticket and barcode

#calls to libraries
from fpdf import FPDF
from pathlib import Path
import os
import io
import barcode
from barcode.writer import ImageWriter

#========================exceptions=================================
class PdfNotFoundError(Exception):
    pass

class ImageNotFound(Exception):
    pass

class PdfDirectoryNotFoundError(PdfNotFoundError):
    pass

class FontDecodingError(Exception):
    pass


#=================================pdf class=================================
class PdfCreator:
    def __init__(self):
        self.pdf= FPDF("L", "mm", "a4")
            
    def pdf_setter(self):
        self.pdf.add_page()
        #setting the font location
        self.dir_location= Path(__file__).resolve().parents[2]
        
        font_location=os.path.join(
                                    self.dir_location,
                                   "Assets",
                                   "fonts", 
                                   "JainiPurva-Regular.ttf"
                                   )
        
        #font settings
        try:
            self.pdf.add_font(fname=font_location, style="", family="jaini purva")
            self.pdf.set_font("jaini purva", "", 30)
        except (FontDecodingError, FileNotFoundError):
            self.pdf.set_font("helvetica", "", 30)
        self.pdf.set_text_color(255, 255, 255)

    def build_ticket_layout(self, user_data):
        self.pdf_setter()
        try:
            image_path=os.path.join(self.dir_location,
                                    "Assets",
                                    "images",
                                    "ticket_base.jpg")
            self.pdf.image(name=image_path, x=0, y=0, w=297, h=210)
        except ImageNotFound:
            return (False, "404 MAIN IMAGE NOT FOUND")
        #---name---
        self.pdf.set_xy(25, 75)
        self.pdf.cell(text=user_data["name"], w=0)
        #---document---
        self.pdf.set_xy(25, 100)
        self.pdf.cell(text=user_data["document"], w=0)
        #---date---
        self.pdf.set_xy(25, 125)
        self.pdf.cell(text=user_data["date"],w=0)
        #---email---
        self.pdf.set_xy(25, 150)
        self.pdf.cell(text=user_data["email"],w=0)
        #---barcode---
        state_and_buffer=self.build_barcode(user_data["token"])
        if state_and_buffer[0]:
            self.pdf.image(name=state_and_buffer[1], x=194, y=182, w=100)
            return (True, "pdf created")
        else:
            return state_and_buffer
    
    def save_ticket_permanently(self, user_data):
        state_and_exception= self.build_ticket_layout(user_data)
        if state_and_exception[0]:
            permanent_ticket_path=os.path.join(self.dir_location,
                                        "Cache",
                                        "Saved tickets",
                                        f"{user_data["document"]}_ticket.pdf")
            try:
                self.pdf.output(permanent_ticket_path)
                return (True, permanent_ticket_path)
            except PdfDirectoryNotFoundError:
                dir_path=os.path.join(self.dir_location,
                                        "Cache",
                                        "Saved tickets")
                os.makedirs(name=dir_path, exist_ok=True)
                self.pdf.output(permanent_ticket_path)
                return (True, permanent_ticket_path)
        else:
            return state_and_exception


    def save_temp_ticket(self, user_data):
        self.build_ticket_layout(user_data) 
        pdf_buffer=io.BytesIO() 
        self.pdf.output(pdf_buffer) 
        pdf_buffer.seek(0) 
        return (True, pdf_buffer)
        
    def build_barcode(self, barcode_hash):
        #create the .png in buffer for faster access
        buffer=io.BytesIO()
        try:
            barcode_class=barcode.get(name="code128", 
                                    code=barcode_hash, 
                                    writer=ImageWriter()
                                    )
        except Exception:
            return (False, "Token its empty")
        barcode_class.write(buffer)
        buffer.seek(0)
        return (True, buffer)



