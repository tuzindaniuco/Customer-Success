# Bases de dados do Customer Care

Quatro planilhas do Google Sheets são os bancos de dados internos do Customer Care. Este arquivo é o mapa delas: para que serve cada uma, quais abas importam, quais colunas e quais regras valem. Atualize aqui sempre que uma aba, coluna ou regra mudar.

Os dados em si (pessoas, e-mails, CNPJs) ficam só nas planilhas. Aqui entram apenas estrutura e regras.

## Mapa

| Nome | Planilha | Link | Dono dos dados |
|---|---|---|---|
| FINANCEIRO | [NIUCO] COBRANÇA | https://docs.google.com/spreadsheets/d/1UF5-sbh0xbhyeXkBpG3pOJliPfiO15IRYGnMdBXlAeY | Cobrança, faturas, contratos |
| INTERNO | [NIUCO] DATABASE | https://docs.google.com/spreadsheets/d/18yYh-WBgBxrfaDVUVkjOComtjCIZmnevTu29uFVWmAM | Dados da plataforma Niuco (workflows, cobertura, logins, funcionários) |
| HEALTHSCORE | [NIUCO] MATRIZ DE HEALTH SCORE | https://docs.google.com/spreadsheets/d/1GFlzeH7DwUai_8Qg9KrlNbshhCH65M33nnnyZkvTH7Q | Cálculo do Health Score por empresa |
| AM/TAM | [AM/TAM] DATABASE | https://docs.google.com/spreadsheets/d/14DEUkFlQrv0AYmc-1sihIwFbWiicBdseMbGPvaGqUjE | Carteira, OKRs, KPIs, projetos, pesquisa de satisfação |

Fluxo geral: a CARTEIRA do INTERNO é um `IMPORTRANGE` da aba `carteira` do AM/TAM. O HEALTHSCORE tem as abas Fonte e Carteira (ocultas) e usa métricas que vêm do INTERNO (workflows, logins, compliance, contratos); a ligação exata ainda não foi mapeada. O FINANCEIRO é a fonte de cobrança (faturas e contratos); o número de funcionários da carteira vem da FATURA (coluna Funcionários, sem parceiros).

## FINANCEIRO ([NIUCO] COBRANÇA)

Abas visíveis:

- **FATURA** (cobrança mensal; fonte do número de funcionários da carteira, coluna Funcionários): uma linha por empresa por mês. Colunas: ID Empresa, Empresa, Data Referência, Funcionários, Parceiros, Gastos Adicionais, Crédito, Data de vencimento, Data de pagamento, Licenças Total, Valor, Multa, Juros, Juros Cartão, Add-On, Mora Anterior, Variação Licenças, Fatura, Variação Fatura, Dias em atraso, Pago, Status. `Data Referência` é data real (primeiro dia do mês). Meses recentes podem estar sem `Funcionários`.
- **CARTEIRA**: mesma carteira do AM/TAM, com colunas extras de cobrança.
- **DADOS_COBRANÇA**: cadastro de cobrança por empresa (CNPJ, modo de cobrança, limite de licenças, % de uso, piso, valor fixo, valor por usuário, add-on fixo, multa, juros, fim do contrato, dia de pagamento).
- **FATURAMENTO HISTÓRICO**: Data Referência, Empresa, Valor, NPS, Fase, Plano, Produto.
- **Emissão NF**: controle de emissão e envio de nota fiscal.
- **base clientes**: nome, razão social, CNPJ, e-mails de cobrança, status, vencimento.
- **INFORAÇÕES BACKLOG** (grafia da aba): Referência, Empresa ID, Empresa, hasEmail, ProvidersCount, Funcionários, Parceiros.
- Ocultas: SAAS GRID, SAAS GRID 2, INFO AGOSTO, CONTROLE DE TIER.

## INTERNO ([NIUCO] DATABASE)

