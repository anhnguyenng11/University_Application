
from models.student import Student
from models.subject import Subject
from models.file_handlers.student_data_file import StudentDataFile
from utils.validator import Validator
from utils.id_generator import IDGenerator


class StudentService:
    def __init__(self, student_data_file: StudentDataFile) -> None:
        self.student_data_file = student_data_file

    def register(
        self,
        name: str,
        email: str,
        password: str
    ) -> Student:

        name = name.strip()
        email = email.strip()

        # Step 1: Validate inputs
        if not Validator.is_not_empty(name):
            raise ValueError("Name cannot be empty.")

        if not Validator.is_valid_email(email):
            raise ValueError("Invalid student email.\nEmail suffix: [@university.com]")

        if not Validator.is_valid_password(password):
            raise ValueError("Invalid password." \
            "\nPassword should contain:" \
            "\n- At least 8 characters" \
            "\n- At least 1 symbol (!, @, #, ...)" \
            "\n- 1 uppercase and 1 lowercase" \
            )

        # Step 2: Check duplicate email
        if self.student_data_file.email_exists(email):
            raise ValueError("Email already registered.")

        # Step 3: Collect existing student IDs
        students = self.student_data_file.load_students()

        existing_ids = set()

        for student in students:
            existing_ids.add(student.student_id)

        # Step 4: Generate a unique ID
        student_id = IDGenerator.generate_student_id(existing_ids)

        # Step 5: Create a Student object
        new_student = Student(
            student_id,
            name,
            email,
            password
        )

        # Step 6: Save the new student
        success = self.student_data_file.add_student(new_student)

        if not success:
            raise ValueError("Student registration failed.")

        return new_student

    def login(self, email: str, password: str) -> Student:
        email = email.strip()

        student = self.student_data_file.find_student_by_email(email)

        if student is None:
            raise ValueError("Student email not found.")

        if student.password != password:
            raise ValueError("Wrong password.")

        return student

    
    def enroll_subject(self, student: Student) -> Subject:
        # Step 1: Load the student's latest saved record
        saved_student = self.student_data_file.find_student_by_id(
            student.student_id
        )

        if saved_student is None:
            raise ValueError("Student not found.")

        # Step 2: Check enrollment limit
        if not saved_student.can_enroll():
            raise ValueError("Maximum 4 subjects allowed.")

        # Step 3: Collect existing subject IDs
        existing_ids = set()

        for subject in saved_student.subjects:
            existing_ids.add(subject.subject_id)

        # Step 4: Generate ID and mark
        subject_id = IDGenerator.generate_subject_id(existing_ids)
        mark = IDGenerator.generate_mark()

        # Step 5: Create the Subject object
        new_subject = Subject(subject_id, mark)

        # Step 6: Add it to the student
        success = saved_student.add_subject(new_subject)

        if not success:
            raise ValueError("Subject enrollment failed.")

        # Step 7: Save the updated student
        saved = self.student_data_file.update_student(saved_student)

        if not saved:
            raise ValueError("Could not save enrollment.")

        # Step 8: Update the logged-in Student object
        student.subjects = saved_student.subjects

        return new_subject

    
    def remove_subject(self, student: Student, subject_id: str) -> bool:
        subject_id = subject_id.strip()

        # Load the latest student record
        saved_student = self.student_data_file.find_student_by_id(student.student_id)

        if saved_student is None:
            raise ValueError("Student not found.")

        # Remove the subject from the student
        removed = saved_student.remove_subject(subject_id)

        if not removed:
            raise ValueError("Subject not found.")

        # Save the updated student to the JSON file
        success = self.student_data_file.update_student(saved_student)

        if not success:
            raise ValueError("Failed to save the updated student.")

        # Update the currently logged-in student
        student.subjects = saved_student.subjects

        return True


    def change_password(
        self,
        student: Student,
        current_password: str,
        new_password: str
    ) -> None:

        # Step 1: Load the latest student record
        saved_student = self.student_data_file.find_student_by_id(student.student_id)

        if saved_student is None:
            raise ValueError("Student not found.")

        # Step 2: Verify the current password
        if saved_student.password != current_password:
            raise ValueError("Current password is incorrect.")

        # Step 3: Validate the new password
        if not Validator.is_valid_password(new_password):
            raise ValueError(
                "New password does not meet requirements." \
                "\nPassword should contain:" \
                "\n- At least 8 characters" \
                "\n- At least 1 symbol (!, @, #, ...)" \
                "\n- 1 uppercase and 1 lowercase" \
            )

        # Step 4: Prevent reusing the current password
        if saved_student.password == new_password:
            raise ValueError("New password must be different.")

        # Step 5: Update the Student object
        saved_student.change_password(new_password)

        # Step 6: Save changes to JSON
        success = self.student_data_file.update_student(saved_student)

        if not success:
            raise ValueError("Failed to save the new password.")

        # Step 7: Update the logged-in object
        student.password = saved_student.password


