import json
from pathlib import Path

data = json.loads(Path("data.json").read_text())
data_json = json.dumps(data, separators=(",", ":"), ensure_ascii=False)

html = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Toll Road Financial Model · Dashboard</title>
<style>
:root{
  --bg-0:#0b0608;--bg-1:#140a0d;--bg-2:#1d1013;--bg-3:#2a171c;
  --line:#3a1f25;--line-strong:#552830;
  --red-1:#ff3955;--red-2:#e21a3c;--red-3:#b01228;--red-4:#6e0a18;
  --red-glow:rgba(255,57,85,.35);
  --accent:#ffb5bf;--accent-2:#ff8895;
  --gold:#ffc46b;--teal:#5ad1c3;--violet:#b58bff;
  --fg-0:#ffeef1;--fg-1:#d9c3c8;--fg-2:#9d8288;--fg-3:#6a5458;
  --pos:#34d399;--neg:#ff5e7a;
  --radius:14px;
  --font: ui-sans-serif,-apple-system,BlinkMacSystemFont,"SF Pro Text","Inter","Noto Sans TC","Helvetica Neue",sans-serif;
  --mono: ui-monospace,SFMono-Regular,"JetBrains Mono",Menlo,monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:var(--bg-0);color:var(--fg-0);font-family:var(--font);-webkit-font-smoothing:antialiased;overflow-x:hidden}
body{
  background:
    radial-gradient(1200px 600px at 85% -10%,rgba(226,26,60,.18),transparent 60%),
    radial-gradient(900px 500px at -10% 20%,rgba(176,18,40,.12),transparent 60%),
    linear-gradient(180deg,#0b0608 0%,#0a0507 100%);
  min-height:100vh;
}
.wrap{max-width:1440px;margin:0 auto;padding:clamp(16px,3vw,36px)}
header.topbar{
  display:flex;align-items:center;justify-content:space-between;gap:20px;
  padding-bottom:20px;border-bottom:1px solid var(--line);margin-bottom:28px;flex-wrap:wrap;
}
.brand{display:flex;align-items:center;gap:14px}
.logo{
  width:44px;height:44px;border-radius:12px;
  background:linear-gradient(135deg,var(--red-2),var(--red-4));
  display:grid;place-items:center;color:#fff;font-weight:800;font-size:20px;
  box-shadow:0 8px 24px -6px var(--red-glow),inset 0 1px 0 rgba(255,255,255,.2);
  position:relative;
}
.logo::after{content:"";position:absolute;inset:0;border-radius:inherit;border:1px solid rgba(255,255,255,.08)}
.brand h1{font-size:clamp(16px,1.6vw,20px);font-weight:700;letter-spacing:.2px}
.brand .sub{font-size:12px;color:var(--fg-2);margin-top:2px;font-family:var(--mono);text-transform:uppercase;letter-spacing:2px}
.meta{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.pill{
  font-size:11px;letter-spacing:1.5px;text-transform:uppercase;
  padding:8px 14px;border-radius:999px;background:var(--bg-2);border:1px solid var(--line);
  color:var(--fg-1);font-family:var(--mono);
}
.pill.live{color:var(--red-1);border-color:var(--red-4)}
.pill.live::before{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--red-1);margin-right:8px;vertical-align:middle;box-shadow:0 0 10px var(--red-1);animation:pulse 1.6s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}

/* Sections */
section{margin-bottom:36px}
h2.section-title{
  font-size:13px;letter-spacing:3px;text-transform:uppercase;color:var(--fg-2);
  font-family:var(--mono);margin-bottom:14px;display:flex;align-items:center;gap:12px;
}
h2.section-title::before{content:"";display:inline-block;width:4px;height:14px;background:var(--red-2);border-radius:2px}
h2.section-title .hint{margin-left:auto;font-size:11px;color:var(--fg-3);text-transform:none;letter-spacing:.5px;font-family:var(--font)}

/* KPI grid */
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}
.kpi{
  position:relative;overflow:hidden;
  background:linear-gradient(180deg,var(--bg-2),var(--bg-1));
  border:1px solid var(--line);border-radius:var(--radius);padding:18px;
  transition:transform .2s ease, border-color .2s ease;
}
.kpi:hover{transform:translateY(-2px);border-color:var(--line-strong)}
.kpi.primary{
  background:linear-gradient(135deg,rgba(226,26,60,.18),rgba(110,10,24,.25));
  border-color:var(--red-4);
  box-shadow:0 10px 30px -12px var(--red-glow);
}
.kpi .label{font-size:11px;text-transform:uppercase;letter-spacing:2px;color:var(--fg-2);font-family:var(--mono)}
.kpi .value{font-size:clamp(22px,2.4vw,30px);font-weight:700;margin-top:10px;line-height:1.1;letter-spacing:-.5px;font-feature-settings:"tnum"}
.kpi .value small{font-size:.55em;font-weight:500;color:var(--fg-2);margin-left:4px}
.kpi .trend{display:inline-flex;align-items:center;gap:4px;margin-top:10px;font-size:12px;color:var(--pos);font-family:var(--mono)}
.kpi .trend.neg{color:var(--neg)}
.kpi::after{
  content:"";position:absolute;right:-30px;top:-30px;width:120px;height:120px;
  background:radial-gradient(circle,var(--red-glow),transparent 70%);
  pointer-events:none;opacity:.5;
}

