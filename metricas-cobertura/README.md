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
- **Grupos**: foto atual (não depende da janela). A base são só as pessoas **na folha** (coluna *Na Folha* = Sim), porque é a folha que o workflow usa para saber quem foi contratado ou desligado. Como todo mundo já está em "Todos os Funcionários", só conta **grupo específico** (qualquer grupo além dele). Primeiro vejo se a empresa tem algum grupo específico; se tiver, cobertura = pessoas da folha com grupo específico ÷ pessoas da folha. Empresas sem nenhum grupo específico aparecem à parte, sem percentual.
- **Tickets**: tickets do portal abertos na janela. Taxa de conclusão = concluídos ÷ abertos.

## Resumo

| Métrica | Resultado (clientes) |
|---|---|
| Offboard: cobertura de disparo | **84,1%** (148 de 176 desligamentos) |
| Offboard: cobertura de execução | **41,9%** (62 de 148). Além disso: 35 pendentes, 28 rejeitados, 23 com erro |
| Onboard: cobertura de disparo | **67,0%** (136 de 203 admissões) |
| Onboard: cobertura de execução | **63,2%** (86 de 136). Além disso: 25 pendentes, 12 rejeitados, 13 com erro |
| Grupos: folha em grupo específico | **73,5%** (5.459 de 7.425) nas 10 empresas que têm grupo específico. Outras 5 empresas (3.098 pessoas na folha) não têm nenhum grupo específico |
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
| LG | 1.020 | 984 | 4 | 32 | 96,5% |

Origem dos tickets da LG na janela: 636 manuais e 384 abertos pelo sistema. Nenhum outro cliente abriu ticket no período; só houve testes internos (Niuco main 7, Apresentação 7).

## Leituras para o time de CS

1. **OLX tem um único grupo específico, com 1 pessoa**: 1.536 pessoas da folha estão sem grupo específico, e nenhuma aciona onboard ou offboard. Isso explica o 0% de disparo da OLX nas duas métricas de workflow.
2. **doc9 (1,7%) e Hubla (25,9%) criaram grupos específicos, mas a maior parte da folha ainda está fora deles.** Na Malga só metade da folha está num grupo específico (51,1%), e na Gupy faltam 88 pessoas (82,1%).
3. **Grancursos, Jusbrasil, Sympla, Bionexo e Mercado Bitcoin não têm nenhum grupo específico** (3.098 pessoas na folha). Na Bionexo e na Jusbrasil o workflow não aciona para ninguém, e Grancursos, Jusbrasil e Mercado Bitcoin também nunca configuraram onboard.
4. **O disparo funciona; o problema está em terminar a execução.**
   - Gupy tem 21 de 24 offboards **aguardando aprovação**: alguém do lado deles precisa aprovar.
   - Blip (13) e LG (12) têm muitos offboards **rejeitados**: vale entender o motivo.
   - A Contabilizei concentra os erros (14 no offboard e 10 no onboard).
5. **Tickets**: o portal é, na prática, uma ferramenta só da LG, que fecha quase tudo o que abre (96,5%). Para os demais clientes a funcionalidade não está em uso, o que é uma oportunidade de adoção.
