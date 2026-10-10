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

    def get_student_id(self):
        """
        Returns the student's unique identifier.
        
        :return: Student ID
        """
        return self.student_id

    # TODO: Implement additional methods for the Student class as needed, such as getters and setters for name, email, and password.