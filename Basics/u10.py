class Person:
    def __init__(self, name : str, age : int): # Constructor
        self.name = name
        self.age = age
    
    def printInfo(self):
        return f"Name: {self.name} \nAge: {self.age}\n" 

persons = []

persons.append(Person("Daniel", 18))
persons.append(Person("Adam", 22))
persons.append(Person("Isak", 21))

for v in persons:
    print(v.printInfo())