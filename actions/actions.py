from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

class summaryForm(FormAction):

    def name(self):
        return "summary_form"

    @staticmethod
    def required_slots(tracker):
        return ["subject", "id_number", "uni_org"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
      return {
              "subject": [
                  self.from_entity(entity="subject"),
                  self.from_intent(intent="outlook", value="outlook"),
                  self.from_intent(intent="vpn", value="vpn"),
              ],
              "id_number": [
                  self.from_text(intent="id_number"),
              ],
              "uni_org": [
                  self.from_text(intent="uni_org"),
              ],
          }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        id_number = tracker.get_slot('id_number')
        uni_org = tracker.get_slot('uni_org')
        subject = tracker.get_slot('subject')

        answer  = "O seu id é " + id_number + ".\nO seu uni_org é " + uni_org + ".\nO seu problema é com " + subject

        dispatcher.utter_message(text=answer)
        return []