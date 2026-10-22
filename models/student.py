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
        return self.subject
    
    def enrol_subj(self):
        if len(self.subjects) >= 4:
            print("You have already enrolled in 4 subjects.")
        while len(self.subjects) < 4:
            k = len(self.subjects)
            random_subject = random.randint(1, 999)
            self.subjects.append(random_subject)
            
            print(f"Subject {k+1} enrolled: {random_subject}")
            
    def mark(self):
        random_mark = random.randint(25, 100) # mark as generated >=25 and <=100
        self.mark = random_mark
        """ 
        how to associate the mark with the subject????
        """
        
    def grade(self):
            
        if self.mark >= 85:
            grade = 'HD'
        elif self.mark >= 75:
            grade = 'D'
        elif self.mark >= 65:
            grade = 'C'
        elif self.mark >= 50:
            grade = 'P'
        else:
            grade = 'Z'
         
##testing
student1 = Student(1,2,3,4)
student1.enrol_subj()



