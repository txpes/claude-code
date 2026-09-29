"""Sensibilidade a datacao da recuperacao judicial (subsecao 5.9).

A RJ e datada pelo primeiro documento entregue a CVM que a menciona. Quando esse documento trata do
andamento do processo, e nao do pedido (natureza_1o_doc == 'andamento' em rj_detectada_2025.csv), a data
pode estar atrasada em relacao ao ajuizamento. Aqui a RJ dessas firmas e antecipada em um ano, o estado,
a entrada e o conjunto de risco sao reconstruidos com a mesma regra dos paineis originais, e os scripts
01, 02 e 13 sao reexecutados sobre o painel alterado.

A reconstrucao reproduz exatamente os paineis originais quando nenhuma data e alterada (verificado abaixo).
Uso: DADOS=../dados python3 15_rj_antecipada.py
"""
import os, shutil, subprocess, sys
import pandas as pd

D = os.environ.get('DADOS', 'dados').rstrip('/')
OUT = os.path.abspath('sens_rj_antecipada')
c = pd.read_csv(f'{D}/painel_completo.csv'); t = pd.read_csv(f'{D}/painel_transicao.csv')
r = pd.read_csv(f'{D}/rj_detectada_2025.csv')


def reconstroi(anos_rj):
    P = c.sort_values(['CD_CVM', 'ano']).reset_index(drop=True).copy()
    arj = P.CD_CVM.map(anos_rj)
    P['crit_d_state'] = arj.notna() & (P.ano >= arj)
    P['crit_d_entry'] = arj.notna() & (P.ano == arj)
    V = P.crit_b | P.crit_c | P.crit_d_state
    g = P.groupby('CD_CVM'); lag = V.groupby(P.CD_CVM).shift(1); cons = (P.ano - g.ano.shift(1)) == 1
    T = t.sort_values(['CD_CVM', 'ano']).reset_index(drop=True).copy()
    T['V_estado'] = V.values; T['V_estado_lag'] = lag.where(cons).values
    T['em_risco'] = ((lag == False) & cons).values; T['V_entrada'] = (T.em_risco & T.V_estado).values
    return P, T


# verificacao: sem alterar datas, a reconstrucao reproduz o painel
base = r.set_index('CD_CVM').ano_rj
_, T0 = reconstroi(base)
t0 = t.sort_values(['CD_CVM', 'ano']).reset_index(drop=True)
assert (T0.V_entrada == t0.V_entrada).all() and (T0.em_risco == t0.em_risco).all(), 'reconstrucao nao reproduz o painel'

alvo = r[r.natureza_1o_doc == 'andamento'].CD_CVM
anos = base.copy(); anos.loc[anos.index.isin(alvo)] -= 1
P, T = reconstroi(anos)
print(f'firmas com primeiro documento de andamento no painel: {int(alvo.isin(c.CD_CVM).sum())}')
print(f'celulas de entrada alteradas: {int((T.V_entrada != t0.V_entrada).sum())} | entradas {int(T.V_entrada.sum())} | risco {int(T.em_risco.sum())}')

os.makedirs(f'{OUT}/dados', exist_ok=True)
for f in os.listdir(D):
    if f.endswith('.csv') and f not in ('painel_completo.csv', 'painel_transicao.csv'):
        shutil.copy(f'{D}/{f}', f'{OUT}/dados')
P.to_csv(f'{OUT}/dados/painel_completo.csv', index=False); T.to_csv(f'{OUT}/dados/painel_transicao.csv', index=False)
for s in ['01_pipeline_sem_vazamento.py', '02_inferencia_bootstrap.py', '13_puros_e_perfil.py']:
    shutil.copy(s, OUT)
env = dict(os.environ, DADOS=f'{OUT}/dados')
for s in ['01_pipeline_sem_vazamento.py', '02_inferencia_bootstrap.py', '13_puros_e_perfil.py']:
    print(f'\n== {s} (RJ antecipada)'); sys.stdout.flush()
    subprocess.run([sys.executable, s], cwd=OUT, env=env, check=True)
