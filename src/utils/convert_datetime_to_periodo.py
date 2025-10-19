from dateutil import parser

def convert_datetime_to_periodo(str_datetime):
    parsed_datetime = parser.parse(str_datetime)
    num_semana = parsed_datetime.isocalendar()[1]

    periodo = dict(
        dia = parsed_datetime.day,
        semana = num_semana,
        mes = parsed_datetime.month,
        ano = parsed_datetime.year
    )

    return periodo