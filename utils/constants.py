"""
This file contains constants used throughout the project.
Add any operational boundaries or constraints that are relevant to the project here. For example, if there are specific limits on the number of students or subjects, they can be defined in this file.
DO NOT MODIFY DEFINED CONSTANTS UNLESS YOU ARE SURE OF WHAT YOU ARE DOING. Changes to these constants can have wide-ranging effects on the project and may lead to unexpected behavior if not handled carefully.
"""
STUDENT_DATABASE = "students.data"
ADMIN_DATABASE = "admins.data"

EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@university\.com"
PASSWORD_REGEX = r"^[A-Z][a-zA-Z]{4,}[0-9]{3,}$"

HD_THRESHOLD = 85
D_THRESHOLD = 75
C_THRESHOLD = 65
P_THRESHOLD = 50

GRADE_DEFINITIONS = {
    "HD": "High Distinction",
    "D": "Distinction",
    "C": "Credit",
    "P": "Pass",
    "Z": "Fail"
}

STUDENT_ID_LENGTH = 6
SUBJECT_ID_LENGTH = 3
SUBJECT_LIMIT = 4

# Message templates, to be shared across both CLI and GUI interfaces
BREAK_LINE = "-" * 30
INVALID_OPTION_MESSAGE = "Invalid option. Please try again."
SUBJECT_LIMIT_MESSAGE = f"Cannot enroll in more than {SUBJECT_LIMIT} subjects."
PASSWORD_REQUIREMENTS_MESSAGE = "A password should meet the following criteria: \
    \n(i) It starts with an upper-case character,  \
    \n(ii) It contains at least five (5) letters,  \
    \n(iii) It is followed by three (3) or more digits."


# GUI Pallette
COLORS = {
    "background": "#FFFFFF",
    "surface": "#FFFFFF",
    "primary": "#2F80ED",
    "primary_hover": "#1769C2",
    "primary_pressed": "#12549B",
    "navy": "#183B56",
    "text": "#263238",
    "muted_text": "#607D8B",
    "border": "#D9E2EC",
    "success": "#2E8B57",
    "error": "#C0392B",
    "disabled": "#B8C7D9",
}
FONTS = {
    "title": ("Segoe UI", 30, "bold"),
    "heading": ("Segoe UI", 18, "bold"),
    "body": ("Segoe UI", 11),
    "body_bold": ("Segoe UI", 11, "bold"),
    "button": ("Segoe UI", 11, "bold"),
    "small": ("Segoe UI", 9),
}

# GUI Window Dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
