import edge, simq
from edge import path, bid
P=path(865529296)
print('cushion | v2 net 52w (W1-26 / W27-52) | v1 net 52w | losing weeks v2 | worst week v2')
for c in (0.10,0.15,0.20):
    res={}
    for v,v2 in (('v1',False),('v2',True)):
        wk=[]
        for reg,s0,cl,i1,i2 in P:
            K=round(s0*(1-c)*2)/2
            b=bid(s0,K,5,(i2 if v2 else i1)[0],v2)
            wk.append((b-max(0,K-cl[4]))*100)
        res[v]=wk
    w2=res['v2']
    print(f"{c:.0%}     | ${sum(w2):,.0f} (${sum(w2[:26]):,.0f} / ${sum(w2[26:]):,.0f}) | ${sum(res['v1']):,.0f} | {sum(x<0 for x in w2)} | ${min(w2):,.0f}")
