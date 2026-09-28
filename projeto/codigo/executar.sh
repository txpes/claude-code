#!/bin/bash
# Uso: DADOS=/caminho/dos/paineis bash executar.sh
# Roda os treze scripts na ordem. O corte temporal padrao e 2021, o do artigo.
set -e
export DADOS="${DADOS:-../dados}"
for s in 01_pipeline_sem_vazamento 02_inferencia_bootstrap 03_metricas_probabilidade 04_entradas_e_saidas \
         05_robustez_e_calendario 06_consolidacao 07_complementos 08_definicoes_de_evento \
         09_decomposicao_por_tipo; do
  echo "== $s"; python3 $s.py
done
echo "== 10_corte_temporal"; python3 10_corte_temporal.py "${ANO_CORTE:-2021}"
for s in 11_tabelas_e_figuras 12_concentracao 13_puros_e_perfil; do
  echo "== $s"; python3 $s.py
done
