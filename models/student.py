"""
Student Class Module.
This module defines the Student class, which represents a student in the university system.
"""
import random 

class Student:
    def __init__(self, student_id, name, email, password):
        """
        Initializes a new Student instance.
        
        :param student_id: Unique identifier for the student
        :param name: Full name of the student
        :param email: Email address of the student
        :param password: Password for the student's account
        """
        self.student_id = student_id
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []  

    def get_student_id(self):
        """
        Returns the student's unique identifier.
        
        :return: Student ID
        """
        return self.student_id
    
    def get_subjects(self):
        """
        Returns the list of subjects the student is enrolled in.
        
        """
        return self.subjects

class Subject:
    def __init__(self):
        self.enrol_sub = random_subject = random.randint(1, 999)
        self.marks = random.randint(25, 100) # mark as generated >=25 and <=100
        self.grade = self.defgrade()
        

    def defgrade(self):
            
        if self.marks >= 85:
            defgrade = 'HD'
        elif self.marks >= 75:
            defgrade = 'D'
        elif self.marks >= 65:
            defgrade = 'C'
        elif self.marks >= 50:
            defgrade = 'P'
        else:
            defgrade = 'Z'
        
        return defgrade
         
##testing
test = Subject()
print(test.enrol_sub, test.marks, test.grade)