---
name: health-score
description: Altera, audita e aprimora o Health Score do Customer Care da Niuco (planilhas INTERNO, MATRIZ DE HEALTH SCORE e AM/TAM, e o cenário do Make que alimenta a PROVIDERS). Use sempre que o pedido envolver métrica do Health Score (A01–A11, C01–C06, E01, bônus BON1/BON2), pesos, categorias, planos, faixas de pontuação, HS Bruto, Consolidado, Matriz/Details, Tendência ou OKRs KRA1/KRT1/KRT2; também para criar, excluir ou renumerar métrica, trocar percentil por faixa, simular nota antes de aplicar, ou investigar valor estranho no score.
---

# Health Score Niuco

Este é o roteiro para mexer no Health Score sem quebrar a cadeia de fórmulas. O registro completo das decisões, com valores e datas, está em `bases-de-dados/README.md`. **Leia o README antes de mexer** e atualize-o na mesma conversa, como pede o `CLAUDE.md`.

## Mapa

| Planilha | ID | Abas que importam |
|---|---|---|
| INTERNO ([NIUCO] DATABASE) | `18yYh-WBgBxrfaDVUVkjOComtjCIZmnevTu29uFVWmAM` | HEALTHSCORE (tabela `healthscore`, sheet 1994005037), HS COMPLETO (`hsbruto`, 1672959028), FAIXAS HS, PROVIDERS (`providers`), WORKFLOWS, SUCCESS RATE WORKFLOW/BOTTON, ADOÇÃO SCORE, GRUPOS, COBERTURA, CARTEIRA, INFO, CATÁLOGO PLANOS (`planos`) |
| MATRIZ DE HEALTH SCORE | `1GFlzeH7DwUai_8Qg9KrlNbshhCH65M33nnnyZkvTH7Q` | Fonte (IMPORTRANGE de `healthscore`), Consolidado (`metrics`), Métricas (`details`), Pesos, Categorias, Matriz (`matriz`), Details, Tendência, Info, Catálogo Planos, Calculadora (oculta) |
| AM/TAM DATABASE | `14DEUkFlQrv0AYmc-1sihIwFbWiicBdseMbGPvaGqUjE` | CONSOLIDADO (import da MATRIZ pelo cabeçalho), OKR AM (KRA1), OKR TAM (KRT1, KRT2), CARTEIRA, INFO (fonte única), CATÁLOGO PLANOS (`planos_catalogo`, fonte única de planos) |
| Relatórios AM/CX | `1AEZzqHfqMGk2tgXYlke8SdiyB81wJ3tyZCAVKOza-Jk` | Solicitações no portal (fonte do BON1), Niuco API (fonte do BON2), Cobertura onboard/offboard/grupos. Atualização semanal. No INTERNO, entram pelas abas PORTAL e API |
| FINANCEIRO | `1UF5-sbh0xbhyeXkBpG3pOJliPfiO15IRYGnMdBXlAeY` | FATURA (Funcionários, nunca Parceiros nem Licenças Total) |

**Make:** o cenário "[BackOffice -> Sheets] Providers" (4513382, time 71525) grava a PROVIDERS em dias úteis às 06:00. O cenário "[HS-> Sheets] Customers Deals" (4424892) grava a CARTEIRA. Nenhum cenário escreve nas abas INFO.

## Fluxo do cálculo

1. **INTERNO, HEALTHSCORE:** uma coluna de nota (0 a 1) por métrica. As fórmulas são `MAP(A2:A; LAMBDA(...))` na linha 2.
2. **INTERNO, HS COMPLETO:** Bruto e Máximo de cada métrica, depois as notas. `Máximo` é o valor de Bruto que daria 100%. Nas métricas por faixa, é o início (ou o teto) da faixa de 100%.
3. **MATRIZ, Fonte:** `IMPORTRANGE` da tabela `healthscore`.
4. **MATRIZ, Consolidado:** filtra `Projeto <> "Implantação"`. As fórmulas genéricas fazem o seguinte:
   - pegam o Plano ID da empresa no catálogo (`planos[Plano]` → `planos[Plano ID]`);
   - usam a coluna desse Plano ID na aba Métricas (TRUE/FALSE) como máscara;
   - leem os pesos com `XLOOKUP(pid; Pesos!$A:$A; Pesos!$A:$AD)` e localizam cada métrica pelo cabeçalho.
   - **HealthScore simples:** média das métricas TRUE que têm valor. A métrica vazia é ignorada.
   - **Ponderado:** soma de peso × nota. A métrica vazia vale 0.
   - **Adoção, Configuração e Engajamento:** mesma conta, com os pesos da aba Categorias.
