# Plano de revisão completa do artigo

**Objeto:** o pacote `projeto/`, com artigo, nota metodológica, tabelas, código e dados, na versão de 28/09/2026.

**Regra geral:** nenhum número muda no artigo sem ser reproduzido pelo código. Quando a reprodução divergir do artigo, o caso é registrado e o artigo não é alterado.

## Frentes

| # | Frente | O que se faz | Entregável |
|---|---|---|---|
| F1 | **Reprodução** | Rodar os 13 scripts do zero, com os dados do pacote. Comparar cada saída com as tabelas do artigo e com a planilha `.xlsx`. | Tabela de reprodução: número a número, reproduz / diverge |
| F2 | **Dados** | Recalcular a partir dos CSV todos os números descritivos: painel, firmas, eventos, critérios, censura, saídas e a Tabela 3. Checar duplicatas, faixas e anos. | Seção "Dados" do relatório |
| F3 | **Código** | Ler os 13 scripts em busca de vazamento, erros de junção, sementes, diferenças entre código e texto, caminhos fixos e o executor. | Seção "Código" |
| F4 | **Consistência numérica** | Extrair todos os números do texto e cruzá-los com as tabelas do artigo, a `.xlsx` e a reprodução. | Lista de divergências com a correção proposta |
| F5 | **Metodologia** | Parecer como de um periódico de ponta: desenho, identificação, inferência, calibração, sobreposição mecânica, poder estatístico, generalização. | Seção "Metodologia" |
| F6 | **Escrita** | Estrutura, argumentação, grau de certeza das afirmações, terminologia, coerência entre resumo, introdução e conclusão, tabelas e notas, ABNT. | Seção "Escrita" |
| F7 | **Referências** | Casar citações no texto com a lista. Levantar as referências de método que faltam e as recentes, conferindo cada uma no Crossref. | Seção "Referências" |
| F8 | **Aplicação** | Aplicar ao `.docx` as correções seguras: texto, números já reproduzidos e referências. Gerar o registro das mudanças. | `Artigo_revisado.docx` e `MUDANCAS.md` |

## O que fica para decisão do autor

Fica com o autor tudo o que exige escolha substantiva, e não correção:
- reenquadrar o resultado central;
- decidir entre corpo e apêndice;
- rodar análises novas, como o teste da RJ atrasada;
- trocar o método de calibração.

Para cada um desses pontos, o relatório traz uma proposta concreta e, quando possível, o resultado já calculado.
