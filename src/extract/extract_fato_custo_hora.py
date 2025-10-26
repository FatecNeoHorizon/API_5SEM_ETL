import logging
from src.utils.convert_datetime_to_periodo import convert_datetime_to_periodo
from src.utils import retorno_dimensoes

logger = logging.getLogger(__name__)

def extrair_todos_fatos_custo_hora(jira_issues, projetos, devs):
    global projeto, periodo, desenvolvedor
    fato_atividade_dict, pk_sequence_array, qtd_final = {}, [], {}
    try:
        for jira_issue in jira_issues:
            extrair_dimensoes(jira_issue, projetos, devs)

            if projeto is None or periodo is None or 'id' not in periodo or not isinstance(desenvolvedor, int):
                continue

            projeto_id = int(projeto)
            periodo_id = int(periodo["id"])
            dev_id = int(desenvolvedor)

            pk = f"{projeto_id}-{periodo_id}-{dev_id}"

            horas = _calcular_horas_issue(jira_issue)
            custo = horas * _obter_custo_hora_por_id(devs, dev_id)

            if pk in pk_sequence_array:
                qtd_final[pk]["horas"] += horas
                qtd_final[pk]["custo"] += custo
            else:
                qtd_final[pk] = {"horas": horas, "custo": custo}
                pk_sequence_array.append(pk)

            fato_atividade_dict[pk] = {
                "dimProjeto": {"id": projeto_id},
                "dimPeriodo": {"id": periodo_id},
                "dimDev": {"id": dev_id},
                "horasQuantidade": qtd_final[pk]["horas"],
                "custo": qtd_final[pk]["custo"]
            }
        return fato_atividade_dict
    except Exception as e:
        logger.warning("Erro ao fato_custo_hora: %s", e)
        return []
    
def extrair_dimensoes(jira_issue, projetos, devs):
    
    #Extrair projetos
    global projeto
    try:
        projeto_jira_id = str(jira_issue["fields"]["project"]["id"])
        projeto = retorno_dimensoes.retornar_dim_projeto_custo_hora(projetos, projeto_jira_id)
        if not projeto:
            logger.warning("Projeto não encontrada")
    except Exception:
        projeto = None
        logger.warning("Falha ao obter projeto da issue")

    #Extrair periodo
    global periodo
    try:
        worklogs = jira_issue["fields"]["worklog"]["worklogs"]
        if len(worklogs) > 0:
            filtro_periodo = convert_datetime_to_periodo(worklogs[0]["started"])
        else:
            filtro_periodo = dict(dia=31, semana=99, mes=12, ano=99)
        periodo = retorno_dimensoes.retornar_dim_periodo(filtro_periodo)
        if not periodo:
            logger.warning("Período não encontrado")
    except Exception:
        periodo = None
        logger.warning("Falha ao obter período da issue")
    
    #extrair devs
    global desenvolvedor
    try:
        devJiraNome = jira_issue["fields"]["assignee"]["displayName"]
        if devJiraNome is None or str(devJiraNome).strip() == "":
            desenvolvedor = 1
        else:
            desenvolvedor = retorno_dimensoes.retornar_dim_dev_custo_hora(devs, devJiraNome) or 1
    except Exception:
        desenvolvedor = 1

def _calcular_horas_issue(jira_issue):
    try:
        total = 0.0
        worklogs = jira_issue["fields"]["worklog"]["worklogs"]
        if len(worklogs) > 0:
            for w in worklogs:
                secs = w.get("timeSpentSeconds") or 0
                total += float(secs) / 3600.0
        else:
            secs = jira_issue["fields"].get("timespent") or 0
            total = float(secs) / 3600.0
        return total
    except Exception:
        return 0.0

def _obter_custo_hora_por_id(devs, dev_id):
    if dev_id == 1:
        return 0.0
    vistos, id_calc = set(), 1
    for d in devs or []:
        nome = (d.get("nome") or "").strip()
        if not nome:
            continue
        k = nome.lower()
        if k in vistos:
            continue
        vistos.add(k)
        id_calc += 1
        if id_calc == dev_id:
            try:
                return float(d.get("custoHora", 0.0) or 0.0)
            except Exception:
                return 0.0
    return 0.0
