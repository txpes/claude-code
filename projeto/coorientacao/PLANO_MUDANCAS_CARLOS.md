# Plano: mudanças pedidas pelo coorientador (áudios de 13 e 14/10/2026)

Base: `projeto/envio/Artigo_Fragilidade_Financeira_v2.docx`, a versão limpa já mandada ao Carlos, com o escore de três indicadores.
Pedidos: os 13 itens de `AUDIOS_CARLOS_2026-10.md`.
Prazo do Carlos: sexta, 16/10, para os itens do áudio 1. Reunião com o Eduardo na semana seguinte.

## 0. Como as mudanças serão aplicadas

- **Versão base:** a v2 é congelada, e a v3 é gerada a partir dela. Até aqui o artigo era regenerado a partir do original com alterações controladas; como você não usa redline, aplicar as mudanças sobre a versão limpa é mais simples e menos frágil.
- **Script novo (`revisao/aplicar_v3.py`):** lê um arquivo de alterações em JSON. Cada alteração tem o par `antigo`/`novo`, e o `antigo` precisa casar exatamente uma vez com o texto. Isso segue a regra registrada nas notas da coorientação. Parágrafos, seções, tabelas e figuras novas entram por âncora, também única. Tudo fica registrado em log.
- **Renumeração automática:** a seção nova e a revisão de literatura mudam a numeração de seções, tabelas e figuras. O `montar_apendice.py` passa a calcular o mapa pela ordem em que as legendas e os títulos aparecem, em vez de usar um mapa fixo, e renumera todas as remissões numa única passada.
- **Verificação depois de cada etapa:**
  - `verificar_artigo.py`: tabelas contra o código, mais os valores novos;
  - checagem de remissões: toda "seção X" ou "subseção X.Y" citada existe, e toda tabela e figura é citada em ordem;
  - referências: em ordem e todas citadas;
  - PDF conferido nas páginas alteradas.

## 1. Feedback ao Carlos sobre os áudios (item 13) — hoje

- Mensagem curta de WhatsApp. Ela confirma o recebimento, diz o que chega na sexta (seção nova, introdução, equações, resposta ao Eduardo com localização e literatura reorganizada), avisa que as citações recentes podem vir em duas levas e confirma a reunião.
- **Aceite:** você manda.

## 2. Seção nova: panorama do Brasil (itens 1, 2 e 4) — quinta

**Decisão necessária: a fonte dos números.**
- **Recomendado: o painel próprio da CVM (2010–2025).** É reproduzível e coerente com o resto do artigo. Por ano, mostra:
  - a parcela de companhias com cobertura de juros abaixo de 1;
  - a parcela com patrimônio líquido negativo;
  - a parcela com EBITDA negativo;
  - as recuperações judiciais detectadas;
  - a taxa de entrada em vulnerabilidade.
- **Complemento: uma ou duas estatísticas oficiais externas, conferidas na fonte.** Por exemplo, o Relatório de Estabilidade Financeira do Banco Central (dívida de empresas com cobertura de juros abaixo de 1) ou os pedidos de recuperação judicial no país (Serasa Experian). Só entra o que for confirmado na publicação original.

**Passos:**
1. **Script novo (`codigo/17_panorama.py`):** gera, a partir dos painéis, a tabela e a figura do panorama, e os números da introdução.
2. **Texto da seção "2. Panorama da fragilidade financeira das empresas abertas brasileiras":** três a quatro parágrafos, com uma figura das séries anuais (recessões de 2015–2016 e de 2020 marcadas) e uma tabela curta. Tom descritivo, anterior à investigação.
3. **Sem duplicar a Figura 4:** a figura atual da §5.8 (séries por estado e por transição) se sobrepõe ao panorama. A proposta é levá-la para a seção nova e remeter a ela na §5.8.
4. **Ressalvas na nota da tabela:** a detecção de recuperação judicial tem taxa estimada de 2,5% de falsos positivos e datação pela divulgação.

**Aceite:**
- números da seção conferidos contra o script pelo verificador;
- figura e tabela citadas no texto;
- seções renumeradas sem remissão quebrada.

## 3. Introdução com números do Brasil (item 1) — quinta

- **Passos:** um parágrafo logo depois dos casos de abertura, com dois ou três números do panorama, como a parcela de companhias com cobertura abaixo de 1 e as recuperações judiciais no período. Remete à seção 2. O parágrafo final que descreve a estrutura do artigo é atualizado para a numeração nova.
- **Aceite:** números idênticos aos da seção 2; roteiro coerente com os títulos.

## 4. Equações como fórmulas (item 3) — quarta ou quinta

- **Passos:**
  1. Converter as três equações (padronização, escore e probit) em objetos de equação do Word, com a numeração (1) a (3) alinhada à direita.
  2. Conferir os símbolos citados no texto corrido (μ, σ, Σ, v₁, Φ).
  3. Se o painel ganhar alguma definição formal, como a regra de entrada, avaliar se ela vira a equação (4).
