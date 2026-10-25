class GUIStudentController:
    def __init__(self, student_service, on_success, on_error, on_registered):
        self.student_service = student_service
        self.on_success = on_success
        self.on_error = on_error
        self.on_registered = on_registered

    def login(self, email, password):
        if not email or not password:
            self.on_error("Email and password are required.")
            return

        try:
            student = self.student_service.login(email, password)

            if student is None:
                self.on_error("Invalid email or password.")
            else:
                self.on_success(student)

        except (ValueError, OSError) as error:
            self.on_error(str(error))

    def register(self, name, email, password):
        try:
            student = self.student_service.register(name, email, password)
        except (ValueError, OSError) as error:
            self.on_error(str(error))
            return

        self.on_registered(student)
