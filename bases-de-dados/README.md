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
- **FAIXAS HS**: faixas de pontuação das métricas A09, A10 e A11 do HEALTHSCORE (limite em % dos funcionários e pontos).
- **COMPANIES**: uma linha por empresa (compliance, passo de onboarding, organograma, autorização, SSO, feature flags, funcionários, suporte).
- **COMPANIES_HISTORIC**: snapshot por empresa por data (`Data Execução` é data real). `Funcionários` traz um JSON por status; `#Funcionários` soma sem FIRED; `Hired`, `Absence` e `Fired` vêm separados, com os respectivos deltas.
- **COBERTURA**: Data, Empresa, Ação, Tipo, Movimentações, Disparos, Rejeitados, Aguardando aprovação, Sem disparo, Sucesso. Tem as mesmas colunas da "Base cobertura diária" do relatório AM/CX (confirmar se é espelho; `metricas-cobertura/` neste repositório calcula a partir das abas de cobertura).
- **LOGINS**: acessos por usuário e empresa, com últimos 30 dias, dias sem acesso e perfil.
- **INFO**: `IMPORTRANGE` da INFO do AM/TAM (fonte única, ver "INFO única no AM/TAM").
- **COMPLIANCE**, **CONTRATOS**, **USERS**, **GRUPOS**, **CONEXÕES DIRETAS**, **APOIO**, **HEALTHSCORE**, **HS COMPLETO**, **GROUPS**.

## HEALTHSCORE ([NIUCO] MATRIZ DE HEALTH SCORE)

- **Métricas**: dicionário dos critérios. Adoção: A01 Login Frequência (logins únicos/22), A02 a A05 eficiência de workflow (onboarding, offboarding, absence, move; média de sucesso dos últimos 30 dias), A06 e A07 cobertura de onboarding e offboarding, A08 providers homologados, A09 a A11 e-mail pessoal, desligados com acesso e desligados que acessaram (faixas de proporção desde 09/10/2026; a descrição na aba ainda fala em percentil). Configuração: C01 a C06. Engajamento: E01 (satisfação DM/EB, do HAPPYSCORE). A linha E02 (NPS) não existe na aba em 09/10/2026, embora Pesos, Categorias e Consolidado tenham E02 (ver "Problemas conhecidos").
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
| A09 | E-mail pessoal | faixas da FAIXAS HS | infratores / teto de infratores para 100% |
| A10 | Desligados com acesso | faixas da FAIXAS HS | infratores / teto de infratores para 100% |
| A11 | Desligados que acessaram | faixas da FAIXAS HS | infratores / teto (0) |
| C01 | Configuração de workflow | IGA/Ultimate: (Onboard + Offboard + Move + bônus) ÷ 4; SAG: tem offboard ÷ 1 | pontos / 4 (1 nos planos SAG) |
| C02 | Cobertura de grupos | GRUPOS: pessoas na folha em grupo específico ÷ pessoas na folha | Com grupo específico / Pessoas na folha (GRUPOS) |
| C03 | Organograma | digitado à mão | nota da HEALTHSCORE / 1 |
| C04 | Contratos ativos | contratos ativos ÷ conexões NoShadow, sem teto | ativos / NoShadow |
| C05 | Gastos cadastrados | ativos com gasto ÷ conexões NoShadow | ativos com gasto / NoShadow (código `C05N` na Matriz) |
| C06 | Conexões diretas | percentil entre as empresas (mais é melhor) | quantidade / vazio |
| E01 | Satisfação DM/EB | fixa em 30% para todas as empresas (Consolidado da MATRIZ) | 3 / 10 fixo (colunas BD a BF) |
| E02 | NPS | removida em 14/10/2026 | removida |

**Semântica da HS Bruto.** `Máximo` é o valor de `Bruto` que levaria a nota a 100%. Nas métricas em que mais é melhor, é o denominador (exemplo: A08, homologados / fornecedores). Em A09, A10 e A11, em que menos é melhor, é o teto de infratores para ficar na faixa de 100%: arredondar para baixo (limite da faixa de 100% × funcionários da CARTEIRA). Nesses três, o desvio é `Bruto - Máximo` (quantos infratores precisam sair); nos demais, `Máximo - Bruto`. Atualizado em 09/10/2026: antes, o Máximo de A09, A10 e A11 era 0 digitado.

### Problemas conhecidos (09/10/2026)

- **Health Score sem erro desde 14/10/2026.** Antes, o Consolidado ficava em `#N/A` por dois motivos: lia a coluna E02, que a aba Métricas não tem, e os planos novos da carteira não existiam em Pesos e Categorias. Os dois foram corrigidos (ver "Planos novos em Pesos e Categorias"). A Tendência tem valores sem erro até 02/10/2026; a semana de 09/10 pode ter sido gravada com erro.
- **Bruto de C05 não chega ao Details:** a Matriz usa o código `C05N` no lugar de `C05B`. As demais métricas da HS COMPLETO reproduzem a nota desde 14/10/2026.
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
- **Onde está a regra:** coluna `Configuração WorKflow` da HEALTHSCORE e colunas AA e AB (Bruto e Máximo) da HS COMPLETO, ambas no INTERNO, além da descrição na aba Métricas da MATRIZ.
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

**Nomes de empresa divergem entre abas** (Grancursos; G4 já é normalizada na importação, Solfacil e SolFacil, JusBrasil e Jusbrasil, ASAAS e Asaas). O `=` do Sheets não diferencia maiúsculas, mas Grancursos exige mapeamento manual. `Solfacil-POC` não é a Solfacil.

**Valores inválidos conhecidos.** COMPANIES_HISTORIC e as abas de cobertura do relatório têm datas impossíveis em algumas linhas (ano 1000, 1986, 2027); desconsidere ao calcular.

## Como manter este arquivo

Quando o usuário apresentar uma nova aba, coluna ou regra, ou corrigir algo aqui, atualize o arquivo na mesma conversa. Registre a data da decisão e o motivo. Não copie dados pessoais para cá.
