from src.config import parameters
import datetime
from dateutil import parser

def extrair_periodos(atividades):
    periodos = []

    try:
        for atividade in atividades:
            worklogs = atividade["fields"]["worklog"]["worklogs"]

            if len(worklogs) > 0:
                started_datetime = worklogs[0]["started"]
                periodo = convert_datetime_to_periodo(started_datetime)
                periodos.append(periodo)
        return periodos
        
    except Exception as e:
        print(f"Erro ao extrair períodos: {e}")
        return []

def convert_datetime_to_periodo(str_datetime):
    # Exemplo de str_datetime: "2025-10-02T16:00:00.000-0300"
    parsed_datetime = parser.parse(str_datetime)

    num_semana = parsed_datetime.isocalendar().week

    periodo = dict(
        dia = parsed_datetime.day,
        semana = num_semana,
        mes = parsed_datetime.month,
        ano = parsed_datetime.year
    )

    return periodo