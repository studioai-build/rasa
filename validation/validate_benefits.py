from database.benefits_list import BENEFITS_LIST


class BenefitValidator:
    """
    A class to validate benefits.
    """

    def __init__(self):
        pass

    def validate(self, benefit):
        """
        Validates a given benefit.

        Parameters:
        - benefit (str): The benefit to be validated.

        Returns:
        - bool: True if the benefit is valid, False otherwise.
        """

        print("validate_benefit")
        print("benefit", benefit)
        print("BENEFITS_LIST", BENEFITS_LIST)

        if benefit in BENEFITS_LIST:
            return True, f"{benefit} is covered."
        else:
            return False, f"{benefit} is not covered. We cover the benefit in list: {str(BENEFITS_LIST)}."