5. **MATRIZ, Matriz:** códigos digitados na coluna A (`X`, `XB` = bruto, `XM` = máximo), alinhados ao `TRANSPOSE` da HS COMPLETO. A aba Details se monta sozinha.
6. **AM/TAM:** o CONSOLIDADO importa `Consolidado!A1:AZ1000` e escolhe cada coluna pelo cabeçalho. KRA1 = média do Ponderado; KRT1 = média da Configuração; KRT2 = média da Adoção.

Para conferir os OKRs, leia `'OKR AM'!A2:C2` e `'OKR TAM'!A2:C3`.

## Regras de negócio vigentes

- **Planos:**
  - Produto SAG ou IGA. O Ultimate (`identity_plataform`) tem os dois.
  - Planos: SAG Essentials, SAG Advanced, IGA Essentials, IGA Advanced e Ultimate.
  - O nome do plano só se edita no catálogo do AM/TAM. Tudo se liga pelo Plano ID.
- **Implantação:** empresa em implantação fica fora do Consolidado. O status fica na INFO do AM/TAM (Chave 1 = empresa, Chave 2 = status).
- **Funcionários (denominador de A09 e A10):** coluna Funcionários da FATURA, sem parceiros.
- **C01:**
  - IGA e Ultimate: (Onboard + Offboard + Move + bônus de no máximo 1, por ABSENT ou IDENTITY_SCREENING) ÷ 4.
  - SAG: offboard (workflow ou botão) ÷ 1.
  - O texto da aba Métricas foi editado pelo usuário para "÷ 5". Confirme com ele antes de mudar a fórmula.
- **Engajamento:** só a E01, fixa em 30% (3/10) até existir nota de satisfação.
- **Métricas por faixa:** A09 (desligados com acesso), A10 (desligados que acessaram) e C06 (conexões diretas). As faixas ficam editáveis na FAIXAS HS.
- **C06:**
  - É a quantidade de conexões diretas: 0–5 = 15%, 6–10 = 30%, 11–15 = 45%, 16–20 = 60%, 21–25 = 75%, 26–30 = 90%, 31 ou mais = 100%.
  - Conexão direta é um provider sem `source` (conector nativo) ou com fonte `atlassian`, `gsuite-*` ou `conector-adobe`.
  - Não contam: `manual`, `compliance-*`, `sso-*` e `jumpcloud`.
- **Bônus (BON1 Portal e BON2 API):**
  - Nota = eficiência × volumetria (faixas nas colunas M a Q da FAIXAS HS).
  - Ficam fora da média e dos 100% dos pesos. Têm 5% cada na aba Pesos, fora do Total.
  - Entram só nas colunas "Bônus" e "Health Score + Bônus" do Consolidado, que pode passar de 100%. Os OKRs não usam bônus.
  - Bônus vazio não tira ponto.
  - Bônus novo: código BONn, categoria Bônus na aba Métricas, coluna nova na Pesos (fora do Total) e uma parcela a mais na fórmula da coluna Bônus do Consolidado.
- **Lista de exclusão do Make:**
  - A conta é feita por `remove(map(11.data; "source"); ...)` no módulo 16 do cenário 4513382.
  - Cliente novo com `sso-google-<nome>` ou outro IdP precisa entrar na lista. Senão, a contagem infla.
  - Nunca deixe espaço no começo de um item: o `remove` compara o texto exato.

## Roteiros

### Mudar a regra de uma métrica (exemplo: percentil → faixa)

1. **Levante os dados de origem** (por exemplo, a PROVIDERS) e **simule em Python** as opções de faixa: nota por empresa, efeito no Ponderado (peso da métrica × diferença) e na categoria (peso da Categorias × diferença), e KRA1/KRT1/KRT2 estimados.
2. **Mande as propostas ao usuário em tabela**, empresa a empresa, com uma recomendação. Não aplique antes de ele escolher.
3. **Aplique:**
   - a faixa na FAIXAS HS, num bloco próprio. Se mais é melhor, a faixa vale "a partir de", com `XLOOKUP(...; 0; -1)`; se menos é melhor, vale "até", com `XLOOKUP(...; 0; 1)`;
   - a fórmula da nota na HEALTHSCORE;
   - Bruto e Máximo na HS COMPLETO, conferindo o formato numérico;
   - o Cálculo e a Observação na aba Métricas, **com um exemplo numérico real**.
4. **Atualize a Fonte:** reescreva `Fonte!A2` com uma pequena variação de espaço, porque o `IMPORTRANGE` fica em cache.
5. **Confira:** leia `Consolidado!B2:AA15` e os OKRs e compare com a simulação.
6. **Registre:** README, commit e push na branch da sessão.

### Criar uma métrica nova

Esse roteiro foi usado na pré-folha:

