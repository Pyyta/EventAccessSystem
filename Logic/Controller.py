#controller: handles the data who´s sent to the repository

#calls to libraries
import re
import bcrypt
import csv
import secrets

from enum import Enum
from datetime import datetime
from typing import Dict, Optional, Any, Tuple

#connecting with other filesO
from DatabaseFunctions import Repository
from Services import PDFCreator
from Services import EmailService

class Controller:
    def __init__(self):
        self._repository=Repository.Repository()
        self._pdfcreator=PDFCreator.PdfCreator()
        self._emailservice=EmailService.EmailService()

#--------------------------data validater-----------------------------
#---------------------(for the string inputs)-------------------------

    #checks only numbers (no commas, no symbols)
    def validate_document(self, document: str) -> bool:
        document=document.strip()
        
        #checks only numbers with a len between 7 and 10
        return re.search(r"\D", document) is None and re.match(r"^\d{7,10}$", document) is not None
         
    #checks no numbers or symbols in that
    def validate_name(self, name: str) -> bool:
        name= name.strip().lower()
        return re.match(r"^[a-záéíóúÁÉÍÓÚñ\s]+$", name) is not None
    
    #checks pattern -> letters/numbers + @ + letters + . + letters
    def validate_email(self, email: str) -> bool:
        email= email.lower().strip()
        return re.match(r"^[A-Za-z0-9._%+-ñ]+@[A-Za-z0-9.-ñ]+\.[A-Za-z]{2,}$", email) is not None

    #calls all functions    
    def validate_all_data(self, user: Dict[str, Any]) -> Dict[str, Any]:
        errors={}
        if not self.validate_document(user["document"]):
            errors["document"]=ValidationResults.invalid
        if not self.validate_name(user["name"]):
            errors["name"]=ValidationResults.invalid
        if not self.validate_email(user["email"]):
            errors["email"]=ValidationResults.invalid
        return errors

    def validate_admin_password(self, admin_password: str) -> Tuple [bool, str]:
        return (False, "The minimum lenght is 8") if admin_password<8 else (True, "Password valid")
#-------------------------------  set  ------------------------------
    #purchase date
    def set_date(self, user: Dict[str, Any]):
        date=datetime.now().strftime("%d/%m/%Y")
        user["date"] = date        
    #to barcode
    def set_token(self, user: Dict[str, Any]):
        user["token"]=secrets.token_urlsafe(16)

    def set_admin(self, admin_credentials: Dict[str, Any]) -> bool:
        admin_credentials["password"] = bcrypt.hashpw(password=admin_credentials["password"].encode(), salt= bcrypt.gensalt())
        with self._repository as connection:
            state= connection.set_admin(admin_credentials)
        return state
   
#-------------------------------   get  ------------------------------ 
    def get_user_by_document(self, document: str):
        with self._repository as connection:
            user = connection.search_user(document)
        return user

    def get_total_gains(self) -> Dict[str]:
        with self._repository as connection:
            gains=connection.get_gains()
        return gains
    
    def get_admin_email(self) -> str:
        with self._repository as connection:
            admin_email=connection.get_admin_email()
        if admin_email: return admin_email[0]
        else: return None


#-------------------------- user transactions -----------------------------
    def register_user(self, user: Dict[str]) -> Optional[Dict[str, Any]]:
        data_errors = self.validate_all_data(user)

        if not data_errors:
            self.set_date(user)
            self.set_token(user)
            with self._repository as connection:
                #the insert_user function returns false if it found an used document
                if not connection.insert_user(user):
                    data_errors["document used"] = ValidationResults.used  
        return data_errors

    def reset_one_user(self, document: str) -> bool:
        with self._repository as connection:
            reset_state=connection.reset_user(document)
        return reset_state
    
    def delete_one_user(self, document: str) -> bool:
        with self._repository as connection:
            delete_state=connection.delete_user(document)
        return delete_state
#-----------------------ticket options-------------------------------------        
    def generate_temp_ticket(self, user: Dict[str])-> Tuple[bool, str]:
        state_and_path = self._pdfcreator.save_temp_ticket(user)
        return state_and_path

    def send_ticket_to_email(self, user: Dict[str])-> Tuple[bool, str]:
        if not user["token"]:
            return (False, "token not created")

        state_and_path= self.generate_temp_ticket(user)
        if state_and_path[0]:
            state=self._emailservice.ticket_email_setter(user=user, ticket_buffer=state_and_path[1])
            return state
        else: return state_and_path
        
    def generate_permanent_ticket(self, user: Dict[str])-> Tuple[bool, str]:
        state_and_path = self._pdfcreator.save_ticket_permanently(user)
        return state_and_path

    def check_scanned_token(self, token: str) -> bool:
        with self._repository as connection:
            is_valid=connection.validate_user(token)
        return is_valid


