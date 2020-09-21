# Tutorial sobre como adicionar um form no rasa

## 1. Adicionar slots no arquivo domain.yml

<pre>
slots:
  id_number:
    type: unfeaturized
  uni_org:
    type: unfeaturized
  subject:
    type: unfeaturized
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
        return ["id_number", "uni_org", "subject"]
</pre>

## 6. No arquivo actions.py na classe criada acima inserir a função slot_mappings, o valor do return  é um dicionário mapeando o slot à uma das suas possveis fontes, entity, intent, uam mensagem ou uma lista deles. A primeira opção a dar match er utilizada para preencher o slot

<pre>
class summaryForm(FormAction):

    def name(self):
        return "summary_form"

    @staticmethod
    def required_slots(tracker):
        return ["id_number", "uni_org", "subject"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
      return {
              "id_number": [
                  self.from_text(intent="id_number"),
              ],
              "uni_org": [
                  self.from_text(intent="uni_org"),
              ],
              "subject": [
                  self.from_entity(intent="outlook"),
                  self.from_entity(intent="vpn"),
              ],
          }
</pre>

## 7. No arquivo NLU.yml criar as intençes id_number e uni_org

<pre>
- intent: id_number
  examples: |
   - Meu x é X234035
   - X234035
   - O meu id é X234035 

- intent: uni_org
  examples: |
   - Estou no GD
   - Estou na sede
   - GD
   - Sede
</pre>

## x. No arquvo incluir  config.yml FormPolicy como uma policy
<pre>
  policies:
  - name: MemoizationPolicy
  - name: TEDPolicy
  <b>- name: FormPolicy</b>
    max_history: 5
    epochs: 100
  - name: RulePolicy
  - name: RulePolicy
</pre>




