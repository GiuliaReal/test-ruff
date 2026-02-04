import requests
import json
import os
import plotly.graph_objects as go

from dotenv import load_dotenv
from collections import Counter

def main():

    # Configurando variáveis
    load_dotenv(r'./.env')
    login = os.getenv("LOGIN")
    server = os.getenv("SERVER")
    key = os.getenv("KEY")

    # Configeurando rota de login
    login_url =f"{server}/api/v2/workspace/login" 
    body = {
        "login": f"{login}",
        "key": f"{key}"
    }
    response = requests.post(url=login_url, json=body,auth=None)
    content = json.loads(response.content)

    # Criando o header com o Token e organization
    token = content['accessToken']
    org = content['organizationLabel']

    headers = {'token':f'{token}','organization':f'{org}'}


    # Criando Dashboards com a quantidade de warnings po<CAMINHO ARQUIVO .ENV>r automação:
    warning_route = f"{server}/api/v2/alerts"
    response_warns =  requests.get(warning_route, headers=headers)
    warns = json.loads(response_warns.content)
    warns_contents =  warns['content']
    warns_infos = []
    for item in warns_contents:
        id = item['botId']
        category = item['type']
        data = {"id": f"{id}",  "type": f"{category}"}
        warns_infos.append(data)


    # Contar a frequência de alertas por ID de automação
    alert_counts = Counter(item['id'] for item in warns_infos)
    bots = list(alert_counts.keys())
    alert_values = list(alert_counts.values())

    # Gráfico de Barras para Alertas por Automação
    fig_alerts = go.Figure(data=[go.Bar(x=bots, y=alert_values, marker_color='mediumturquoise')])
    fig_alerts.update_layout(
        title_text='Total de Alertas por Automação',
        xaxis_title='ID da Automação',
        yaxis_title='Número de Alertas',
        template='plotly_dark'
    )
    fig_alerts.show()


    errors_route = f"{server}/api/v2/error"
    response_errors =  requests.get(errors_route, headers=headers)
    errors = json.loads(response_errors.content)
    errors_content =  errors['content']
    errors_infos = []
    for item in errors_content:
        id = item['botId']
        category = item['type']
        data = {"id": f"{id}", "Error category": f"{category}"}  
        errors_infos.append(data)


    # Contar a frequência de erros por ID de automação
    error_counts = Counter(item['id'] for item in errors_infos)
    bots = list(error_counts.keys())
    error_values = list(error_counts.values())

    # Gráfico de Barras para Erros por Automação
    fig_errors = go.Figure(data=[go.Bar(x=bots, y=error_values)])
    fig_errors.update_layout(
        title_text='Total de Erros por Automação',
        xaxis_title='ID da Automação',
        yaxis_title='Número de Erros',
        template='plotly_white'
    )
    fig_errors.show() 

    # Pie Chart para tipos de erros:
    type_errors = Counter(item['Error category'] for item in errors_infos)
    categories = list(type_errors.keys())
    amounts = list(type_errors.values())

    pie_chart = go.Figure(data=[go.Pie(labels=categories, values=amounts)])
    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']

    pie_chart.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    pie_chart.show()


if __name__ == "__main__":
    main()