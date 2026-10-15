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
| Legado | [PROJETO] Health Score | https://docs.google.com/spreadsheets/d/1SL5uLyBEpyVua9yExkw2tv3XHgTn12lAQIZyISjZPWw | Health Score antigo; ainda alimenta as colunas HealthScore, Adoção, Configuração e Engajamento da CARTEIRA do AM/TAM |

Fluxo geral: a CARTEIRA do INTERNO é um `IMPORTRANGE` da aba `carteira` do AM/TAM. A MATRIZ DE HEALTH SCORE importa as notas por métrica do INTERNO (tabelas `healthscore` e `hsbruto`) e aplica os pesos; o fluxo completo está em "Health Score: como o cálculo flui". O FINANCEIRO é a fonte de cobrança (faturas e contratos); o número de funcionários da carteira vem da FATURA (coluna Funcionários, sem parceiros).

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
- **FAIXAS HS**: faixas de pontuação das métricas A09 (Desligados com acesso) e A10 (Desligados que acessaram) do HEALTHSCORE (limite em % dos funcionários e pontos). O bloco de e-mail pessoal ficou sem uso desde 15/10/2026. Nas colunas J e K fica a faixa da C06 (Conexões diretas), em que mais é melhor.
- **COMPANIES**: uma linha por empresa (compliance, passo de onboarding, organograma, autorização, SSO, feature flags, funcionários, suporte).
- **COMPANIES_HISTORIC**: snapshot por empresa por data (`Data Execução` é data real). `Funcionários` traz um JSON por status; `#Funcionários` soma sem FIRED; `Hired`, `Absence` e `Fired` vêm separados, com os respectivos deltas.
- **COBERTURA**: Data, Empresa, Ação, Tipo, Movimentações, Disparos, Rejeitados, Aguardando aprovação, Sem disparo, Sucesso. Tem as mesmas colunas da "Base cobertura diária" do relatório AM/CX (confirmar se é espelho; `metricas-cobertura/` neste repositório calcula a partir das abas de cobertura).
- **LOGINS**: acessos por usuário e empresa, com últimos 30 dias, dias sem acesso e perfil.
- **INFO**: `IMPORTRANGE` da INFO do AM/TAM (fonte única, ver "INFO única no AM/TAM").
- **COMPLIANCE**, **CONTRATOS**, **USERS**, **GRUPOS**, **CONEXÕES DIRETAS**, **APOIO**, **HEALTHSCORE**, **HS COMPLETO**, **GROUPS**.

## HEALTHSCORE ([NIUCO] MATRIZ DE HEALTH SCORE)

- **Métricas**: dicionário dos critérios. Adoção: A01 Login Frequência (logins únicos/22), A02 a A05 eficiência de workflow (onboarding, offboarding, absence, move; média de sucesso dos últimos 30 dias), A06 e A07 cobertura de onboarding e offboarding, A08 providers homologados, A09 desligados com acesso, A10 desligados que acessaram (faixas de proporção desde 09/10/2026), A11 eficiência pré-folha. A antiga A09 (e-mail pessoal) foi excluída em 15/10/2026 e os códigos foram renumerados. Configuração: C01 a C06. Engajamento: E01 (satisfação DM/EB, do HAPPYSCORE). A linha E02 (NPS) não existe na aba em 09/10/2026, embora Pesos, Categorias e Consolidado tenham E02 (ver "Problemas conhecidos").
- **Pesos** e **Categorias**: peso de cada critério por plano (FinOPs, Sec Automation, Identity Managment, Ultimate, Sec Automation Gran) e por categoria.
- **Matriz**, **Details**, **Consolidado**, **Tendência** (semanal): pontuação por empresa, `HealthScore` e `Health Score Ponderado`, com Adoção, Configuração e Engajamento.
- Ocultas: Fonte, Calculadora, Carteira.

## Health Score: como o cálculo flui

Mapeado em 09/10/2026 a partir das fórmulas.

1. **Ingestão (INTERNO).** Make grava as abas brutas: WORKFLOWS, LOGINS, COMPLIANCE, PROVIDERS (oculta), CONTRATOS, GROUPS, COMPANIES, COMPANIES_HISTORIC. COBERTURA e COBERTURA GRUPOS são `IMPORTRANGE` do relatório AM/CX; CARTEIRA é `IMPORTRANGE` do AM/TAM.
2. **Transformação (INTERNO).** WORKFLOWS calcula os deltas entre snapshots. SUCCESS RATE WORKFLOW (tabela `adoção_sr`) soma os deltas em janela de 31 dias para cada sexta da aba APOIO. SUCCESS RATE BOTTON (`srbotton`) faz o mesmo com Disparos e Sucesso da COBERTURA, só para o plano Sec Automation. ADOÇÃO SCORE (`scoreadocao`) junta eficiência e cobertura por semana; a cobertura é disparos ÷ movimentações numa janela de 30 dias que termina 7 dias antes da sexta. GRUPOS calcula a cobertura de grupos específicos a partir da COBERTURA GRUPOS.
3. **Nota por métrica (INTERNO, aba HEALTHSCORE, tabela `healthscore`).** Uma coluna por métrica, de 0 a 1. As empresas (A e B) são digitadas.
4. **HS Bruto (INTERNO, aba HS COMPLETO, tabela `hsbruto`).** Para cada métrica, `Bruto` (valor de origem) e `Máximo` (valor de Bruto que daria 100%), seguidos das notas.
5. **Ponderação (MATRIZ).** Fonte importa `healthscore`. Consolidado (tabela `metrics`) tira as empresas com Projeto = Implantação, calcula E01 (HAPPYSCORE mais recente ÷ 10) e E02 (NPS da CARTEIRA convertido para 0 a 1: (NPS ÷ 100 + 1) ÷ 2) e gera HealthScore (média simples), Health Score Ponderado (Pesos por plano) e Adoção, Configuração e Engajamento (Categorias). Matriz transpõe a HS COMPLETO com códigos digitados (A01B = bruto, A01M = máximo, A01 = nota). Details cruza métrica × empresa com Peso, Pontuação, Bruto e Máximo. Calculadora (oculta) é uma cópia do Consolidado para testes. Tendência guarda o Consolidado por semana, como valores fixos.
6. **Consumo (AM/TAM).** CONSOLIDADO importa a tabela `metrics` da MATRIZ. OKR AM KRA1 é a média do Health Score Ponderado; OKR TAM KRT1 e KRT2 são as médias de Configuração e Adoção. As colunas HealthScore, Adoção, Configuração e Engajamento da CARTEIRA não vêm da MATRIZ: vêm da planilha legada [PROJETO] Health Score, aba Tratadão proporcional.

