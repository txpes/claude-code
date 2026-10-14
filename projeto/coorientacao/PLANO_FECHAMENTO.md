# Plano de fechamento: material completo para o Carlos e para a reunião com o Eduardo

**Situação de partida (14/10/2026).**
- A v3 já atende aos pedidos dos áudios do Carlos: panorama, números na introdução, equações, literatura em dois pilares e primeira leva de citações recentes.
- A resposta ao Eduardo item a item, com a localização de cada mudança, está pronta.
- O e-mail e o WhatsApp para o Carlos estão prontos.

**Objetivo.** Chegar à reunião da semana de 19/10 com o material final:
- artigo v4, com os dados corrigidos, os números atualizados e todas as citações conferidas;
- resposta ao Eduardo atualizada para a v4;
- apresentação para a reunião;
- e-mail ao Carlos com o que mudou desde a v3.

**O que falta, por bloco:**

| Bloco | O que é | Por que importa | Quando |
|---|---|---|---|
| A | Correção completa do painel e nova execução do código | Hoje o texto admite três emissores estrangeiros indevidos e quatro firma-anos errados. É melhor chegar ao Eduardo com os dados limpos | Qui 15 |
| B | Atualização dos números do artigo (v4) | Consequência do bloco A | Qui 15 – Sex 16 |
| C | Segunda leva de citações recentes | O Carlos sentiu falta de trabalhos de 2020 em diante; hoje são 7 de 54 | Qui 15 – Sex 16 |
| D | Pequenas conferências de dados pendentes | Fechar dúvidas abertas na verificação | Qui 15 |
| E | Material de envio: resposta ao Eduardo, e-mail ao Carlos e nota de decisões | Coerência de numeração com a v4 | Sex 16 |
| F | Apresentação para a reunião com o Eduardo | O Carlos pediu que você apresente o que foi feito | Seg 19 |
| G | O que depende do Carlos | Retorno sobre técnicas de avaliação e pontos do e-mail prometido | Quando chegar |

---

## A. Correção completa do painel (qui 15)

1. **Excluir os três emissores estrangeiros:** Aura Minerals, G2D Investments e Inter & Co. A regra passa a ser explícita: sai todo código CVM fora do cadastro de companhias abertas com sede no exterior. Revarrer o painel para confirmar que não sobra nenhum.
2. **Corrigir os quatro firma-anos a partir dos arquivos da CVM:**
   - Águas do Rio 1 e 4, 2021: usar a demonstração anual de 31/12, e não a especial de julho;
   - Equatorial Pará, 2025: usar a versão 2 da DFP;
   - COSERN, 2010: preencher a receita.

   Recalcular os indicadores dessas linhas.
3. **Manter a atribuição às partições:** a divisão das firmas entre as partições é feita sobre a lista original. Assim, retirar firmas não reembaralha as demais, e a diferença nos números reflete só os dados.
4. **Rodar de novo os 17 scripts** com o `executar.sh`, em diretório limpo.

**Critério de aceite:**
- o comparador contra a CVM dá 100% nas firmas do painel;
- nenhum código de emissor estrangeiro sobra;
- a execução completa termina sem erro;
- as medidas sem estimação mudam no máximo na terceira casa decimal, como a sensibilidade já mostrou.

## B. Números do artigo na v4 (qui 15 – sex 16)

1. **Planilha:** regenerar com o `atualizar_planilha.py`.
2. **Script novo de comparação:** compara cada quantidade do código entre a execução antiga e a nova, na precisão em que aparece no artigo, e lista o que mudou.
3. **Atualizar, numa lista de alterações em JSON** (mesma regra de casar uma única vez):
   - as células de tabela que mudaram, apontadas pelo `verificar_artigo.py`;
   - os números do texto que mudaram, localizados pelo valor antigo junto do seu contexto;
   - os números do panorama, que vêm do script 17.
4. **Retirar da §5.1** a frase sobre os emissores que permaneceram e voltar a "quinze emissores estrangeiros excluídos". Atualizar 7.419 observações e 730 companhias.
5. **Conferir as frases que dependem de significância:** por exemplo, p de Bonferroni perto de 0,05 ou um intervalo que passa a conter o zero. Em cada caso, ajustar a redação, e não só o número.

**Critério de aceite:**
- `verificar_artigo.py` sem divergências;
- `checar_estrutura.py` sem problemas;
- nenhum número antigo sobrando no texto, segundo a varredura da lista do passo 2;
- PDF conferido nas páginas alteradas.

## C. Segunda leva de citações recentes (qui 15 – sex 16)

