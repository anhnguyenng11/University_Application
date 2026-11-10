
from models.student import Student
from models.subject import Subject
from models.file_handlers.student_data_file import StudentDataFile
from utils import constants
from utils.validator import Validator
from utils.id_generator import IDGenerator


class StudentService:
    """
    This class provides services for managing student-related operations.
    Methods:
    - register: Registers a new student with the provided name, email, and password.
    - login: Authenticates a student using email and password. 
    - enroll_subject: Enrolls a student in a new subject.
    """

    def __init__(self, student_data_file: StudentDataFile) -> None:
        self.student_data_file = student_data_file

    def register(
        self,
        name: str,
        email: str,
        password: str
    ) -> Student:
        """
        Registers a new student with the provided name, email, and password.
        Raises ValueError if the name, email, or password is invalid or if the email is already registered.
        Returns the newly created Student object.
        """

        name = name.strip()
        email = email.strip()

        # Step 1: Validate inputs
        if not Validator.is_not_empty(name):
            raise ValueError("Name cannot be empty.")

        if not Validator.is_valid_email(email):
            raise ValueError("Invalid student email.\nEmail suffix: [@university.com]")

        if not Validator.is_valid_password(password):
            raise ValueError("Invalid password. " + constants.PASSWORD_REQUIREMENTS_MESSAGE)

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
        """
        Authenticates a student using email and password. Calls the StudentDataFile model to find the student.
        Raises ValueError if the email is not found or the password is incorrect.
        Returns the authenticated Student object.
        """
        email = email.strip()

        student = self.student_data_file.find_student_by_email(email)

        if student is None:
            raise ValueError("Student email not found.")

        if student.password != password:
            raise ValueError("Wrong password.")

        return student

    
    def enroll_subject(self, student: Student) -> Subject:
        """
        Enrolls the currently active student in a new subject, given a valid student ID, and they are not over their enrollment limit. Calls the StudentDataFile model to update the student's subjects.
        Raises ValueError if the student is not found, if the student has reached the maximum number of subjects, or if the enrollment fails.
        Returns the newly enrolled Subject object.
        """
        # Step 1: Load the student's latest saved record
        saved_student = self.student_data_file.find_student_by_id(
            student.student_id
        )

        if saved_student is None:
            raise ValueError("Student not found.")

        # Step 2: Check enrollment limit
        if not saved_student.can_enroll():
            raise ValueError(constants.SUBJECT_LIMIT_MESSAGE)

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
        """
        Removes a subject from the currently active student's enrolled subjects, given a valid student ID and subject ID. Calls the StudentDataFile model to update the student's subjects.
        Raises ValueError if the student is not found, if the subject is not found, or if the removal fails.
        Returns True if the removal is successful, otherwise False.
        """
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
        """
        Changes the password of a student, given their email is valid and the current password matches. The new password must meet specific criteria.
        Raises ValueError if any of the conditions are not met.
        """

        # Step 1: Load the latest student record
        saved_student = self.student_data_file.find_student_by_id(student.student_id)

        if saved_student is None:
            raise ValueError("Student not found.")

        # Step 2: Verify the current password
        if saved_student.password != current_password:
            raise ValueError("Current password is incorrect.")

        # Step 3: Validate the new password
        if not Validator.is_valid_password(new_password):
            raise ValueError("New password does not meet requirements. " + constants.PASSWORD_REQUIREMENTS_MESSAGE)          

        # Step 4: Prevent reusing the current password
        if saved_student.password == new_password:
            raise ValueError("New password must be different.")

        # Step 5: Update the Student object
        saved_student._change_password(new_password)

        # Step 6: Save changes to JSON
        success = self.student_data_file.update_student(saved_student)

        if not success:
            raise ValueError("Failed to save the new password.")

        # Step 7: Update the logged-in object
        student.password = saved_student.password