| Código | Métrica | Nota (HEALTHSCORE) | Bruto / Máximo (HS COMPLETO) |
|---|---|---|---|
| A01 | Login frequência | maior % de acesso de um único usuário nos últimos 30 dias (dias únicos ÷ 22) | dias únicos do usuário mais ativo / 22 |
| A02 | Eficiência onboarding | Δ sucesso ÷ Δ iniciados de WORKFLOWS, últimos 30 dias (a partir de 16/04/2026) | Δ sucesso / Δ iniciados |
| A03 | Eficiência offboarding | ADOÇÃO SCORE da sexta mais recente (botão para Sec Automation, WORKFLOWS para os demais) | Sucessos / Iniciados OFFBOARD da sexta da nota (`srbotton` para Sec Automation, `adoção_sr` para os demais) |
| A04 | Eficiência absent | WORKFLOWS, a partir de 04/08/2026 | Δ sucesso / Δ iniciados |
| A05 | Eficiência move | WORKFLOWS | Δ sucesso / Δ iniciados |
| A06 | Cobertura onboarding | ADOÇÃO SCORE: disparos ÷ admissões | disparos ONBOARD / movimentações de Admissão da COBERTURA, na janela da nota (desde 14/10/2026) |
| A07 | Cobertura offboarding | ADOÇÃO SCORE: disparos ÷ demissões | disparos OFFBOARD / movimentações de Demissão da COBERTURA, na janela da nota (desde 14/10/2026) |
| A08 | Providers homologados | homologados ÷ fornecedores | homologados / fornecedores |
| A09 | Desligados com acesso | faixas da FAIXAS HS | infratores / teto de infratores para 100% |
| A10 | Desligados que acessaram | faixas da FAIXAS HS | infratores / teto (0) |
| A11 | Eficiência pré-folha | sucesso ÷ iniciados de WORKFLOWS do tipo IDENTITY_SCREENING, últimos 30 dias (a partir de 16/04/2026), mesma regra da A05 | Δ sucesso / Δ iniciados (colunas BD a BF da HS COMPLETO; códigos A11, A11B e A11M na Matriz) |
| C01 | Configuração de workflow | IGA/Ultimate: (Onboard + Offboard + Move + bônus) ÷ 4; SAG: tem offboard ÷ 1 | pontos / 4 (1 nos planos SAG) |
| C02 | Cobertura de grupos | GRUPOS: pessoas na folha em grupo específico ÷ pessoas na folha | Com grupo específico / Pessoas na folha (GRUPOS) |
| C03 | Organograma | digitado à mão | nota da HEALTHSCORE / 1 |
| C04 | Contratos ativos | contratos ativos ÷ conexões NoShadow, sem teto | ativos / NoShadow |
| C05 | Gastos cadastrados | ativos com gasto ÷ conexões NoShadow | ativos com gasto / NoShadow |
| C06 | Conexões diretas | quantidade de conexões diretas (PROVIDERS), por faixas da FAIXAS HS (versão de 15/10/2026, à tarde) | conexões diretas / 31 (a quantidade que dá 100%) |
| E01 | Satisfação DM/EB | fixa em 30% para todas as empresas (Consolidado da MATRIZ) | 3 / 10 fixo (colunas BA a BC) |
| E02 | NPS | removida em 14/10/2026 | removida |
| BON1 | Bônus Portal | eficiência × volumetria das solicitações no portal, 30 dias (aba PORTAL) | positivas / concluídas com resultado (colunas BG a BI) |
| BON2 | Bônus API | eficiência × volumetria das chamadas à Niuco API, 30 dias (aba API) | chamadas 2xx / total de chamadas (colunas BJ a BL) |

**Semântica da HS Bruto.** `Máximo` é o valor de `Bruto` que levaria a nota a 100%. Nas métricas em que mais é melhor, é o denominador (exemplo: A08, homologados / fornecedores). Em A09 e A10 (códigos atuais), em que menos é melhor, é o teto de infratores para ficar na faixa de 100%: arredondar para baixo (limite da faixa de 100% × funcionários da CARTEIRA). Nesses dois, o desvio é `Bruto - Máximo` (quantos infratores precisam sair); nos demais, `Máximo - Bruto`. Atualizado em 09/10/2026: antes, o Máximo de A09, A10 e A11 era 0 digitado.

### Problemas conhecidos (09/10/2026)

- **Health Score sem erro desde 14/10/2026.** Antes, o Consolidado ficava em `#N/A` por dois motivos: lia a coluna E02, que a aba Métricas não tem, e os planos novos da carteira não existiam em Pesos e Categorias. Os dois foram corrigidos (ver "Planos novos em Pesos e Categorias"). A Tendência tem valores sem erro até 02/10/2026; a semana de 09/10 pode ter sido gravada com erro.
- **Bruto de C05 no Details:** corrigido em 15/10/2026. A Matriz usava o código `C05N` no lugar de `C05B`.
- **Métrica vazia vale 0 no ponderado.** Exemplo: sem NPS, uma empresa Sec Automation perde os 5 pontos de E02; Malga e G4 Educação ficam com cerca de metade do peso vazio.
- **C04 sem teto** (Malga 104%).
- **Status de projeto:** resolvido em 14/10/2026. Agora há uma fonte única, a INFO do AM/TAM (ver "INFO única no AM/TAM").
- **Dois Health Scores em produção:** a CARTEIRA mostra o legado; os OKRs usam a MATRIZ. No legado, DOT Digital Group, G4 Educação e Blip ficam sem HS na CARTEIRA (nome diferente ou empresa ausente).

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

**HS Bruto de A06 e A07 = disparos e movimentações da COBERTURA (aplicado em 14/10/2026).** Antes, o Bruto de A06 e A07 na HS COMPLETO do INTERNO era cópia do Bruto de A02 e A03 (sucessos de WORKFLOWS) e o Máximo dava `#REF!`. Agora as colunas O a R usam a mesma conta da nota no ADOÇÃO SCORE: pegam a sexta mais recente com cobertura preenchida, montam a janela de 30 dias que termina 7 dias antes dela e somam na tabela `cobertura`. Bruto é `Disparos` com Tipo ONBOARD ou OFFBOARD; Máximo é `Movimentações` com Ação Admissão ou Demissão. Quando a nota está em branco, Bruto e Máximo também ficam em branco. Conferido em 14/10/2026: Bruto ÷ Máximo reproduz a nota nas 7 empresas com cobertura (exemplos: Gupy 9/12 = 75%, Blip 24/27 = 88,89%, Hubla offboarding 4/5 = 80%), e os códigos A06B, A06M, A07B e A07M chegam à Matriz. O desvio é `Máximo - Bruto`, ou seja, as movimentações que ficaram sem disparo.

