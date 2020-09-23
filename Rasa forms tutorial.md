# Tutorial sobre como adicionar um form no rasa

## 1. No arquivo domain.yml Adicionar slots e o nome do form

<pre>
slots:
  id_number:
    type: unfeaturized
  uni_org:
    type: unfeaturized
  subject:
    type: unfeaturized

forms:
  - summary_form
</pre>

## 2. No arquivo actions.py importar a biblioteca FormAction

<pre>
  from rasa_sdk.forms import FormAction
</pre>

## 3. No arquivo actions.py inserir uma classe cujo único argumento é FormAction
<pre>
  class summaryForm(FormAction):
</pre>

## 4. No arquivo actions.py na classe criada acima inserir a função name, o valor do return é o nome ao qual o form será mencionado

<pre>
  class summaryForm(FormAction):
    def name(self):
      return "summary_form"
</pre>

## 5. No arquivo actions.py na classe criada acima inserir a função required_slots, o valor do return  uma lista com o nome dos slots requeridos Obs: adicionar o decorator @staticmethod

<pre>
  class summaryForm(FormAction):
    def name(self):
      return "summary_form"
    
    @staticmethod
    def required_slots(tracker):
        return [ "subject","id_number", "uni_org"]
</pre>

## 6. No arquivo actions.py na classe criada acima inserir a função slot_mappings, o valor do return  é um dicionário mapeando o slot à uma das suas possveis fontes, entity, intent, uam mensagem ou uma lista deles. A primeira opção a dar match será utilizada para preencher o slot

<pre>
class summaryForm(FormAction):

    def name(self):
        return "summary_form"

    @staticmethod
    def required_slots(tracker):
        return ["id_number", "uni_org", "subject"]

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
</pre>

## 7. No arquivo actions.py na classe criada acima inserir a função submit, essa função é responsável por devolver os as respostas coletadas.

<pre>
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
</pre>



## 8. No arquivo NLU.yml criar as seguintes intenções. Obs: Não esquecer de registrar essas intenções no arquvo domain.yml

<pre>
## intent:greet
- hey
- hello
- hi
- Oi
- Olá
- Iae
- Bom dia
- Boa tarde
- Boa noite

## intent:goodbye
- bye
- goodbye
- Tchau
- Até mais
- Obrigado

## intent:affirm
- yes
- y
- Sim
- s
- correto
- exato

## intent:deny
- no
- n
- Não
- nunca

## intent:vpn
- Minha [vpn](subject) não conecta
- Estou com problema na [vpn](subject)
- [vpn](subject)
- A [vpn](subject) não funciona

## intent:outlook
- Não consigo logar no [outlook](subject)
- Meu [outlook](subject) não funciona
- Como acesso o [outlook](subject) de casa?
- [outlook](subject)

## intent:id_number
- O meu ID é [x234035](id_number)
- [x234035](id_number)
- ID [T445612](id_number)
- Claro o meu ID é [F234035](id_number)

## intent:uni_org
- Estou na [sede](uni_org)
- Esotu no [GB](uni_org)
- Esotu no [NOC](uni_org)
- [sede](uni_org)
- [gd](uni_org)
- [noc](uni_org)

## intent:piada
- Me conte uma piada
- Fala uma piada
- Conta uma piada

## intent:clima
- Como está o clima hoje?
- Me fale sobre o clima hoje por favor.
- Hoje vai fazer sol?
- Hoje vai fazer chuva?

## intent:sentido
- Qual o sentido da vida?
- qual o significado da vida, do universo e tudo mais
- Me fale o sentido da vida

## intent:problema
- Estou com um problema
- Meu computador esta quebrado
- Estou com problemas na [vpn](subject)
- Estou com problema para acessar o [outlook](subject)

</pre>

## 9. No arquivo config.yml incluir as seguintes policies
<pre>
policies:
  - name: MemoizationPolicy
  - name: AugmentedMemoizationPolicy
  - name: TEDPolicy
    max_history: 5
    epochs: 100
  - name: MappingPolicy
  - name: "FormPolicy"
  - name: "FallbackPolicy"
    nlu_threshold: 0.4
    core_threshold: 0.3
    fallback_action_name: "action_default_fallback"
</pre>

## 10. No arquivo stories.yml criar as stories para coletar as informações dos slots o comando form{"name": "summary_form"} ativa o formulario

<pre>
## greet
* greet
  - utter_greet

## goodbye
* goodbye
  - utter_goodbye

## greet + problema + happy path
* greet
  - utter_greet
* problema OR outlook OR vpn
  - summary_form
  - form{"name": "summary_form"}
  - form{"name": null}

## greet + problema + unhappy path 1
* greet
  - utter_greet
* problema OR outlook OR vpn
  - summary_form
  - form{"name": "summary_form"}
* piada
  - utter_piada
  - utter_resp
  - summary_form
  - form{"name": null}

## greet + problema + unhappy path 2
* greet
  - utter_greet
* problema OR outlook OR vpn
  - summary_form
  - form{"name": "summary_form"}
* clima
  - utter_clima
  - summary_form
  - form{"name": null}

## greet + problema + unhappy path 3
* greet
  - utter_greet
* problema OR outlook OR vpn
  - summary_form
  - form{"name": "summary_form"}
* sentido
  - utter_sentido
  - summary_form
  - form{"name": null}

## piada
* piada
  - utter_piada
  - utter_resp

## clima
* clima
  - utter_clima

## sentido
* sentido
  - utter_sentido

</pre>


