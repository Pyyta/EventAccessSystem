#Repository: Handles the database

#calls to libraries
import sqlite3 as sq
import os

class Repository:
    def __enter__(self):
        db_path = os.path.join(os.path.dirname(__file__), "Database.db")
        self.__conn = sq.connect(db_path)
        cursor=self.__conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;") 
        return self

#-------------------------------table creation & seeding-----------------------------
    def create_tables(self):
        cursor=self.__conn.cursor()
        #admin credentials (password hashed)
        cursor.execute("""CREATE TABLE IF NOT EXISTS admin(
                            id INTEGER NOT NULL PRIMARY KEY,
                            email TEXT NOT NULL,
                            password TEXT NOT NULL,
                            temp_recovery_password TEXT,
                            attemps INTEGER NOT NULL)""")
        #Users table
        cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
                       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                       document TEXT UNIQUE NOT NULL,
                       name TEXT NOT NULL,
                       email TEXT NOT NULL,
                       age INTEGER NOT NULL,
                       validated INTEGER NOT NULL DEFAULT 0,
                       date TEXT NOT NULL,
                       token TEXT UNIQUE NOT NULL,
                       phase_id INTEGER NOT NULL,
                       FOREIGN KEY (phase_id) REFERENCES Phases(id))""")
        #Phases table
        cursor.execute("""CREATE TABLE IF NOT EXISTS Phases(
                       id INTEGER NOT NULL PRIMARY KEY,
                       phase TEXT NOT NULL,
                       price INTEGER NOT NULL
                       )""")

        #Intermediate table between Users and Accesories (1:N) -> (N:1)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Users_Assets(
                       id_user INTEGER NOT NULL,
                       id_asset INTEGER NOT NULL,
                       num_locker TEXT,
                       PRIMARY KEY (id_user, id_asset),
                       FOREIGN KEY (id_user) REFERENCES Users(id)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                       FOREIGN KEY (id_asset) REFERENCES Assets(id)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE
                       )""")
        #Assets table
        cursor.execute("""CREATE TABLE IF NOT EXISTS Assets(
                       id INTEGER NOT NULL PRIMARY KEY,
                       accesory TEXT NOT NULL,
                       price INT NOT NULL
                       )""")
        self.__conn.commit()
        return True

    def seeding_assets(self):
        cursor=self.__conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Assets")
        is_empty=cursor.fetchone()[0]
        
        if is_empty == 0:
            cursor.execute("""INSERT INTO Assets(id, accesory, price)
                           VALUES 
                                (1, "Locker", 8000),
                                (2, "Bandana", 4000)
                                """)
            self.__conn.commit()
            return True
        else:
            return False
           
    def seeding_phases_table(self):
        cursor=self.__conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Phases")
        is_empty=cursor.fetchone()[0]
        
        if is_empty == 0:
            cursor.execute("""INSERT INTO Phases(id, phase, price)
                           VALUES 
                                (1, "Fase-1", 18000),
                                (2, "Fase-2", 22000),
                                (3, "Taquilla", 30000),
                                (4, "Invitacion especial", 0)
                                """)
            self.__conn.commit()
            return True
        else: 
            return False

#----------------------------------------admin---------------------------------------    
    def update_admin(self, admin_credentials):
        cursor=self.__conn.cursor()
        cursor.execute("UPDATE admin SET email = (?), password= (?) WHERE id = 1", (admin_credentials["email"], admin_credentials["password"]))
        self.__conn.commit()
        return cursor.rowcount == 1

    def set_admin(self, admin_credentials):
        cursor=self.__conn.cursor()
        cursor.execute("INSERT INTO admin(email, password, attemps) VALUES (?, ?, ?)", (admin_credentials["email"], admin_credentials["password"], 0))
        self.__conn.commit()
        return cursor.rowcount == 1
            
    def get_hashed_admin_password(self):
        cursor=self.__conn.cursor()       
        cursor.execute("SELECT password FROM admin WHERE id = 1")
        password_hashed=cursor.fetchone()
        return password_hashed[0]
    
    def save_admin_temp_pin(self, temp_pin):
        cursor=self.__conn.cursor()
        cursor.execute("UPDATE admin SET temp_recovery_password = (?) WHERE id = 1 ", (temp_pin, ))    
        self.__conn.commit()
        return cursor.rowcount == 1
    
    def clear_admin_temp_pin(self):
        cursor=self.__conn.cursor()
        cursor.execute("UPDATE admin SET temp_recovery_password = (?) WHERE id = 1 ", (None, ))    
        self.__conn.commit()
        
    def update_admin_password(self, new_password):
        cursor=self.__conn.cursor()
        cursor.execute("UPDATE admin SET password = (?) WHERE admin = 1", (new_password, ))
        self.__conn.commit()
        return cursor.rowcount == 1
        
    def get_password_recovery_attemps(self):
        cursor=self.__conn.cursor()
        cursor.execute("SELECT attemps FROM admin WHERE id = 1")
        curr_attemps= int(cursor.fetchone()[0])
        return curr_attemps

    def add_password_recovery_attemp(self):
        cursor=self.__conn.cursor()
        curr_attemps= self.get_password_recovery_attemps()
        cursor.execute("UPDATE admin SET attemps = (?) WHERE admin = 1", (curr_attemps))
        return cursor.rowcount == 1

    def get_admin_email(self):
        cursor=self.__conn.cursor()
        cursor.execute("SELECT email FROM admin WHERE id = 1")
        return cursor.fetchone()