- **CARTEIRA**: importa a carteira do AM/TAM. A coluna **Funcionários** (BC) é preenchida por fórmula a partir da FATURA do FINANCEIRO (ver "Regras e decisões").
- **WORKFLOWS**: um snapshot por workflow por dia de execução, com contadores acumulados (Erros, Falhas, Na Fila, Sucesso, Execuções, Iniciados, Concluídos) e deltas contra o snapshot anterior (`Delta Iniciados`, `Delta Success`, `Delta Failed`, `Delta Fila`, `Delta Rejected`, `Delta Aborted`, `Delta Success Rate`). Tipos: ONBOARD, OFFBOARD, ABSENT, MOVE, IDENTITY_SCREENING.
- **SUCCESS RATE WORKFLOW** e **SUCCESS RATE BOTTON**: Week, TAM, Plano, Empresa, Data, Tipo, Iniciados, Sucessos, Eficiência, Projeto. Agregam os deltas de WORKFLOWS em janela móvel de cerca de 31 dias, atualizada às sextas (datas da aba APOIO). `SUCCESS RATE BOTTON` é a versão do botão de offboard.
- **ADOÇÃO SCORE**: por semana, Success Rate (onboarding, offboarding, F&A, move, pré-folha), cobertura de onboarding e offboarding e Adoção Score, com deltas.
- **FAIXAS HS**: faixas de pontuação das métricas A09, A10 e A11 do HEALTHSCORE (limite em % dos funcionários e pontos).
- **COMPANIES**: uma linha por empresa (compliance, passo de onboarding, organograma, autorização, SSO, feature flags, funcionários, suporte).
- **COMPANIES_HISTORIC**: snapshot por empresa por data (`Data Execução` é data real). `Funcionários` traz um JSON por status; `#Funcionários` soma sem FIRED; `Hired`, `Absence` e `Fired` vêm separados, com os respectivos deltas.
- **COBERTURA**: Data, Empresa, Ação, Tipo, Movimentações, Disparos, Rejeitados, Aguardando aprovação, Sem disparo, Sucesso. Tem as mesmas colunas da "Base cobertura diária" do relatório AM/CX (confirmar se é espelho; `metricas-cobertura/` neste repositório calcula a partir das abas de cobertura).
- **LOGINS**: acessos por usuário e empresa, com últimos 30 dias, dias sem acesso e perfil.
- **COMPLIANCE**, **CONTRATOS**, **USERS**, **GRUPOS**, **CONEXÕES DIRETAS**, **INFO**, **APOIO**, **HEALTHSCORE**, **HS COMPLETO**, **GROUPS**.

## HEALTHSCORE ([NIUCO] MATRIZ DE HEALTH SCORE)

- **Métricas**: dicionário dos critérios. Adoção: A01 Login Frequência (logins únicos/22), A02 a A05 eficiência de workflow (onboarding, offboarding, absence, move; média de sucesso dos últimos 30 dias), A06 e A07 cobertura de onboarding e offboarding, A08 providers homologados, A09 a A11 e-mail pessoal, desligados com acesso e desligados que acessaram (percentil, menor é melhor). Configuração: C01 a C06. Engajamento: E01 e E02 (satisfação).
- **Pesos** e **Categorias**: peso de cada critério por plano (FinOPs, Sec Automation, Identity Managment, Ultimate, Sec Automation Gran) e por categoria.
- **Matriz**, **Details**, **Consolidado**, **Tendência** (semanal): pontuação por empresa, `HealthScore` e `Health Score Ponderado`, com Adoção, Configuração e Engajamento.
- Ocultas: Fonte, Calculadora, Carteira.

## AM/TAM ([AM/TAM] DATABASE)

