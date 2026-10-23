import random
from utils.constants import HD_GRADE_THRESHOLD, D_GRADE_THRESHOLD, C_GRADE_THRESHOLD, P_GRADE_THRESHOLD

class Subject:
    def __init__(self):
        """
        Initializes a new Subject instance with a random enrollment subject, marks, and grade.
        """
        self.enrol_sub = random_subject = random.randint(1, 999)
        self.marks = random.randint(25, 100) # mark as generated >=25 and <=100
        self.grade = self.defgrade()
        

    def defgrade(self):
            
        if self.marks >= HD_GRADE_THRESHOLD:
            defgrade = 'HD'
        elif self.marks >= D_GRADE_THRESHOLD:
            defgrade = 'D'
        elif self.marks >= C_GRADE_THRESHOLD:
            defgrade = 'C'
        elif self.marks >= P_GRADE_THRESHOLD:
            defgrade = 'P'
        else:
            defgrade = 'Z'
        
        return defgrade
         
##testing
test = Subject()
print(test.enrol_sub, test.marks, test.grade)