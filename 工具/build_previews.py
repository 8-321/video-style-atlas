# -*- coding: utf-8 -*-
"""生成风格库预览拼图。可重复运行。"""
from __future__ import annotations
import os, subprocess, tempfile, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = Path(r"E:\视频工厂\10-风格库")
PREV = BASE / "预览"
TMP = PREV / "_tmp"
FONT_B = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_R = r"C:\Windows\Fonts\msyh.ttc"
FONT_SERIF = r"C:\Windows\Fonts\simsun.ttc"

W, CELL_W, CELL_H, HEADER = 1560, 500, 300, 96
COLS, ROWS = 3, 2

STYLES = [
    dict(id="S01", name="纸张拼贴 · VOX 编辑插画", spec="16:9 · 25s / 115s · 30fps · 4 色", accent="#D95D39", kind="images",
         cells=[r"E:\AI视频工程\VOX-奥德赛时期\keyframes\kf_2.jpg", r"E:\AI视频工程\VOX-奥德赛时期\keyframes\kf_4.jpg",
                r"E:\AI视频工程\VOX-奥德赛时期\keyframes\kf_6.jpg", r"E:\AI视频工程\VOX-奥德赛时期\keyframes\kf_9.jpg",
                r"E:\AI视频工程\VOX-奥德赛时期\keyframes\kf_12.jpg", r"E:\AI视频工程\VOX-奥德赛时期\keyframes\kf_15.jpg"]),
    dict(id="S02", name="暖木档案桌 · 纸片木偶", spec="9:16 · 277s · 30fps · 41 镜", accent="#E8A33D", kind="video",
         src=r"E:\AI视频工程\MBTI\productions\ai-mbti\drafts\MBTI-AI-时代-复刻.mp4", times=[0.05,0.2,0.35,0.5,0.65,0.8]),
    dict(id="S03", name="微缩定格 · 树脂人偶", spec="4:3 · 146s · 30fps · 26 句", accent="#E7B96E", kind="images",
         cells=[r"E:\AI视频工程\MBTI\productions\projection\review\final\frame-018.5.png", r"E:\AI视频工程\MBTI\productions\projection\review\final\frame-034.8.png",
                r"E:\AI视频工程\MBTI\productions\projection\review\final\frame-057.5.png", r"E:\AI视频工程\MBTI\productions\projection\review\final\frame-082.0.png",
                r"E:\AI视频工程\MBTI\productions\projection\review\final\frame-110.5.png", r"E:\AI视频工程\MBTI\productions\projection\review\final\frame-131.0.png"]),
    dict(id="S04", name="双轨字幕 · 人物史诗", spec="16:9 · 177.6s · 30fps · 78 镜", accent="#F5F090", kind="video",
         src=r"E:\AI视频工程\复刻马斯克SpaceX\05_成片\一场坚持了22年火星豪赌_SpaceX.mp4", times=[0.02,0.18,0.34,0.5,0.66,0.82]),
    dict(id="S05", name="黑金 · 知识解说", spec="16:9 · 310.7s · 30fps · 148 切", accent="#C9A227", kind="video",
         src=r"E:\AI视频工程\狼人杀\05_成片\为什么狼人杀越来越凉_纯画面_1080p30_发布版.mp4", times=[0.03,0.18,0.33,0.48,0.63,0.78]),
    dict(id="S06", name="暖棕电影感 · 实拍长解说", spec="16:9 · 465–472s · 30fps · 96 镜", accent="#C8552B", kind="video",
         src=r"E:\复刻kele说视频\05_成片\为什么我说亚文化必然兴起_纯画面1080p.mp4", times=[0.04,0.2,0.36,0.52,0.68,0.84]),
    dict(id="S07", name="巨字卡点 · 角色展示", spec="16:9 · 60s · 30fps · 13 段", accent="#F2B21C", kind="video",
         src=r"C:\Users\34137\projects\mbti-nt-clone\productions\sp-group-showcase\drafts\sp-showcase-v5.mp4", times=[0.02,0.18,0.34,0.5,0.66,0.82]),
    dict(id="S08", name="纯黑设备 · App 发布动画", spec="16:9 · 45s · 30fps · 9 屏", accent="#8A93A6", kind="video",
         src=r"E:\AI视频工程\第二文化-开场45s\05-成片\第二文化-开场45s-1920x1080.mp4", times=[0.03,0.10,0.25,0.40,0.70,0.94]),
    dict(id="S09", name="暗室档案馆 · 心理/哲学", spec="9:16 · 规范型 · 无成片", accent="#E4572E", kind="specimen"),
    dict(id="S10", name="胶片化 · 可叠加滤镜", spec="2.39:1 / 原画幅 · FFmpeg", accent="#D9B8A0", kind="beforeafter"),
    dict(id="S11", name="AI 漫剧 · 照片级 3D", spec="21:9 · 214s 目标 / 实测 4 镜 40.2s · 24fps · 56 镜 · 0 切点", accent="#D98C62", kind="multi",
         cells=[(r"E:\漫剧AI\shot01.mp4", 1.5), (r"E:\漫剧AI\shot12.mp4", 4.5), (r"E:\漫剧AI\shot12b.mp4", 5.5),
                (r"E:\漫剧AI\丧尸清道夫_第三段_12秒.mp4", 3.0), (r"E:\漫剧AI\丧尸清道夫_第三段_12秒.mp4", 8.5),
                (r"E:\漫剧AI\shot12.mp4", 10.5)]),
    dict(id="S12", name="扁平动态图形 · Flat Motion Graphics", spec="16:9 / 9:16 · 30–120s · ≤4 色", accent="#7C3AED", kind="specimen",
         badge="参考规范 · 未实测", serif=False, motto_serif=False,
         palette=[("#0F172A","深板岩底"),("#7C3AED","紫"),("#4F46E5","靛"),("#EC4899","品红"),("#06B6D4","青"),("#F8FAFC","近白")],
         title_line="47 个工具，只有 3 个真的有用。",
         title_note="Space Grotesk 700 · tracking -0.03em",
         body_lines=["每 2–3 秒必须出现一个新视觉元素。","一屏最多 4 色，深底也算 1 色。"],
         body_note="Noto Sans SC Bold · 正文 400 · 对比度 ≥4.5:1",
         mono_line="01 / 03", mono_note="数字卡 800 · 停留 2.0s",
         frame_label="16:9 版式示意", frame_note="转场 0.3s + 音效",
         motto="纯平色块\n禁止渐变"),
    dict(id="S13", name="吉卜力手绘动画 · Anime Ghibli", spec="16:9 · 60–180s · 24fps · 水彩", accent="#FFB347", kind="specimen",
         badge="参考规范 · 未实测",
         palette=[("#0A0A1A","深夜底"),("#2D5016","森林绿"),("#1B4332","深林绿"),("#FFB347","暖金"),("#FF6B9D","樱粉"),("#A8E6CF","灵光青"),("#FFF3B0","暖金白")],
         title_line="风把夏天吹回来了。",
         title_note="Noto Serif JP 500 · 标题 54–72px",
         body_lines=["同场景 2–3 张微变图，交叉淡化 1–1.5s。","前中后景必须分得开，每张图都加暗角。"],
         body_note="Noto Sans 300 · 行高 1.7 · 字幕后期叠",
         mono_line="04 / 06", mono_note="单场 4–6s · 全片无快切",
         frame_label="16:9 分层示意", frame_note="前景 / 中景 / 背景",
         motto="水彩边缘\n不要 3D"),
    dict(id="S14", name="高端极简 · Premium Minimalist", spec="16:9 · 45–180s · 一帧一焦点", accent="#2563EB", kind="specimen",
         badge="参考规范 · 未实测", serif=False, motto_serif=False,
         palette=[("#F9FAFB","米白底"),("#111827","炭黑"),("#374151","次级"),("#6B7280","弱化"),("#2563EB","钴蓝"),("#0F766E","深青")],
         title_line="结论先说：这件事现在就能做。",
         title_note="Inter 700 · tracking -0.01em",
         body_lines=["非对称编辑网格，大留白，硬对齐。","动效只建立层级，不装饰。"],
         body_note="Inter 400 · 行高 1.55 · −16 LUFS",
         mono_line="+38%", mono_note="数字卡 800 · 停留 3.25s",
         frame_label="非对称网格示意", frame_note="一帧一个焦点物",
         motto="留白是确定\n不是没做完"),
    dict(id="S15", name="极简图解 · Minimalist Diagram", spec="16:9 · 60–300s · 单红强调", accent="#E94560", kind="specimen",
         badge="参考规范 · 未实测", serif=False, motto_serif=False,
         palette=[("#FAFAFA","浅灰纸"),("#1A1A2E","主线条"),("#16213E","次级"),("#E94560","唯一强调红"),("#0F3460","结构深蓝")],
         title_line="把系统拆成 4 个节点。",
         title_note="IBM Plex Sans 600 · 网格对齐",
         body_lines=["全片只有一个红色强调，只在关键节点。","线宽统一，连线用「生长」不用「闪现」。"],
         body_note="IBM Plex Sans 400 · 行高 1.7 · 单镜 3–15s",
         mono_line="NODE 03", mono_note="IBM Plex Mono · 标签/时间码",
         frame_label="图解版式示意", frame_note="一屏 ≤7 个节点",
         motto="单色 + 一个红\n不要彩色"),
]