/* Cards grid */
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:18px}
.card{
  background:linear-gradient(180deg,var(--bg-2),var(--bg-1));
  border:1px solid var(--line);border-radius:var(--radius);padding:20px;
  min-width:0;overflow:hidden;
}
.card h3{font-size:14px;font-weight:600;margin-bottom:4px}
.card .desc{font-size:12px;color:var(--fg-2);margin-bottom:14px}
.card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:14px;flex-wrap:wrap}
.card-head .tag{
  font-size:10px;font-family:var(--mono);letter-spacing:1.5px;text-transform:uppercase;
  padding:4px 8px;border-radius:6px;background:var(--bg-3);color:var(--accent);border:1px solid var(--line-strong);
}
.span-6{grid-column:span 6}
.span-12{grid-column:span 12}
.span-4{grid-column:span 4}
.span-8{grid-column:span 8}

@media(max-width:1100px){
  .span-6,.span-4,.span-8{grid-column:span 12}
}

/* Chart */
.chart{width:100%;height:auto;display:block}
.chart text{fill:var(--fg-2);font-family:var(--mono);font-size:10px}
.chart .axis-label{fill:var(--fg-3);font-size:9px;letter-spacing:1px;text-transform:uppercase}
.chart .grid-line{stroke:var(--line);stroke-width:1;stroke-dasharray:2 3}
.chart .axis{stroke:var(--line-strong);stroke-width:1}
.legend{display:flex;flex-wrap:wrap;gap:14px;margin-top:12px;font-size:12px;color:var(--fg-1)}
.legend-item{display:flex;align-items:center;gap:6px;font-family:var(--mono)}
.legend-swatch{width:10px;height:10px;border-radius:2px}

/* Donut */
.donut-wrap{display:flex;align-items:center;gap:24px;flex-wrap:wrap}
.donut-wrap svg{flex:0 0 auto}
.donut-legend{flex:1;min-width:160px;display:flex;flex-direction:column;gap:10px}
.donut-legend .item{display:flex;justify-content:space-between;align-items:center;gap:10px;padding-bottom:8px;border-bottom:1px dashed var(--line)}
.donut-legend .lbl{display:flex;align-items:center;gap:8px;font-size:13px}
.donut-legend .val{font-family:var(--mono);font-size:13px;color:var(--fg-0);font-weight:600}

/* Assumptions table */
.assump{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:8px 18px}
.assump .row{display:flex;justify-content:space-between;align-items:baseline;gap:10px;padding:10px 0;border-bottom:1px dashed var(--line);font-size:13px}
.assump .k{color:var(--fg-1)}
.assump .v{font-family:var(--mono);color:var(--accent);font-weight:600;text-align:right;white-space:nowrap}

/* Tooltip */
.tt{
  position:fixed;pointer-events:none;background:rgba(10,5,7,.96);
  border:1px solid var(--red-4);border-radius:8px;padding:8px 12px;font-size:12px;
  font-family:var(--mono);color:var(--fg-0);transform:translate(-50%,-120%);
  white-space:nowrap;opacity:0;transition:opacity .12s ease;z-index:100;
  box-shadow:0 10px 30px -6px rgba(0,0,0,.6);
}
.tt.show{opacity:1}
.tt .yr{color:var(--fg-2);font-size:10px;letter-spacing:1px;margin-bottom:4px;text-transform:uppercase}
.tt .ln{display:flex;justify-content:space-between;gap:12px}
.tt .ln b{color:var(--fg-0)}
.tt .sw{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:6px;vertical-align:middle}

footer{margin-top:40px;padding-top:20px;border-top:1px solid var(--line);font-size:11px;color:var(--fg-3);font-family:var(--mono);display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}

