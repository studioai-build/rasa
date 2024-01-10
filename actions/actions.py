from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, ActionExecuted, EventType, SlotSet, FollowupAction
from messages.messages import generate_message
from validation.validate_member_id import MemberIDValidator
from validation.validate_benefits import BenefitValidator

USER_IDS = {}
USER_SESSIONS = {}
member_id_validator = MemberIDValidator()
benefit_validator = BenefitValidator()

class ActionSessionStart(Action):

        def name(self) -> Text:
            return "action_session_start"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            events = [SessionStarted()]
            events.append(ActionExecuted("action_listen"))
            USER_IDS[tracker.sender_id] = tracker.sender_id
            USER_SESSIONS[USER_IDS[tracker.sender_id]] = {"user_id": tracker.sender_id, "session_id": tracker.sender_id}

            return events

class ActionPriorAuthorization(Action):
        def name(self) -> Text:
            return "action_prior_authorization"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            print('ActionPriorAuthorization')
            entities = tracker.latest_message['entities']
            next_action = get_prior_auth_next_action(entities)

            if next_action:
                return [FollowupAction(next_action)]

            return [FollowupAction("action_listen")]



            flag_member_id = False

            for i in entities:
                if i['entity'] == 'member_id':
                    member_id = i['value']
                    flag_member_id = True
                    validated_message  = member_id_validator.validate(member_id)
                    dispatcher.utter_message(text=validated_message)

            if flag_member_id == False:
                dispatcher.utter_message(text=generate_message()["prior_authorization_not_found"])
            return []

class ActionPriceExplore(Action):

        def name(self) -> Text:
            return "action_price_explore"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            entities = tracker.latest_message['entities']

            for i in entities:
                if i['entity'] == 'benefits':
                    benefits = i['value']
                    dispatcher.utter_message(text=generate_message(benefits = benefits, action_name="CostEstimation")["price_explore"])
                else:
                    dispatcher.utter_message(text=generate_message()["benefits_not_found"])

            return [FollowupAction("action_disclaimers")]

class ActionBenefitsExplore(Action):

        def name(self) -> Text:
            return "action_benefits_explore"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            entities = tracker.latest_message['entities']
            flag_benefits = False

            for i in entities:
                if i['entity'] == 'benefits':
                    benefits = i['value']
                    flag_benefits = True
                    dispatcher.utter_message(text=generate_message(benefits = benefits, action_name="BenefitsExplore")["benefits"])

            if flag_benefits == False or len(entities) == 0:
                dispatcher.utter_message(text=generate_message()["benefits_not_found"])
                return []

            return []

class ActionBenefitsLimitation(Action):
        def name(self) -> Text:
            return "action_benefits_limitation"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            entities = tracker.latest_message['entities']
            flag_benefits = False

            for i in entities:
                if i['entity'] == 'benefits':
                    benefits = i['value']
                    flag_benefits = True
                    dispatcher.utter_message(text=generate_message(benefits = benefits, action_name="BenefitLimitation")["benefits"])

            if flag_benefits == False or len(entities) == 0:
                dispatcher.utter_message(text=generate_message()["benefits_not_found"])
                return []

            return [FollowupAction("action_disclaimers")]

class ActionBenefitsCalculation(Action):
        def name(self) -> Text:
            return "action_benefits_calculation"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            entities = tracker.latest_message['entities']
            flag_benefits = False

            for i in entities:
                if i['entity'] == 'benefits':
                    benefits = i['value']
                    flag_benefits = True
                    dispatcher.utter_message(text=generate_message(benefits = benefits, action_name="BenefitCalculation")["benefits"])

            if flag_benefits == False or len(entities) == 0:
                dispatcher.utter_message(text=generate_message()["benefits_not_found"])
                return []

            return [FollowupAction("action_disclaimers")]

class ActionBenefitsExplanation(Action):
        def name(self) -> Text:
            return "action_benefits_explanation"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            entities = tracker.latest_message['entities']
            flag_benefits = False

            for i in entities:
                if i['entity'] == 'benefits':
                    benefits = i['value']
                    flag_benefits = True
                    dispatcher.utter_message(text=generate_message(benefits = benefits, action_name="BenefitExplanation")["benefits"])

            if flag_benefits == False or len(entities) == 0:
                dispatcher.utter_message(text=generate_message()["benefits_not_found"])
                return []

            return [FollowupAction("action_disclaimers")]

