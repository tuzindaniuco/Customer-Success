# Métricas de cobertura (CS)

Fonte: planilha **Relatórios AM/CX 2026.Q3**, abas *Cobertura offboard*, *Cobertura onboard*, *Cobertura grupos* e *Solicitações no portal*.
Janela: **08/09/2026 a 08/10/2026** (data base 08/10/2026, 30 dias para trás).
Tenants internos (Niuco main/homolog/Apresentação, CX teste) ficam fora dos totais. Os CSVs completos estão em `resultados/`.

Para recalcular: exporte as 4 abas como JSON (`off.json`, `on.json`, `grp.json`, `portal.json`) numa pasta fora do repo e rode
`python3 calcular_metricas.py <pasta> <AAAA-MM-DD>`. Os arquivos brutos têm dados pessoais e não devem ser versionados.

## Como cada métrica é calculada

- **Onboard / Offboard**: considera só as movimentações vindas do organograma (admissão ou desligamento) dentro da janela, contadas **por pessoa**. Uma pessoa pode ter vários workflows (ex.: "Offboarding" e "Encerramento de contas"); ela entra uma vez só.
  - **Cobertura de disparo** = pessoas com pelo menos um workflow executado ÷ pessoas que entraram ou saíram do organograma.
  - **Cobertura de execução** = pessoas em que **todas** as execuções terminaram em "Concluído com sucesso" ÷ pessoas com disparo. Quando há mais de uma execução, vale o pior status: falha/erro > rejeitado > pendente > sucesso.
  - "Sem workflow configurado" = status *Anterior ao onboard*: a empresa nunca rodou um workflow de onboard, então não há o que disparar.
- **Grupos**: foto atual (não depende da janela). A base são os usuários com status **Contratado** (casados com o organograma). Cobertura = contratados em pelo menos um grupo aprovado ÷ contratados. Também mostro quantos estão num grupo **específico**, ou seja, qualquer grupo além de "Todos os Funcionários", que é o que dá permissão por função.
- **Tickets**: tickets do portal abertos na janela. Taxa de conclusão = concluídos ÷ abertos.

## Resumo

| Métrica | Resultado (clientes) |
|---|---|
| Offboard: cobertura de disparo | **84,1%** (148 de 176 desligamentos) |
| Offboard: cobertura de execução | **41,9%** (62 de 148). Além disso: 35 pendentes, 28 rejeitados, 23 com erro |
| Onboard: cobertura de disparo | **67,0%** (136 de 203 admissões) |
| Onboard: cobertura de execução | **63,2%** (86 de 136). Além disso: 25 pendentes, 12 rejeitados, 13 com erro |
| Grupos: contratados em grupo | **78,7%** (7.406 de 9.409). 2.003 sem grupo, todos em OLX, Sympla e Mercado Bitcoin |
| Tickets: taxa de conclusão | **96,5%** (984 de 1.020). Só a LG usa o portal |

## Offboard por empresa

| Empresa | Desligamentos | Disparados | Cob. disparo | Sucesso | Erro | Rejeitado | Pendente | Cob. execução |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Contabilizei | 56 | 56 | 100% | 34 | 14 | 2 | 6 | 60,7% |
| LG | 27 | 27 | 100% | 10 | 5 | 12 | 0 | 37,0% |
| Gupy | 24 | 24 | 100% | 1 | 2 | 0 | 21 | 4,2% |
| Blip | 21 | 21 | 100% | 3 | 1 | 13 | 4 | 14,3% |
| OLX | 21 | 0 | 0% | – | – | – | – | – |
| Grancursos | 10 | 9 | 90% | 5 | 0 | 0 | 4 | 55,6% |
| Bionexo | 6 | 0 | 0% | – | – | – | – | – |
| Mercado Bitcoin | 6 | 6 | 100% | 5 | 1 | 0 | 0 | 83,3% |
| Hubla | 5 | 5 | 100% | 4 | 0 | 1 | 0 | 80,0% |

## Onboard por empresa