**HS Bruto alinhado à nota em A03, C01, C02, C03, E01 e E02 (aplicado em 14/10/2026).** Na HS COMPLETO do INTERNO, Bruto ÷ Máximo passou a reproduzir a nota em todas as métricas (em C01, com teto de 100%). Quando a nota está em branco, Bruto e Máximo também ficam.
- A03: soma Sucessos e Iniciados OFFBOARD na sexta mais recente usada pela nota, em `srbotton` para Sec Automation e em `adoção_sr` para os demais planos. Antes somava WORKFLOWS dos últimos 30 dias a partir de hoje, uma janela diferente da nota.
- C01: ver "C01 dividido por 4" abaixo.
- C02: Bruto é `Com grupo específico` e Máximo é `Pessoas na folha` da aba GRUPOS. Antes contava workflows de onboarding com grupo e grupos da empresa. A busca é pelo nome. Desde 14/10/2026, a G4 é normalizada na importação e aparece como G4 Educação.
- C03: Bruto lê a nota da HEALTHSCORE e Máximo é 1. O Bruto digitado antes estava desalinhado da nota em 8 empresas, provavelmente deslocado de linha.
- E01 e E02: ver "Engajamento só com E01" abaixo.

**C01, Configuração de workflow (decisão de 14/10/2026).** Conta os tipos de workflow configurados, ou seja, com pelo menos um workflow na aba WORKFLOWS do INTERNO. Hoje todos os workflows de lá estão ENABLED.
- **IGA e Ultimate (Máximo 4):** 1 ponto para cada tipo entre Onboard, Offboard e Move. Mais 1 ponto de bônus se a empresa tiver Férias e Afastamento (`ABSENT`) ou Pré-folha (`IDENTITY_SCREENING`). O bônus vale no máximo 1: é bom ter pelo menos um dos dois.
- **SAG (Máximo 1):** o SAG tem direito a desligar pessoas pelo botão de offboard. Vale 100% se a empresa tiver workflow OFFBOARD ou algum disparo de Offboard na COBERTURA (botão), e 0% se não tiver.
- **Empresa sem nenhum workflow:** fica com 0%, e não mais em branco.
- **Onde está a regra:** coluna `Configuração WorKflow` da HEALTHSCORE e colunas Y e Z (Bruto e Máximo) da HS COMPLETO, desde 15/10/2026, ambas no INTERNO, além da descrição na aba Métricas da MATRIZ.
- **Valores em 14/10/2026:** Blip 4/4. Gupy, Contabilizei e LG 3/4. Malga, G4 e Hubla 2/4. Sympla 0/4. Entre os SAG, Gran Cursos, Mercado Bitcoin e SolFacil 1/1; os demais 0/1.
- **C01 no SAG Advanced (14/10/2026):** o C01 passou a contar no SAG Advanced. Na aba Métricas, C01 ficou TRUE na coluna Sec Automation, que também define o conjunto de métricas do SAG Advanced e do SAG Essentials. Em Pesos, a linha SAG Advanced ganhou 8% de C01, tirados da própria Configuração, que continua com 34% no total: C03 e C04 foram de 9% para 7%, e C05 e C06 de 8% para 6%. Adoção (49%) e Engajamento (17%) não mudaram. A linha antiga Sec Automation ficou sem peso de C01.

**Engajamento só com E01 (decisão de 14/10/2026).** No desenho novo, o Engajamento tem uma nota só: E01, Satisfação DM/EB. O E02 (NPS) saiu do Health Score. Como ainda não há nenhuma nota de satisfação, o E01 fica em 30% (3 de 10) para todas as empresas até a regra ser definida.
- **Consolidado da MATRIZ:** E01 = 0,3 fixo; a fórmula antiga, com o HAPPYSCORE mais recente ÷ 10, está no histórico de versões. A coluna E02 ficou vazia, sem fórmula; a coluna foi mantida para não deslocar o CONSOLIDADO do AM/TAM nem a Tendência. HealthScore e Health Score Ponderado leem E:V, e os Pesos C:T. Engajamento lê só V e Categorias T.
- **Pesos:** o peso do E02 foi somado ao E01 e a coluna E02 ficou vazia. FinOPs 21%, Sec Automation 17%, Identity Managment 9%, Ultimate 5%, Sec Automation Gran 15%. O total de cada plano continua 100%.
- **HS COMPLETO do INTERNO:** E01 = 3 / 10 para todas as empresas, por fórmula. As colunas do E02 foram apagadas, e a Matriz voltou a terminar em E01M (linha 55).
- **Resultado em 14/10/2026:** HealthScore, Ponderado e as três categorias calculam para todas as empresas, depois da inclusão dos planos novos.