#---------------------------asset options-------------------------------------------
    def buy_accessory(self, asset_data: Dict[str, Any])-> bool:
        with self._repository as connection:
            transaction_succesfull= connection.buy_accesory(asset_data)
        return transaction_succesfull
   
    def get_lockers(self) -> Dict[str]:
        with self._repository as connection:
            lockers=connection.get_lockers()
        return lockers

#----------------------------admin general options-----------------------------------

    def get_attemps(self) -> int:
        with self._repository as connection:
            attemps= connection.get_password_recovery_attemps()
        return attemps

    def has_attemps(self) -> Tuple[bool, str]:
        attemps=int(self.get_attemps())
        return (True, f"{5-attemps} remaining ") if attemps <= 5 else (False, "no attemps remaining")

    def add_attemp(self) -> bool:
        with self._repository as connection:
            state= connection.add_password_recovery_attemp()
        return state

    def admin_password_recovery(self) -> Tuple[bool, str]:
        admin_temp_pin= secrets.randbelow(90000)+10000
        email_sending_status=self.send_recovery_email(admin_temp_pin)
        if email_sending_status[0]:
            hashed_pin= bcrypt.hashpw(password= admin_temp_pin, salt= bcrypt.gensalt())
            self.save_temp_admin_pin(hashed_pin)
            return (True, "email sent")
        else: return email_sending_status

    def get_recovery_pin(self) -> bool:
        with self._repository as connection:
            temp_pin=connection.get_admin_temp_pin()
        return temp_pin
    
    def update_admin_password(self, new_password: str):
        with self._repository as connection:
            update_state=connection.update_admin_password(new_password)
            temp_password_state=connection.clear_admin_temp_pin()
        return update_state and temp_password_state
    
    def check_recovery_pin(self, temp_pin_attemp: str) -> Tuple[bool, str]:
        recovery_pin= self.get_recovery_pin()
        if recovery_pin:
            is_valid= bcrypt.checkpw(temp_pin_attemp.encode(), recovery_pin)
            return (True, "Correct") if is_valid else (True, "Incorrect")
        else: return (None, "ERROR, temporal pin not found")

    def send_recovery_email(self, admin_temp_pin: str) -> bool:
        admin_email=self.get_admin_email()
        state=self._emailservice.admin_password_reset(admin_email, admin_temp_pin)
        return state
    
    def save_temp_admin_pin(self, temp_pin: str) -> bool:
        with self._repository as connection:
            status= connection.save_admin_temp_pin(temp_pin)
        return status

#------------------------------- general transactions ------------------------------

    def export_all_users(self) -> bool:
        #save all users in one variable
        with self._repository as connection:
            all_users = connection.show_all_users()
        
        if not all_users:
            return None
        
        try:
            file_route="data.csv"
            with open(file_route, "w", newline="", encoding="utf-8") as csv_connection:
                csv_cursor=csv.writer(csv_connection, delimiter=";")
                #titles
                csv_cursor.writerow(["id", "cedula", "nombre", "correo", "edad", "validado", "fecha", "token", "fase"])
                #data insertion
                for user in all_users:
                    csv_cursor.writerow(user)
            return True
        except (PermissionError, OSError, UnicodeDecodeError):
            return False
       
    def check_admin_credentials(self, admin_pin: str, username: str)-> bool:
        with self._repository as connection:
            password_hashed=connection.get_hashed_admin_password(username)
        if password_hashed:
            is_password_correct=bcrypt.checkpw(admin_pin.encode(), password_hashed[0])
            return (True, "Success") if is_password_correct else (False, "Wrong Password")
        else: return (None, "User not found")

    def delete_all_users(self)-> bool:
        with self._repository as connection:
            delete_state= connection.delete_all_users()
        return delete_state
    
    def reset_all_users(self) -> bool:
        with self._repository as connection:
            reset_state= connection.reset_all_users()
        return reset_state
    




#------------------------------ DATA STATES-------------------------------    
class ValidationResults(Enum):
    invalid=1
    used=2


def testing_controller():
    user_1 = {
    "document": "28654123",
    "name": "Ricardo Jose Olarte Rincon",
    "email": "impresionespitaa@gmail.com",
    "age": 21,
    "validated": 0,
    "date": "",
    "token": "",
    "phase_id": 1
}

    controlador=Controller()
    print(controlador.admin_password_recovery())
    
    

testing_controller()