/* Accent decorations */
.accent-bar{height:2px;background:linear-gradient(90deg,transparent,var(--red-2),transparent);margin:6px 0 18px}
</style>
</head>
<body>
<div class="wrap">
  <header class="topbar">
    <div class="brand">
      <div class="logo">R</div>
      <div>
        <h1>Toll Road Concession · Financial Model</h1>
        <div class="sub">Base Case Scenario · 40-Year Projection</div>
      </div>
    </div>
    <div class="meta">
      <span class="pill live">Live Model</span>
      <span class="pill">GBP £</span>
      <span class="pill">Fiscal Yr 1–40</span>
    </div>
  </header>

  <section>
    <h2 class="section-title">Key Performance Indicators <span class="hint">Internal rates & capital structure</span></h2>
    <div class="kpi-grid" id="kpi-grid"></div>
  </section>

  <section>
    <h2 class="section-title">Capital Structure & Funding</h2>
    <div class="grid">
      <div class="card span-6">
        <div class="card-head">
          <div>
            <h3>Sources of Funds</h3>
            <div class="desc">Debt vs Equity split of total project financing</div>
          </div>
          <span class="tag">£ thousands</span>
        </div>
        <div id="donut-sources"></div>
      </div>
      <div class="card span-6">
        <div class="card-head">
          <div>
            <h3>Uses of Funds</h3>
            <div class="desc">Construction cost, fees & capitalized interest</div>
          </div>
          <span class="tag">£ thousands</span>
        </div>
        <div id="donut-uses"></div>
      </div>
    </div>
  </section>

  <section>
    <h2 class="section-title">Revenue & Traffic Projection</h2>
    <div class="grid">
      <div class="card span-8">
        <div class="card-head">
          <div>
            <h3>Nominal Revenue by Vehicle Class</h3>
            <div class="desc">Passenger Car (PC) and Heavy Vehicle (HV) revenue over the 40-year concession</div>
          </div>
          <span class="tag">k£ / year</span>
        </div>
        <div id="chart-revenue"></div>
      </div>
      <div class="card span-4">
        <div class="card-head">
          <div>
            <h3>Traffic Volumes</h3>
            <div class="desc">Annual vehicle throughput</div>
          </div>
          <span class="tag">vehicles / yr</span>
        </div>
        <div id="chart-traffic"></div>
      </div>
    </div>
  </section>

  <section>
    <h2 class="section-title">Profitability</h2>
    <div class="grid">
      <div class="card span-12">
        <div class="card-head">
          <div>
            <h3>EBITDA · EBIT · Net Profit</h3>
            <div class="desc">Earnings progression from operations start through concession end</div>
          </div>
          <span class="tag">k£ / year</span>
        </div>
        <div id="chart-profit"></div>
      </div>
    </div>
  </section>

  <section>
    <h2 class="section-title">Debt Service & Cash Flow</h2>
    <div class="grid">
      <div class="card span-6">
        <div class="card-head">
          <div>
            <h3>Debt Outstanding &amp; Annual Service</h3>
            <div class="desc">Senior debt amortization schedule</div>
          </div>
          <span class="tag">k£</span>
        </div>
        <div id="chart-debt"></div>
      </div>
      <div class="card span-6">
        <div class="card-head">
          <div>
            <h3>CFADS vs Dividends</h3>
            <div class="desc">Cash available for debt service and equity distributions</div>
          </div>
          <span class="tag">k£ / year</span>
        </div>
        <div id="chart-cashflow"></div>
      </div>
    </div>
  </section>

  <section>
    <h2 class="section-title">Balance Sheet Composition</h2>
    <div class="grid">
      <div class="card span-12">
        <div class="card-head">
          <div>
            <h3>Assets &amp; Financing Over Time</h3>
            <div class="desc">Fixed asset depreciation, cash build-up, debt paydown, and equity stability</div>
          </div>
          <span class="tag">k£</span>
        </div>
        <div id="chart-bs"></div>
      </div>
    </div>
  </section>

  <section>
    <h2 class="section-title">Input Assumptions</h2>
    <div class="card">
      <div id="assump-list" class="assump"></div>
    </div>
  </section>

  <footer>
    <div>Financial Model Dashboard · Fintech visualization · rendered locally</div>
    <div>Source: Financial_Model.xlsx · Base Case</div>
  </footer>
</div>

<div class="tt" id="tooltip"></div>

<script id="data" type="application/json">__DATA__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const YEARS = D.years;
const fmt = {
  num: n => {
    if (n == null || !isFinite(n)) return '—';
    const a = Math.abs(n);
    if (a >= 1e6) return (n/1e6).toFixed(2)+'M';
    if (a >= 1e3) return (n/1e3).toFixed(1)+'K';
    if (a >= 100) return n.toFixed(0);
    return n.toFixed(2);
  },
  money: n => '£'+fmt.num(n),
  pct: n => (n*100).toFixed(2)+'%',
  int: n => Math.round(n).toLocaleString(),
};

