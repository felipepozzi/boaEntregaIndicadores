from http.client import HTTPException, BAD_REQUEST

from flask import Flask, request, jsonify, abort
import dbConnector as dbMysql
import dynamoConnect as dynamoConnect

app = Flask(__name__)


@app.route('/boaentrega/indicadores', methods=['GET'])
def get_indicadores():
    args = request.args
    nome_indicador = args.get('nome_indicador')
    data_inicio = args.get('data_inicio')
    data_fim = args.get('data_fim')

    if nome_indicador is None:
        abort(BAD_REQUEST)

    try:
        if nome_indicador.upper() == "OTP":
            response = dbMysql.selectIndicadorOtp(data_inicio, data_fim)
            return app.response_class(response=response, mimetype='application/json')

        if nome_indicador.upper() == "OTD":
            response = dbMysql.selectIndicadorOtd(data_inicio, data_fim)
            return app.response_class(response=response, mimetype='application/json')

        if nome_indicador.upper() == "OTIF":
            response = dbMysql.selectIndicadorOtif(data_inicio, data_fim)
            return app.response_class(response=response, mimetype='application/json')

    except HTTPException as e:
        return HTTPException(422, "erro ao realizar consulta", jsonify({'error': e}))


@app.route('/boaentrega/indicadores', methods=['POST'])
def post_indicadores():
    try:
        if request.is_json:
            body = request.get_json()

            if body is None:
                abort(BAD_REQUEST)

            response = dbMysql.saveIndicadores(body)
            print(response)
            return app.response_class(response=response, mimetype='application/json')

    except HTTPException as e:
        return HTTPException(422, "erro ao realizar a gravação do evento na base", jsonify({'error': e}))


@app.route('/boaentrega/eventos_historicos', methods=['POST'])
def post_eventos_historicos():
    try:
        if request.is_json:
            body = request.get_json()
            idEntrega = body['id_entrega']
            idPedido = body['id_pedido']
            dataFimEntrega = body['data_fim_entrega']

            if idEntrega and idPedido and dataFimEntrega is None:
                abort(BAD_REQUEST)

            response = dynamoConnect.save(idEntrega, idPedido, dataFimEntrega, body)
            print(response)
            return app.response_class(response=response, mimetype='application/json')

    except HTTPException as e:
        return HTTPException(422, "erro ao realizar consulta", jsonify({'error': e}))


if __name__ == '__main__':
    app.run(debug=True)
