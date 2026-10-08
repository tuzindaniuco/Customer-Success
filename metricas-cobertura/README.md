# Métricas de cobertura (CS)

Fonte: planilha **Relatórios AM/CX 2026.Q3**, abas *Cobertura offboard*, *Cobertura onboard*, *Cobertura grupos* e *Solicitações no portal*.
Janela: **01/09/2026 a 01/10/2026**. A data base é 08/10/2026, com **7 dias de defasagem** e 30 dias de janela. A defasagem dá tempo de a fila de aprovação andar antes de medir; uma movimentação de ontem quase sempre ainda está aguardando aprovação.
Tenants internos (Niuco main/homolog/Apresentação, CX teste) ficam fora dos totais. Os CSVs completos estão em `resultados/`.

Para recalcular: exporte as 4 abas como JSON (`off.json`, `on.json`, `grp.json`, `portal.json`) numa pasta fora do repo e rode
`python3 calcular_metricas.py <pasta> <data base AAAA-MM-DD> [defasagem em dias, padrão 7]`. Os arquivos brutos têm dados pessoais e não devem ser versionados.

## Como cada métrica é calculada

- **Onboard / Offboard**: considera só as movimentações vindas do organograma (admissão ou desligamento) dentro da janela, contadas **por pessoa**. Uma pessoa pode ter vários workflows (ex.: "Offboarding" e "Encerramento de contas"); ela entra uma vez só.
  - **Cobertura de disparo** = pessoas com workflow disparado ÷ pessoas que entraram ou saíram do organograma. Só conta como disparo o que rodou de fato: quem só tem execuções **rejeitadas** ou **aguardando aprovação** continua na base, mas não conta como disparado.
  - **Cobertura de execução** = pessoas com execução concluída com sucesso ÷ pessoas disparadas. Quando há mais de uma execução que rodou, vale o pior status: erro > em andamento > sucesso.
  - "Sem workflow configurado" = status *Anterior ao onboard*: a empresa nunca rodou um workflow de onboard, então não há o que disparar.
- **Grupos**: foto atual (não depende da janela). A base são só as pessoas **na folha** (coluna *Na Folha* = Sim), porque é a folha que o workflow usa para saber quem foi contratado ou desligado. Como todo mundo já está em "Todos os Funcionários", só conta **grupo específico** (qualquer grupo além dele). Primeiro vejo se a empresa tem algum grupo específico; se tiver, cobertura = pessoas da folha com grupo específico ÷ pessoas da folha. Empresas sem nenhum grupo específico aparecem à parte, sem percentual.
- **Tickets**: tickets do portal abertos na janela. Taxa de conclusão = concluídos ÷ abertos.

## Resumo

| Métrica | Resultado (clientes) |
|---|---|
| Offboard: cobertura de disparo | **80,0%** (152 de 190 desligamentos). Não contam como disparo 7 aguardando aprovação e 2 rejeitados |
| Offboard: cobertura de execução | **81,6%** (124 de 152 disparados) |
| Onboard: cobertura de disparo | **61,5%** (88 de 143 admissões). Não contam como disparo 1 aguardando aprovação e 3 rejeitados |
| Onboard: cobertura de execução | **84,1%** (74 de 88 disparados) |
| Grupos: folha em grupo específico | **73,5%** (5.459 de 7.425) nas 10 empresas que têm grupo específico. Outras 5 empresas (3.098 pessoas na folha) não têm nenhum grupo específico |
| Tickets: taxa de conclusão | **99,6%** (1.630 de 1.637). Só a LG usa o portal |

## Offboard por empresa

| Empresa | Desligamentos | Sem disparo | Sem workflow configurado | Rejeitado | Aguardando | Disparados | Cob. disparo | Sucesso | Erro / em andamento | Cob. execução |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Contabilizei | 61 | 0 | 0 | 0 | 1 | 60 | 98,4% | 46 | 14 / 0 | 76,7% |
| Blip | 28 | 0 | 0 | 1 | 0 | 27 | 96,4% | 25 | 2 / 0 | 92,6% |
| Gupy | 27 | 0 | 0 | 0 | 2 | 25 | 92,6% | 20 | 5 / 0 | 80,0% |
| OLX | 22 | 22 | 0 | 0 | 0 | 0 | 0% | – | – | – |
| LG | 20 | 0 | 0 | 0 | 0 | 20 | 100% | 15 | 5 / 0 | 75,0% |
| Grancursos | 12 | 1 | 0 | 0 | 4 | 7 | 58,3% | 7 | 0 / 0 | 100% |
| Mercado Bitcoin | 9 | 0 | 0 | 0 | 0 | 9 | 100% | 7 | 2 / 0 | 77,8% |
| Bionexo | 6 | 6 | 0 | 0 | 0 | 0 | 0% | – | – | – |
| Hubla | 5 | 0 | 0 | 1 | 0 | 4 | 80,0% | 4 | 0 / 0 | 100% |

## Onboard por empresa

