# Instalação do Rasa e de um servidor para actions via docker 

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
- action_hello_world: é equivaletente a uma utter padrão

## 6. Adicionar action_hello_world no arquivo domain.yml
```
actions:
  - utter_greet
  - utter_cheer_up
  - utter_did_that_help
  - utter_happy
  - utter_goodbye
  - utter_iamabot
  - utter_info
  - action_hello_world
```

action_hello_world
## 7. Criar uma intent e uma storie para testar o custom comand
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

## 8. Treinar o modelo novamente
```
    docker run --user 1000 -v $(pwd):/app rasa/rasa train
```

## 9. Criar uma imagem rasa/rasa-sdk a partir do Dockerfile
```
    docker build -t rasa/rasa-sdk .
```
 - build: cria uma imagem a parir de um Dockerfile
 - -t rasa/rasa-sdk: nome da imagem 
 - .: diretório onde esta o Dockerfile 

## 10. Para conectar o container rasa/rasa com o rasa/rasa-sdk preciamos criar uma network
```
    docker network create action_connect
```
 - network create: cria uma network
 -action_connect: nome da network 

## 11 Entrar na pasta actions e criar um container rasa/rasa-sdk com o servidor action-server
```
    cd actions
    docker run -v $(pwd):/app/actions --net action_connect --name action-server rasa/rasa-sdk
``` 
 - --net : nome da network
 - name: nome do container 
 - rasa/rasa-sdk: nome da imagem

## 12 No arquivo endpoints.yml desconmentar a action_endpoint: e alterar a url para
```
    action_endpoint:
        url: "http://action-server:5055/webhook"
```
Alterando essa linha de comando o container que será criado a partir da imagem rasa/rasa poderá se comunicar como container criar a patir da imagem rasa/rasa-sdk

## 13 Conectar o servidor action-server com o container do rasa
```
    docker run --user 1000 -it -v $(pwd):/app -p 5005:5005 --net action_connect rasa/rasa shell
```
- -it: Essa flag permite rodar o shell dentro do container
- -p 5005:5005: Mapeamento das portas do containers

## 14 Testar o boot
Se tudo ocorreu bem, consersando com o bot de acordo com a conversa abaixo você consegui ser o Hello Word! 
```
    Your input ->  hi                                                                                                                             
    Hey! How are you?
    Your input ->  I wanna know more about your company                                                                                           
    Hello World!

```


# Instalação do Rasa X 

# comandos úteis
Acessar o shell do container com usuário root
```
    docker exec -u root -it <hash id do container> /bin/bash
```



