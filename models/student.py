"""
Student Class Module.
This module defines the Student class, which represents a student in the university system.
"""

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
        self.subject = []  

    def get_student_id(self):
        """
        Returns the student's unique identifier.
        
        :return: Student ID
        """
        return self.student_id

class Subject:
    def __init__(self, subjectid, mark, grade):
        """
        subjectid = unique, randomly generated 3-digit, from 001 to 999
        mark = random generated >=25 and <=100
        grade = depends on mark = ?????
        """
        self.subjectid = subjectid
        self.mark = mark
        self.grade = grade
        
        
    random_subject = random.randint(1, 999) ## assigned when enrolled --- enrol function? 
    subjectid = random_subject
    
    random_mark = random.randint(25, 100) # mark as generated >=25 and <=100
    mark = random_mark
    
    if mark >= 85:
        grade = 'HD'
    elif mark >= 75:
        grade = 'D'
    elif mark >= 65:
        grade = 'C'
    elif mark >= 50:
        grade = 'P'
    else:
        grade = 'Z'




##test
print(f"[  Subject::{Subject.subjectid} -- Mark = {Subject.mark} -- grade =   {Subject.grade} ]")
print(Student.student_id) 