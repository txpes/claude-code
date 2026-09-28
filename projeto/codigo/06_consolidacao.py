import pandas as pd, numpy as np, pickle, warnings
warnings.filterwarnings('ignore')
exec(open('01_pipeline_sem_vazamento.py').read().split("out = {}")[0])
A=pickle.load(open('blocoA.pkl','rb')); D=pd.read_csv('blocoD.csv')
EF=pickle.load(open('blocoEF.pkl','rb')); R=pickle.load(open('robustez.pkl','rb'))
N={}
for h in (1,2):
    E,y,pred=A[h]['ref']; N[f'n{h}']=len(y); N[f'ev{h}']=int(y.sum()); N[f'fi{h}']=E.CD_CVM.nunique()
    for m in ['F','PLS','GB','BA','COB','ROA','LC','ALV']:
        N[f'{m}{h}']=auc(pred[m],y); a=np.array(A[h]['res'][m]); N[f'{m}{h}_mu']=a.mean(); N[f'{m}{h}_sd']=a.std(ddof=1)
for _,r in D.iterrows():
    k=r.comparacao.split(' vs ')[0]+('_COB' if r.comparacao=='GB vs COB' else '')+str(int(r.h))
    N['d_'+k]=r.dif; N['lo_'+k]=r.lo; N['hi_'+k]=r.hi; N['p_'+k]=r.p_boot; N['pb_'+k]=r.p_bonf; N['pd_'+k]=r.p_delong
pickle.dump(N,open('N.pkl','wb'))
for k in sorted(N): print(f'{k:14s} {N[k]:.4f}' if isinstance(N[k],float) else f'{k:14s} {N[k]}')
# ---- PCA intrafirma, fora da amostra, media historica da firma apenas ate t (sem informacao futura)
E,y,pred=A[1]['ref']; fm=folds(P.CD_CVM.values,5,1); Pf=P.CD_CVM.map(fm).values; Ef=E.CD_CVM.map(fm).values
X=orient(P); Xw=X-X.groupby(P.CD_CVM.values).transform(lambda s: s.expanding().mean())
Ew=E[['CD_CVM','ano']].merge(pd.concat([P[['CD_CVM','ano']],Xw],axis=1),on=['CD_CVM','ano'],how='left')[IND]
fw=np.zeros(len(E))
for j in range(5):
    tr=Xw[Pf!=j]; mu,sd=tr.mean(),tr.std(ddof=1); Z=(tr-mu)/sd
    ev,vec=np.linalg.eigh(np.corrcoef(Z.values,rowvar=False)); o=np.argsort(ev)[::-1]; v=vec[:,o][:,0]; v=v if v.sum()>0 else -v
    fw[Ef==j]=((Ew[Ef==j]-mu)/sd).values@v
print(f'\nPCA intrafirma fora da amostra, media ate t: {auc(fw,y):.4f}')
pickle.dump({'within':auc(fw,y)},open('within2.pkl','wb'))
# ---- Figura 2 a partir das predicoes limpas
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'serif','font.serif':['DejaVu Serif'],'font.size':9,'axes.grid':True,'grid.alpha':.25,
    'grid.linewidth':.5,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':200})
def roc(x,yy):
    o=np.argsort(-x); yy=yy[o]; return np.r_[0,np.cumsum(1-yy)/(1-yy).sum()],np.r_[0,np.cumsum(yy)/yy.sum()]
fig,ax=plt.subplots(figsize=(4.3,4.1))
for nm,k,c,ls in [('Cobertura de juros','COB','#b03030','--'),('Árvores impulsionadas','GB','#7a5195','-.'),
                  ('Mínimos quadrados parciais','PLS','#2e7d32','-'),('Componentes principais','F','#1f3a5f','-')]:
    f_,t_=roc(pred[k],y); ax.plot(f_,t_,color=c,ls=ls,lw=1.5,label=nm)
ax.plot([0,1],[0,1],color='#bbb',lw=.8); ax.set_xlabel('1 − especificidade'); ax.set_ylabel('Sensibilidade')
ax.legend(loc='lower right',fontsize=7.5,frameon=False); fig.tight_layout(); fig.savefig('fig2_roc_limpa.png',bbox_inches='tight'); plt.close()
print('figura 2 regenerada')
