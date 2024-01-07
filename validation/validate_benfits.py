from database.benefits_list import BENEFITS_LIST


class BenefitValidator:
    def __init__(self):
        pass
    
    def validate_benefit(self, benefit):
        if benefit in BENEFITS_LIST:
            return True
        else:
            return False
