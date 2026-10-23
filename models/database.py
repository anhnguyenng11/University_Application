"""Database Model

This file contains methods to interact with the student database (students.data). This is where we read and write student records to the database.
It provides functionality to add, retrieve, update, and delete student records. 
The database is implemented as a simple text file. The first line contains the number of records in the database, and each subsequent line contains a student record in the format: "id;name;email;password".

Exported Functions:
- read_students_from_database(database_name): Reads student records from the specified database file and returns a tuple containing the number of records and a list of Student objects.
"""
from models.student import Student

class Database:

    def read_students_from_database(self, filename) -> tuple[int, list[Student]]:
        """
        Version 1.0.
        Reads student records from students.data
        """
        # TODO: Read the students.data file and return a list of Student objects.
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                num_records = int(lines[0].strip())
                students = []
                for line in lines[1:(num_records + 1)]:
                    student_data = line.strip().split(';')
                    if len(student_data) == 4:
                        student_id, name, email, password = student_data
                        students.append(Student(student_id, name, email, password))
                return num_records, students
        except FileNotFoundError:
            print("Database file not found.")
            return 0, []
        except Exception as e:
            print(f"An error occurred while reading the database: {e}")
            return 0, []