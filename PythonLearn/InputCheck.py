#Input File Check
from Student import Students
import re

y = True
while y == True:
    
    
    print("Gebe Nachname, Name und Matrikelnummer ein!")
    C = Students(str(input("Nachname: \n")), input("Name \n"), input("Matrikelnummer \n"))
    name = C.getName()
    fname = C.getfirstname()
    id = C.getId()
    print(name)

    Check_Name = bool(re.search(r"[0-9]", name))
    Check_fname = bool(re.search(r"[0-9]", fname))
    Check_id = bool(re.search(r"[a-zA-Z]", id)) 
    print(Check_Name, Check_fname, Check_id)

    try:      
         if not (Check_fname or Check_Name or Check_id):
            y = False
    except:
          print("Falsche Eingabe, versuche es erneut!")


print(str(C))