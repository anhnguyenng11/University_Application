"""
This file contains constants used throughout the project.
Add any operational boundaries or constraints that are relevant to the project here. For example, if there are specific limits on the number of students or subjects, they can be defined in this file.
DO NOT MODIFY DEFINED CONSTANTS UNLESS YOU ARE SURE OF WHAT YOU ARE DOING. Changes to these constants can have wide-ranging effects on the project and may lead to unexpected behavior if not handled carefully.
"""
STUDENT_DATABASE = "students.data"
ADMIN_DATABASE = "admins.data"

EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@university\.com"
PASSWORD_REGEX = r"^[A-Z][a-zA-Z]{5,}[0-9]{3,}$"

HD_THRESHOLD = 85
D_THRESHOLD = 75
C_THRESHOLD = 65
P_THRESHOLD = 50