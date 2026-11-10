# -*- coding: utf-8 -*-
"""从 styles.json 重建 index.html。可重复运行。"""
import json, html, os
BASE = r"E:/视频工厂/10-风格库"
d = json.load(open(os.path.join(BASE, "styles.json"), encoding="utf-8"))
S = d["styles"]
LABEL = {"verified": "已验证", "tested": "测试中", "spec": "规范型", "reference": "参考规范"}
e = lambda s: html.escape(str(s), quote=True)

def card(s):
    sp = s.get("spec", {})
    meta = " · ".join([str(sp.get("aspect","")), str(sp.get("resolution","")), f'{sp.get("fps","")}fps', str(sp.get("duration",""))])
    chips = "".join(f'<span class="chip"><i style="background:{e(c["hex"])}"></i>{e(c["name"])} {e(c["hex"])}</span>' for c in s.get("palette", []))
    tags = "".join(f'<span class="tag">{e(t)}</span>' for t in s.get("best_for", []))
    text = " ".join([s["id"], s["name"], s.get("one_liner","")] + s.get("aliases",[]) + s.get("best_for",[])).lower()
    return f'''    <article class="card" data-id="{e(s["id"])}" data-text="{e(text)}">
      <a class="thumb" href="{e(s["preview"])}" target="_blank"><img loading="lazy" src="{e(s["preview"])}" alt="{e(s["name"])}"></a>
      <div class="body">
        <div class="top"><span class="sid">{e(s["id"])}</span><span class="status {e(s["status"])}">{e(LABEL.get(s["status"], s["status"]))}</span></div>
        <h2>{e(s["name"])}</h2>
        <p class="one">{e(s.get("one_liner",""))}</p>
        <div class="meta">{e(meta)}</div>
        <div class="chips">{chips}</div>
        <div class="tags">{tags}</div>
        <div class="links"><a href="{e(s["card"])}">打开风格卡 (md)</a><a href="{e(s["preview"])}" target="_blank">看大图</a></div>
      </div>
    </article>'''

CSS = """<style>
:root{--bg:#0c0d10;--panel:#141519;--line:#2a2b31;--text:#f0eee8;--muted:#93939c;--accent:#e8a33d}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:"Microsoft YaHei","PingFang SC",system-ui,sans-serif}
header{padding:44px 48px 24px;border-bottom:1px solid var(--line)}
h1{margin:0 0 8px;font-size:34px;letter-spacing:.02em}
.sub{color:var(--muted);font-size:14px;line-height:1.7}
.docs{display:flex;gap:10px;flex-wrap:wrap;padding:18px 48px;border-bottom:1px solid var(--line);background:#101116}
.docs a{color:#c9c7c0;text-decoration:none;font-size:13px;border:1px solid var(--line);background:var(--panel);padding:9px 14px;border-radius:8px}
.docs a:hover{border-color:var(--accent);color:var(--accent)}
.docs b{color:var(--accent);font-weight:700}
.toolbar{padding:20px 48px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;border-bottom:1px solid var(--line);position:sticky;top:0;background:rgba(12,13,16,.94);backdrop-filter:blur(8px);z-index:9}
input{width:min(520px,100%);background:var(--panel);border:1px solid var(--line);color:var(--text);padding:12px 14px;border-radius:8px;font-size:15px;outline:none}
input:focus{border-color:var(--accent)}
.count{color:var(--muted);font-size:13px}
.grid{padding:28px 48px 60px;display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:22px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;transition:.18s}
.card:hover{transform:translateY(-2px);border-color:#45464e}
.thumb{display:block;aspect-ratio:1560/736;background:#000;overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.body{padding:18px 20px 20px;display:flex;flex-direction:column;gap:10px;flex:1}
.top{display:flex;justify-content:space-between;align-items:center}
.sid{font-weight:900;font-size:22px;color:var(--accent);letter-spacing:.05em}
.status{font-size:12px;padding:3px 9px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}
.status.verified{color:#9fd3a8;border-color:#2e5a37}
.status.tested{color:#e8c27a;border-color:#5a4a2e}
.status.spec{color:#9fb8d3;border-color:#2e405a}
.status.reference{color:#c4b5fd;border-color:#4c3f7a}
h2{margin:0;font-size:20px;line-height:1.35}
.one{margin:0;color:#c9c7c0;font-size:14px;line-height:1.6}
.meta{font-size:12px;color:var(--muted);font-family:Consolas,monospace}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:11px;color:#c9c7c0;display:flex;align-items:center;gap:5px;background:#0e0f12;border:1px solid var(--line);padding:4px 7px;border-radius:5px}
.chip i{width:11px;height:11px;border-radius:2px;display:inline-block}
.tags{display:flex;flex-wrap:wrap;gap:6px}
.tag{font-size:11px;color:var(--muted);border:1px dashed #34353c;padding:3px 7px;border-radius:999px}
.links{margin-top:auto;display:flex;gap:16px;padding-top:6px}
.links a{color:var(--accent);text-decoration:none;font-size:13px}
.links a:hover{text-decoration:underline}
footer{padding:24px 48px 50px;color:var(--muted);font-size:12px;border-top:1px solid var(--line)}
@media(max-width:720px){header,.toolbar,.grid,footer,.docs{padding-left:20px;padding-right:20px}.grid{grid-template-columns:1fr}}
</style>"""

n = len(S)
doc = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>视频风格资产库 · {n} 套</title>
{CSS}</head>
<body>
<header>
  <h1>视频风格资产库</h1>
  <div class="sub">{n} 套视觉风格 · 10 套叙事骨架 · 9 条复刻工作流 · 每套都有预览、色值、提示词、验收数字<br>
  唯一真源：E:\\视频工厂\\10-风格库 ｜ 机器可读：styles.json ｜ 清单：MANIFEST.json</div>
</header>
<div class="docs">
  <a href="复刻工作流.md"><b>复刻工作流</b> · 拿到一条片子怎么拆、怎么排工序</a>
  <a href="叙事骨架.md"><b>叙事骨架</b> · N01–N10 结构</a>
  <a href="通用规格.md"><b>通用规格</b> · 画幅/字幕/响度/质检</a>
  <a href="index.html"><b>风格墙</b> · 当前页</a>
</div>
<div class="toolbar">
  <input id="q" placeholder="搜索：VOX / 档案桌 / 心理 / 人物 / 黑金 / 设备 / 漫剧 / 吉卜力 / 图解…" autocomplete="off">
  <span class="count" id="count">{n} 套</span>
</div>
<main class="grid" id="grid">
{chr(10).join(card(s) for s in S)}</main>
<footer>用法：先选一套 → 打开风格卡 → 复制提示词锚点 → 出片后按「验收数字」核对。不要混用两套视觉系统。<br>
「参考规范」= 外部成熟规范整理，本机尚无成片；要用它出片，先做一条测试片再升级为已验证。</footer>
<script>
const q=document.querySelector('#q'),cards=[...document.querySelectorAll('.card')],count=document.querySelector('#count');
q.addEventListener('input',()=>{{
  const v=q.value.trim().toLowerCase(); let n=0;
  cards.forEach(c=>{{const hit=!v||c.dataset.text.includes(v);c.style.display=hit?'':'none';if(hit)n++;}});
  count.textContent=n+' 套';
}});
</script>
</body></html>
"""
open(os.path.join(BASE, "index.html"), "w", encoding="utf-8").write(doc)
print("index.html", len(doc), "cards", n)
