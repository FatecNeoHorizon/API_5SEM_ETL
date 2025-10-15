from src.config import parameters

def extrair_todos_status(atividades):
    back_status_array = []

    try:

        for atividade in atividades:
            status_category = atividade["fields"]["statusCategory"]

            back_status = dict(
            nome = status_category['name'],
            statusJiraId = status_category['id']  )

            back_status_array.append(back_status)

        return back_status_array
        
    except Exception as e:
        print(e)
        return[]