#------------------------------- general options--------------------------------   
    def reset_all_users(self):
        cursor=self.__conn.cursor()
        cursor.execute("UPDATE Users SET validated=0")
        self.__conn.commit()
        return cursor.rowcount ==1
    
    def delete_all_users(self):
        cursor=self.__conn.cursor()

        #deleting the child table at first
        cursor.execute("DELETE FROM Users")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'Users'")
        
        self.__conn.commit()

        #verifies if there are users remaining
        cursor.execute("SELECT COUNT(*) FROM Users")
        users_existing=cursor.fetchone()[0]

        #True if it deleted all users; False if there is still one remaining
        return users_existing == 0

    def show_all_users(self):
        cursor=self.__conn.cursor()
        cursor.execute("SELECT * FROM Users")
        return cursor.fetchall()

#------------------------------- user options--------------------------------  
    def delete_user(self, document):
        cursor = self.__conn.cursor()
        
        cursor.execute("DELETE FROM Users WHERE document = ?", (document,))
        
        self.__conn.commit()
        return cursor.rowcount == 1

    def reset_user(self, document):
        cursor=self.__conn.cursor()
        cursor.execute("UPDATE Users SET validated = 0 WHERE document = (?)", (document, ))
        self.__conn.commit()
        return cursor.rowcount == 1

#---------------------------------user transactions----------------------------------
    def insert_user(self, data):
        cursor=self.__conn.cursor()
        try:
            cursor.execute("""INSERT INTO Users(document, name, email, age, validated, date, token, phase_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                            (data["document"], 
                            data["name"], 
                            data["email"], 
                            data["age"], 
                            data["validated"], 
                            data["date"], 
                            data["token"],
                            data["phase_id"]))
            #update changes to the database
            self.__conn.commit()
            return True
        except sq.IntegrityError:
            #if it doesnt find it: return the operation
            self.__conn.rollback()
            return False
        
    def search_user(self, document):
        cursor=self.__conn.cursor()
        cursor.execute("SELECT id, document, name, age, validated, date, token, phase_id FROM Users WHERE document=(?)", (document, ))
        return cursor.fetchone()

    def validate_user(self, scanned_token):
        cursor=self.__conn.cursor()

        cursor.execute("SELECT validated, name FROM Users WHERE token=(?)", (scanned_token, ))
        state_and_name=cursor.fetchone()

        #not found
        if state_and_name is None:
            return None
        
        #if it hasnt been validated (state -> 0) 
        elif state_and_name[0] == 0:    #[0]= state ; [1]= name
            
            cursor.execute("UPDATE Users SET validated = 1 WHERE token=(?)", (scanned_token, ))
            self.__conn.commit()
            return state_and_name[1]
            
        #if it was found but it was already validated (state -> 1)
        return False

#---------------------------------buying transactions----------------------------------
    def buy_accesory(self, data_accesories):
        cursor=self.__conn.cursor()
        user_document=data_accesories["document"]
        user_full_data= self.search_user(user_document)
        
        if user_full_data:
            cursor.execute("""INSERT INTO Users_Assets (id_user, id_asset, num_locker)
                                VALUES (?, ?, ?)""", (user_full_data[0], data_accesories["id_asset"], data_accesories["num_locker"]))
            self.__conn.commit()
            return True
        else:
            return False

    def get_lockers(self):
        cursor=self.__conn.cursor()
        cursor.execute("""SELECT Users.document, name, num_locker
                       FROM Users
                       JOIN Users_Assets
                       ON Users.id = Users_Assets.id_user
                       WHERE num_locker <> '' """)
        lockers_info= cursor.fetchall()
        return lockers_info
                                                                        
    def get_gains(self):

        cursor=self.__conn.cursor()          

        #total $ sold at the first two phases                    
        cursor.execute("""SELECT SUM(price)
                       FROM Users
                       JOIN Phases
                        ON Users.phase_id = Phases.id 
                        WHERE phase_id <> 3 """)
     
        earlier_phases=cursor.fetchone()[0] or 0

        #total $ sold at the checkout
        cursor.execute("""SELECT SUM(price)
                       FROM Users
                       JOIN Phases
                        ON Users.phase_id = Phases.id 
                        WHERE phase_id = 3""")      
        sold_at_checkout=cursor.fetchone()[0] or 0

        #total $ sold in accesories
        cursor.execute("""SELECT SUM(price)
                        FROM Assets as Ast
                        JOIN Users_Assets as Ua
                        ON Ast.id = Ua.id_asset
                        """)
        total_accesories=cursor.fetchone()[0] or 0
        total={
            "earlier phases": earlier_phases,
            "sold at checkout":sold_at_checkout,
            "total accesories": total_accesories,
            "total_gains": earlier_phases+sold_at_checkout+total_accesories
        }
        return total
         
    def aux(self):
        cursor=self.__conn.cursor()
        cursor.execute("SELECT * FROM admin")
        return cursor.fetchone()

#---------------------------------other----------------------------------   
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__conn:
            if exc_type:
                self.__conn.rollback()    
            self.__conn.close()