| Empresa | Admissões | Sem disparo | Sem workflow configurado | Rejeitado | Aguardando | Disparados | Cob. disparo | Sucesso | Erro / em andamento | Cob. execução |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Contabilizei | 30 | 1 | 0 | 0 | 0 | 29 | 96,7% | 26 | 3 / 0 | 89,7% |
| LG | 30 | 0 | 0 | 0 | 0 | 30 | 100% | 20 | 10 / 0 | 66,7% |
| Blip | 26 | 0 | 0 | 3 | 1 | 22 | 84,6% | 21 | 1 / 0 | 95,5% |
| Grancursos | 15 | 0 | 15 | 0 | 0 | 0 | 0% | – | – | – |
| OLX | 13 | 13 | 0 | 0 | 0 | 0 | 0% | – | – | – |
| Bionexo | 12 | 12 | 0 | 0 | 0 | 0 | 0% | – | – | – |
| Gupy | 8 | 1 | 0 | 0 | 0 | 7 | 87,5% | 7 | 0 / 0 | 100% |
| Mercado Bitcoin | 6 | 0 | 6 | 0 | 0 | 0 | 0% | – | – | – |
| Hubla | 2 | 2 | 0 | 0 | 0 | 0 | 0% | – | – | – |
| Jusbrasil | 1 | 0 | 1 | 0 | 0 | 0 | 0% | – | – | – |

## Grupos por empresa (pessoas na folha)

| Empresa | Na folha | Tem grupo específico? | Com grupo específico | Sem grupo específico | Cobertura |
|---|---:|:---:|---:|---:|---:|
| Contabilizei | 1.841 | Sim | 1.841 | 0 | 100% |
| **OLX** | 1.537 | Sim | 1 | **1.536** | **0,1%** |
| LG | 1.393 | Sim | 1.392 | 1 | 99,9% |
| Blip | 1.185 | Sim | 1.185 | 0 | 100% |
| G4 | 572 | Sim | 572 | 0 | 100% |
| Gupy | 491 | Sim | 403 | 88 | 82,1% |
| **doc9** | 238 | Sim | 4 | **234** | **1,7%** |
| **Hubla** | 112 | Sim | 29 | **83** | **25,9%** |
| Malga | 47 | Sim | 24 | 23 | 51,1% |
| Solfacil-POC | 9 | Sim | 8 | 1 | 88,9% |
| Grancursos | 1.081 | **Não** | – | – | – |
| Jusbrasil | 642 | **Não** | – | – | – |
| Sympla | 600 | **Não** | – | – | – |
| Bionexo | 448 | **Não** | – | – | – |
| Mercado Bitcoin | 327 | **Não** | – | – | – |

## Tickets do portal

| Empresa | Abertos | Concluídos | Cancelados | Em aberto | Taxa de conclusão |
|---|---:|---:|---:|---:|---:|
| LG | 1.637 | 1.630 | 5 | 2 | 99,6% |

Origem dos tickets da LG na janela: 632 manuais, 390 abertos pelo sistema e 615 importados. Os importados entraram em lote e vêm já concluídos, então puxam a taxa para cima. Nenhum outro cliente abriu ticket no período; só houve testes internos.

## Leituras para o time de CS

1. **OLX tem um único grupo específico, com 1 pessoa**: 1.536 pessoas da folha estão sem grupo específico, e nenhuma aciona onboard ou offboard. Isso explica o 0% de disparo da OLX nas duas métricas de workflow.
2. **doc9 (1,7%) e Hubla (25,9%) criaram grupos específicos, mas a maior parte da folha ainda está fora deles.** Na Malga só metade da folha está num grupo específico (51,1%), e na Gupy faltam 88 pessoas (82,1%).
3. **Grancursos, Jusbrasil, Sympla, Bionexo e Mercado Bitcoin não têm nenhum grupo específico** (3.098 pessoas na folha). Na Bionexo e na Jusbrasil o workflow não aciona para ninguém, e Grancursos, Jusbrasil e Mercado Bitcoin também nunca configuraram onboard.
4. **A fila parada é sinal de alerta.** Mesmo com 7 dias de defasagem, ainda há desligamentos aguardando aprovação: 4 na Grancursos, 2 na Gupy e 1 na Contabilizei. Se continuarem assim, o cliente provavelmente fez o desligamento por fora da Niuco.
5. **Entre os disparados, os erros se concentram em poucas empresas.**
   - No offboard: Contabilizei (14), LG (5) e Gupy (5).
   - No onboard: LG tem 10 erros em 30 admissões disparadas (66,7%).
6. **Tickets**: o portal é, na prática, uma ferramenta só da LG. Para os demais clientes a funcionalidade não está em uso, o que é uma oportunidade de adoção.

## Base diária para o Looker

A aba **Base cobertura diária** da planilha tem uma linha por dia, empresa e tipo (Onboard/Admissão ou Offboard/Demissão), calculada por uma única fórmula em A2 a partir das abas de origem. Só entram movimentações a partir de 01/01/2026, incluindo datas futuras já agendadas no organograma. Colunas: Data, Empresa, Ação, Tipo, Movimentações, Disparos, Rejeitados, Aguardando aprovação, Sem disparo e Sucesso. Cada pessoa conta uma vez por dia, com a mesma regra da aba Métricas CS.

No Looker, as coberturas devem ser campos calculados sobre as somas, nunca médias de percentuais diários:
- Cobertura de disparo = `SUM(Disparos) / SUM(Movimentações)`
- Cobertura de execução = `SUM(Sucesso) / SUM(Disparos)`
