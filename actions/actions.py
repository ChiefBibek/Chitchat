# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# Define a custom action to fetch COVID-19 statistics
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests

class ActionCovidInfo(Action):
    def name(self) -> str:
        return "action_covid_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Extract location from the latest user message
        location = next(tracker.get_latest_entity_values("location"), None)
        
        if location is None:
            dispatcher.utter_message(text="Please provide a location to get COVID-19 statistics.")
            return []

        # Fetch COVID-19 data from an API
        url = f"https://covid-193.p.rapidapi.com/statistics?country={location}"
        headers = {
            "x-rapidapi-host": "covid-193.p.rapidapi.com",
            "x-rapidapi-key": "fb629554c6mshfe62df2185104bdp13a132jsn9efcae51842e"  #api key
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()

            if data["results"] > 0:
                # Fetch the relevant data
                country_data = data["response"][0]
                cases = country_data["cases"]["total"]
                deaths = country_data["deaths"]["total"]
                tests = country_data["tests"]["total"]
                
                # Set slot values
                return [SlotSet("cases", cases), SlotSet("deaths",deaths) ,SlotSet("tests",tests), SlotSet("location", location)]
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find any data for {location}.")
                return []
        else:
            dispatcher.utter_message(text="Failed to fetch data. Please try again later.")
            return []
