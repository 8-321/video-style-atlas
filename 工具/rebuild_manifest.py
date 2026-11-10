# -*- coding: utf-8 -*-
"""重建 MANIFEST.json（排除 _research 原始抓取件与 __pycache__）。"""
import os, json, hashlib
BASE = r"E:/视频工厂/10-风格库"
EXCL_DIRS = {"_research", "__pycache__", "_tmp", "外部参考"}
EXCL_FILES = {"MANIFEST.json"}

files = []
for root, dirs, names in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in EXCL_DIRS]
    for n in names:
        if n in EXCL_FILES:
            continue
        p = os.path.join(root, n)
        rel = os.path.relpath(p, BASE).replace("\\", "/")
        h = hashlib.sha256(open(p, "rb").read()).hexdigest().upper()
        files.append({"path": rel, "bytes": os.path.getsize(p), "sha256": h})
files.sort(key=lambda x: x["path"])
man = {
    "schema": "video-style-library-manifest@1",
    "root": "E:/视频工厂/10-风格库",
    "updated": "2026-11-04",
    "file_count": len(files),
    "total_bytes": sum(f["bytes"] for f in files),
    "files": files,
}
json.dump(man, open(os.path.join(BASE, "MANIFEST.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("files", man["file_count"], "bytes", man["total_bytes"])
for f in files:
    print(f'{f["bytes"]:>8}  {f["path"]}')
