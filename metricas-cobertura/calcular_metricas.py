"""Métricas de cobertura de CS (onboard, offboard, grupos RBAC e tickets do portal).

Fonte: planilha "Relatórios AM/CX 2026.Q3" (Google Sheets), abas
"Cobertura offboard", "Cobertura onboard", "Cobertura grupos" e
"Solicitações no portal", exportadas como JSON {"values": [[...], ...]}.

Uso:
    python3 calcular_metricas.py <pasta_com_jsons> [data_base AAAA-MM-DD]

Os JSONs (off.json, on.json, grp.json, portal.json) têm dados pessoais e
não são versionados. Só os agregados por empresa vão para o repositório.
"""
import collections
import csv
import datetime as dt
import json
import os
import sys

INTERNOS = {"Niuco (main)", "Niuco (homolog)", "Niuco Apresentacao", "CX teste"}

SUCESSO = "Concluído com sucesso"
# Execuções que não rodaram de fato: ficam fora da cobertura de execução.
NAO_EXECUTADAS = {"Aguardando aprovação", "Rejeitado"}
COM_ERRO = {"Falhou", "Concluído com erros", "Em andamento com erros"}
SEM_EXECUCAO = {"Sem workflow", "Anterior ao offboard", "Anterior ao onboard"}


def carregar(pasta, nome):
    valores = json.load(open(os.path.join(pasta, nome)))["values"]
    cab = valores[0]
    return [dict(zip(cab, linha + [""] * (len(cab) - len(linha)))) for linha in valores[1:]]


def pct(n, d):
    return round(100 * n / d, 1) if d else None


def cobertura_workflow(linhas, col_data, inicio, fim):
    """Cobertura de disparo e de execução por empresa, contando pessoas (não execuções)."""
    pessoas = collections.defaultdict(list)
    for l in linhas:
        if not l["Origem da Data"].startswith("Organograma"):
            continue  # só movimentações vindas do organograma
        if inicio <= l[col_data] <= fim:
            pessoas[(l["Company"], l["Email"])].append(l["Status"])

    por_empresa = collections.defaultdict(collections.Counter)
    for (empresa, _), status in pessoas.items():
        c = por_empresa[empresa]
        c["movimentacoes"] += 1
        execs = [s for s in status if s not in SEM_EXECUCAO]
        if not execs:
            if any(s.startswith("Anterior") for s in status):
                c["sem_workflow_configurado"] += 1
            else:
                c["sem_disparo"] += 1
            continue
        executadas = [s for s in execs if s not in NAO_EXECUTADAS]
        if not executadas:
            c["rejeitado" if "Rejeitado" in execs else "aguardando_aprovacao"] += 1
            continue
        # Só conta como disparo o que rodou de fato; vale o pior status entre essas execuções.
        c["disparados"] += 1
        if any(s in COM_ERRO for s in executadas):
            c["erro"] += 1
        elif all(s == SUCESSO for s in executadas):
            c["sucesso"] += 1
        else:
            c["em_andamento"] += 1

    saida = []
    for empresa, c in por_empresa.items():
        saida.append({
            "empresa": empresa,
            "interno": empresa in INTERNOS,
            "movimentacoes": c["movimentacoes"],
            "sem_disparo": c["sem_disparo"],
            "sem_workflow_configurado": c["sem_workflow_configurado"],
            "rejeitado": c["rejeitado"],
            "aguardando_aprovacao": c["aguardando_aprovacao"],
            "disparados": c["disparados"],
            "cobertura_disparo_%": pct(c["disparados"], c["movimentacoes"]),
            "sucesso": c["sucesso"],
            "erro": c["erro"],
            "em_andamento": c["em_andamento"],
            "cobertura_execucao_%": pct(c["sucesso"], c["disparados"]),
        })
    return sorted(saida, key=lambda r: (r["interno"], -r["movimentacoes"]))


def tem_grupo_especifico(grupos):
    """Todo mundo está em "Todos os Funcionários"; só conta grupo além dele."""
    return any(g and not g.startswith("Todos os Funcionários") for g in grupos.split("; "))


