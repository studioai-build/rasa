from database.price_list import BENEFITS_PRICE


def generate_message(member_id=None, benefits=None):
    return {
        "prior_authorization" : f'Affirm Prior Authorization for member id: {member_id}',
        "prior_authorization_not_found" : "Please provide member id",
        "price_explore" : f"{benefits} price is {BENEFITS_PRICE.get(benefits)}",
        "benefits" : f"Yes, {benefits} is covered and cost is {BENEFITS_PRICE.get(benefits)}",
        "benefits_not_found" : "What specific benefits you want to know?",
        "greetings": "Hello there how can i help you",
        "goodbye": "Goodbye",
        "default_fallback": "Sorry, I didn't get that. Can you rephrase?",
    }

