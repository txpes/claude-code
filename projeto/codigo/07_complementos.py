import pandas as pd, numpy as np, pickle, warnings
from scipy.stats import ks_2samp
warnings.filterwarnings('ignore')
exec(open('01_pipeline_sem_vazamento.py').read().split("out = {}")[0])
N=pickle.load(open('N.pkl','rb'))
# validacao minskyana: escores de 8 e de 7 indicadores (painel completo; exercicio descritivo, sem avaliacao preditiva)
d=P.copy(); d['c1']=(d.COB<1).astype(int); d['ponzi']=((d.c1==1)&(d.groupby('CD_CVM')['c1'].shift(1)==1)).astype(int)
for lab,cols in [('8',IND),('7',[c for c in IND if c!='COB'])]:
    X=d[cols].astype(float).copy()
    for c in [c for c in NEG if c in cols]: X[c]=-X[c]
    Z=(X-X.mean())/X.std(ddof=1); ev,vec=np.linalg.eigh(np.corrcoef(Z.values,rowvar=False)); o=np.argsort(ev)[::-1]
    v=vec[:,o][:,0]; v=v if v.sum()>0 else -v; s=Z.values@v
    N[f'mk{lab}_pz']=s[d.ponzi.values==1].mean(); N[f'mk{lab}_np']=s[d.ponzi.values==0].mean()
    N[f'mk{lab}_ks']=ks_2samp(s[d.ponzi.values==1],s[d.ponzi.values==0]).statistic; N[f'mk{lab}_auc']=auc(s,d.ponzi.values)
N['pz_n']=int(d.ponzi.sum()); N['pz_pct']=d.ponzi.mean()
# sobreviventes: ROA
A=pickle.load(open('blocoA.pkl','rb')); E,y,pred=A[1]['ref']
ult=P.groupby('CD_CVM').ano.max(); ativas=set(ult[ult==P.ano.max()].index); k=E.CD_CVM.isin(ativas).values
S=E[k]; ys=S.V1.values.astype(int); N['sv_ROA']=auc(-S.ROA.values,ys)
# winsorizacao dos oito indicadores dentro das particoes, escore avaliado fora da amostra
fm=folds(P.CD_CVM.values,5,1); Pf=P.CD_CVM.map(fm).values; Ef=E.CD_CVM.map(fm).values; fw=np.zeros(len(E))
for j in range(5):
    tr=orient(P[Pf!=j]); lo,hi=tr.quantile(.01),tr.quantile(.99); trw=tr.clip(lo,hi,axis=1)
    mu,sd=trw.mean(),trw.std(ddof=1); Z=(trw-mu)/sd
    ev,vec=np.linalg.eigh(np.corrcoef(Z.values,rowvar=False)); o=np.argsort(ev)[::-1]; v=vec[:,o][:,0]; v=v if v.sum()>0 else -v
    te=orient(E[Ef==j]).clip(lo,hi,axis=1); fw[Ef==j]=((te-mu)/sd).values@v
N['wins_auc']=auc(fw,y)
Xw=orient(P).clip(orient(P).quantile(.01),orient(P).quantile(.99),axis=1); Zw=(Xw-Xw.mean())/Xw.std(ddof=1)
eww=np.sort(np.linalg.eigvalsh(np.corrcoef(Zw.values,rowvar=False)))[::-1]
N['wins_cp1']=eww[0]/8; N['wins_acum3']=eww[:3].sum()/8; N['wins_kaiser']=int((eww>1).sum())
pickle.dump(N,open('N.pkl','wb'))
for k_ in ['mk8_pz','mk8_np','mk8_ks','mk8_auc','mk7_pz','mk7_np','mk7_ks','mk7_auc','pz_n','pz_pct','sv_ROA','wins_auc','wins_cp1','wins_acum3','wins_kaiser']:
    print(f'{k_:12s} {N[k_]}')
print('\nvalores de referencia h=1 (4 casas):', {m: round(N[f"{m}1"],4) for m in ['F','PLS','GB','BA','COB','ROA','LC','ALV']})
