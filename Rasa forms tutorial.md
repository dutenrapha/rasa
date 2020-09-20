# 1. Adicionar slots no arquivo domain.yml

<pre>
slots:
  id_number:
    type: unfeaturized
  uni_org:
    type: unfeaturized
  subject:
    type: unfeaturized
</pre>

# 2. No arquivo actions.py importar a biblioteca FormAction
<pre>
  from rasa_sdk.forms import FormAction
</pre>

# 3. No arquivo actions.py inserir uma classe cujo único argumento é FormAction
<pre>
  class summaryForm(FormAction):
</pre>

# 4. No arquvo incluir  config.yml FormPolicy como uma policy
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
