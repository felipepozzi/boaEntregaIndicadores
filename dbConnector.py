import mysql.connector
from flask import json, jsonify

mydb = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='12345fe',
    database='boaentregadb'
)

mycursor = mydb.cursor()

def selectIndicadorOtp(dataInicio, dataFim):
    mycursor.execute("select id_entrega, data_hora_compra, data_hora_inicio_sepracao, data_hora_fim_sepracao, " +
                     "data_hora_entrega, status_entrega, id_rota, valor_frete," +
                     "timestampdiff(HOUR, data_hora_inicio_sepracao, data_hora_fim_sepracao) as OTP " +
                     "from entregas where data_hora_compra between '" + dataInicio + "' and '" + dataFim + "'")
    row_headers = [x[0] for x in mycursor.description]
    result = mycursor.fetchall()
    json_data = []
    for row in result:
        json_data.append(dict(zip(row_headers, row)))
    return json.dumps(json_data)

def selectIndicadorOtd(dataInicio, dataFim):
    mycursor.execute("SELECT count(distinct id_entrega) AS total_entregas, " +
    " count(distinct if(status_entrega = 'Efetuada no Prazo' , id_entrega, null )) AS entregas_sucesso" +
    " from entregas where data_hora_compra between '" + dataInicio + "' and '" + dataFim + "'")
    result = mycursor.fetchall()
    lst = result[0][1]/result[0][0] * 100
    response = jsonify(
        indicador_otd=lst
    )
    return response.data

def selectIndicadorOtif(dataInicio, dataFim):
    mycursor.execute("SELECT count(distinct id_entrega) AS total_entregas, " +
    " count(distinct if(pontualidade = true and coformidade = true, id_entrega, null)) as entrega_perfeita" +
    " from entregas where data_hora_compra between '" + dataInicio + "' and '" + dataFim + "'")
    result = mycursor.fetchall()
    lst = result[0][1] / result[0][0] * 100
    response = jsonify(
        indicador_otif=lst
    )
    return response.data