- **CARTEIRA** (a fonte da carteira): semáforos de AM e TAM, fase, categoria, HealthScore, NPS, atividades, datas de contrato e renovação, plano, produto, MRR, valor por usuário, funcionários ativos, recuperação, autópsia, adoção, configuração, engajamento, risco, fase do projeto.
- **FATURAMENTO** e **TENDÊNCIA REVENUE** (RVO1, evolução semanal, quarter).
- **OKR AM** (KRA1 em diante), **OKR TAM** (KRT1 em diante) e as abas **TENDÊNCIA OKR - AM/TAM**.
- **KPI AM** (KPIA1 a KPIA9, global GLO2) e **KPI TAM** (KPIT1 a KPIT7, global GLO1), cada um com Atual, Meta, Proporcional, Desvio, Delta Semanal, Válido, Peso e Nota. Abas de tendência: TENDÊNCIA KPI - AM e TENDÊNCIA KPI - TAM.
- **PROJETOS** (tarefas do ClickUp por empresa, com hierarquia, vencimentos e atrasos) e **TENDÊNCIA PROJETOS**.
- **PESQUISA DE SATISFAÇÃO** (NPS, CX Rating, respostas por empresa), **HAPPYSCORE**, **CONSOLIDADO**, **RELAÇÃO BUGS**, **IDEAS**, **DECISION TREE** e **DECISION TREE DADOS**, **INFO** (códigos de fase e AMs).
- Ocultas: NRR, PLANOS, BACKUP PLANOS, ANÁLISE PROJETOS, ANÁLISE DE PLANOS, FEATURE/INTEGRAÇÃO, FUPS AM, SENTIMENTOS, SENTIMENTOS ACUMULADO, TICKETS - PROJETOS, Cópia de PROJETOS, TENDÊNCIA PLANOS.

## Regras e decisões

**Delta de WORKFLOWS é a fonte para acompanhar variação.** A análise diária olha a diferença entre uma linha e a anterior. O primeiro snapshot de cada workflow tem delta igual ao acumulado inteiro e deve ser descartado em qualquer soma. O delta cobre o intervalo desde o snapshot anterior, não um dia exato (um intervalo de 18 dias aparece como uma linha só). Quando a plataforma reclassifica falhas, `Delta Concluídos` fica negativo (exemplo: -142 no Gran Cursos em 28/07/2026); não é variação operacional.

**Comparação entre fontes de execução (08/05 a 09/10/2026, 8 empresas, onboard e offboard).** O índice (deltas de WORKFLOWS) tem 2.053 iniciados e 1.504 sucessos (73%). A aba `Cobertura offboard` e `Cobertura onboard` do relatório AM/CX (uma linha por pessoa, por Data Execução) tem cerca de 2.096 iniciados e 1.592 sucessos (76%). A Base cobertura diária tem 1.295 e 956 (74%) e parece subconjunto: faltam execuções em LG onboard, Blip onboard e Hubla offboard. O índice conta execuções; a Cobertura conta pessoas com status final. Em nível agregado batem, por empresa divergem nos dois sentidos. A decisão do time é manter o delta do índice para acompanhamento diário; usar a Cobertura quando precisar do número por pessoa, com lastro auditável.

**Número de funcionários da CARTEIRA = coluna Funcionários da FATURA, sem parceiros.** Decisão de 09/10/2026. Na FATURA, `Funcionários` (coluna D) e `Parceiros` (coluna E) são separados e `Licenças Total` (coluna J) é a soma dos dois. Para a análise do Customer Care só contam os funcionários, então a coluna `Funcionários` (BC) do INTERNO usa o último valor preenchido de `Funcionários` da FATURA de cada empresa, nunca `Licenças Total` nem `Parceiros`:

```
=LET(fatura; IMPORTRANGE("https://docs.google.com/spreadsheets/d/1UF5-sbh0xbhyeXkBpG3pOJliPfiO15IRYGnMdBXlAeY/edit"; "FATURA!B2:D"); empresas; INDEX(fatura; ; 1); datas; INDEX(fatura; ; 2); funcionarios; INDEX(fatura; ; 3); MAP(D2:D; LAMBDA(empresa; IF(empresa=""; ""; IFNA(INDEX(SORT(FILTER(funcionarios; empresas=empresa; funcionarios<>""); FILTER(datas; empresas=empresa; funcionarios<>""); FALSE); 1); "")))))
```