/* ---------- KPIs ---------- */
const K = D.kpis;
const kpis = [
  {lbl:'Project IRR', val: fmt.pct(K.project_irr), primary:true, sub:'Unlevered return'},
  {lbl:'Equity IRR', val: fmt.pct(K.equity_irr), primary:true, sub:'Levered return to sponsors'},
  {lbl:'Total Uses', val: '£'+(K.total_uses/1000).toFixed(1)+'M', sub:'Fully funded'},
  {lbl:'Senior Debt', val: '£'+(K.total_debt/1000).toFixed(1)+'M', sub:(K.total_debt/K.total_uses*100).toFixed(1)+'% gearing'},
  {lbl:'Sponsor Equity', val: '£'+(K.total_equity/1000).toFixed(1)+'M', sub:(K.total_equity/K.total_uses*100).toFixed(1)+'% equity'},
  {lbl:'Concession', val: K.concession_duration+' yrs', sub: K.construction_duration+' construction + '+K.operations_duration+' ops'},
  {lbl:'Peak Revenue', val: '£'+(K.peak_revenue/1000).toFixed(1)+'M', sub:'Year 40 nominal'},
  {lbl:'Lifetime Dividends', val: '£'+(K.total_dividends/1000).toFixed(1)+'M', sub:'Cumulative to equity'},
];
document.getElementById('kpi-grid').innerHTML = kpis.map(k=>`
  <div class="kpi ${k.primary?'primary':''}">
    <div class="label">${k.lbl}</div>
    <div class="value">${k.val}</div>
    <div class="trend">${k.sub||''}</div>
  </div>
`).join('');

/* ---------- Tooltip ---------- */
const TT = document.getElementById('tooltip');
function showTT(x,y,html){TT.innerHTML=html;TT.style.left=x+'px';TT.style.top=y+'px';TT.classList.add('show');}
function hideTT(){TT.classList.remove('show');}

/* ---------- SVG helpers ---------- */
const NS='http://www.w3.org/2000/svg';
function el(n,a={}){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);return e;}

function niceMax(v){
  if (v<=0) return 1;
  const p = Math.pow(10, Math.floor(Math.log10(v)));
  const n = v/p;
  let m;
  if (n<=1) m=1; else if (n<=2) m=2; else if (n<=5) m=5; else m=10;
  return m*p;
}
function niceMin(v){ if (v>=0) return 0; return -niceMax(-v); }

