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