**Planos novos em Pesos e Categorias (14/10/2026).** A carteira passou a usar os planos novos. O catálogo completo é o campo **Plano** do negócio no HubSpot (`plano`): SAG Essentials, SAG Advanced, IGA Essentials, IGA Advanced e Ultimate (valor interno `identity_plataform`), além dos antigos Sec Automation (`saas_asset_management`), FinOps e Identity Managment (`idm`). A coluna Plano ID da CARTEIRA do AM/TAM traz esse valor interno, e a aba INFO do AM/TAM traduz para o nome e o produto. O ID de cada linha da CARTEIRA é o ID do negócio no HubSpot, não o da empresa. A relação antigo → novo está na planilha "De-Para | Planos & Hubspot" (aba Theusview, https://docs.google.com/spreadsheets/d/1DuvD0r07yy7OGbjLuK_jJo_lbcJZiGBhnZDD0pamp9Y):

| Plano antigo | Plano novo | Produto novo |
|---|---|---|
| Sec Automation | SAG Advanced | Software Access Governance |
| Identity Managment | IGA Essentials | Identity Governance |
| Ultimate | Ultimate | Identity Platform |

- **Pesos e Categorias da MATRIZ:** ganharam as linhas SAG Advanced e IGA Essentials, com os mesmos pesos dos planos antigos correspondentes. Os pesos foram copiados como valores; a Categorias usa a mesma fórmula das outras linhas. As linhas antigas foram mantidas.
- **Consolidado:** HealthScore, Ponderado, Adoção, Configuração e Engajamento leem as linhas 2 a 8 de Pesos e Categorias. Os planos novos usam o conjunto de métricas do plano antigo, ou seja, as colunas Sec Automation e Identity Managment da aba Métricas.
- **Gran Cursos:** era Sec Automation Gran e virou SAG Advanced, então usa os pesos de Sec Automation. A linha Sec Automation Gran ficou sem uso.
- **Malga:** passou de Ultimate para IGA Essentials em 14/10/2026, conforme o De-Para. A mudança foi feita no negócio Malga do HubSpot (ID 44566937104): campo Plano = IGA Essentials e Produto contratado = IGA (valor interno `IDM`). Também foi feita na coluna Plano ID da CARTEIRA do AM/TAM, que alimenta as outras planilhas.
- **Planos sem empresa:** SAG Essentials e IGA Advanced também foram cadastrados em Pesos e Categorias, com os pesos em branco até a definição. As fórmulas dessas linhas usam IFERROR para não mostrar erro. No Consolidado, SAG Essentials usa o conjunto de métricas do Sec Automation e IGA Advanced o do Identity Managment, até a aba Métricas ganhar colunas próprias.
- **C01 nos planos SAG:** a regra de ÷ 1 não afeta a nota final hoje, porque C01 não faz parte do conjunto de métricas do Sec Automation (peso vazio).

**Empresas em implantação fora do Health Score (corrigido em 14/10/2026).** A regra é que empresas com Projeto = Implantação não entram no Consolidado da MATRIZ. O filtro estava quebrado: quando a coluna Satisfação DM/EB entrou na HEALTHSCORE do INTERNO, o Projeto passou da coluna W para a X na aba Fonte, mas o Consolidado continuou filtrando a W (Adoção Automação, sempre vazia). Com isso, nenhuma empresa era excluída. Agora o Consolidado filtra `Fonte!X2:X<>"Implantação"`, e os cabeçalhos V, W e X da Fonte foram corrigidos. Na mesma data, Hubla e Sympla foram marcadas como Implantação na aba INFO do INTERNO (estavam como Ativado). O Consolidado passou de 16 para 14 empresas, e os OKRs do AM/TAM que fazem média dele também mudam.

**G4 Educação na COBERTURA e na COBERTURA GRUPOS (corrigido em 14/10/2026).** O relatório AM/CX (Relatórios AM/CX 2026.Q3) traz o nome da plataforma, "G4". As abas COBERTURA e COBERTURA GRUPOS do INTERNO agora trocam "G4" por "G4 Educação" na importação, dentro do `IMPORTRANGE`. Não dá para trocar no relatório, porque a próxima carga sobrescreveria. Com isso, GRUPOS, ADOÇÃO SCORE e o botão de offboard do C01 enxergam a G4: o C02 dela passou a 100% (572/572). O A06 dela continua vazio porque a G4 não tem linhas de cobertura depois de 21/07/2026. Para outro nome divergente, como Grancursos, é só acrescentar a troca nessas duas fórmulas.

**INFO única no AM/TAM (14/10/2026).** As três abas INFO foram concentradas em uma só, no mesmo modelo da CARTEIRA:
- **Fonte:** a aba INFO do [AM/TAM] DATABASE (tabela `INFO`, colunas ID, Chave 1, Chave 2) é a única onde se edita. Nenhum cenário do Make escreve em INFO; é tudo digitado.
- **Conteúdo:** as linhas que existiam só no INTERNO (usuários da plataforma por UUID e status de projeto por empresa) foram copiadas, como valores, para as linhas 142 a 326 da INFO do AM/TAM. Não há colisão: o AM/TAM busca por ID (código de fase, plano, ID de usuário do HubSpot e e-mail), e o INTERNO busca por Chave 1 (e-mail do usuário ou nome da empresa).
- **INFO do INTERNO:** é `IMPORTRANGE` da tabela `INFO` do AM/TAM, em A2. A tabela `info` e as buscas `info[Chave 1]` → `info[Chave 2]` (Projeto na HEALTHSCORE, ADOÇÃO SCORE, WORKFLOWS) continuam iguais.
- **Info da MATRIZ (Chave, Valor):** é `IMPORTRANGE` da INFO do AM/TAM filtrado pelas linhas de status (Chave 2 = Ativado, Implantação, Perdido ou POC). Ela alimenta a Tendência.
- **Status de projeto por empresa:** edite na INFO do AM/TAM, na linha em que Chave 1 é o nome da empresa e Chave 2 é o status. Empresa com Implantação sai do Consolidado.
- **Divergência resolvida:** a MATRIZ tinha DOT Digital Group como Implantação e o INTERNO como Perdido; ficou Perdido.

**Catálogo de planos (aplicado em 14/10/2026).** No HubSpot, o produto é SAG ou IGA, e os planos são subcategorias deles. O Ultimate tem os dois produtos (SAG, IGA). O nome dos planos agora fica em um lugar só.

- **Fonte:** aba CATÁLOGO PLANOS do AM/TAM, tabela `planos_catalogo`.
  - Colunas digitadas: **Plano ID** (valor interno do campo Plano do negócio no HubSpot), **Plano** (nome exibido), **Produto** (SAG, IGA ou SAG, IGA) e **Ativo**.
  - Colunas calculadas a partir do Produto: Tem SAG, Tem IGA, Divisor C01 (4 se tem IGA, 1 se não tem) e Usa botão offboard (Sim se tem SAG e não tem IGA).
  - Não confundir com a aba PLANOS do AM/TAM, que é gravada pelo Make a partir do ClickUp.
- **Chave:** tudo se liga pelo Plano ID. Todos os planos novos têm ID igual ao nome, menos o Ultimate (`identity_plataform`). O Plano ID não muda.
- **Cópias do catálogo:** a aba CATÁLOGO PLANOS do INTERNO (tabela `planos`) e a aba Catálogo Planos da MATRIZ (tabela `planos`) são `IMPORTRANGE` do catálogo.
- **CARTEIRA do AM/TAM:** Plano e Produto (colunas T e U) vêm do catálogo pelo Plano ID (coluna X). O Produto passou a aparecer como SAG, IGA ou SAG, IGA. As linhas de plano da INFO foram apagadas.
- **INTERNO:** nenhuma fórmula tem nome de plano escrito. As regras consultam o catálogo:
  - C01 na HEALTHSCORE e na HS COMPLETO (colunas Y e Z desde 15/10/2026);
  - A06 na HEALTHSCORE;
  - A03 Bruto e Máximo na HS COMPLETO (colunas I e J);
  - ADOÇÃO SCORE (colunas D, F, H e Q);
  - SUCCESS RATE BOTTON (coluna D).
- **MATRIZ:**
  - **Métricas:** uma coluna TRUE/FALSE por Plano ID: SAG Essentials, SAG Advanced, IGA Essentials, IGA Advanced e identity_plataform. SAG Essentials copiou o conjunto do SAG Advanced, e IGA Advanced copiou o do IGA Essentials.
  - **Pesos e Categorias:** a coluna A é o Plano ID. A linha Sec Automation Gran e as linhas dos planos antigos foram apagadas.
  - **Consolidado:** HealthScore, Health Score Ponderado, Adoção, Configuração e Engajamento usam uma fórmula genérica. Ela pega o Plano ID da empresa no catálogo, usa a coluna desse ID na Métricas e aplica a linha desse ID em Pesos ou Categorias. A Calculadora usa a mesma fórmula, e a coluna Peso do Details também busca pelo Plano ID.
- **Para renomear um plano:** altere a coluna Plano no catálogo do AM/TAM.
- **Para criar um plano:** são três passos:
  1. Uma linha no catálogo, com o Plano ID do HubSpot.
  2. Uma coluna com esse ID na aba Métricas.
  3. Uma linha com esse ID em Pesos e outra em Categorias.
- **Bugs corrigidos junto:**
  - **Botão de offboard:** desde a troca de Sec Automation para SAG Advanced, a SUCCESS RATE BOTTON estava vazia, e o ADOÇÃO SCORE tratava as empresas SAG como workflow. Agora o offboard das SAG volta a vir do botão. A03 e A07 mudaram em SolFacil, Mercado Bitcoin e Gran Cursos, sem efeito no Consolidado, porque essas métricas não pesam no SAG.
  - **Nome da Gran Cursos:** "Grancursos" virou "Gran Cursos" na importação da COBERTURA e da COBERTURA GRUPOS, do mesmo jeito que a G4.
- **Mudança de resultado:** o HealthScore simples do Ultimate passou a respeitar a aba Métricas, onde A04 e A05 estão FALSE. Antes, a fórmula usava todas as métricas para o Ultimate. Contabilizei foi de 68,51% para 66,56%, e Blip de 66,40% para 62,20%. O Ponderado e as categorias não mudaram.
- **E02:** a coluna E02 foi apagada do Consolidado em 14/10/2026. Pesos e Categorias ainda têm a coluna E02 vazia.

**OKRs lendo a coluna errada (corrigido em 14/10/2026).** O CONSOLIDADO do AM/TAM importava a tabela `metrics` da MATRIZ por posição, mas tinha os cabeçalhos digitados. Quando o E02 foi apagado da MATRIZ, as colunas da direita andaram uma posição. Com isso:
- KRA1 (Health Score Ponderado) mostrava a média da Adoção.
- KRT1 (Configuração) mostrava a média do Engajamento.
- KRT2 (Adoção) mostrava a média da Configuração.

Agora o A2 do CONSOLIDADO importa `Consolidado!A1:AZ1000` com o cabeçalho e escolhe cada coluna pelo nome do cabeçalho do próprio CONSOLIDADO. Coluna que não existe na MATRIZ, como o E02, fica em branco. Valores corrigidos em 14/10: KRA1 50,79%, KRT1 56,43% e KRT2 52,13%. Lição: no Sheets não existem `DROP` nem `XMATCH`, e o `LET` não aceita nome de variável que pareça endereço de célula (`b2`) ou que repita nome de tabela (`pesos`).

**A12, Eficiência Workflow Pré-folha (criada em 14/10/2026; hoje A11).** Mede o sucesso dos workflows de pré-folha (`IDENTITY_SCREENING`), com a mesma regra da A05 (Move).
- **Métricas:** categoria Adoção. TRUE em IGA Essentials, IGA Advanced e identity_plataform; FALSE nos planos SAG, que não têm pré-folha.
- **Peso:** 2% no IGA Essentials e no Ultimate, tirados de A02 e A03 (1 ponto de cada). O total da Adoção não muda. Critério: pré-folha é bônus de IGA, da família de eficiência de workflow. SAG fica com 0%. Os pesos de IGA Advanced continuam em aberto.
- **Efeito no Ponderado:**

  | Empresa | Antes | Depois | Motivo |
  |---|---|---|---|
  | Gupy | 77,54% | 77,59% | A12 = 100% |
  | Blip | 76,37% | 76,45% | A12 = 95,65% |
  | Contabilizei | 75,62% | 74,04% | sem pré-folha, a A12 vazia conta como 0 |
  | LG | 74,16% | 72,42% | sem pré-folha, a A12 vazia conta como 0 |

  KRA1 foi para 50,56%. O "vale 0 quando vazio" é a regra de métrica vazia, que está em aberto no ClickUp.
- **A04 e A05:** em 14/10/2026, o usuário marcou A04 (Férias/Afastamento) e A05 (Move) como TRUE para IGA e Ultimate na aba Métricas. Elas entram no HealthScore simples, mas continuam com peso 0.

**Como adicionar uma métrica nova (roteiro usado na A12, hoje A11).**
1. **INTERNO, HEALTHSCORE:** inserir a coluna da nota no lugar certo da ordem (a A12 ficou depois da A11). A tabela cresce sozinha, e as referências de outras fórmulas se ajustam.
2. **INTERNO, HS COMPLETO:** acrescentar nota, Bruto e Máximo **no fim da tabela** (colunas novas depois de BF, em 15/10/2026), para não deslocar a Matriz.
3. **MATRIZ, Fonte:** corrigir os cabeçalhos, que andam uma coluna (hoje Projeto está na X).
4. **MATRIZ, Consolidado:** inserir a coluna com o código da métrica na mesma posição e ajustar o filtro do A2 (hoje `filter(Fonte!A2:U;Fonte!B2:B<>"";Fonte!X2:X<>"Implantação")`). As fórmulas genéricas se ajustam sozinhas.
5. **MATRIZ, Métricas:** inserir a linha da métrica (ID, critério, categoria, cálculo e TRUE/FALSE por plano).
6. **MATRIZ, Pesos:** inserir a coluna e redistribuir os pesos, para cada plano somar 100%. Categorias: inserir a coluna e só escrever o cabeçalho. A fórmula de cada linha descobre a categoria pela aba Métricas.
7. **MATRIZ, Matriz:** cadastrar os códigos (`X`, `XB`, `XM`) nas linhas que o `TRANSPOSE` da HS COMPLETO ocupa e estender a tabela `matriz`. A aba Details se monta sozinha.
8. **MATRIZ, Tendência:** inserir a coluna (histórico em branco).
9. **AM/TAM, CONSOLIDADO:** inserir a coluna com o mesmo cabeçalho. O import busca pelo nome.
10. **Conferir:** HealthScore e Ponderado antes e depois, e os OKRs do AM/TAM.

**A09 fora do Health Score (15/10/2026).** "Usuários com E-mail pessoal" saiu de todos os cálculos. Na aba Métricas ela está FALSE para todos os planos, e em Pesos não tem peso. No mesmo dia, a métrica foi excluída de vez (ver "A09 excluída e códigos renumerados" abaixo).

**Pesos e Categorias à prova de reorganização (15/10/2026).** Em 15/10, a aba Pesos foi reorganizada: linhas em outra ordem, coluna E02 apagada, colunas de soma Adoção, Configuração e Engajamento acrescentadas, pesos novos. Isso quebrou duas coisas:
- A busca do Ponderado tinha virado `Pesos!$A$6:$A$30` quando as linhas mudaram de lugar, e só achava o identity_plataform. As outras empresas ficaram com Ponderado 0%.
- As fórmulas da Categorias ficaram com largura diferente da Pesos e deram `#VALUE!`. Adoção, Configuração e Engajamento ficaram em 0%.

Agora, Ponderado, categorias, a aba Categorias e o Peso do Details buscam a linha do plano pela coluna inteira (`Pesos!$A:$A` → `Pesos!$A:$AD`) e o peso pelo nome da métrica no cabeçalho (`Pesos!$A$1:$AD$1`). Mover linhas, inserir colunas ou acrescentar colunas de soma não quebra mais. A Categorias perdeu a coluna E02 e busca o plano pelo Plano ID da própria linha. Pesos e Categorias foram alargadas até a coluna AD.

Regra de consistência: peso em métrica com FALSE na aba Métricas é ignorado. Em 15/10, o IGA Advanced tinha 4% em A08 com A08 FALSE, ou seja, somava 96% na prática. Não afeta ninguém, porque nenhuma empresa está nesse plano.

Valores em 15/10/2026, com os pesos novos e sem a A09: KRA1 47%, KRT1 58,66%, KRT2 47,49%.

**Textos da aba Métricas revisados (15/10/2026).** As colunas Cálculo e Observação foram reescritas a partir das fórmulas reais:
- A06 e A07: disparos ÷ admissões ou demissões da COBERTURA. Antes falavam em "Delta Fired/Hired".
- E-mail pessoal, Desligados com acesso e Desligados que acessaram: faixas da FAIXAS HS. Antes falavam em "percentil".
- C02: pessoas na folha em grupo específico.
- E01: fixa em 30%.

O critério E01 passou a se chamar "Satisfação DM/EB" (antes "DB/EB").

**A09 excluída e códigos renumerados (15/10/2026).** A métrica "Usuários com E-mail pessoal" foi apagada de todas as abas, e as métricas seguintes subiram um código:

| Antes | Depois | Métrica |
|---|---|---|
| A09 | (apagada) | Usuários com E-mail pessoal |
| A10 | A09 | Desligados com Acesso |
| A11 | A10 | Desligados que acessaram |
| A12 | A11 | Eficiência Workflow Pré-folha |

- **INTERNO:** a coluna da nota saiu da HEALTHSCORE. Na HS COMPLETO saíram a nota e o Bruto e o Máximo (antigas U e V); C01 Bruto e Máximo ficaram em Y e Z, E01 em BA a BC e pré-folha em BD a BF.
- **MATRIZ:**
  - Fonte: cabeçalhos refeitos; Projeto está na X.
  - Consolidado: coluna apagada e filtro do A2 = `filter(Fonte!A2:U;Fonte!B2:B<>"";Fonte!X2:X<>"Implantação")`.
  - Métricas: linha apagada e IDs renumerados.
  - Pesos, Categorias e Tendência: coluna apagada e cabeçalhos renumerados.
  - Matriz: códigos A2:A55 reescritos (tabela `matriz` com 55 linhas). O `C05N` virou `C05B`, e o Bruto de C05 passou a chegar ao Details.
- **AM/TAM:** coluna apagada do CONSOLIDADO, cabeçalhos renumerados. O import busca pelo nome, então nada mais mudou.
- **Tendência:** o histórico do e-mail pessoal foi perdido junto com a coluna. Nas semanas anteriores a 15/10, as colunas A09 e A10 já guardam Desligados com acesso e Desligados que acessaram (o rótulo mudou, o dado não).
- **Conferido em 15/10/2026:** HealthScore, Ponderado e categorias iguais aos de antes (Bionexo 38,56% / 29,74%, Gupy 78,25% / 64,03%, Blip 69,42% / 71,31%). OKRs iguais: KRA1 47%, KRT1 58,66%, KRT2 47,49%.
- **Fora do escopo:** a Calculadora (oculta) não foi atualizada, e o bloco de e-mail pessoal da FAIXAS HS ficou sem uso.

**C06, Conexões diretas, por faixas (15/10/2026).** A C06 deixou de usar percentil entre as empresas, que mudava a nota de uma empresa quando as outras mudavam. Agora a nota vem da proporção Conexões Diretas ÷ Fornecedores Homologados da aba PROVIDERS do INTERNO, limitada a 100%. A proporção vira pontos pelas faixas das colunas J e K da FAIXAS HS. Cada faixa vale a partir do limite, inclusive.

| Proporção | Pontos |
|---|---|
| 60% ou mais | 100% |
| 40% ou mais | 80% |
| 25% ou mais | 60% |
| 15% ou mais | 40% |
| 8% ou mais | 20% |
| menos de 8% | 0% |

- **Por que homologados:** com Conexões NoShadow no denominador, Gupy, Contabilizei e G4 tiravam 100%, porque não têm cadastro manual. Com homologados, a Gupy cai para 44%. Contabilizei, G4 e Malga continuam em 100%, porque só homologaram o que veio pela conexão direta; elas já perdem na A08.
- **Faixa:** escolhida pela distribuição dos homologados, em que metade das empresas fica entre 5% e 30%.
- **HS COMPLETO:** Bruto = conexões diretas (coluna AI) e Máximo = fornecedores homologados (coluna AJ), que antes ficava vazio.
- **Métricas:** o Cálculo tem as faixas e um exemplo: Blip tem 21 diretas e 74 homologados, 28,4%, nota 60%.
- **Notas em 15/10/2026, antes da correção do Make (ver abaixo):**
  - 100%: Contabilizei, Superlogica, Malga, G4 e Jusbrasil.
  - 80%: Gupy.
  - 60%: Mercado Bitcoin, Blip, Hubla e Sympla.
  - 40%: Gran Cursos e LG.
  - 20%: SolFacil e OLX.
  - 0%: Bionexo e Ebanx.
- **OKRs:** KRA1 foi de 47% para 47,42% e KRT1 de 58,66% para 60,8%. KRT2 ficou em 47,49%.

**Conexões Diretas da PROVIDERS corrigida no Make (15/10/2026).** A PROVIDERS do INTERNO é gravada pelo cenário "[BackOffice -> Sheets] Providers" (Make 4513382), em dias úteis às 06:00. Ele lê `GET /companies/{id}/providers` do BackOffice. A variável `conexoes_diretas` (módulo 16) conta os providers cuja `source` não está numa lista de exclusão.
- **Bug:** quase todos os itens `sso-google-<cliente>` da lista começavam com espaço (`" sso-google-mb"`). Por isso, não removiam nada, e os apps vistos pelo SSO Google contavam como conexão direta.
- **Correção:** os espaços foram tirados. Também entraram `jumpcloud` (por decisão, JumpCloud é SSO e não conexão direta) e `sso-google-blip.ai`, que faltava.
- **Regra:** conexão direta é um provider com conector próprio (sem `source`, como GitHub, Slack, Microsoft 365, AWS IAM e HubSpot) ou vindo de um conector de SaaS (`atlassian`, `gsuite-<cliente>`, `conector-adobe`). Não contam: `manual`, `compliance-*`, `sso-*` e `jumpcloud`.
- **Cliente novo com SSO Google:** a fonte `sso-google-<nome>` precisa entrar na lista. Sem isso, os apps do SSO contam como diretos. Para conferir, use a coluna Conexões da PROVIDERS, que lista as fontes de cada empresa.
- **Conferido no Mercado Bitcoin:** de 419 providers, ficaram 25 sem fonte, 12 `atlassian` e 3 `gsuite-mb`, total 40 (antes 81). Saíram 32 `jumpcloud` e 9 `sso-google-mb`.
- **Mudanças nas conexões diretas:**
  - Mercado Bitcoin: 81 → 40.
  - Contabilizei: 54 → 16.
  - Superlogica: 51 → 25.
  - Jusbrasil: 40 → 25.
  - Gupy: 27 → 18.
  - G4: 28 → 23.
  - Malga: 20 → 18.
  - Hubla: 20 → 17.
  - Blip: 21 → 20.
- **Efeito na C06:**
  - Mercado Bitcoin: 60% → 20%.
  - Contabilizei: 100% → 60%.
  - Gupy: 80% → 60%.
  - Superlogica: 100% → 80%.
  - Jusbrasil: 100% → 80%.
- **OKRs:** KRA1 foi de 47,42% para 46,9% e KRT1 de 60,8% para 58,16%.

**C06 por quantidade absoluta (15/10/2026, versão atual).** Depois da correção do Make, a C06 deixou de ser proporção e passou a usar a quantidade de conexões diretas. A faixa escolhida foi a proposta A, em degraus de 5. Ela fica nas colunas J e K da FAIXAS HS, e cada faixa vale a partir da quantidade indicada:

| Conexões diretas | Pontos |
|---|---|
| 0 a 5 | 15% |
| 6 a 10 | 30% |
| 11 a 15 | 45% |
| 16 a 20 | 60% |
| 21 a 25 | 75% |
| 26 a 30 | 90% |
| 31 ou mais | 100% |

- **HEALTHSCORE:** `XLOOKUP(diretas; 'FAIXAS HS'!J2:J8; 'FAIXAS HS'!K2:K8; 0; -1)`.
- **HS COMPLETO:** Bruto = conexões diretas (coluna AI). Máximo = `MAX('FAIXAS HS'!J2:J8)` = 31, o início da faixa de 100% (coluna AJ, com formato numérico).
- **Métricas:** o Cálculo tem as faixas e o exemplo da Blip (20 conexões, nota 60%).
- **Notas:**
  - 100%: Mercado Bitcoin (40).
  - 90%: SolFacil (27), Gran Cursos (28) e Sympla (29).
  - 75%: Bionexo e OLX (21), G4 (23), Superlogica e Jusbrasil (25).
  - 60%: Contabilizei (16), Hubla (17), Gupy e Malga (18) e Blip (20).
  - 30%: Ebanx e LG (10).
- **OKRs:** KRA1 = 48,14%, KRT1 = 64,35% e KRT2 = 47,49%.
- **Limitação:** o número absoluto não considera o tamanho do parque. A Bionexo tem 21 diretas para 417 homologados e tira a mesma nota da OLX.
- **Versão anterior:** a proporção sobre os homologados, descrita acima, foi substituída.

**Categoria Bônus: BON1 (Portal) e BON2 (API) (15/10/2026).** São métricas de recursos específicos. Elas só somam: quem não usa o recurso não perde ponto.
- **Fonte:**
  - Abas "Solicitações no portal" e "Niuco API" do relatório Relatórios AM/CX (`1AEZzqHfqMGk2tgXYlke8SdiyB81wJ3tyZCAVKOza-Jk`), atualizadas semanalmente.
  - No INTERNO, elas são importadas por `IMPORTRANGE` nas abas **PORTAL** e **API**.
  - A ideia é trocar essa fonte por um banco de dados ligado direto ao Looker, quando houver acesso ao banco da empresa.
- **BON1 (Portal) = eficiência × volumetria,** últimos 30 dias pela Data de Abertura. As solicitações com Fonte = Importado ficam fora, porque são cargas em lote.
  - Eficiência = positivas (Conta criada, Acesso revogado, Conta atualizada, Com operação realizada) ÷ (positivas + negativas: Conta não criada, Acesso não revogado, Com operação não realizada).
  - Volumetria = solicitações ÷ Funcionários da CARTEIRA, pela faixa das colunas M e N da FAIXAS HS: a partir de 10% = 100%; 5% = 75%; 2% = 50%; acima de 0 = 25%.
- **BON2 (API) = eficiência × volumetria,** últimos 30 dias pela Última chamada de cada linha. A base é consolidada por chave, endpoint e status, então a janela é aproximada.
  - Eficiência = chamadas com HTTP 2xx ÷ total de chamadas da empresa.
  - Volumetria = chamadas com sucesso, pela faixa das colunas P e Q da FAIXAS HS: a partir de 4.000 = 100%; 2.000 = 75%; 400 = 50%; 1 = 25%.
  - Em 15/10/2026, os limites foram multiplicados por 4 (antes eram 1.000, 500, 100 e 1). Motivo: o uso da OLX se concentrou em uma semana, e um mês de uso naquele ritmo é o que deve valer 100%.
  - A empresa é localizada pelo nome exato. A LogComex aparece como "LogComex (company não encontrada na base)" e não casa com nenhuma empresa.
- **Sem uso na janela:** o bônus fica vazio.
- **INTERNO:**
  - HEALTHSCORE: colunas W (Bônus Portal) e X (Bônus API). Adoção Automação foi para Y e Projeto para Z.
  - HS COMPLETO: nota, Bruto e Máximo nas colunas BG a BL. A tabela `hsbruto` foi estendida.
- **MATRIZ:**
  - **Fonte:** cabeçalhos refeitos, com Projeto na Z. O filtro do Consolidado é `filter(Fonte!A2:U;Fonte!B2:B<>"";Fonte!Z2:Z<>"Implantação")`.
  - **Métricas:** a categoria Bônus entrou no dropdown. BON1 e BON2 estão TRUE em todos os planos.
  - **Pesos:** colunas BON1 e BON2 com 5% em todos os planos, fora do Total. O Total continua `SUM(C:T)` = 100%.
  - **Categorias:** sem coluna de bônus.
  - **Média de Pesos e Categorias:** ignora a categoria Bônus.
  - **Consolidado:** depois de E01 vêm BON1 e BON2. Depois do Ponderado vêm **Bônus** = 5% × BON1 + 5% × BON2 (só se a métrica está TRUE no plano) e **Health Score + Bônus** = Ponderado + Bônus, que pode passar de 100%.
  - **HealthScore simples, Ponderado e categorias:** continuam lendo só de E até V, então os bônus não entram neles.
  - **Matriz:** importa `HS COMPLETO!E1:BL` e tem os códigos BON1, BON1B, BON1M, BON2, BON2B e BON2M nas linhas 56 a 61.
  - **Tendência:** colunas BON1 e BON2 depois de E02, e Bônus e Health Score + Bônus depois do Ponderado, com o histórico em branco.
- **AM/TAM:** o CONSOLIDADO ganhou as colunas BON1, BON2, Bônus e Health Score + Bônus. O import busca pelo cabeçalho. Os OKRs continuam no Ponderado, na Adoção e na Configuração, sem bônus.
- **Valores em 15/10/2026:**
  - LG: BON1 = 90,79% (651 de 717 positivas; 750 solicitações para 812 funcionários), Bônus +4,54, Health Score + Bônus = 64,63%.
  - OLX: eficiência de 99,59% (1.693 de 1.700 chamadas). Com volumetria de 50% (faixa 400–1.999), BON2 = 49,79%, Bônus +2,49 e Health Score + Bônus = 32,9%.
  - As chamadas da OLX são de 16 e 17/09 e saem da janela em 17/10, se a base não for atualizada.
- **OKRs, com os pesos dos planos SAG que o usuário reorganizou no mesmo dia:** KRA1 = 46,61%, KRT1 = 64,35% e KRT2 = 45,62%.

**Grupos de teste não contam na C02 (15/10/2026).** Na aba GRUPOS do INTERNO, um grupo com a palavra "teste" no nome não conta mais como grupo específico, assim como "Todos os Funcionários". Quem só está em grupo de teste conta como sem grupo.
- **Regra:** a palavra precisa estar separada por espaço, no começo ou no fim do nome, sem diferenciar maiúsculas. Com isso, "Grupo de teste 02", "Grupo Teste", "Teste 1 Cx - Barbara", "Ferias e Afastamento - Teste" e outros saem da conta. Grupos de cargo como "NOVOS-NEGOCIOS-CELULA-TESTE-ANALISTA-PLENO" e "TECNOLOGIA-TESTES-..." continuam contando.
- **Regex no `REGEXREPLACE`:** `(?i)(^|; )(Todos os Funcionários[^;]*|([^;]* )?teste( [^;]*)?)`.
- **Efeito:**
  - Gupy: 403 → 402 com grupo específico. O Yudi Makibara só estava no "Grupo de teste 02". A C02 continua em 82%.
  - G4 Educação: 572 → 189. As 572 pessoas estavam no "Grupo Teste". A C02 foi de 100% para 33%.
  - doc9 deixou de ter grupo específico.
  - Tenants internos (CX teste, Niuco Apresentacao) também mudaram.
- **OKRs depois:** KRA1 = 46,69%, KRT1 = 63,16% e KRT2 = 45,84%.

**Coluna Média de Pesos e Categorias (15/10/2026).** A Média passou a ser 1 ÷ número de métricas TRUE do plano na aba Métricas, ou seja, quanto cada métrica vale no HealthScore simples. A fórmula busca a coluna do Plano ID na Métricas. Antes, a Pesos contava só as métricas com peso (o SAG Advanced dava 1/9 com 12 métricas TRUE), e a Categorias tinha 5,56% em todas as linhas. Valores: SAG Essentials 12,50% (8 métricas), SAG Advanced 8,33% (12), IGA Essentials 6,67% (15), IGA Advanced 6,25% (16), Ultimate 5,56% (18). É informativa e não entra no cálculo.

**Incoerências entre Pesos e Métricas em 15/10/2026 (em validação).**
- **TRUE sem peso:** C01, A03 e A07 no SAG Advanced; C01 no SAG Essentials. Entram no HealthScore simples, mas não no Ponderado.
- **Métricas descritas como bônus que têm peso:** A04 (8%) e A11 (4% no IGA Essentials; 1% no IGA Advanced e no Ultimate). Quem não usa leva 0 no Ponderado.
- **A08 FALSE só no IGA Essentials:** está TRUE no IGA Advanced e no Ultimate.

**Nomes de empresa divergem entre abas** (G4 e Grancursos já são normalizadas na importação da COBERTURA; Solfacil e SolFacil, JusBrasil e Jusbrasil, ASAAS e Asaas). O `=` do Sheets não diferencia maiúsculas. `Solfacil-POC` não é a Solfacil.

**Valores inválidos conhecidos.** COMPANIES_HISTORIC e as abas de cobertura do relatório têm datas impossíveis em algumas linhas (ano 1000, 1986, 2027); desconsidere ao calcular.

## Como manter este arquivo

Quando o usuário apresentar uma nova aba, coluna ou regra, ou corrigir algo aqui, atualize o arquivo na mesma conversa. Registre a data da decisão e o motivo. Não copie dados pessoais para cá.