/* ---------- Line chart (multi-series, with hover crosshair) ---------- */
function lineChart(containerId, series, opts={}){
  const host = document.getElementById(containerId);
  host.innerHTML = '';
  const W = 1000, H = opts.height||320;
  const pad = {t:20,r:20,b:34,l:56};
  const iw = W-pad.l-pad.r, ih = H-pad.t-pad.b;
  const allV = series.flatMap(s=>s.data);
  let vmax = niceMax(Math.max(...allV, 0));
  let vmin = niceMin(Math.min(...allV, 0));
  const xs = YEARS;
  const n = xs.length;
  const x = i => pad.l + (iw * (i/(n-1)));
  const y = v => pad.t + ih - (ih*(v-vmin)/(vmax-vmin));

  const svg = el('svg',{viewBox:`0 0 ${W} ${H}`, class:'chart', preserveAspectRatio:'xMidYMid meet'});
  // grid
  const gridSteps=5;
  for(let i=0;i<=gridSteps;i++){
    const val = vmin + (vmax-vmin)*i/gridSteps;
    const yy = y(val);
    svg.appendChild(el('line',{class:'grid-line',x1:pad.l,x2:W-pad.r,y1:yy,y2:yy}));
    const t = el('text',{x:pad.l-8,y:yy+3,'text-anchor':'end'});
    t.textContent = fmt.num(val);
    svg.appendChild(t);
  }
  // x axis labels (every 5 years)
  for(let i=0;i<n;i+=5){
    const xx = x(i);
    svg.appendChild(el('line',{class:'grid-line',x1:xx,x2:xx,y1:pad.t,y2:pad.t+ih}));
    const t = el('text',{x:xx,y:H-pad.b+14,'text-anchor':'middle'});
    t.textContent = 'Y'+xs[i];
    svg.appendChild(t);
  }
  // zero axis if relevant
  if (vmin<0 && vmax>0){
    svg.appendChild(el('line',{x1:pad.l,x2:W-pad.r,y1:y(0),y2:y(0),stroke:'#552830','stroke-width':1}));
  }
  // series
  series.forEach((s,si)=>{
    if (s.fill){
      let d = `M ${x(0)} ${y(0)}`;
      s.data.forEach((v,i)=>d += ` L ${x(i)} ${y(v)}`);
      d += ` L ${x(n-1)} ${y(0)} Z`;
      svg.appendChild(el('path',{d,fill:s.color,opacity:.14}));
    }
    let d = '';
    s.data.forEach((v,i)=>d += (i?' L ':'M ')+x(i)+' '+y(v));
    svg.appendChild(el('path',{d,fill:'none',stroke:s.color,'stroke-width':2.2,'stroke-linejoin':'round','stroke-linecap':'round',filter:s.glow?'drop-shadow(0 0 6px '+s.color+')':''}));
  });
  // hover overlay
  const overlay = el('rect',{x:pad.l,y:pad.t,width:iw,height:ih,fill:'transparent'});
  const cross = el('line',{x1:0,x2:0,y1:pad.t,y2:pad.t+ih,stroke:'#ff3955','stroke-width':1,'stroke-dasharray':'3 3',opacity:0});
  const dots = series.map(s=>el('circle',{r:4,fill:s.color,stroke:'#0b0608','stroke-width':2,opacity:0}));
  svg.appendChild(cross);
  dots.forEach(d=>svg.appendChild(d));
  svg.appendChild(overlay);
  overlay.addEventListener('mousemove',ev=>{
    const rect = svg.getBoundingClientRect();
    const sx = (ev.clientX - rect.left) * (W/rect.width);
    const idx = Math.max(0, Math.min(n-1, Math.round((sx-pad.l)/iw*(n-1))));
    cross.setAttribute('x1',x(idx));cross.setAttribute('x2',x(idx));cross.setAttribute('opacity',.8);
    series.forEach((s,si)=>{
      dots[si].setAttribute('cx',x(idx));dots[si].setAttribute('cy',y(s.data[idx]));dots[si].setAttribute('opacity',1);
    });
    const lines = series.map(s=>`<div class="ln"><span><span class="sw" style="background:${s.color}"></span>${s.name}</span><b>${fmt.num(s.data[idx])}</b></div>`).join('');
    showTT(ev.clientX, ev.clientY, `<div class="yr">Year ${xs[idx]}</div>${lines}`);
  });
  overlay.addEventListener('mouseleave',()=>{
    cross.setAttribute('opacity',0);
    dots.forEach(d=>d.setAttribute('opacity',0));
    hideTT();
  });
  host.appendChild(svg);
  // legend
  const lg = document.createElement('div');
  lg.className='legend';
  lg.innerHTML = series.map(s=>`<span class="legend-item"><span class="legend-swatch" style="background:${s.color}"></span>${s.name}</span>`).join('');
  host.appendChild(lg);
}

