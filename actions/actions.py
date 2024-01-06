from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SessionStarted, ActionExecuted, EventType, SlotSet, FollowupAction
from database.price_list import BENFITS_PRICE

USER_IDS = {}
USER_SESSIONS = {}

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
            
            #check in entites if there are pation id if not ask for pation id if found return some benfits
            entities = tracker.latest_message['entities']
            print("entities: ", entities)
            for i in entities:
                if i['entity'] == 'patient_id':
                    print("patient_id: ", i['value'])
                    patient_id = i['value']
                    flag_patient_id = True
                    dispatcher.utter_message(text="Affirm Prior Authorization for pation id: "+patient_id) 
                else:
                    flag_patient_id = False
            if flag_patient_id == False:
                dispatcher.utter_message(text="Please provide pation id")      
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
                if i['entity'] == 'benfits':
                    print("benfits: ", i['value'])
                    benfits = i['value']
                    if benfits == 'knee replacement surgery':
                        dispatcher.utter_message(text=f"knee replacement surgery price is {BENFITS_PRICE[benfits]}")
                    elif benfits == 'maternity':
                        dispatcher.utter_message(text=f"maternity price is {BENFITS_PRICE[benfits]}")
                    else:
                        dispatcher.utter_message(text="benfits not found")
                else:
                    dispatcher.utter_message(text="What specific benfits you want to know?")
            return []

class ActionBenfitsExplore(Action):
            
        def name(self) -> Text:
            return "action_benfits_explore"
        
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            entities = tracker.latest_message['entities']
            print("entities: ", entities)
            if len(entities) == 0:
                dispatcher.utter_message(text="What specific benfits you want to know?")
                return []
            for i in entities:
                if i['entity'] == 'benfits':
                    print("benfits: ", i['value'])
                    benfits = i['value']
                    if benfits == 'knee replacement surgery':
                        dispatcher.utter_message(text=f"Yes, knee replacement surgery benfits is covered and cost is {BENFITS_PRICE[benfits]}")
                    elif benfits == 'maternity':
                        dispatcher.utter_message(text=f"Yes, maternity benfits is covered and cost is {BENFITS_PRICE[benfits]} ")
                else:
                    dispatcher.utter_message(text="What specific benfits you want to know?")
            
            return []

class ActionGreet(Action):
                    
        def name(self) -> Text:
            return "action_greet"
        
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            dispatcher.utter_message(text="hello there how can i help you")
            
            return []

class ActionGoodbye(Action):
    
    def name(self) -> Text:
        return "action_goodbye"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Goodbye")
        
        return []

class ActionDefaultFallback(Action):
        
        def name(self) -> Text:
            return "action_default_fallback"
        
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            dispatcher.utter_message(text="Default Fallback")
            
            return []
        
