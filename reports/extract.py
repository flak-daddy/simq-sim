import json, re, subprocess, sys
sys.path.insert(0,'/home/claude/simq-sim')
import simbook
st=json.load(open('/home/claude/simq-sim/run-002-state.json')); ev=st['events']
trades=[]
for e in ev:
    if e['t']=='sell':
        trades.append(dict(id=len(trades)+1,w=e['w'],ph=e['ph'],kind=e['kind'],k=e['k'],fill=e['fill'],ask=e['ask'],spot=e['spot'],out=None))
    elif e['t']=='btc':
        t=trades[e['id']-1]; t.update(out='btc',close=e['price'],close_w=e['w'],close_ph=e['ph'])
    elif e['t'] in('expire','assign','called'):
        t=trades[e['id']-1]; t.update(out=e['t'],close_w=e['w'],close_spot=e['spot'])
# ledger regime table
rows={}
for line in open('/home/claude/simq-sim/run-002-ledger.md'):
    m=re.match(r'\| (\d+) \| (calm_up|chop|selloff|crash|rebound) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| ([+-][\d.]+)% \| ([\d.]+)',line)
    if m:
        g=m.groups(); rows[int(g[0])]=dict(regime=g[1],open=float(g[2]),mon=float(g[3]),tue=float(g[4]),wed=float(g[5]),thu=float(g[6]),fri=float(g[7]),wkpct=float(g[8]),interest=float(g[9]))
weeks=[]
for w in range(1,53):
    out=subprocess.run(['python3','simbook.py','weekpnl',str(w)],capture_output=True,text=True,cwd='/home/claude/simq-sim').stdout
    m=re.search(r'\$([\d,]+\.\d\d) -> \$([\d,]+\.\d\d)',out)
    a,b=[float(x.replace(',','')) for x in m.groups()]
    sh=re.search(r'\| Shares \|[^|]*\| ([+-])\$([\d,]+\.\d\d)',out)
    shares=(1 if sh and sh.group(1)=='+' else -1)*float(sh.group(2).replace(',','')) if sh else 0.0
    passes=[e['ph'] for e in ev if e['t']=='pass' and e['w']==w]
    weeks.append(dict(w=w,start=a,end=b,shares=shares,passes=passes,**rows[w]))
json.dump(dict(trades=trades,weeks=weeks),open('/home/claude/simq-report/data.json','w'),indent=1)
print(len(trades),len(weeks)); print(weeks[0]); print(weeks[31]); print(trades[0],trades[-1])