/* ---------- Stacked area (PC + HV revenue) ---------- */
function stackedArea(containerId, series, opts={}){
  const host = document.getElementById(containerId);
  host.innerHTML='';
  const W=1000,H=opts.height||340;
  const pad={t:20,r:20,b:34,l:60};
  const iw=W-pad.l-pad.r, ih=H-pad.t-pad.b;
  const n=YEARS.length;
  const totals = YEARS.map((_,i)=>series.reduce((s,se)=>s+se.data[i],0));
  const vmax = niceMax(Math.max(...totals,1));
  const x = i => pad.l + iw*(i/(n-1));
  const y = v => pad.t + ih - ih*(v/vmax);
  const svg = el('svg',{viewBox:`0 0 ${W} ${H}`,class:'chart',preserveAspectRatio:'xMidYMid meet'});
  for(let i=0;i<=5;i++){
    const v=vmax*i/5;
    const yy=y(v);
    svg.appendChild(el('line',{class:'grid-line',x1:pad.l,x2:W-pad.r,y1:yy,y2:yy}));
    const t=el('text',{x:pad.l-8,y:yy+3,'text-anchor':'end'});t.textContent=fmt.num(v);svg.appendChild(t);
  }
  for(let i=0;i<n;i+=5){
    const xx=x(i);
    const t=el('text',{x:xx,y:H-pad.b+14,'text-anchor':'middle'});t.textContent='Y'+YEARS[i];svg.appendChild(t);
  }
  // build stacks bottom->top
  const stack = series.map(()=>new Array(n).fill(0));
  for(let i=0;i<n;i++){
    let acc=0;
    series.forEach((s,si)=>{acc+=s.data[i];stack[si][i]=acc;});
  }
  // draw areas top->bottom
  for(let si=series.length-1;si>=0;si--){
    const s=series[si];
    const top = stack[si];
    const bot = si>0?stack[si-1]:new Array(n).fill(0);
    let d=`M ${x(0)} ${y(top[0])}`;
    for(let i=1;i<n;i++) d+=` L ${x(i)} ${y(top[i])}`;
    for(let i=n-1;i>=0;i--) d+=` L ${x(i)} ${y(bot[i])}`;
    d+=' Z';
    svg.appendChild(el('path',{d,fill:s.color,opacity:.85,stroke:s.color,'stroke-width':.5}));
  }
  // hover
  const overlay = el('rect',{x:pad.l,y:pad.t,width:iw,height:ih,fill:'transparent'});
  const cross = el('line',{x1:0,x2:0,y1:pad.t,y2:pad.t+ih,stroke:'#ff3955','stroke-width':1,'stroke-dasharray':'3 3',opacity:0});
  svg.appendChild(cross);svg.appendChild(overlay);
  overlay.addEventListener('mousemove',ev=>{
    const r=svg.getBoundingClientRect();
    const sx=(ev.clientX-r.left)*(W/r.width);
    const idx=Math.max(0,Math.min(n-1,Math.round((sx-pad.l)/iw*(n-1))));
    cross.setAttribute('x1',x(idx));cross.setAttribute('x2',x(idx));cross.setAttribute('opacity',.8);
    const tot = totals[idx];
    const lines = series.map(s=>`<div class="ln"><span><span class="sw" style="background:${s.color}"></span>${s.name}</span><b>${fmt.num(s.data[idx])}</b></div>`).join('');
    showTT(ev.clientX,ev.clientY,`<div class="yr">Year ${YEARS[idx]}</div>${lines}<div class="ln" style="border-top:1px solid #3a1f25;padding-top:4px;margin-top:4px"><span>Total</span><b>${fmt.num(tot)}</b></div>`);
  });
  overlay.addEventListener('mouseleave',()=>{cross.setAttribute('opacity',0);hideTT();});
  host.appendChild(svg);
  const lg=document.createElement('div');lg.className='legend';
  lg.innerHTML=series.map(s=>`<span class="legend-item"><span class="legend-swatch" style="background:${s.color}"></span>${s.name}</span>`).join('');
  host.appendChild(lg);
}

