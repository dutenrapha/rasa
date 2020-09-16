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

