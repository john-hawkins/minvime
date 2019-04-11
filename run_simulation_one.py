import pandas as pd
import estimator as esti # The file estimator.py

tps = [20000,10000,8000,6000,4000,2000,1000,500]
fps = [-1000,-900,-800,-600,-500,-400,-200,-100]

tn = 0
fn = 0
minroi = 10000
cases = 100000
baserate = 0.001

rez = pd.DataFrame()

for tp in tps:
    for fp in fps:
        auc, prec, recall = esti.estimate_model_requirements(tp=tp, fp=fp, tn=tn, fn=fn, cases=cases, baserate=baserate, minroi=minroi)
        rez = rez.append({'tp':tp, 'fp':fp, 'auc':auc}, ignore_index=True)

print(rez)