/* ---------- Bar+Line combo (debt) ---------- */
function barLineChart(containerId, bars, line, opts={}){
  const host=document.getElementById(containerId);host.innerHTML='';
  const W=1000,H=opts.height||320;
  const pad={t:20,r:56,b:34,l:56};
  const iw=W-pad.l-pad.r, ih=H-pad.t-pad.b;
  const n=YEARS.length;
  const bmax=niceMax(Math.max(...bars.data,1));
  const lmax=niceMax(Math.max(...line.data.map(Math.abs),1));
  const x = i => pad.l + iw*((i+0.5)/n);
  const xBar = i => pad.l + iw*(i/n);
  const bw = iw/n*0.72;
  const yB = v => pad.t + ih - ih*(v/bmax);
  const yL = v => pad.t + ih - ih*((v+lmax)/(2*lmax));
  const svg=el('svg',{viewBox:`0 0 ${W} ${H}`,class:'chart',preserveAspectRatio:'xMidYMid meet'});
  for(let i=0;i<=5;i++){
    const v=bmax*i/5, yy=yB(v);
    svg.appendChild(el('line',{class:'grid-line',x1:pad.l,x2:W-pad.r,y1:yy,y2:yy}));
    const t=el('text',{x:pad.l-8,y:yy+3,'text-anchor':'end'});t.textContent=fmt.num(v);svg.appendChild(t);
  }
  // right axis for line
  for(let i=0;i<=4;i++){
    const v=-lmax+2*lmax*i/4;
    const yy=yL(v);
    const t=el('text',{x:W-pad.r+8,y:yy+3,'text-anchor':'start',fill:'#ff8895'});t.textContent=fmt.num(v);svg.appendChild(t);
  }
  for(let i=0;i<n;i+=5){
    const t=el('text',{x:xBar(i)+bw/2+iw/n*0.14,y:H-pad.b+14,'text-anchor':'middle'});t.textContent='Y'+YEARS[i];svg.appendChild(t);
  }
  // bars
  bars.data.forEach((v,i)=>{
    const bx=xBar(i)+iw/n*0.14;
    const by=yB(v), bh=pad.t+ih-by;
    svg.appendChild(el('rect',{x:bx,y:by,width:bw,height:Math.max(0,bh),fill:'url(#barGrad)',rx:2}));
  });
  // gradient def
  const defs=el('defs');
  defs.innerHTML=`<linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#e21a3c" stop-opacity="0.95"/>
    <stop offset="100%" stop-color="#6e0a18" stop-opacity="0.6"/>
  </linearGradient>`;
  svg.appendChild(defs);
  // line
  let d='';
  line.data.forEach((v,i)=>d+=(i?' L ':'M ')+x(i)+' '+yL(v));
  svg.appendChild(el('path',{d,fill:'none',stroke:line.color,'stroke-width':2.2,'stroke-linejoin':'round'}));
  // hover
  const overlay=el('rect',{x:pad.l,y:pad.t,width:iw,height:ih,fill:'transparent'});
  const cross=el('line',{x1:0,x2:0,y1:pad.t,y2:pad.t+ih,stroke:'#ff3955','stroke-width':1,'stroke-dasharray':'3 3',opacity:0});
  svg.appendChild(cross);svg.appendChild(overlay);
  overlay.addEventListener('mousemove',ev=>{
    const r=svg.getBoundingClientRect();
    const sx=(ev.clientX-r.left)*(W/r.width);
    const idx=Math.max(0,Math.min(n-1,Math.floor((sx-pad.l)/iw*n)));
    cross.setAttribute('x1',x(idx));cross.setAttribute('x2',x(idx));cross.setAttribute('opacity',.7);
    showTT(ev.clientX,ev.clientY,`<div class="yr">Year ${YEARS[idx]}</div>
      <div class="ln"><span><span class="sw" style="background:#e21a3c"></span>${bars.name}</span><b>${fmt.num(bars.data[idx])}</b></div>
      <div class="ln"><span><span class="sw" style="background:${line.color}"></span>${line.name}</span><b>${fmt.num(line.data[idx])}</b></div>`);
  });
  overlay.addEventListener('mouseleave',()=>{cross.setAttribute('opacity',0);hideTT();});
  host.appendChild(svg);
  const lg=document.createElement('div');lg.className='legend';
  lg.innerHTML=`<span class="legend-item"><span class="legend-swatch" style="background:#e21a3c"></span>${bars.name}</span>
    <span class="legend-item"><span class="legend-swatch" style="background:${line.color}"></span>${line.name}</span>`;
  host.appendChild(lg);
}

/* ---------- Donut ---------- */
function donut(containerId, slices){
  const host=document.getElementById(containerId);host.innerHTML='';
  const total = slices.reduce((a,b)=>a+b.value,0);
  const size=220, cx=size/2, cy=size/2, r=90, rInner=58;
  const svg=el('svg',{viewBox:`0 0 ${size} ${size}`,width:size,height:size});
  let ang=-Math.PI/2;
  slices.forEach(s=>{
    const frac=s.value/total;
    const a2=ang+frac*Math.PI*2;
    const large=frac>0.5?1:0;
    const x1=cx+r*Math.cos(ang), y1=cy+r*Math.sin(ang);
    const x2=cx+r*Math.cos(a2), y2=cy+r*Math.sin(a2);
    const x3=cx+rInner*Math.cos(a2), y3=cy+rInner*Math.sin(a2);
    const x4=cx+rInner*Math.cos(ang), y4=cy+rInner*Math.sin(ang);
    const d=`M ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2} L ${x3} ${y3} A ${rInner} ${rInner} 0 ${large} 0 ${x4} ${y4} Z`;
    const p=el('path',{d,fill:s.color,stroke:'#0b0608','stroke-width':2});
    p.addEventListener('mousemove',ev=>showTT(ev.clientX,ev.clientY,`<div class="yr">${s.name}</div><div class="ln"><b>£${fmt.num(s.value)}K</b><span style="margin-left:8px">${(frac*100).toFixed(1)}%</span></div>`));
    p.addEventListener('mouseleave',hideTT);
    svg.appendChild(p);
    ang=a2;
  });
  // center total
  const t1=el('text',{x:cx,y:cy-4,'text-anchor':'middle',fill:'#d9c3c8',style:'font-size:10px;letter-spacing:2px;text-transform:uppercase'});t1.textContent='Total';
  const t2=el('text',{x:cx,y:cy+16,'text-anchor':'middle',fill:'#ffeef1',style:'font-size:16px;font-weight:700;font-family:ui-monospace,monospace'});t2.textContent='£'+fmt.num(total)+'K';
  svg.appendChild(t1);svg.appendChild(t2);
  const wrap=document.createElement('div');wrap.className='donut-wrap';
  wrap.appendChild(svg);
  const lg=document.createElement('div');lg.className='donut-legend';
  lg.innerHTML=slices.map(s=>{
    const pct=(s.value/total*100).toFixed(1);
    return `<div class="item">
      <div class="lbl"><span class="legend-swatch" style="background:${s.color}"></span>${s.name}</div>
      <div class="val">£${fmt.num(s.value)}K · ${pct}%</div>
    </div>`;
  }).join('');
  wrap.appendChild(lg);
  host.appendChild(wrap);
}

