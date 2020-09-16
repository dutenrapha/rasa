FROM rasa/rasa-sdk

WORKDIR /app

USER root

COPY ./actions /app/actions

USER 1000
