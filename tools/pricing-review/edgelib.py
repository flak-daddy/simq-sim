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
