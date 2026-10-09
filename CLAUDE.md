# Customer Success Niuco

## Bases de dados

- Os bancos de dados internos do Customer Care são quatro planilhas: FINANCEIRO, INTERNO, HEALTHSCORE e AM/TAM. Mapa, abas, colunas e regras em `bases-de-dados/README.md`.
- Leia esse arquivo antes de mexer em qualquer uma delas. Ao receber nova informação sobre as planilhas (aba, coluna, regra, decisão), atualize-o na mesma conversa.
- Número de funcionários por empresa na CARTEIRA: coluna `Funcionários` da aba FATURA do FINANCEIRO (fatura mais recente com valor), sem parceiros. Nunca somar `Parceiros` nem usar `Licenças Total`.

## Padrão de nome das conversas

- Todo título de conversa começa com a tag do projeto entre colchetes: `[GTM] ...`, `[Customer-Success] ...`, `[Projetos] ...`.
- A tag segue o assunto da conversa, não só o repositório aberto. Em dúvida, use o projeto do repositório principal.
- No início de toda conversa nova, defina o título nesse formato (`set_session_title`), com o assunto em poucas palavras.
- Conversa que mudar de projeto no meio: troque a tag do título.
