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
- **COMPLIANCE**, **CONTRATOS**, **USERS**, **GRUPOS**, **CONEXÕES DIRETAS**, **INFO**, **APOIO**, **HEALTHSCORE**, **HS COMPLETO**, **GROUPS**.

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
| A03 | Eficiência offboarding | ADOÇÃO SCORE da sexta mais recente (botão para Sec Automation, WORKFLOWS para os demais) | Δ sucesso / Δ iniciados de WORKFLOWS; vazio para Sec Automation |
| A04 | Eficiência absent | WORKFLOWS, a partir de 04/08/2026 | Δ sucesso / Δ iniciados |
| A05 | Eficiência move | WORKFLOWS | Δ sucesso / Δ iniciados |
| A06 | Cobertura onboarding | ADOÇÃO SCORE: disparos ÷ admissões | Bruto copiado de A02; Máximo com `#REF!` |
| A07 | Cobertura offboarding | ADOÇÃO SCORE: disparos ÷ demissões | Bruto copiado de A03; Máximo com `#REF!` |
| A08 | Providers homologados | homologados ÷ fornecedores | homologados / fornecedores |
| A09 | E-mail pessoal | faixas da FAIXAS HS | infratores / teto de infratores para 100% |
| A10 | Desligados com acesso | faixas da FAIXAS HS | infratores / teto de infratores para 100% |
| A11 | Desligados que acessaram | faixas da FAIXAS HS | infratores / teto (0) |
| C01 | Configuração de workflow | tipos distintos de workflow ÷ 2 (1 para Gran Cursos), limitado a 100% | tipos / 2 (3 para Contabilizei) |
| C02 | Cobertura de grupos | GRUPOS: pessoas na folha em grupo específico ÷ pessoas na folha | workflows de onboarding com grupo / grupos da empresa (outra definição) |
| C03 | Organograma | digitado à mão | digitado à mão, separado da nota |
| C04 | Contratos ativos | contratos ativos ÷ conexões NoShadow, sem teto | ativos / NoShadow |
| C05 | Gastos cadastrados | ativos com gasto ÷ conexões NoShadow | ativos com gasto / NoShadow (código `C05N` na Matriz) |
| C06 | Conexões diretas | percentil entre as empresas (mais é melhor) | quantidade / vazio |
| E01 | Satisfação DM/EB | calculada no Consolidado da MATRIZ | não existe na HS COMPLETO |
| E02 | NPS | calculada no Consolidado da MATRIZ | coluna NPS da HS COMPLETO, NPS ÷ 100 sem converter para 0 a 1 |

**Semântica da HS Bruto.** `Máximo` é o valor de `Bruto` que levaria a nota a 100%. Nas métricas em que mais é melhor, é o denominador (exemplo: A08, homologados / fornecedores). Em A09, A10 e A11, em que menos é melhor, é o teto de infratores para ficar na faixa de 100%: arredondar para baixo (limite da faixa de 100% × funcionários da CARTEIRA). Nesses três, o desvio é `Bruto - Máximo` (quantos infratores precisam sair); nos demais, `Máximo - Bruto`. Atualizado em 09/10/2026: antes, o Máximo de A09, A10 e A11 era 0 digitado.

### Problemas conhecidos (09/10/2026)

- **Health Score em erro.** No Consolidado da MATRIZ, HealthScore e Health Score Ponderado estão em `#N/A` e Engajamento em `#VALUE!` para todas as empresas; o OKR AM KRA1 herda o erro. A aba Métricas tem 18 códigos (sem E02) e o Consolidado tem 19 colunas de métrica, então os `XLOOKUP` comparam listas de tamanhos diferentes. A Tendência tem valores sem erro até 02/10/2026.
- **HS COMPLETO não reproduz a nota** em A03 (Sec Automation), A06, A07, C01, C02, C03 e E02; E01 não está na aba; a Matriz usa o código `C05N` no lugar de `C05B`, então o Bruto de C05 não chega ao Details.
- **Métrica vazia vale 0 no ponderado.** Exemplo: sem NPS, uma empresa Sec Automation perde os 5 pontos de E02; Malga e G4 Educação ficam com cerca de metade do peso vazio.
- **C04 sem teto** (Malga 104%).
- **Dois status de projeto:** o Consolidado filtra pela tabela `info` do INTERNO e a Tendência usa a aba Info da MATRIZ; Hubla e Malga estão como Implantação numa e Ativado na outra.
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

**Nomes de empresa divergem entre abas** (G4 e Grancursos, Solfacil e SolFacil, JusBrasil e Jusbrasil, ASAAS e Asaas). O `=` do Sheets não diferencia maiúsculas, mas G4 e Grancursos exigem mapeamento manual. `Solfacil-POC` não é a Solfacil.

**Valores inválidos conhecidos.** COMPANIES_HISTORIC e as abas de cobertura do relatório têm datas impossíveis em algumas linhas (ano 1000, 1986, 2027); desconsidere ao calcular.

## Como manter este arquivo

Quando o usuário apresentar uma nova aba, coluna ou regra, ou corrigir algo aqui, atualize o arquivo na mesma conversa. Registre a data da decisão e o motivo. Não copie dados pessoais para cá.
