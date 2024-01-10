from database.price_list import BENEFITS_PRICE

def generate_message(member_id=None, benefits=None, plan=None, action_name=None):
    """
    Generate a message based on the provided member ID and benefits.

    Args:
        member_id (str, optional): The member ID. Defaults to None.
        benefits (str, optional): The benefits to be checked. Defaults to None.

    Returns:
        dict: A dictionary containing different types of messages based on the inputs.
    """

    # for testing only
    suffix = action_name if action_name is not None else ''

    return {
        "prior_authorization" : f'Affirm Prior Authorization for member id: {member_id}',
        "prior_authorization_not_found" : "Please provide member id",
        "price_explore" : f"{benefits} price is {BENEFITS_PRICE.get(benefits)} [{suffix}]",
        "benefits" : f"Yes, {benefits} is covered and cost is {BENEFITS_PRICE.get(benefits)}. [{suffix}]",
        "benefits_not_found" : "What specific benefits you want to know?",
        "disclaimers": f"The content provided on this website/blog/article is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. [{suffix}]",
        "greetings": "Hello there how can i help you",
        "goodbye": "Goodbye",
        "default_fallback": f"Sorry, I didn't get that. Can you rephrase? {f'[{suffix}]' if suffix else ''}",
        "tmp": f"Lorem Ipsum is simply dummy text of the printing and typesetting industry {f'[{suffix}]' if suffix else ''}"
    }

