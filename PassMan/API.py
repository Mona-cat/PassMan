import requests

BASE_URL = "http://127.0.0.1:8000"

class APIClient:
    
    def login(self, password: str):

        response = requests.post(
                    f"{BASE_URL}/login/",
                    params={ "password": password})

        return response
    

    def get_passwords(self):
         
         response = requests.get(f"{ BASE_URL}/passwords/")
         return response.json()

    def get_password(self, id: int):

        response = requests.get(f"{BASE_URL}/passwords/{id}")
        return response.json()

    def copy_password(self, id: int):
         
         response = requests.get(f"{BASE_URL}/passwords/{id}/copy")
         return response.json()
    
    def add_password(self, service, email, password):
            
            response = requests.post(f"{BASE_URL}/passwords/add",
                                     params={"service": service,
                                           "email": email,
                                           "password": password})
            
            return response

    def change_password(self, service, email, password, id: int):
         response = requests.put(f"{BASE_URL}/passwords/{id}/change",
                                   params={"service": service,
                                           "email": email,
                                           "password": password})
         return response
    
    def delete_password(self, id: int):
         
         response = requests.delete(f"{BASE_URL}/passwords/{id}/delete")

    def Server_Shutdown(self):
         response = requests.post(f"{BASE_URL}/shutdown")
         return response

    