class ActionBenefitValidator(Action):
        def name(self) -> Text:
            return "action_benefit_validator"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            entities = tracker.latest_message['entities']
            next_action = get_benefit_next_action(entities)

            for i in entities:
                if i['entity'] == 'benefits':
                    benefit = i['value']
                    is_valid, validated_message = benefit_validator.validate(benefit)

                    # for testing only
                    validated_message = f"{validated_message} [BenefitValidation]"

                    if is_valid:
                        dispatcher.utter_message(text=validated_message)
                        if next_action is not None:
                            return [FollowupAction(next_action)]
                        return [FollowupAction("action_disclaimers")]
                    else:
                        dispatcher.utter_message(text=validated_message)
                        break

            dispatcher.utter_message(text=generate_message(action_name="BenefitValidation")["default_fallback"])
            return [FollowupAction("action_listen")]

class ActionDisclaimers(Action):

        def name(self) -> Text:
            return "action_disclaimers"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            dispatcher.utter_message(text=generate_message(action_name="Disclaimers")["disclaimers"])

            return [FollowupAction("action_listen")]

class ActionGreet(Action):

        def name(self) -> Text:
            return "action_greet"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            dispatcher.utter_message(text=generate_message()["greetings"])

            return []

class ActionGoodbye(Action):

    def name(self) -> Text:
        return "action_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=generate_message()["goodbye"])

        return []

class ActionDefaultFallback(Action):

        def name(self) -> Text:
            return "action_default_fallback"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            dispatcher.utter_message(text=generate_message()["default_fallback"])

            return [FollowupAction("action_listen")]

class ActionPlanExplore(Action):
        def name(self) -> Text:
            return "action_plan_explore"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            entities = tracker.latest_message['entities']
            next_action = get_plan_next_action(entities)
            print('ActionPlanExplore')
            print('next_action', next_action)
            if next_action != 'action_plan_explore':
                return [FollowupAction(next_action)]

            dispatcher.utter_message(text=generate_message(action_name="PlanBenefitsExplore")["tmp"])
            return [FollowupAction("action_disclaimers")]

class ActionPlanExploreRecommendation(Action):
        def name(self) -> Text:
            return "action_plan_explore_recommendation"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print('ActionPlanExploreRecommendation')
            dispatcher.utter_message(text=generate_message(action_name="PlanBenefitsRecommendation")["tmp"])
            return [FollowupAction("action_disclaimers")]


class ActionPriorAuthorizationStatus(Action):
        def name(self) -> Text:
            return "action_prior_authorization_status"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print('ActionPriorAuthorizationStatus')
            dispatcher.utter_message(text=generate_message(action_name="PriorAuthStatus")["tmp"])
            return [FollowupAction("action_prior_authorization_requirement")]

class ActionPriorAuthorizationRequirement(Action):
        def name(self) -> Text:
            return "action_prior_authorization_requirement"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print('ActionPriorAuthorizationRequirement')
            dispatcher.utter_message(text=generate_message(action_name="PriorAuthRequirements")["tmp"])
            return [FollowupAction("action_disclaimers")]

class ActionProviderRecommendation(Action):
        def name(self) -> Text:
            return "action_provider_recommendation"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            print('ActionProviderRecommendation')
            dispatcher.utter_message(text=generate_message(action_name="ProviderRecommendation")["tmp"])
            return [FollowupAction("action_disclaimers")]


def get_benefit_next_action(entities = []):
    next_action = None
    for i in entities:
        if i['entity'] == 'limitations':
            next_action = 'action_benefits_limitation'
            break
        elif i['entity'] == 'calculation':
            next_action = 'action_benefits_calculation'
            break
        elif i['entity'] == 'explanation':
            next_action = 'action_benefits_explanation'
            break

    return next_action


def get_plan_next_action(entities = []):
    next_action = 'action_plan_explore'

    for i in entities:
        if i['entity'] == 'recommendation':
            next_action = 'action_plan_explore_recommendation'
            break

    return next_action

def get_prior_auth_next_action(entities = []):
    next_action = None

    for i in entities:
        if i['entity'] == 'prior_auth_status':
            next_action = 'action_prior_authorization_status'
            break
        if i['entity'] == 'prior_auth_requirements':
            next_action = 'action_prior_authorization_requirement'
            break

    return next_action
