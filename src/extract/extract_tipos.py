from src.config import parameters


def extrair_todos_tipos(atividades):
    back_tipos = []

    try:

        for atividade in atividades:
            issue_type = atividade["fields"]["issuetype"]

            back_tipo = dict(
            nome = issue_type['name'],
            descricao = issue_type['description'],
            tipoJiraId = issue_type['id']  )

            back_tipos.append(back_tipo)

        return back_tipos
        
    except Exception as e:
        print(e)
        return[]