def font(path, size):
    return ImageFont.truetype(path, size, index=0)

def run(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, (p.stderr or b"").decode("utf-8", "replace")

def grab(src: str, t: float, out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    # 先定位再解码，速度快且不受关键帧影响
    rc, err = run(["ffmpeg","-nostdin","-y","-ss",f"{t:.3f}","-i",src,"-frames:v","1","-vf","scale=1000:-2","-q:v","2",str(out)])
    if rc != 0 or not out.exists():
        raise RuntimeError(f"ffmpeg 抽帧失败: {src} @ {t}\n{err[-800:]}")

def fit(im: Image.Image, w: int, h: int) -> Image.Image:
    im = ImageOps.exif_transpose(im).convert("RGB")
    return ImageOps.pad(im, (w, h), color=(10,10,10), method=Image.LANCZOS)

def make_sheet(st: dict, thumbs: list[Image.Image], labels: list[str] | None = None):
    H = HEADER + ROWS*CELL_H + 40
    canvas = Image.new("RGB", (W, H), (12,12,14))
    d = ImageDraw.Draw(canvas)
    # 顶栏
    d.rectangle([0,0,W,HEADER], fill=(18,18,21))
    d.rectangle([0,HEADER-4,W,HEADER], fill=st["accent"])
    d.text((34,22), st["id"], font=font(FONT_B, 40), fill=st["accent"])
    d.text((122,22), st["name"], font=font(FONT_B, 34), fill=(240,238,232))
    d.text((124,64), st["spec"], font=font(FONT_R, 20), fill=(150,150,158))
    d.text((W-40,32), "视频工厂 · 风格库", font=font(FONT_R, 18), fill=(110,110,118), anchor="ra")
    # 网格
    gap = (W - COLS*CELL_W) // (COLS+1)
    y0 = HEADER + 20
    for i, im in enumerate(thumbs[:COLS*ROWS]):
        c, r = i % COLS, i // COLS
        x = gap + c*(CELL_W+gap)
        y = y0 + r*(CELL_H+20)
        canvas.paste(fit(im, CELL_W, CELL_H), (x,y))
        d.rectangle([x,y,x+CELL_W-1,y+CELL_H-1], outline=(46,46,52), width=2)
        if labels and i < len(labels) and labels[i]:
            tw = d.textlength(labels[i], font=font(FONT_B, 16))
            d.rectangle([x+8,y+8,x+18+tw,y+36], fill=(0,0,0))
            d.text((x+13,y+11), labels[i], font=font(FONT_B, 16), fill=st["accent"])

    out = PREV / f"{st['id']}.jpg"
    canvas.save(out, quality=92)
    return out

DEFAULT_PALETTE = [("#0B0D10","近黑底"),("#E8E4DC","纸白"),("#E4572E","朱砂 A"),("#4FB3BF","青 B"),("#C9A227","金 C")]

def make_specimen(st: dict):
    """规范示意板：没有成片时，用色板/字体/版面示意替代真实帧。"""
    H = 1000
    canvas = Image.new("RGB", (W,H), (11,13,16))
    d = ImageDraw.Draw(canvas)
    d.rectangle([0,0,W,HEADER], fill=(18,18,21))
    d.rectangle([0,HEADER-4,W,HEADER], fill=st["accent"])
    d.text((34,22), st["id"], font=font(FONT_B,40), fill=st["accent"])
    d.text((122,22), st["name"], font=font(FONT_B,34), fill=(232,228,220))
    d.text((124,64), st["spec"], font=font(FONT_R,20), fill=(150,150,158))
    if st.get("badge"):
        d.text((W-40,64), st["badge"], font=font(FONT_R,18), fill=(150,150,158), anchor="ra")
    d.text((W-40,32), "视频工厂 · 风格库", font=font(FONT_R,18), fill=(110,110,118), anchor="ra")

    palette = st.get("palette", DEFAULT_PALETTE)
    n = max(len(palette), 1)
    box_w = min(180, int((880 - 16*(n-1))/n))
    x = 60
    for hexv, lab in palette:
        rgb = tuple(int(hexv[i:i+2],16) for i in (1,3,5))
        d.rectangle([x,140,x+box_w,260], fill=rgb, outline=(60,60,66))
        d.text((x,274), hexv, font=font(FONT_R,18), fill=(190,190,196))
        d.text((x,300), lab, font=font(FONT_R,18), fill=(140,140,148))
        x += box_w + 16

    tf = FONT_SERIF if st.get("serif", True) else FONT_B
    d.text((60,370), st.get("title_line","他不是冷淡，是在自保。"), font=font(tf,54), fill=(232,228,220))
    d.text((60,440), st.get("title_note","Noto Serif SC · 标题/引语 72–96px"), font=font(FONT_R,18), fill=(130,130,138))
    bl = st.get("body_lines", ["心理学把这种反应叫「投射」——","简单说，你看见的别人，其实是你自己。"])
    y = 500
    for ln in bl[:2]:
        d.text((60,y), ln, font=font(FONT_R,28), fill=(232,228,220)); y += 40
    d.text((60,580), st.get("body_note","Noto Sans SC · 正文/字幕 44–52px"), font=font(FONT_R,18), fill=(130,130,138))
    d.text((60,640), st.get("mono_line","03 / 07"), font=font(FONT_R,40), fill=st["accent"])
    d.text((60,692), st.get("mono_note","IBM Plex Mono · 数字/时间码 32–40px"), font=font(FONT_R,18), fill=(130,130,138))

    d.rectangle([980,370,1500,900], outline=(70,70,78), width=2)
    d.rectangle([1000,390,1480,880], fill=(20,22,26))
    d.text((1018,410), st.get("frame_label","9:16 安全区示意"), font=font(FONT_R,18), fill=(120,120,128))
    d.rectangle([1000,390,1480,490], fill=(35,37,42))
    d.rectangle([1000,780,1480,880], fill=(35,37,42))
    d.text((1018,800), st.get("frame_note","字幕基线距底 300px"), font=font(FONT_R,18), fill=(180,180,188))
    d.text((1018,590), st.get("motto","一屏只允许\n一个信号色"), font=font(tf if st.get("motto_serif", True) else FONT_B,26), fill=st["accent"])
    out = PREV / f"{st['id']}.jpg"
    canvas.save(out, quality=92)
    return out

def make_beforeafter(st: dict):
    before = Image.open(r"E:\AI视频工程\自传微电影\07_复盘\对照\01_原片.png").convert("RGB")
    after = Image.open(r"E:\AI视频工程\自传微电影\07_复盘\对照\02_胶片化.png").convert("RGB")
    H = 1000
    canvas = Image.new("RGB",(W,H),(12,12,14))
    d = ImageDraw.Draw(canvas)
    d.rectangle([0,0,W,HEADER], fill=(18,18,21))
    d.rectangle([0,HEADER-4,W,HEADER], fill=st["accent"])
    d.text((34,22), st["id"], font=font(FONT_B,40), fill=st["accent"])
    d.text((122,22), st["name"], font=font(FONT_B,34), fill=(240,238,232))
    d.text((124,64), st["spec"], font=font(FONT_R,20), fill=(150,150,158))
    d.text((W-40,32), "视频工厂 · 风格库", font=font(FONT_R,18), fill=(110,110,118), anchor="ra")
    box_w, box_h = 720, 405
    for i,(im,lab,col) in enumerate([(before,"改前：AI 直出（数码感）",(120,120,128)),(after,"改后：胶片化（退色+暖高光+泛光+颗粒+暗角）",st["accent"])]):
        x = 40 + i*(box_w+40); y = 150
        canvas.paste(fit(im,box_w,box_h),(x,y))
        d.rectangle([x,y,x+box_w-1,y+box_h-1], outline=(60,60,66), width=2)
        d.text((x,y+box_h+16), lab, font=font(FONT_B,20), fill=col)
    d.text((40,760), "FFmpeg 链：curves 退色曲线 → colorbalance 暖高光冷阴影 → eq 降饱和 → screen 泛光 → vignette → noise 颗粒", font=font(FONT_R,20), fill=(170,170,178))
    d.text((40,800), "可选：scale 1280:535 + pad 1280:720 加 2.39:1 遮幅；CRF 18 / preset medium / faststart", font=font(FONT_R,20), fill=(170,170,178))
    out = PREV / f"{st['id']}.jpg"
    canvas.save(out, quality=92)
    return out

def make_index(paths: list[Path]):
    tw, th, cols = 480, 300, 3
    rows = (len(paths)+cols-1)//cols
    W2 = cols*tw + (cols+1)*30
    H2 = 120 + rows*(th+70) + 20
    canvas = Image.new("RGB",(W2,H2),(12,12,14))
    d = ImageDraw.Draw(canvas)
    d.text((40,32), f"视频风格资产库 · {len(paths)} 套", font=font(FONT_B,38), fill=(240,238,232))
    d.text((42,82), "E:\\视频工厂\\10-风格库 ｜ 预览图由各成片/关键帧自动生成", font=font(FONT_R,18), fill=(140,140,148))
    for i,p in enumerate(paths):
        c, r = i%cols, i//cols
        x = 30 + c*(tw+30); y = 120 + r*(th+70)
        im = Image.open(p).convert("RGB")
        canvas.paste(fit(im,tw,th),(x,y))
        d.rectangle([x,y,x+tw-1,y+th-1], outline=(50,50,56), width=2)
        d.text((x+6,y+th+8), p.stem, font=font(FONT_B,20), fill=(190,190,198))
    out = PREV / "index.jpg"
    canvas.save(out, quality=90)
    return out

def main():
    PREV.mkdir(parents=True, exist_ok=True)
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    made = []
    for st in STYLES:
        sid = st["id"]
        if st["kind"] == "video":
            thumbs=[]; labels=[]
            for i,pct in enumerate(st["times"]):
                p = TMP / f"{sid}-{i}.jpg"
                # 用时长百分比定位
                grab(st["src"], _duration(st["src"])*pct, p)
                thumbs.append(Image.open(p))
                labels.append(f"{pct*100:.0f}%")
            made.append(make_sheet(st, thumbs, labels))
        elif st["kind"] == "images":
            thumbs=[Image.open(p) for p in st["cells"]]
            made.append(make_sheet(st, thumbs))
        elif st["kind"] == "multi":
            thumbs=[]; labels=[]
            for i,(src,t) in enumerate(st["cells"]):
                p = TMP / f"{sid}-{i}.jpg"
                grab(src, t, p)
                thumbs.append(Image.open(p))
                labels.append(f"{os.path.basename(src)} @{t:.1f}s")
            made.append(make_sheet(st, thumbs, labels))
        elif st["kind"] == "specimen":
            made.append(make_specimen(st))
        elif st["kind"] == "beforeafter":
            made.append(make_beforeafter(st))
        print("OK", made[-1])
    make_index(made)
    print("OK", PREV/"index.jpg")

_dur_cache={}
def _duration(src: str) -> float:
    if src in _dur_cache: return _dur_cache[src]
    p = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",src],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    v = float(p.stdout.decode("utf-8","replace").strip().splitlines()[0])
    _dur_cache[src]=v
    return v

if __name__ == "__main__":
    main()