- **Aceite:** as equações abrem como fórmula no Word e aparecem corretas no PDF; as remissões às equações continuam certas.

## 5. Revisão de literatura em dois pilares (itens 8, 9, 10 e 12) — quinta

**Estrutura proposta da antiga seção 2 (agora 3):**
- **3. Fragilidade financeira: construção de índices e previsão:** a abertura apresenta os dois universos e por que o artigo usa os dois.
- **3.1 Conceitos:** fragilidade, vulnerabilidade e distress. O texto já existe e é reaproveitado.
- **3.2 Pilar não supervisionado: medir fragilidade.** Minsky e a operacionalização (Tymoigne, Davis et al., Nishi, Torres Filho et al., Mantoan et al.), firmas zumbis e índices compostos por redução de dimensionalidade.
- **3.3 Pilar supervisionado: prever dificuldade financeira.** De Altman e Ohlson às técnicas de aprendizado de máquina, com a literatura brasileira.
- **3.4 Duas propostas, uma comparação.** É o conteúdo da 2.3 reescrito, com dois pontos:
  - o que cada critério otimiza: máxima variância contra máxima covariância com o desfecho;
  - por que a comparação é justa: mesmas oito variáveis, mesmo pré-processamento e mesma avaliação fora da amostra. O que se mede é o valor da informação do desfecho na ponderação (item 10).

**O que sai e o que entra:**
- **A 2.4 "A lacuna" deixa de ser seção (item 12).** As seis dimensões do desenho vão para a introdução, na forma de contribuição. Zmijewski (1984) continua citado só pelo que diz sobre amostras, e não como sustentação de lacuna.
- **Frase explícita sobre a contribuição (item 9), na introdução e na 3.4:** PCA e PLS não são novos; a contribuição está em confrontá-los sob condições controladas e em decompor o resultado por rota de deterioração.
- **Aceite:**
  - nenhum trecho do texto atual se perde sem destino registrado no log;
  - toda afirmação nova sobre a literatura vem de obra conferida.

## 6. Citações recentes (item 11) — quinta e sexta, em duas levas se preciso

- **Meta:** de 8 a 12 trabalhos de 2020 em diante, distribuídos entre os dois pilares e o panorama:
  - índices de fragilidade e firmas zumbis;
  - previsão de insolvência com aprendizado de máquina;
  - avaliação e calibração;
  - Brasil.
- **Passos:**
  1. Buscar no OpenAlex e no Crossref.
  2. Conferir os dados bibliográficos pelo DOI e o conteúdo citado no resumo ou no texto do autor.
  3. Registrar em `referencias_conferidas.csv`, como nas 48 atuais.
- **Aceite:** cada obra nova conferida, citada no texto, em ABNT e na ordem alfabética. Não entra nada que não tenha sido verificado.

## 7. Resposta ao Eduardo com localização (item 5) — sexta, depois da renumeração

- **Passos:**
  1. Reescrever a resposta item a item já pronta, acrescentando onde está cada mudança (seção, tabela e página da v3).
  2. Mandar ao Carlos, e não ao Eduardo, junto com a v3.
  3. Atualizar o e-mail ao Carlos com o que mudou desde a v2.
- **Aceite:** toda localização citada confere com a v3.

## 8. Fechamento da v3 — sexta

- **Passos:**
  1. Rodar o verificador completo.
  2. Gerar o PDF e conferir as páginas alteradas.
  3. Atualizar a planilha, os LEIAMEs e o `ESCRUTINIO_COMPLETO.md`.
  4. Fazer o commit.
- **Entregáveis:**
  - `Artigo_Fragilidade_Financeira_v3.docx`;
  - o e-mail ao Carlos;
  - a resposta ao Eduardo com a localização de cada mudança.

## 9. Depois de sexta

- **Apresentação ao Eduardo (item 6), semana de 19/10:** slides com o que foi feito e como cada comentário foi respondido. Faço se você quiser.
- **Pontos do e-mail que o Carlos disse que mandaria:** cada um entra como tarefa nova.
- **Formato de artigo e submissão (item 7):** depois da reunião.

## Riscos e como ficam cobertos

| Risco | Cobertura |
|---|---|
| Remissão a seção, tabela ou figura quebrada pela renumeração | Mapa calculado pela ordem do documento e checagem automática de que todo número citado existe |
| Afirmação sobre a literatura que o autor citado não sustenta | Só entra obra conferida na fonte, como nas 48 atuais |
| Panorama repetir a Figura 4 ou contradizer números do artigo | A figura vai para a seção nova, e os números saem do mesmo código |
| Seção nova parecer extensão de escopo (o Eduardo pediu foco) | Seção curta e descritiva, motivando a pergunta, sem análise nova |
| Literatura em dois pilares perder a ligação com a pergunta | A 3.4 fecha a seção com a comparação que o artigo faz |
| Prazo apertado para as citações | Primeira leva na sexta; o Carlos aceitou pendências para a reunião |