1. **Meta:** mais 4 a 6 trabalhos de 2020 em diante, chegando a 11–13. Prioridade:
   - previsão de insolvência no Brasil (BBR, RCF, RAC);
   - revisões recentes de aprendizado de máquina em previsão de falência;
   - firmas zumbis e dificuldade financeira;
   - Minsky em nível de firma.
2. **Candidatas já identificadas, à espera de um resumo verificável:**
   - Álvarez, García-Posada e Mayordomo (2023): buscar a versão de working paper do Banco de España;
   - Bibi e Chandorkar (2025): versão SSRN;
   - Dasilas e Rigani (2024).
3. **Mesma regra de antes:** dados pelo DOI, conteúdo pelo resumo ou pelo texto do autor, registro no CSV, inserção no texto e nas referências.

**Critério de aceite:** toda obra nova conferida, citada no ponto certo dos dois pilares e em ABNT.

## D. Conferências pendentes (qui 15)

1. **Grupo Casas Bahia, 2024:** a base classifica o caso como recuperação judicial. Pelo que se sabe, foi extrajudicial. Conferir no documento da CVM. Não altera o critério de evento, que abrange as duas, mas altera a contagem por tipo.
2. **Predebom et al. (2025):** confirmar o título exato (o registro traz "Trailed" e "Traded") e o número do artigo na página da revista.
3. **Rolim et al. (2021):** confirmar as páginas.

## E. Material de envio (sex 16)

1. **Resposta ao Eduardo:** atualizar `CARTA_EDUARDO.md` para a v4, com a localização de cada item, que volta a ser conferida automaticamente contra o documento.
2. **E-mail ao Carlos:** atualizar `CARTA_CARLOS.md` com o que mudou desde a v3 (dados corrigidos e segunda leva de citações) e anexar a v4.
3. **Nota de decisões:** proponho **não enviar** nesta rodada. A resposta ao Eduardo cobre o mesmo conteúdo, e manter a nota em dia com a numeração é trabalho sem leitor. Se você preferir enviar, eu atualizo.
4. **Arquivos:** `Artigo_Fragilidade_Financeira_v4.docx` para anexar e o PDF para você conferir.

**Critério de aceite:** todas as localizações citadas conferem com a v4; um único anexo por e-mail.

## F. Apresentação para a reunião com o Eduardo (seg 19)

**Conteúdo:** de 12 a 15 slides, para 20 minutos.
1. Pergunta e resultado central.
2. Panorama do Brasil.
3. Desenho: os dois pilares e o que a comparação mede.
4. Os comentários dele, agrupados em quatro blocos (vazamento e inferência, calendário e saídas, métricas, moderação), com o que mudou e onde está.
5. Decomposição por rota e escore com três indicadores.
6. Robustez.
7. Próximos passos: formato de artigo e submissão, como o Carlos sugeriu.

**Formato:** apresentação que baixa como PowerPoint e PDF. Figuras e números saem do mesmo código do artigo.

**Critério de aceite:** todo número do slide igual ao da v4.

## G. O que depende do Carlos

- **Técnicas de avaliação:** a proposta de manter a lista atual, com duas adições opcionais (gráfico de calibração e taxa de captura no decil de maior risco), aguarda a resposta dele. Se ele aceitar alguma, entra na v4 ou depois da reunião.
- **E-mail com pontos pontuais:** ele disse que mandaria e ainda não chegou. Quando chegar, cada ponto vira tarefa, com o escopo confirmado antes de mexer no artigo.

---

## Decisões que preciso de você

1. **Corrigir os dados antes da reunião (A e B)?** Recomendo que sim. Com a atribuição às partições mantida, os números mudam pouco, e o Eduardo vê a versão definitiva, sem a frase sobre emissores que ficaram.
2. **Formato da apresentação:** PowerPoint baixável (recomendado) ou outro?
3. **Nota de decisões:** não enviar (recomendado) ou atualizar?
4. **WhatsApp e e-mail ao Carlos já enviados com a v3?** Se ainda não, sugiro mandar só o WhatsApp agora e o e-mail com a v4 na sexta, para ele não receber duas versões em dois dias.

## Riscos

| Risco | Cobertura |
|---|---|
| Um número do texto ficar desatualizado depois da nova execução | Comparação automática de todas as quantidades entre as duas execuções, mais a varredura dos valores antigos |
| Alguma conclusão mudar perto do limiar de significância | Revisão de redação nos casos apontados, e não só troca de número |
| A segunda leva de citações não ficar pronta | A primeira já cobre os dois pilares; a segunda pode vir depois da reunião |
| A apresentação divergir do artigo | Números e figuras gerados pelo mesmo código |
