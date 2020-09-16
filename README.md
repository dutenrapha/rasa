# Instalação do Rasa, Rasa X e servidor para custom command 

## 1. Instalar a imagem do rasa através do comando
```
    docker run --user 1000 -v $(pwd):/app rasa/rasa init -no-prompt
```
 - run: inicializa o container
 - --user 1000: cria um usuário chamado 1000
 - -v $(pwd):/app: mapeia o diretório atual com o diretório app do container 
 - rasa/rasa init -no-prompt: inicializa o projeto default do rasa a patir da imagem "rasa/rasa" sem utilizar o prompt

## 2. Treinar o modelo 
```
    docker run --user 1000 -v $(pwd):/app rasa/rasa train
```

## 3. Criar um arquivo chamado Dockerfile com o seguinte conteúdo
```
   FROM rasa/rasa-sdk

   WORKDIR /app

   USER root

   COPY ./actions /app/actions

   USER 1000
```
 - FROM rasa/rasa-sdk: criar uma nova imagam a partir da imagem rasa/rasa-sdk
 - WORKDIR /app: define o diretório de trabalho principal como app
 - USER root: loga como usuário root
 - COPY ./actions /app/actions: copia todo o conteúdo do diretório ./actions para o diretório /app/actions do conteiner
 - USER 1000: loga com o usuário 1000

## 4. Caso não exista o diretório actions no ditório raíz do projeto cria-la, mover o arquivo actions.py para essa pasta e criar um arquivo vazio chamado __init__.py
```
    mkdir actions
    mv actions.py actions
    cd actions
    touch __init__.py
```

## 5. Editar arquivo actions.py  dentro do diretório actions da seguinte forma:
```
    # This files contains your custom actions which can be used to run
    # custom Python code.
    #
    # See this guide on how to implement these action:
    # https://rasa.com/docs/rasa/core/actions/#custom-actions/


    # This is a simple example for a custom action which utters "Hello World!"

    from typing import Any, Text, Dict, List

    from rasa_sdk import Action, Tracker
    from rasa_sdk.executor import CollectingDispatcher


    class ActionHelloWorld(Action):

        def name(self) -> Text:
            return "action_hello_world"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            dispatcher.utter_message(text="Hello World!")

            return []

```

## 6. Criar uma intenção e uma storei para testar o custom comand
No arquivo nlu.yml adiconar
```
    - intent: Information
      examples: |
        - tell me more about your company
        - I want more information
        - Can I get something else from your company?
```
No arquivo stories.yml adiconar
```
    - story: information happy path
      steps:
      - intent: Information
      - action: action_hello_world

```

# comandos úteis
Acessar o chatbot do rasa via shell
```
    docker run -it --user 1000 -v $(pwd):/app rasa/rasa shell
```
- -it: Essa flag permite rodar o shell dentro do container

Acessar o shell do container com usuário root
```
    docker excec -u root -it <hash id do container> /bin/bash
```



