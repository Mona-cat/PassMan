from fastapi import FastAPI, Depends, HTTPException

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PasmanDB import PasswordEntry, vault_metadata, Base
from Security import Verschlüsselung, Entschlüsselung, masterpw_set
from pasman import Passwordgen

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select, insert, delete, create_engine, and_, inspect
import os

Directory = os.path.join(
    os.getenv("APPDATA"),
    "PassMan"
)

os.makedirs(Directory, exist_ok=True)

DBfile_path = os.path.join(Directory, "database.db")

engine = create_engine(
    f"sqlite:///{DBfile_path}",
    connect_args={"check_same_thread": False}
)

sessionlocal = sessionmaker(bind=engine)
database = sessionlocal()

#Globale Variablen um diese damit diese innerhalb jeder Funktionen genutzt werden kann
from pydantic import BaseModel

class AccountResponse(BaseModel):
       id: int
       service: str
       email: str
       password: str

def get_db():
    try:
        yield database
    finally:
        database.close()

db: Session = Depends(get_db)

def set_aes_key(password: str):
        salt = get_salt()
        return masterpw_set(salt, password)
       
#Check if Table exist
def check_table_exist():
        inspector = inspect(engine)
        if inspector.has_table("Vault"):
                return True
        else: 
                Base.metadata.create_all(engine)
                return False   

def create_masterpassword(password: str):
       ph = PasswordHasher()
       salt = os.urandom(32) #32 Byte Salt

       hash_pw = ph.hash(password)
       query = insert(vault_metadata).values(id = 1, phash = hash_pw, salt = salt)
       database.execute(query)
       database.commit()
       return True

def get_login_password():
        query = select(vault_metadata.phash).where(vault_metadata.id == 1)
        query_exe = database.execute(query)
        return query_exe.scalar_one_or_none()

def get_salt():
        query = select(vault_metadata.salt).where(vault_metadata.id == 1)
        query_exe = database.execute(query)
        return query_exe.scalar_one_or_none()

def copy_password(id: int, aes):
        query = database.get(PasswordEntry, id)
        ciphertext = query.ciphertext
        nonce = query.nonce

        password = Entschlüsselung(nonce, ciphertext, aes)
        return password

#Functions for navigating inside the Database
def get_passwords(skip: int=0, limit: int=10):
        query = select(PasswordEntry).offset(skip).limit(limit)
        query_exe = database.execute(query)
        return query_exe.scalars().all()

def get_password(id: int):
        query = select(PasswordEntry).where(PasswordEntry.id == id)
        query_exe = database.execute(query)
        return query_exe.scalars().all()

def new_password(new_email: str, new_service: str, new_password: str):
        nonce = os.urandom(12)

        pass_encode = Verschlüsselung(password_en= new_password, aes= app.state.aes_key, nonce= nonce)

        query = insert(PasswordEntry).values(email = new_email, service = new_service, ciphertext = pass_encode, nonce = nonce)
        database.execute(query)
        database.commit()

        get_id = select(PasswordEntry.id).where(and_(PasswordEntry.email == new_email, PasswordEntry.service == new_service))
        get_id_exe = database.execute(get_id)
        return get_id_exe.scalar_one_or_none()

def change_password(new_email: str, new_service: str, new_password: str, id: int):

        query = database.execute(select(PasswordEntry).where(PasswordEntry.id == id)).scalar_one_or_none()
        print("Changing...")
        if not (new_password == Entschlüsselung(query.nonce, query.ciphertext, app.state.aes_key)):
                en_pass = Verschlüsselung(new_password, app.state.aes_key, query.nonce)
                query.ciphertext = en_pass

        query.email = new_email
        query.service = new_service

        database.commit()
        print("Changed!")
        return{"detail": "Entry has changed"}


def delete_password(chosen_id: int):
        print("Deleting...")    
        query = delete(PasswordEntry).where(PasswordEntry.id == chosen_id)
        database.execute(query)
        database.commit()
        return{"detail": "Entry is deleted"}


from argon2 import PasswordHasher

#FastAPI Funktionen (Schnittstelle zwischen Datenbank und GUI)
app = FastAPI()
app.state.aes_key = AESGCM


@app.get("/")
def start():
        return{"status": "Server running"}

@app.post("/login/")
def get_login_pass(password: str):
        checker = check_table_exist()
        print(f"{checker}")

        if checker == False:
                create_masterpassword(password)

        key = set_aes_key(password)
        
        ph = PasswordHasher()
        db_hash = get_login_password()

        try:
                ph.verify(db_hash, password)
                app.state.aes_key = key
        except:
                raise HTTPException(status_code=401, detail="Wrong Password!")
        
        return{"detail", "Authorized"}

@app.get("/passwords/", response_model=list[AccountResponse])
async def get_passwords_app():
       
       try:
                data = get_passwords()
                liste = []

                for i in data:
                       pw = Entschlüsselung(i.nonce, i.ciphertext, app.state.aes_key)

                       liste.append({
                                        "id": i.id,
                                        "service": i.service,
                                        "email": i.email,
                                        "password": pw
                                })
                return liste
       except: 
                raise HTTPException(status_code=404, detail="Data was not found")
       
@app.get("/passwords/{id}", response_model=list[AccountResponse])
async def get_password_app(id: int):

        try:
                data = get_password(id)[0]
                liste = [{
                        "id": data.id,
                        "service": data.service,
                        "email": data.email,
                        "password": Entschlüsselung(data.nonce, data.ciphertext, app.state.aes_key)
                }]
                
                return liste
        except:
               raise HTTPException(status_code=404, detail="Data was not found")

@app.get("/passwords/{id}/copy")
async def copy_password_app(id: int):
        password = copy_password(id, app.state.aes_key)
        return {"password": password}

@app.post("/passwords/add")
async def post_password(email: str, service:str, password: str):
        return new_password(email, service, password)

@app.put("/passwords/{id}/change")
async def change_password_app(email: str, service:str, password: str, id: int):
        return change_password(email, service, password, id)

@app.delete("/passwords/{id}/delete")
async def delete_password_app(id: int):
        print("Delete...")
        table = select(PasswordEntry).where(id == id)
        query = database.execute(table)
        if query is None:
               raise HTTPException(status_code=404, detail="Entry not found!")

        return delete_password(id)


import uvicorn
import signal
import threading

@app.post("/shutdown")
def shutdown():

        def stop():
                os.kill(os.getpid(), signal.SIGTERM)

        threading.Timer(0.2, stop).start()

        return{"message": "Server shutdown"}

if __name__ == "__main__":

        uvicorn.run(
                     app,
                     host="127.0.0.1",
                     port=8000,
                     log_config=None
                        )


