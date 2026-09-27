from pasman import Passwordgen
import PasmanDB as db
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, select, insert
import os
from Security import Verschlüsselung, Entschlüsselung, masterpw_set
from argon2 import PasswordHasher
import pyperclip
from getpass import getpass

ph = PasswordHasher()

Directory = os.getcwd()
DBfile_path = f"{Directory}/database.db"
login = bool(False)
master_password = getpass("Enter your Password: ", echo_char="*")

#Log into the Database
if os.path.exists(DBfile_path):

        engine =  create_engine("sqlite:///database.db")
        Session_maker = sessionmaker(bind=engine)
        session = Session_maker()
        
        phash_db = select(db.vault_metadata.phash).where(db.vault_metadata.id == 1)
        hash_select = session.execute(phash_db)
        result_hash = hash_select.scalar_one_or_none()

        try: 
                ph.verify(result_hash, master_password)
                login = True

        except:
                print("Wrong Password!")


else :
        print("Database does not exist yet")
        print("Create Database ...")

        salt = os.urandom(32) # 32 Byte Salt for extra extra security
        hashed_pw = ph.hash(master_password)

        engine = create_engine("sqlite:///database.db")
        db.Base.metadata.create_all(engine) #Create Tables

        Session_ = sessionmaker(bind=engine)
        session = Session_()

        insert_user = insert(db.vault_metadata).values(id = 1, salt = salt, phash = hashed_pw)
        session.execute(insert_user)

        test = select(db.vault_metadata)
        testexe = session.execute(test)
        session.commit()

        for user in testexe.scalars():
                print(f"{user.id}, {user.salt}, {user.phash}")



# #Simple Menu for Insert and Select (read and write data)
if True: 

        engine =  create_engine("sqlite:///database.db")
        Session_maker = sessionmaker(bind=engine)
        session = Session_maker()

        salt_db = select(db.vault_metadata.salt).where(db.vault_metadata.id == 1)
        salt_res = session.execute(salt_db).scalar_one_or_none()
        aes = masterpw_set(salt_res, master_password)

        while True:
                print("Options\nInsert Password: 1\nGet Password: 2\nSelect Password: 3\nExit: 0")

                switch = int(input("Which Option do you choose?: "))
                

                match switch:
        
                        case switch if switch == 1:
                                
                                Email_ = str(input("Enter Email: "))
                                Service_ = str(input("Enter Service: "))
                                new_password = Passwordgen()

                                nonce_ = os.urandom(12)

                                secure_pw = Verschlüsselung(new_password, aes, nonce_)

                                insert_query = insert(db.PasswordEntry).values(email = Email_, nonce = nonce_, ciphertext = secure_pw, service = Service_)
                                session.execute(insert_query)
                                session.commit()
                        
                        case switch if switch == 2:

                                select_query = select(db.PasswordEntry)
                                query_exe = session.execute(select_query)
                                
                                for query in query_exe.scalars():
                                        print(f"||\nid:[{query.id}]\nemail:[{query.email}]\nservice:[{query.service}]\npw:{Entschlüsselung(query.nonce, query.ciphertext, aes)}]\n||\n")

                        case switch if switch == 3:

                                get_id = int(input("Which Password do you want? (Enter ID!): "))

                                copy_cipher = session.get(db.PasswordEntry, get_id)

                                copy_pw = Entschlüsselung(copy_cipher.nonce,copy_cipher.ciphertext, aes)
                                
                                pyperclip.copy(copy_pw)
                                print(f"{copy_pw} is now copied!\n")

                        case switch if switch == 0:
                                print("Exit Programm...")
                                break

                        case any: 
                                print("Not a valid option!\n")

pyperclip.copy('')


#FastAPI instead of previous Menu
# from fastapi import Depends, FastAPI, HTTPException, Query#
# from typing import Annotated
 
# engine = create_engine("sqlite:///database.db")
# SessionLocal = sessionmaker(autoflush=False, bind=engine)
# #Funktionen zu erstellung der Datenbank und zugriff auf diese
# def get_Table(database: Session,table_id: int):
#         return database.query(db.PasswordEntry).filter(db.PasswordEntry.id == table_id).first()

# def get_tables(database: Session, skip: int = 0, limit: int = 10):
#         return database.query(db.PasswordEntry).offset(skip).limit(limit).all()

# def create_Table(datasession: Session, email: str, ciphertext: bytes, service: str):
#         database: db.PasswordEntry
#         db_password = db.PasswordEntry(email = database.email, service = database.service, ciphertext = database.ciphertext)
#         datasession.add(db_password)
#         datasession.commit()
#         datasession.refresh(db_password)
#         return db_password

# def get_db():
#         database = SessionLocal()
#         try: 
#                 yield database
#         finally:
#                 database.close()


# app = FastAPI()

# @app.post("/PasswordData/")
#  async def create_table_endpoint(email: str, ciphertext: bytes, service: str, database: Annotated[Session, Depends(get_db)]): 
#                 return create_Table(database, email, ciphertext, service)

# @app.get("Table/{table_id}")
# async def get_table_endpoint(table_id: int, database: Annotated[Session, Depends(get_db)]):
#                 table = get_Table(database, table_id)
#                 if table is None:
#                         raise HTTPException(status_code=404, detail="Table not found")
#                 return table

# @app.get("/Tables/")
# async def read_tables(skip: int = 0, limit: int = 10, database: Session = Depends(get_db)):
#               db_tables = get_tables(database, skip = skip, limit = limit)
#                return db_tables

# @app.put("/Table/{table_id}")
# async def update_table_endpoint(table_id: int, database: Annotated[Session, Depends(get_db)]):
#                table = database.query(db.PasswordEntry).filter(db.PasswordEntry.id == table_id).first()
#               if table is None:
#                        raise HTTPException(status_code=404, detail="Table not found")

#                database.commit()
#               database.refresh()

#               return table

# @app.delete("/Table/{table_id}")
# async def delete_table_endpoint(item_id: int, database: Session = Depends(get_db)):
#               table = database.query(db.PasswordEntry).filter(db.PasswordEntry.id == item_id).first()
#               if table is None:
#                        raise HTTPException(status_code=404, detail="Table not found")
        
#               database.delete(db.PasswordEntry)
#               database.commit()

#               return {"detail": "Table deleted"}
                                