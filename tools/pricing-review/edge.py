import random, math, statistics as stt, simq, collections
def path(seed, W=52):
    S, reg, a1, a2 = simq.S_START, "chop", 0.58, 0.76
    out=[]
    for k in range(1,W+1):
        rng=random.Random(seed*1000+k)
        probs=simq.TRANS[reg]; reg=rng.choices(list(probs),weights=list(probs.values()))[0]
        p=simq.REG[reg]; s0=S; cl=[]; i1=[a1]; i2=[a2]
        for _ in range(5):
            u=p['mu']+p['sig']*simq.t_draw(rng); r=3*u-simq.DRAG
            S=max(0.5,S*max(0.3,1+r)); g=rng.gauss(0,0.02)
            i1.append(min(1.3,max(0.35,p['iv']+2.5*max(0,-r)+g)))
            i2.append(min(1.7,max(0.5,simq.REG2_IV[reg]+3.0*max(0,-r)+g)))
            cl.append(round(S,2))
        S=cl[-1]; a1,a2=i1[-1],i2[-1]
        out.append((reg,s0,cl,i1,i2))
    return out
def bid(S,K,td,iv,v2):
    simq.SKEW_V2=v2; simq.SPREAD_V2=v2
    return simq.quote(S,K,td/252,iv,'P')[0]
CUSH=[0.05,0.10,0.15,0.20]
acc={(v,ph,c):[0,0,0] for v in ('v1','v2') for ph in ('Mon','Wed') for c in CUSH}  # premium, payout, collateral
byreg=collections.defaultdict(lambda:[0,0,0])
rv=collections.defaultdict(list); ivr=collections.defaultdict(lambda:[[],[]])
rng=random.Random(7)
for s in range(400):
    for reg,s0,cl,i1,i2 in path(rng.randrange(10**8,10**9)):
        S5=cl[4]
        rets=[math.log(cl[0]/s0)]+[math.log(cl[i]/cl[i-1]) for i in range(1,5)]
        rv[reg].append(stt.pstdev(rets)*math.sqrt(252)); 
        ivr[reg][0].append(i1[3]); ivr[reg][1].append(i2[3])
        for ph,S,td,j in (('Mon',s0,5,0),('Wed',cl[2],2,3)):
            for c in CUSH:
                K=round(S*(1-c)*2)/2
                pay=max(0,K-S5)
                for v,ivv,v2 in (('v1',i1[j],False),('v2',i2[j],True)):
                    b=bid(S,K,td,ivv,v2)
                    a=acc[(v,ph,c)]; a[0]+=b; a[1]+=pay; a[2]+=K
                    if ph=='Mon' and c==0.15: x=byreg[(v,reg)]; x[0]+=b; x[1]+=pay; x[2]+=K
print('Realized vs implied vol by regime (Wed IV, i.e. regime known):')
for reg in simq.REG:
    print(f"  {reg:8s} realized {stt.mean(rv[reg]):.0%}  v1 IV {stt.mean(ivr[reg][0]):.0%}  v2 IV {stt.mean(ivr[reg][1]):.0%}  n={len(rv[reg])}")
print('\nPut seller edge, held to Friday (premium at bid minus payout), % of collateral per week:')
print('phase cushion | v1 prem  v1 payout  v1 edge | v2 prem  v2 payout  v2 edge | v2 prem/payout')
for ph in ('Mon','Wed'):
    for c in CUSH:
        r1=acc[('v1',ph,c)]; r2=acc[('v2',ph,c)]
        f=lambda r:(r[0]/r[2]*100,r[1]/r[2]*100,(r[0]-r[1])/r[2]*100)
        a,b,e=f(r1); a2,b2,e2=f(r2)
        print(f"{ph} {c:.0%}      | {a:.3f}%  {b:.3f}%  {e:+.3f}% | {a2:.3f}%  {b2:.3f}%  {e2:+.3f}% | {r2[0]/max(r2[1],1e-9):.2f}x")
print('\nMonday 15%-cushion put by regime (edge % collateral):')
for reg in simq.REG:
    x1=byreg[('v1',reg)]; x2=byreg[('v2',reg)]
    print(f"  {reg:8s} v1 {(x1[0]-x1[1])/x1[2]*100:+.3f}%  v2 {(x2[0]-x2[1])/x2[2]*100:+.3f}%  v2 prem/payout {x2[0]/max(x2[1],1e-9):.2f}x")