A fórmula ordena pela Data Referência e devolve o `Funcionários` da fatura mais recente com valor; se o mês mais novo estiver em branco, usa o anterior. Empresas sem fatura (Idwall, Alura, Buser) ficam em branco. Empresas sem fatura recente trazem um mês antigo (Asaas e Logcomex em set/2026, Conta Azul em mai/2026, Kenlo em abr/2026). O primeiro uso exige abrir o INTERNO e clicar em "Permitir acesso" no `IMPORTRANGE`; sem isso a coluna mostra `#REF!`. Alternativa descartada: o `Hired` do COMPANIES_HISTORIC, que não conta ausentes e vem 0 quando o snapshot é `UNKNOWN` (Sympla).

**Health Score: A09, A10 e A11 por faixas de proporção (aplicado em 09/10/2026).** As colunas `Usuários com E-mail pessoal`, `Desligados com Acesso` e `Desligados que acessaram` da aba HEALTHSCORE do INTERNO deixaram de usar percentil (`1 - PERCENTRANK`) e passaram a usar a proporção infratores ÷ `Funcionários` da CARTEIRA (coluna BC, que vem da FATURA), convertida em pontos por faixas. As faixas ficam na aba `FAIXAS HS` do INTERNO, editáveis, e as fórmulas leem essa aba. Cada faixa vale até o limite, inclusive; acima do último limite a pontuação é 0.

| Pontos | E-mail pessoal | Desligados com acesso | Desligados que acessaram |
|---|---|---|---|
| 100% | até 1% | até 2% | 0% |
| 80% | até 3% | até 5% | |
| 70% | | | até 0,5% |
| 60% | até 5% | até 10% | |
| 40% | até 10% | até 20% | até 1% |
| 20% | até 20% | até 30% | até 2% |
| 10% | | até 50% | |
| 0% | acima de 20% | acima de 50% | acima de 2% |

Pontos que valem registrar:
- Desligados com acesso pode passar de 100% dos funcionários (Bionexo 195%, Malga 128% em 09/10/2026), porque o numerador acumula ex-funcionários e o denominador é o quadro atual. O teto de 50% (acima disso, 0) foi aprovado.
- Desligados que acessaram é 0 em todas as empresas, e isso é o dado real; todas ficam com 100%.
- Alternativa não adotada: dividir desligados com acesso pelo total de desligados, que mede melhor a higiene de acesso (LG e OLX têm 5% a 7% dos desligados com acesso, Gupy tem 74%). Não adotada porque o histórico de desligados falha em Hubla, Jusbrasil, Sympla e Malga.
- Empresas pequenas oscilam mais (uma pessoa na Hubla muda quase 1 ponto percentual).
- Linhas sem funcionários na CARTEIRA ficam em branco. O denominador vem de outra fonte (FATURA) e pode ter um mês de defasagem.
- A aba Tendência da planilha MATRIZ DE HEALTH SCORE guarda valores fixos das semanas anteriores (calculados por percentil); as semanas novas usam a escala por faixas, então as séries de A09, A10 e A11 não são comparáveis antes e depois de 09/10/2026.
- A versão anterior das fórmulas (percentil) está no histórico de versões do Google Sheets.

**Nomes de empresa divergem entre abas** (G4 e Grancursos, Solfacil e SolFacil, JusBrasil e Jusbrasil, ASAAS e Asaas). O `=` do Sheets não diferencia maiúsculas, mas G4 e Grancursos exigem mapeamento manual. `Solfacil-POC` não é a Solfacil.

**Valores inválidos conhecidos.** COMPANIES_HISTORIC e as abas de cobertura do relatório têm datas impossíveis em algumas linhas (ano 1000, 1986, 2027); desconsidere ao calcular.

## Como manter este arquivo

Quando o usuário apresentar uma nova aba, coluna ou regra, ou corrigir algo aqui, atualize o arquivo na mesma conversa. Registre a data da decisão e o motivo. Não copie dados pessoais para cá.
