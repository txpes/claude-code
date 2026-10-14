# E-mail ao coorientador (versão 4)

**Assunto:** Artigo revisado: panorama, introdução, equações, literatura e resposta ao Eduardo

Carlos, tudo bem?

Segue a nova versão do artigo, com os ajustes que você pediu nos áudios. Abaixo, a resposta ao Eduardo item a item, com a localização de cada mudança no texto; ainda não mandei para ele.

**O que mudou**
1. **Panorama do Brasil (nova seção 2).** Usa os dados da CVM, com o mesmo painel dos testes, de 2010 a 2025:
   - a parcela de companhias com cobertura de juros abaixo de 1 tem média de 43,4% e pico de 62,8% em 2015, na recessão;
   - EBITDA negativo e patrimônio líquido negativo também são mostrados ao longo do período;
   - 72 companhias entraram em recuperação judicial ou extrajudicial no período.

   Tudo isso aparece numa figura (Figura 1) e numa tabela por período (Tabela 1). As demais seções foram renumeradas.
2. **Introdução.** Ganhou um parágrafo com esses números.
3. **Equações.** As três estão no editor de fórmulas, numeradas.
4. **Revisão de literatura.** Reorganizada em dois pilares:
   - 3.1 conceitos;
   - 3.2 não supervisionado, ou seja, medir a fragilidade;
   - 3.3 supervisionado, ou seja, prever a dificuldade financeira;
   - 3.4 o que a comparação entre os dois mede.

   Ficou explícito que PCA e PLS não são métodos novos e que a contribuição está na comparação controlada e na decomposição por rota. A seção "A lacuna" saiu, e o argumento não se apoia mais no trabalho de 1984.
5. **Citações recentes.** Entraram dez trabalhos de 2020 em diante, quatro deles brasileiros, todos conferidos na fonte. A lista passa a ter 11 referências desse período.
6. **Dados conferidos com a CVM.** Conferi o painel contra os arquivos originais da CVM. Achei três emissores estrangeiros que deveriam ter sido excluídos e quatro firma-anos com valores errados, e corrigi tudo. Depois rodei o código de novo, mantendo a mesma divisão das firmas entre os grupos de teste. Nenhuma conclusão muda, e as tabelas conferem com o código.
   - Alguns números mudaram na terceira casa: o escore fica em 0,763, contra 0,894 da cobertura.
   - Um resultado secundário perdeu significância. A vantagem do escore sobre o PLS nas entradas por patrimônio negativo ficou no limite (intervalo encostando no zero), e o texto agora a trata como nominal.

Com o panorama na frente, as tabelas do corpo ganharam um número: a de métricas é agora a 15, e a de decomposição por tipo, a 11. As do apêndice não mudaram.

**Técnicas de avaliação.** Mantive a proposta que te mandei antes: fechar a lista atual e, se você achar útil, acrescentar o gráfico de calibração e a captura no decil de maior risco.

Podemos manter a apresentação ao Eduardo na semana que vem? Estou preparando os slides.

Abraço,
Thomas

---
Anexo: `Artigo_Fragilidade_Financeira_v4.docx`
Abaixo, a resposta ao Eduardo (ver `CARTA_EDUARDO.md`).
