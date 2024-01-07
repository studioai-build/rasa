from database.benefits_list import BENEFITS_LIST


class BenefitValidator:
    """
    A class to validate benefits.
    """

    def __init__(self):
        pass
    
    def validate_benefit(self, benefit):
        """
        Validates a given benefit.

        Parameters:
        - benefit (str): The benefit to be validated.

        Returns:
        - bool: True if the benefit is valid, False otherwise.
        """
        if benefit in BENEFITS_LIST:
            return True
        else:
            return False
