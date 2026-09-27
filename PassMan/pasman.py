#Passwort Manager 
#Random pass generator
import string 
import secrets

s1 = list(string.ascii_letters + string.digits + string.punctuation)
s2 = list(string.punctuation)
s3 = list(string.ascii_lowercase)
s4 = list(string.ascii_uppercase)
s5 = list(string.digits)

def Passwordgen(): 

        while True:

                try: 
                        length = int(input("Enter password length: "))
                        characters_number = int(length)

                        if characters_number < 12:

                                print("Make sure to use more Character to have a secure password!")

                                length = int(input("Enter Again the length of your password: "))

                        else:
                                break
                        
                except:
                        
                        print("Please, Enter numbers only.")

        print("1 = Nach Vorgaben 8-4")
        print("2 = Zufällig mit mind. 20% Sonderzeichen")
        Choice = int(input("Enter Case: "))
        pw = Password(Choice, length)

        return pw

def Password(Choice, length):
    match Choice:
        case 1:
            Vg = round(length * 1/8)
            Rest = length - (Vg*4)

            result = []

            for x in range(Vg):

                result.append(secrets.choice(s2))
                result.append(secrets.choice(s3))
                result.append(secrets.choice(s4))
                result.append(secrets.choice(s5))

            for x in range(Rest):
                result.append(secrets.choice(s1))

            password = "".join(result)

            return password
        
        case 2:

            ALetters = round(length * 80/100)
            PLetters = length - ALetters

            result = []

            for x in range(ALetters):
                result.append(secrets.choice(s1))

            for x in range(PLetters):
                result.append(secrets.choice(s2))

            password = "".join(result)

            return password
        
        case _:
            return "Nicht gegebene Eingabe"