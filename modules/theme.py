PREMIUM_CSS = """
<style>
:root {
    --ink:#14213d; --muted:#68758f; --line:rgba(114,133,174,.18);
    --blue:#315bea; --violet:#7c4dff; --cyan:#16b8d4; --green:#159a73;
}
html, body, [class*="css"] { font-family:Inter,"Microsoft YaHei","PingFang SC",sans-serif; }
.stApp {
    background:radial-gradient(circle at 78% 6%,rgba(124,77,255,.10),transparent 28%),
    radial-gradient(circle at 28% 22%,rgba(22,184,212,.08),transparent 24%),
    linear-gradient(180deg,#f8faff 0%,#f2f5fb 100%); color:var(--ink);
}
header[data-testid="stHeader"] { background:transparent; }
[data-testid="stSidebar"] {
    background:linear-gradient(175deg,#0c1630 0%,#152750 62%,#26327a 100%);
    border-right:1px solid rgba(255,255,255,.08);
}
[data-testid="stSidebar"] * { color:#eef3ff; }
[data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.12); }
[data-testid="stSidebar"] .stButton button { background:rgba(255,255,255,.08); border-color:rgba(255,255,255,.16); color:white; }
.block-container { max-width:1480px; padding-top:1.1rem; padding-bottom:3rem; }
.app-header {
    position:relative; overflow:hidden; display:flex; align-items:center; justify-content:space-between; gap:2rem;
    padding:1.45rem 1.65rem; margin-bottom:1.25rem;
    background:linear-gradient(118deg,#10234f 0%,#244ab7 54%,#7851cf 100%);
    border:1px solid rgba(255,255,255,.18); border-radius:24px;
    box-shadow:0 18px 45px rgba(28,51,118,.22); color:white;
}
.app-header::before { content:""; position:absolute; width:280px; height:280px; border-radius:50%; right:-80px; top:-170px; background:rgba(255,255,255,.14); }
.app-header::after { content:""; position:absolute; width:140px; height:140px; border-radius:42px; right:22%; bottom:-115px; transform:rotate(28deg); background:rgba(30,230,220,.16); }
.hero-copy,.hero-side { position:relative; z-index:2; }
.app-kicker { font-size:.7rem; font-weight:800; letter-spacing:.16em; color:#98f1ee; margin-bottom:.35rem; }
.app-title { font-size:1.75rem; font-weight:820; letter-spacing:-.035em; color:white; }
.app-subtitle { color:rgba(255,255,255,.78); font-size:.9rem; margin-top:.35rem; }
.status-pill { color:#effff9; background:rgba(12,32,68,.34); border:1px solid rgba(255,255,255,.24); border-radius:999px; padding:.55rem .85rem; font-size:.78rem; white-space:nowrap; backdrop-filter:blur(12px); }
.hero-meta { margin-top:.65rem; display:flex; gap:.4rem; justify-content:flex-end; }
.hero-chip { padding:.3rem .52rem; border-radius:999px; background:rgba(255,255,255,.12); font-size:.68rem; color:#eaf1ff; }
.brand-block { padding:.35rem .15rem 1rem; }
.brand-mark { width:46px; height:46px; display:flex; align-items:center; justify-content:center; border-radius:15px; background:linear-gradient(135deg,#54d8ff,#7c4dff); font-size:1.35rem; box-shadow:0 10px 25px rgba(65,112,255,.35); margin-bottom:.8rem; }
.brand-title { font-size:1.22rem; font-weight:800; letter-spacing:-.02em; }
.brand-sub { font-size:.73rem; color:#9fb0d3; margin-top:.18rem; }
.side-progress { height:5px; background:rgba(255,255,255,.10); border-radius:99px; overflow:hidden; margin:.9rem 0 1.1rem; }
.side-progress>span { display:block; height:100%; background:linear-gradient(90deg,#45d7e8,#a17cff); border-radius:99px; }
.step-card { display:flex; align-items:center; gap:.72rem; padding:.72rem .75rem; margin:.32rem 0; border-radius:13px; color:#93a5c8; border:1px solid transparent; }
.step-card.active { background:rgba(255,255,255,.10); border-color:rgba(255,255,255,.12); color:white; box-shadow:0 8px 18px rgba(0,0,0,.12); }
.step-card.done { color:#9eead6; }
.step-index { width:27px; height:27px; border-radius:9px; display:flex; align-items:center; justify-content:center; background:rgba(255,255,255,.08); font-size:.76rem; font-weight:750; }
.step-card.active .step-index { background:linear-gradient(135deg,#3bd5da,#765cf6); color:white; }
.step-name { font-size:.86rem; font-weight:650; }
.page-intro { display:flex; align-items:flex-end; justify-content:space-between; gap:1rem; margin:.55rem 0 1.2rem; }
.page-eyebrow { font-size:.68rem; font-weight:800; letter-spacing:.14em; color:var(--blue); margin-bottom:.28rem; }
.page-title { font-size:1.72rem; font-weight:820; letter-spacing:-.035em; color:var(--ink); }
.page-subtitle { color:var(--muted); font-size:.88rem; margin-top:.3rem; }
.mini-badge { padding:.42rem .68rem; background:#fff; border:1px solid var(--line); border-radius:999px; color:#53617c; font-size:.73rem; box-shadow:0 8px 20px rgba(39,61,112,.06); }
.stat-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:.72rem; margin-bottom:1rem; }
.stat-card { background:rgba(255,255,255,.86); border:1px solid var(--line); border-radius:16px; padding:.85rem 1rem; box-shadow:0 10px 28px rgba(35,54,105,.06); }
.stat-label { color:var(--muted); font-size:.7rem; }
.stat-value { color:var(--ink); font-size:1.08rem; font-weight:800; margin-top:.18rem; }
.stat-accent-blue { border-top:3px solid #466dfa; } .stat-accent-cyan { border-top:3px solid #20c1cf; } .stat-accent-violet { border-top:3px solid #8a5ff4; }
.panel { background:rgba(255,255,255,.88); border:1px solid var(--line); border-radius:20px; padding:1.15rem 1.2rem; margin-bottom:.8rem; box-shadow:0 12px 34px rgba(31,45,90,.07); backdrop-filter:blur(10px); }
.panel-title { font-weight:780; font-size:1rem; margin-bottom:.7rem; color:#182644; }
.panel-kicker { font-size:.66rem; letter-spacing:.12em; color:#7759de; font-weight:800; margin-bottom:.28rem; }
.field-row { display:grid; grid-template-columns:96px 1fr auto; gap:.65rem; align-items:center; padding:.58rem 0; border-bottom:1px solid #edf0f7; font-size:.84rem; }
.field-row:last-child { border-bottom:0; } .field-label { color:var(--muted); } .field-value { color:var(--ink); font-weight:650; }
.field-dot { width:7px; height:7px; border-radius:50%; background:#d8deeb; } .field-dot.done { background:#25bd8a; box-shadow:0 0 0 4px rgba(37,189,138,.10); }
.requirement-progress { height:7px; background:#edf1f8; border-radius:99px; overflow:hidden; margin:.35rem 0 .9rem; }
.requirement-progress>span { display:block; height:100%; background:linear-gradient(90deg,#23c6c8,#6869f2); border-radius:99px; }
.source-item { padding:.82rem .9rem; margin:.55rem 0; background:linear-gradient(135deg,#fbfcff,#f2f6ff); border:1px solid #dfe7f8; border-radius:15px; }
.source-name { font-weight:700; color:#23385f; } .source-meta { color:var(--muted); font-size:.78rem; margin-top:.18rem; }
.format-chips { display:flex; flex-wrap:wrap; gap:.4rem; margin:.75rem 0; }
.format-chip { padding:.3rem .55rem; border-radius:9px; background:#eef3ff; color:#4760a5; font-size:.7rem; font-weight:700; }
.skeleton-note { padding:.78rem .88rem; background:linear-gradient(135deg,#fff8e8,#fff3d7); color:#77520a; border:1px solid #f1d38b; border-radius:14px; font-size:.82rem; }
.slide-card { min-height:190px; color:white; border-radius:19px; padding:1.2rem; display:flex; flex-direction:column; justify-content:space-between; margin-bottom:.75rem; box-shadow:0 14px 30px rgba(32,58,132,.18); position:relative; overflow:hidden; }
.slide-card::after { content:""; position:absolute; width:110px; height:110px; border-radius:50%; right:-45px; top:-45px; background:rgba(255,255,255,.13); }
.slide-theme-0 { background:linear-gradient(145deg,#163b9d,#3478e8); } .slide-theme-1 { background:linear-gradient(145deg,#5133ad,#8a5ff4); } .slide-theme-2 { background:linear-gradient(145deg,#087f99,#20bdc9); } .slide-theme-3 { background:linear-gradient(145deg,#c24d73,#f4787d); }
.slide-kicker { font-size:.7rem; opacity:.78; letter-spacing:.08em; } .slide-title { font-size:1.14rem; line-height:1.35; font-weight:780; margin:.6rem 0; } .slide-copy { font-size:.78rem; opacity:.9; line-height:1.65; }
.success-banner { display:flex; align-items:center; gap:.8rem; padding:.9rem 1rem; border-radius:16px; background:linear-gradient(135deg,#e9fbf5,#effffb); border:1px solid #bfead9; color:#12694f; margin:.65rem 0 1rem; }
.success-icon { width:34px; height:34px; display:flex; align-items:center; justify-content:center; background:#20b982; color:white; border-radius:11px; font-weight:900; }
.download-summary { padding:1rem; border-radius:16px; background:linear-gradient(135deg,#f0f4ff,#f8f5ff); border:1px solid #dbe3fa; margin-bottom:.75rem; }
.download-title { font-size:1rem; font-weight:780; color:#203054; } .download-meta { font-size:.74rem; color:#6d7890; margin-top:.25rem; }
[data-testid="stChatMessage"] { background:rgba(255,255,255,.84); border:1px solid var(--line); border-radius:18px; padding:.45rem .65rem; box-shadow:0 8px 22px rgba(37,55,98,.05); }
div[data-testid="stButton"] button,div[data-testid="stDownloadButton"] button { border-radius:12px; font-weight:700; min-height:2.7rem; transition:.18s ease; }
div[data-testid="stButton"] button:hover,div[data-testid="stDownloadButton"] button:hover { transform:translateY(-1px); box-shadow:0 9px 20px rgba(49,91,234,.14); }
button[kind="primary"] { background:linear-gradient(100deg,#315bea,#7956e8)!important; border:0!important; }
div[data-testid="stFileUploader"] { background:rgba(255,255,255,.8); border-radius:16px; border:1px dashed #b8c6e7; padding:.2rem; }
[data-testid="stExpander"] { background:rgba(255,255,255,.78); border:1px solid var(--line); border-radius:14px!important; box-shadow:0 7px 18px rgba(38,53,92,.04); }
.stTabs [data-baseweb="tab-list"] { gap:.35rem; background:rgba(233,238,250,.75); padding:.28rem; border-radius:13px; }
.stTabs [data-baseweb="tab"] { border-radius:10px; padding:.55rem .95rem; }
.stTabs [aria-selected="true"] { background:white; box-shadow:0 5px 15px rgba(34,50,90,.08); }
.stTextInput input,.stTextArea textarea { border-radius:13px!important; border-color:#d8dfef!important; background:rgba(255,255,255,.86)!important; }
@media(max-width:900px) { .app-header{flex-direction:column;align-items:flex-start}.hero-meta{justify-content:flex-start}.stat-grid{grid-template-columns:1fr}.page-intro{align-items:flex-start;flex-direction:column} }
</style>
"""