/* ---------- Render all ---------- */
donut('donut-sources',[
  {name:'Senior Debt', value:K.total_debt, color:'#e21a3c'},
  {name:'Sponsor Equity', value:K.total_equity, color:'#ffb5bf'},
]);
donut('donut-uses',[
  {name:'Construction (CAPEX)', value:K.capex, color:'#e21a3c'},
  {name:'Engagement Fee', value:K.engagement_fee, color:'#ff8895'},
  {name:'Capitalized Interest', value:K.capitalized_interest, color:'#b01228'},
  {name:'Arrangement Fee', value:K.arrangement_fee, color:'#6e0a18'},
]);

stackedArea('chart-revenue',[
  {name:'Heavy Vehicle (HV)', data:D.rev_hv, color:'#6e0a18'},
  {name:'Passenger Car (PC)', data:D.rev_pc, color:'#e21a3c'},
]);

lineChart('chart-traffic',[
  {name:'PC vehicles', data:D.traffic_pc, color:'#ff3955'},
  {name:'HV vehicles', data:D.traffic_hv, color:'#ffc46b'},
],{height:260});

lineChart('chart-profit',[
  {name:'EBITDA', data:D.ebitda, color:'#ff3955', fill:true, glow:true},
  {name:'EBIT', data:D.ebit, color:'#ffc46b'},
  {name:'Net Profit', data:D.net_profit, color:'#5ad1c3'},
],{height:340});

barLineChart('chart-debt',
  {name:'Debt Outstanding (EoP)', data:D.debt_closing},
  {name:'Principal Repayment', data:D.principal_rep, color:'#ffc46b'},
{height:320});

lineChart('chart-cashflow',[
  {name:'CFADS', data:D.cfads, color:'#ff3955', fill:true},
  {name:'Dividends', data:D.dividends.map(v=>-v), color:'#b58bff'},
],{height:320});

lineChart('chart-bs',[
  {name:'Fixed Asset (NBV)', data:D.asset_bs, color:'#ff3955', fill:true},
  {name:'Cash in Hand', data:D.cash_bs, color:'#5ad1c3'},
  {name:'Debt Outstanding', data:D.debt_bs, color:'#ffc46b'},
  {name:'Equity', data:D.equity_bs, color:'#b58bff'},
],{height:360});

/* ---------- Assumptions list ---------- */
const unitFmt = (v, u) => {
  if (u === '%') return (v*100).toFixed(2)+'%';
  if (u === '£') return '£'+(+v).toLocaleString(undefined,{maximumFractionDigits:2});
  if (u === '£/year') return '£'+(+v).toLocaleString()+'/yr';
  if (u === 'veh/year') return (+v).toLocaleString()+' veh/yr';
  if (u === 'years') return v+' yrs';
  if (u === 'per year') return (v*100).toFixed(2)+'% p.a.';
  if (u === 'of margin') return (v*100).toFixed(0)+'% of margin';
  return v;
};
const assump = D.assumptions;
const order = [
  'Concession Duration','Construction Duration','Operations Duration',
  'Traffic - Passenger Car (PC)','Traffic - Heavy Vehicule (HV)',
  'Toll Rate - Passenger Car (PC)','Toll Rate - Heavy Vehicule (HV)',
  'Traffic Evolution per year (PC & HV)','Inflation per year',
  'CAPEX (including SPV costs)','Maintenance (including heavy maintenance & SPV costs)',
  'Base Interest Rate','Fixed Rate Margin','Arrangement fee','Engagement fee',
  'Gearing','Tax Rate','Dividend distribution policy',
];
document.getElementById('assump-list').innerHTML = order
  .filter(k=>assump[k])
  .map(k=>`<div class="row"><span class="k">${k}</span><span class="v">${unitFmt(assump[k].value, assump[k].unit)}</span></div>`).join('');

</script>
</body>
</html>
"""

html = html.replace("__DATA__", data_json)
Path("dashboard.html").write_text(html)
print(f"dashboard.html written: {len(html):,} bytes")
