class Person:
    def __init__(self, name : str, age : int): # Constructor
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"Name: {self.name} \nAge: {self.age}\n" 
    
    
class Student(Person):
    def __init__(self, name, age, school, average_grade: str):
        super().__init__(name, age)
        self.school = school
        self.average_grade = average_grade

    def __repr__(self):
        return f"Name: {self.name} \nAge: {self.age}\nSchool: {self.school}\nAverage Grade: {self.average_grade}" 


persons = []

persons.append(Person("Daniel", 18))
persons.append(Person("Adam", 22))
persons.append(Person("Isak", 21))
persons.append(Student("Krister", 18, "Nacka Gymnasium", "C"))

for v in persons:
    print(v)