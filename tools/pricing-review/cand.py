import random, math, statistics as st, simq, collections
RV={r:3*p['sig']*math.sqrt(252) for r,p in simq.REG.items()}
def run(base, seeds=300, bump=3.0):
    acc=collections.defaultdict(lambda:[0,0,0]); ivm=collections.defaultdict(list)
    rng=random.Random(5)
    for _ in range(seeds):
        seed=rng.randrange(10**8,10**9); S,reg,a=simq.S_START,'chop',base['chop']
        for k in range(1,53):
            r_=random.Random(seed*1000+k); probs=simq.TRANS[reg]; reg=r_.choices(list(probs),weights=list(probs.values()))[0]
            p=simq.REG[reg]; s0=S; cl=[]; iv=[a]
            for _ in range(5):
                u=p['mu']+p['sig']*simq.t_draw(r_); r=3*u-simq.DRAG; S=max(.5,S*max(.3,1+r)); g=r_.gauss(0,.02)
                iv.append(min(1.7,max(.4,base[reg]+bump*max(0,-r)+g))); cl.append(round(S,2))
            S=cl[-1]; a=iv[-1]; ivm[reg].append(iv[3])
            simq.SKEW_V2=simq.SPREAD_V2=True
            for ph,Sx,td,j in (('Mon',s0,5,0),('Wed',cl[2],2,3)):
                for c in (0.10,0.15):
                    K=round(Sx*(1-c)*2)/2; b=simq.quote(Sx,K,td/252,iv[j],'P')[0]; pay=max(0,K-cl[4])
                    for key in ((ph,c),(ph,c,reg)):
                        x=acc[key]; x[0]+=b; x[1]+=pay; x[2]+=K
    return acc,ivm
def show(name,base):
    acc,ivm=run(base)
    print(f"== {name}: " + ", ".join(f"{r} {base[r]:.2f}" for r in base))
    print("   Wed IV / theoretical realized: " + ", ".join(f"{r} {st.mean(ivm[r])/RV[r]:.2f}x" for r in simq.REG))
    for ph in ('Mon','Wed'):
        for c in (0.10,0.15):
            x=acc[(ph,c)]; print(f"   {ph} {c:.0%}: edge {(x[0]-x[1])/x[2]*100:+.3f}%/wk  prem/payout {x[0]/x[1]:.2f}x  | by regime: " + ", ".join(f"{r} {(acc[(ph,c,r)][0]-acc[(ph,c,r)][1])/acc[(ph,c,r)][2]*100:+.2f}%" for r in simq.REG))
print("theoretical realized vol:", {r:round(v,3) for r,v in RV.items()})
#show("v2", simq.REG2_IV)
# v3 candidate: IV ~ realized x real-world ratio (calm 1.20, chop 1.20, rebound 1.15, selloff 1.05, crash 1.00), net of avg down-day bump
#show("v3a", {"calm_up":0.49,"chop":0.70,"selloff":0.92,"crash":1.05,"rebound":0.95})
show("v3b", {"calm_up":0.54,"chop":0.75,"selloff":0.92,"crash":1.05,"rebound":0.95})
