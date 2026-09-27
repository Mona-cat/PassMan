
#Syntax

x = int(1)
y = float(2.542010)
z = 2

print(x)
print(y)
print(z)
print(x+y)
print (x+z)
'spam eggs'

character = str("hallo")
print(character)

x = [1,2,3,4,5,6]
print(x[:3])

y = []

for i in range(10) :
    y.append(i+1)

print(y)

i = 1

while i < 3:     
    u = []          # u ist nicht out of range heißt Objekte in Schleifen werden Global gespeichert und nicht Lokal
    u.append(i)
    i = i+1

print(u)

