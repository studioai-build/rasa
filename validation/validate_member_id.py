from database.member_id_list import MEMBERS_LIST_ID
from messages.messages import generate_message


class MemberIDValidator:
    def __init__(self):
        pass

    def validate(self, member_id):
        if len(member_id) != 9:
            return "Please provide valid member id of 9 digits"
        elif member_id in MEMBERS_LIST_ID:
            return generate_message(member_id = member_id)["prior_authorization"]
        else:
            return "Member id not found in database"