import json, simq
st=json.load(open('/home/claude/simq-sim/run-002-state.json')); ev=st['events']
simq.BASE_SEED=st['seed']; simq.RESEED={}
def ivs(w,v2):
    simq.PRICING_V2_FROM = 1 if v2 else 999
    return simq.gen_week(w)
def q(S,K,td,iv,kind,v2):
    simq.SKEW_V2=v2; simq.SPREAD_V2=v2
    return simq.quote(S,K,td/252,iv,kind)
trades=[]; 
for e in ev:
    if e['t']=='sell':
        trades.append(dict(e)) 
    elif e['t']=='btc': trades[e['id']-1]['btc']=e['price']
tot={'v2':[0,0],'v1':[0,0]}; rows=[]
for t in trades:
    w=t['w']; mid=t['ph']=='mid'
    out={}
    for v2 in (True,False):
        reg,s0,cl,iv=ivs(w,v2)
        S=cl[2] if mid else s0; ivv=iv[3] if mid else iv[0]; td=2 if mid else 5
        bid,ask=q(S,t['k'],td,ivv,t['kind'],v2)
        bb=0
        if 'btc' in t:
            # buy-back happened at Wednesday close (only midweek closes exist)
            _,a2=q(cl[2],t['k'],2,iv[3],t['kind'],v2); bb=a2
        out['v2' if v2 else 'v1']=(bid,bb)
    # sanity: v2 recompute equals recorded fill
    assert abs(out['v2'][0]-t['fill'])<0.006,(t,out)
    if 'btc' in t: assert abs(out['v2'][1]-t['btc'])<0.006,(t,out)
    for k in out: tot[k][0]+=out[k][0]*100; tot[k][1]+=out[k][1]*100
    rows.append((w,t['ph'],t['kind'],t['k'],out['v2'],out['v1']))
for k,(p,b) in tot.items(): print(k,'premium',round(p),'buybacks',round(b),'net',round(p-b))
for half,(lo,hi) in (('W1-26',(1,26)),('W27-52',(27,52))):
    for k in ('v2','v1'):
        i=0 if k=='v2' else 1
        p=sum(r[4+i][0] for r in rows if lo<=r[0]<=hi)*100; b=sum(r[4+i][1] for r in rows if lo<=r[0]<=hi)*100
        print(half,k,round(p),round(b),round(p-b))
nob=sum(1 for r in rows if r[5][0]<=0); print('trades with no bid under v1:',nob)
ratio=[r[5][0]/r[4][0] for r in rows if r[4][0]>0]
import statistics; print('median v1/v2 premium ratio',round(statistics.median(ratio),2))
for kind in 'PC':
    rr=[r[5][0]/r[4][0] for r in rows if r[2]==kind and r[4][0]>0]; print(kind,round(statistics.median(rr),2),len(rr))
