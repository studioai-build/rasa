from database.member_id_list import MEMBERS_LIST_ID
from messages.messages import generate_message


class MemberIDValidator:
    """
    A class to validate member IDs.

    Methods:
    - validate(member_id): Validates the provided member ID.
    """

    def __init__(self):
        pass

    def validate(self, member_id):
        """
        Validates the provided member ID.

        Parameters:
        - member_id (str): The member ID to be validated.

        Returns:
        - str: The validation result message.
        """
        if len(member_id) != 9:
            return "Please provide a valid member ID of 9 digits"
        elif member_id in MEMBERS_LIST_ID:
            return generate_message(member_id=member_id)["prior_authorization"]
        else:
            return "Member ID not found in the database"