def cobertura_grupos(linhas):
    """Cobertura de grupos específicos entre as pessoas na folha (é a folha que o workflow olha)."""
    por_empresa = collections.defaultdict(collections.Counter)
    for l in linhas:
        c = por_empresa[l["Company"]]
        especifico = tem_grupo_especifico(l["Grupos"])
        c["usuarios_com_grupo_especifico"] += especifico
        if l["Na Folha"] != "Sim":
            continue
        c["folha"] += 1
        c["folha_grupo_especifico"] += especifico
        c["folha_em_algum_grupo"] += l["Em Grupo"] == "Sim"
        c["folha_aciona_onboard"] += l["Aciona Onboard"] == "Sim"
        c["folha_aciona_offboard"] += l["Aciona Offboard"] == "Sim"

    saida = []
    for empresa, c in por_empresa.items():
        possui = c["usuarios_com_grupo_especifico"] > 0
        saida.append({
            "empresa": empresa,
            "interno": empresa in INTERNOS,
            "pessoas_na_folha": c["folha"],
            "possui_grupo_especifico": "Sim" if possui else "Não",
            "com_grupo_especifico": c["folha_grupo_especifico"],
            "sem_grupo_especifico": c["folha"] - c["folha_grupo_especifico"] if possui else None,
            "cobertura_grupos_especificos_%": pct(c["folha_grupo_especifico"], c["folha"]) if possui else None,
            "em_algum_grupo_%": pct(c["folha_em_algum_grupo"], c["folha"]),
            "aciona_onboard_%": pct(c["folha_aciona_onboard"], c["folha"]),
            "aciona_offboard_%": pct(c["folha_aciona_offboard"], c["folha"]),
        })
    return sorted(saida, key=lambda r: (r["interno"], -r["pessoas_na_folha"]))


def cobertura_tickets(linhas, inicio, fim):
    por_empresa = collections.defaultdict(collections.Counter)
    for l in linhas:
        if not (inicio <= l["Data de Abertura"][:10] <= fim):
            continue
        c = por_empresa[l["Cliente"]]
        c["abertos"] += 1
        c[l["Status"]] += 1
        c["fonte_" + l["Fonte"]] += 1
    saida = []
    for empresa, c in por_empresa.items():
        saida.append({
            "empresa": empresa,
            "interno": empresa in INTERNOS,
            "tickets_abertos": c["abertos"],
            "concluidos": c["Concluído"],
            "cancelados": c["Cancelado"],
            "em_aberto": c["Aberto"] + c["Em andamento"],
            "taxa_conclusao_%": pct(c["Concluído"], c["abertos"]),
            "taxa_tratados_%": pct(c["Concluído"] + c["Cancelado"], c["abertos"]),
            "fonte_manual": c["fonte_Manual"],
            "fonte_sistema": c["fonte_Sistema"],
            "fonte_importado": c["fonte_Importado"],
        })
    return sorted(saida, key=lambda r: (r["interno"], -r["tickets_abertos"]))


def gravar_csv(caminho, linhas):
    with open(caminho, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)


def main():
    pasta = sys.argv[1]
    base = dt.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else dt.date.today()
    inicio, fim = (base - dt.timedelta(days=30)).isoformat(), base.isoformat()
    destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
    os.makedirs(destino, exist_ok=True)

    resultados = {
        "offboard": cobertura_workflow(carregar(pasta, "off.json"), "Data de desligamento", inicio, fim),
        "onboard": cobertura_workflow(carregar(pasta, "on.json"), "Data de entrada", inicio, fim),
        "grupos": cobertura_grupos(carregar(pasta, "grp.json")),
        "tickets": cobertura_tickets(carregar(pasta, "portal.json"), inicio, fim),
    }
    for nome, linhas in resultados.items():
        gravar_csv(os.path.join(destino, f"{nome}_{fim}.csv"), linhas)
    json.dump({"inicio": inicio, "fim": fim, **resultados},
              open(os.path.join(destino, f"metricas_{fim}.json"), "w"), ensure_ascii=False, indent=1)
    print(f"Janela {inicio} a {fim}; CSVs em {destino}")


if __name__ == "__main__":
    main()
