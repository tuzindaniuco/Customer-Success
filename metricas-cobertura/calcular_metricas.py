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
PENDENTES = {"Aguardando aprovação", "Em andamento"}
# Ordem de gravidade para resumir várias execuções da mesma pessoa
# (o pior status define o resultado da pessoa).
GRAVIDADE = [
    "Falhou",
    "Concluído com erros",
    "Em andamento com erros",
    "Rejeitado",
    "Aguardando aprovação",
    "Em andamento",
    SUCESSO,
]
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
        c["disparados"] += 1
        pior = min(execs, key=GRAVIDADE.index)
        if pior == SUCESSO:
            c["sucesso"] += 1
        elif pior in PENDENTES:
            c["pendente"] += 1
        elif pior == "Rejeitado":
            c["rejeitado"] += 1
        else:
            c["erro"] += 1
        c["execucoes"] += len(execs)
        c["execucoes_sucesso"] += sum(s == SUCESSO for s in execs)

    saida = []
    for empresa, c in por_empresa.items():
        saida.append({
            "empresa": empresa,
            "interno": empresa in INTERNOS,
            "movimentacoes": c["movimentacoes"],
            "disparados": c["disparados"],
            "sem_disparo": c["sem_disparo"],
            "sem_workflow_configurado": c["sem_workflow_configurado"],
            "cobertura_disparo_%": pct(c["disparados"], c["movimentacoes"]),
            "sucesso": c["sucesso"],
            "erro": c["erro"],
            "rejeitado": c["rejeitado"],
            "pendente": c["pendente"],
            "cobertura_execucao_%": pct(c["sucesso"], c["disparados"]),
            "execucoes": c["execucoes"],
            "execucoes_sucesso": c["execucoes_sucesso"],
        })
    return sorted(saida, key=lambda r: (r["interno"], -r["movimentacoes"]))


def cobertura_grupos(linhas):
    por_empresa = collections.defaultdict(collections.Counter)
    for l in linhas:
        c = por_empresa[l["Company"]]
        em_grupo = l["Em Grupo"] == "Sim"
        c["usuarios"] += 1
        c["usuarios_em_grupo"] += em_grupo
        if l["Status Niuco"] == "Contratado":
            c["contratados"] += 1
            c["contratados_em_grupo"] += em_grupo
            especificos = [g for g in l["Grupos"].split("; ") if g and not g.startswith("Todos os Funcionários")]
            c["contratados_grupo_especifico"] += bool(especificos)
            c["contratados_aciona_onboard"] += l["Aciona Onboard"] == "Sim"
            c["contratados_aciona_offboard"] += l["Aciona Offboard"] == "Sim"
        if l["Grupos Não Aprovados"]:
            c["com_grupo_pendente_ou_suspenso"] += 1

    saida = []
    for empresa, c in por_empresa.items():
        saida.append({
            "empresa": empresa,
            "interno": empresa in INTERNOS,
            "contratados": c["contratados"],
            "contratados_em_grupo": c["contratados_em_grupo"],
            "contratados_sem_grupo": c["contratados"] - c["contratados_em_grupo"],
            "cobertura_grupos_contratados_%": pct(c["contratados_em_grupo"], c["contratados"]),
            "contratados_grupo_especifico_%": pct(c["contratados_grupo_especifico"], c["contratados"]),
            "contratados_aciona_onboard_%": pct(c["contratados_aciona_onboard"], c["contratados"]),
            "contratados_aciona_offboard_%": pct(c["contratados_aciona_offboard"], c["contratados"]),
            "usuarios_total": c["usuarios"],
            "usuarios_em_grupo": c["usuarios_em_grupo"],
            "cobertura_grupos_todos_%": pct(c["usuarios_em_grupo"], c["usuarios"]),
            "com_grupo_pendente_ou_suspenso": c["com_grupo_pendente_ou_suspenso"],
        })
    return sorted(saida, key=lambda r: (r["interno"], -r["contratados"]))


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
