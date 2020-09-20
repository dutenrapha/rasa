# 1. Adicionar slots no arquivo domain.yml

```
slots:
  id_number:
    type: unfeaturized
  uni_org:
    type: unfeaturized
  subject:
    type: unfeaturized
```
# 2. No arquivo actions.py importar a biblioteca FormAction
```
  from rasa_sdk.forms import FormAction

```

# 3. No arquivo actions.py inserir uma classe cujo único argumento é FormAction
```
  class summaryForm(FormAction):
```

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
