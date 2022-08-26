#!/bin/bash

echo Bem vindo ao ambiente da Boa entrega

echo Executando o docker-compose para o serviço MySql
docker-compose -f mysql/docker-compose.yml up -d --remove-orphans

echo fim da execução
