"""Database Model

This file contains methods to interact with the student database (students.data). This is where we read and write student records to the database.
It provides functionality to add, retrieve, update, and delete student records. 
The database is implemented as a simple text file. The first line contains the number of records in the database, and each subsequent line contains a student record in the format: "id;name;email;password".
"""
from models.student import Student

class Database:
    filename = "students.data"

    def read_students(self, filename):
        """
        Reads student records from students.data
        """
        # TODO: Read the students.data file and return a list of Student objects.
        