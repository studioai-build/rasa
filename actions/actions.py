from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, ActionExecuted, EventType, SlotSet, FollowupAction
from messages.messages import generate_message
from validation.validate_member_id import MemberIDValidator

USER_IDS = {}
USER_SESSIONS = {}
member_id_validator =MemberIDValidator()

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
            
            print("USER_IDS: ", USER_IDS), print("USER_SESSIONS: ", USER_SESSIONS)

            return events

class ActionPriorAuthorization(Action):
    
        def name(self) -> Text:
            return "action_prior_authorization"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            entities = tracker.latest_message['entities']
            flag_member_id = False
            print("entities: ", entities)
            for i in entities:
                if i['entity'] == 'member_id':
                    print("member_id: ", i['value'])
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
            print("entities: ", entities)

            for i in entities:
                if i['entity'] == 'benefits':
                    print("benefits: ", i['value'])
                    benefits = i['value']
                    dispatcher.utter_message(text=generate_message(benefits = benefits)["price_explore"])
                else:
                    dispatcher.utter_message(text=generate_message()["benefits_not_found"])
            return []

class ActionBenefitsExplore(Action):
            
        def name(self) -> Text:
            return "action_benefits_explore"
        
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            entities = tracker.latest_message['entities']
            flag_benefits = False
            print("entities: ", entities)

            for i in entities:
                if i['entity'] == 'benefits':
                    benefits = i['value']
                    flag_benefits = True
                    dispatcher.utter_message(text=generate_message(benefits = benefits)["benefits"])
            
            if flag_benefits == False or len(entities) == 0:
                dispatcher.utter_message(text=generate_message()["benefits_not_found"])
            return []

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
        
