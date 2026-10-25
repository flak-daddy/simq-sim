import random, statistics as st
from edgelib import path, bid
def mech(seed,c,v2=True):
    tot=0
    for reg,s0,cl,i1,i2 in path(seed):
        K=round(s0*(1-c)*2)/2
        tot+=(bid(s0,K,5,(i2 if v2 else i1)[0],v2)-max(0,K-cl[4]))*100
    return tot
rng=random.Random(11); seeds=[rng.randrange(10**8,10**9) for _ in range(600)]
for c,run2 in ((0.10,2615),(0.15,1563)):
    xs=sorted(mech(s,c) for s in seeds)
    pct=sum(x<run2 for x in xs)/len(xs)
    print(f"{c:.0%}: median ${st.median(xs):,.0f}, mean ${st.mean(xs):,.0f}, 10th ${xs[60]:,.0f}, 90th ${xs[540]:,.0f}, share of years losing {sum(x<0 for x in xs)/len(xs):.0%}; Run 2 path ${run2:,} = {pct:.0%} percentile")
