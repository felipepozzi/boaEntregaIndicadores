import boto3
from flask import jsonify


def save(idEntrega, idPedido, dataFimEntrega, body):
    client = boto3.resource('dynamodb',
                            region_name='sa-east-1',
                            endpoint_url='http://localhost:4566')
    table = client.Table("entregas")
    print(table.table_status)

    table.put_item(Item={'id_entrega': idEntrega, 'id_pedido':  idPedido, 'data_fim_entrega': dataFimEntrega,
                         'body': body})

    response = jsonify(
        status='gravado com sucesso'
    )

    return response
