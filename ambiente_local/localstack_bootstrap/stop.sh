#!/bin/bash

echo Bem vindo ao ambiente da Boa entrega

echo Executando o docker-compose para o serviço SQS
docker-compose -f sqs/docker-compose.yml down

echo Executando o docker-compose para o serviço SQL Server
docker-compose -f sqlServer/docker-compose.yml down