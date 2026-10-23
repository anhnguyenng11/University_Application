import random 

class Subject:
    def __init__(self):
        self.enrol_sub = random_subject = random.randint(1, 999)
        self.marks = random.randint(25, 100) # mark as generated >=25 and <=100
        self.grade = self.defgrade()
        

    def defgrade(self):
            
        if self.marks >= 85:
            defgrade = 'HD'
        elif self.marks >= 75:
            defgrade = 'D'
        elif self.marks >= 65:
            defgrade = 'C'
        elif self.marks >= 50:
            defgrade = 'P'
        else:
            defgrade = 'Z'
        
        return defgrade
         
##testing
test = Subject()
print(test.enrol_sub, test.marks, test.grade)