1. **HEALTHSCORE:** insira a coluna na ordem certa.
2. **HS COMPLETO:** acrescente nota, Bruto e Máximo **no fim da tabela**, para não deslocar a Matriz.
3. **Fonte:** corrija os cabeçalhos e confira onde ficou a coluna Projeto.
4. **Consolidado:** insira a coluna com o código e ajuste o filtro do A2. Hoje ele é `filter(Fonte!A2:U;Fonte!B2:B<>"";Fonte!Z2:Z<>"Implantação")`, com Projeto na Z desde os bônus.
5. **Métricas:** insira a linha (ID, critério, categoria, cálculo, observação e TRUE/FALSE por plano).
6. **Pesos:** insira a coluna e redistribua os pesos para cada plano somar 100%.
7. **Categorias:** insira a coluna e escreva só o cabeçalho; a fórmula descobre a categoria sozinha.
8. **Matriz:** cadastre os códigos e estenda a tabela `matriz`.
9. **Tendência:** insira a coluna.
10. **CONSOLIDADO do AM/TAM:** insira a coluna com o mesmo cabeçalho.
11. **Confira:** compare HealthScore e Ponderado antes e depois, e os OKRs.

### Excluir uma métrica

Faça o roteiro acima ao contrário: apague a coluna ou linha em todas as abas e **renumere os códigos** em Métricas, Pesos, Categorias, Consolidado, Tendência, Matriz e CONSOLIDADO do AM/TAM.

Os valores precisam continuar iguais aos de antes, se a métrica já estava sem peso.

### Auditar pesos × Métricas

Para cada plano, confira:
- se a soma dos pesos dá 100%;
- se os subtotais batem: Adoção 65%, Configuração 20% e Engajamento 15%, ou o valor que estiver nas colunas de soma;
- se há métrica TRUE sem peso: entra no HealthScore simples, mas não no Ponderado;
- se há peso em métrica FALSE: é ignorado;
- se há métrica "bônus" com peso: vale 0 para quem não usa.

A coluna Média é 1 ÷ número de métricas TRUE do plano.

## Armadilhas do Google Sheets (já custaram retrabalho)

- **Funções que não existem:** `DROP` e `XMATCH`. Use `CHOOSEROWS`/`SEQUENCE` e `MATCH`.
- **Nomes no `LET`:** não podem parecer endereço de célula (`b2`) nem repetir nome de tabela (`pesos`). As duas coisas dão `#ERROR!` de parse.
- **Arrays dentro de `MAP`/`LAMBDA`:** operações com array pedem `ARRAYFORMULA`.
- **Referências a outras abas:** busque linhas e colunas pelo nome (`XLOOKUP` na coluna inteira e no cabeçalho), nunca por posição. O usuário reorganiza Pesos e apaga colunas.
- **Imports entre planilhas:** sempre pelo cabeçalho. Import por posição já fez os OKRs lerem a coluna errada.
- **Cache do `IMPORTRANGE`:** depois de mudar o INTERNO, reescreva `Fonte!A2` para forçar a atualização.
- **Tabela que precisa crescer:** escrever logo depois do fim de uma tabela não a estende. Use `appendDimension`, se a grade for pequena, e depois `updateTable` com o `range` novo. Para mudar as opções de um dropdown da tabela, use `updateTable` com `columnProperties` completo.
- **Formato herdado:** coluna nova herda o formato da antiga. Por exemplo, o Máximo saiu como `3100%`; corrija com `repeatCell` e `numberFormat`.
- **Parênteses:** confira o balanceamento antes de gravar fórmulas longas.

## Armadilhas do Make

- **Atualizar o cenário:** `scenarios_update` substitui o blueprint inteiro. Busque o blueprint com `scenarios_get`, edite o JSON por script, confira que só a variável desejada mudou e envie tudo. Os `samples` do designer podem ficar de fora.
- **Testar uma fórmula:** peça ao usuário o bundle de saída do módulo (JSON) e reproduza em Python. Em `map()`, item sem a chave conta como valor vazio e **entra** no `length`.
- **Depois de editar:** rode o cenário (`scenarios_run`), acompanhe com `executions_list` e confira a PROVIDERS.

## Comportamento esperado

- O usuário quer autonomia. Execute e mostre o resultado com números, mas proponha antes de aplicar mudanças de regra ou de peso.
- Trabalhe em português. Ao reportar, use tabela por empresa e o antes e depois dos OKRs.
- Não altere pesos por conta própria. Aponte as incoerências e deixe o usuário decidir.
- Pendências conhecidas:
  - pesos do IGA Advanced e do SAG Essentials;
  - C01 TRUE ou FALSE e com ou sem peso nos planos SAG;
  - A04 e A11 como bônus: a categoria Bônus já existe (BON1/BON2); falta decidir se A04 e A11 migram para ela;
  - regra de métrica vazia;
  - Calculadora (oculta) desatualizada.
