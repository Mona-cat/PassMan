#OOP
#private Methoden/Attribute beginnen mit 2 Unterstrichen __ , nicht von außen Aufrufbar zudem wird intern von Python der Klassenname vor dem variablennamen gesetzt 
# Heißt self.__name heißt nach compilen _Students__name. Verhindert das ausversehen die Variable geändert wird z-B. in Unterklassen
# Ein _ bedeutet das es Privat ist und soll nur intern genutzt werden. Trotzdem können die Variablen von außen zugegriffen werden

class Students:
    #__init__ dient als Initializierung des Objekts, Default Values "name = unk..."
    def __init__(self, name = "unknown", fname = "unknown", id = 000000):
        self.__name = name
        self.__first_name = fname
        self.__id_number = id
    
    def getName(self):
        return self.__name
    
    def getfirstname(self):
        return self.__first_name
    
    def getId(self):
        return self.__id_number
    
    def __eq__ (self, other): #Vergeleichoperator Definition
        return self.__id_number == other.__id_number


    def __repr__(self):
        return "Student(\"" + self.__name + "\", \"" + self.__first_name +"\" , " + str(self.__id_number) + ")"
    
    def __str__(self):
        return "Name:\" " + self.__first_name + " \",\" " + self.__name + "\" , " + str(self.__id_number) + " "


# A = Students("Mustermann", "Max", 111111)
# B = Students("Normen", "Izzy", 111111)

# liste = [A,B, Students("A", "b", 111211)]
# print(liste)
# print(liste[2])


# a_repr = repr(A)
# a_str = str(A)
# print(A == B)
# print(a_repr)
# print(a_str)
# print(A.getfirstname())