| Empresa | Admissões | Disparados | Cob. disparo | Sucesso | Erro | Rejeitado | Pendente | Cob. execução |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Contabilizei | 65 | 64 | 98,5% | 26 | 10 | 5 | 23 | 40,6% |
| LG | 33 | 33 | 100% | 31 | 2 | 0 | 0 | 93,9% |
| Blip | 27 | 27 | 100% | 23 | 1 | 3 | 0 | 85,2% |
| OLX | 27 | 0 | 0% | – | – | – | – | – |
| Bionexo | 13 | 0 | 0% | – | – | – | – | – |
| Grancursos | 12 | 0 (sem onboard configurado) | 0% | – | – | – | – | – |
| Gupy | 12 | 10 | 83,3% | 6 | 0 | 2 | 2 | 60,0% |
| Mercado Bitcoin | 10 | 0 (sem onboard configurado) | 0% | – | – | – | – | – |
| Hubla | 3 | 2 | 66,7% | 0 | 0 | 2 | 0 | 0% |
| Jusbrasil | 1 | 0 (sem onboard configurado) | 0% | – | – | – | – | – |

## Grupos por empresa (contratados)

| Empresa | Contratados | Sem grupo | Cobertura | Em grupo específico* |
|---|---:|---:|---:|---:|
| Contabilizei | 1.841 | 0 | 100% | 100% |
| Blip | 1.185 | 0 | 100% | 100% |
| **OLX** | 1.181 | **1.180** | **0,1%** | 0,1% |
| Grancursos | 1.009 | 0 | 100% | 0% |
| LG | 809 | 0 | 100% | 100% |
| Jusbrasil | 642 | 0 | 100% | 0% |
| G4 | 572 | 0 | 100% | 100% |
| **Sympla** | 492 | **492** | **0%** | 0% |
| Gupy | 491 | 0 | 100% | 82,1% |
| Bionexo | 450 | 0 | 100% | 0% |
| **Mercado Bitcoin** | 330 | **330** | **0%** | 0% |
| doc9 | 238 | 0 | 100% | 1,7% |
| Hubla | 113 | 0 | 100% | 25,7% |
| Malga | 47 | 0 | 100% | 51,1% |
| Solfacil-POC | 9 | 1 | 88,9% | 88,9% |

\* Em algum grupo além de "Todos os Funcionários".

## Tickets do portal

| Empresa | Abertos | Concluídos | Cancelados | Em aberto | Taxa de conclusão |
|---|---:|---:|---:|---:|---:|
| LG | 1.020 | 984 | 4 | 32 | 96,5% |

Origem dos tickets da LG na janela: 636 manuais e 384 abertos pelo sistema. Nenhum outro cliente abriu ticket no período; só houve testes internos (Niuco main 7, Apresentação 7).

## Leituras para o time de CS

1. **OLX, Sympla e Mercado Bitcoin estão sem grupo** porque o grupo "Todos os Funcionários" deles está **Pendente** de aprovação. Aprovar esse grupo resolve 2.003 pessoas de uma vez. Na OLX isso explica o 0% de disparo em onboard e offboard: sem grupo, nenhum workflow é acionado.
2. **Bionexo** tem 100% em grupo, mas 0% dos contratados acionam workflow (coluna *Aciona Workflow*) e nada disparou na janela. O grupo existe, mas não está ligado a nenhum workflow.
3. **Grancursos, Jusbrasil e Mercado Bitcoin nunca configuraram onboard.** Grancursos e Jusbrasil só têm o grupo genérico, sem RBAC por função.
4. **O disparo funciona; o problema está em terminar a execução.**
   - Gupy tem 21 de 24 offboards **aguardando aprovação**: alguém do lado deles precisa aprovar.
   - Blip (13) e LG (12) têm muitos offboards **rejeitados**: vale entender o motivo.
   - A Contabilizei concentra os erros (14 no offboard e 10 no onboard).
5. **Tickets**: o portal é, na prática, uma ferramenta só da LG, que fecha quase tudo o que abre (96,5%). Para os demais clientes a funcionalidade não está em uso, o que é uma oportunidade de adoção.
