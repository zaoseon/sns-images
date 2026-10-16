#!/usr/bin/env python3
"""저장소 에셋을 분류해 catalog.json 으로 색인한다.
분류 기준: 쓰임(캐릭터/배경/폰트/모션소스/완성물/참고자료) + 규격(비율) + 주제.
"""
import json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/zaoseon/sns-images")
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "/home/claude/sns-studio/catalog.json")

IMG = {".jpg", ".jpeg", ".png", ".webp"}
VID = {".mp4", ".mov", ".webm"}
FONT = {".ttf", ".otf", ".woff2"}
VEC = {".svg"}
DOC = {".md", ".txt", ".json", ".tsv"}


def ratio_name(w, h):
    if not w or not h:
        return "unknown"
    r = w / h
    for name, val in (("9:16", 9 / 16), ("3:4", 3 / 4), ("4:5", 4 / 5),
                      ("1:1", 1.0), ("3:2", 3 / 2), ("16:9", 16 / 9)):
        if abs(r - val) < 0.02:
            return name
    return f"{w}x{h}"


def dims(p: Path):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(p)],
            capture_output=True, text=True, timeout=20).stdout.strip().split("\n")[0]
        w, h = out.split("x")[:2]
        return int(w), int(h)
    except Exception:
        return None, None


def classify(rel: str):
    """쓰임과 주제를 경로로 판정한다."""
    low = rel.lower()
    if low.startswith("characters/"):
        use = "캐릭터"
    elif low.startswith("assets/brand_bg"):
        use = "브랜드배경"
    elif low.startswith("samples/"):
        use = "대표샘플"
    elif low.startswith("2026-motion/"):
        use = "모션소스"
    elif low.startswith("reuse/"):
        use = "재활용묶음"
    elif low.startswith("naver/"):
        use = "네이버원고"
    elif low.startswith(("clips_", "2026-w", "2026-r", "2026-final", "2026-pick",
                         "2026-pilot", "2026-carousel", "2026-reels")):
        use = "완성물"
    elif low.startswith("pipeline/"):
        use = "제작도구"
    elif low.startswith("docs/"):
        use = "운영문서"
    else:
        use = "기타"

    topic = []
    for key, label in (("zodiac", "띠"), ("night", "밤"), ("car", "캐러셀"),
                       ("reel", "릴스"), ("clip", "클립"), ("halloween", "핼러윈"),
                       ("event", "이벤트"), ("earlybird", "얼리버드"),
                       ("psych", "심리"), ("free", "무료풀이"),
                       ("monthly", "월간"), ("intro", "소개"), ("vote", "투표"),
                       ("sample", "샘플"), ("tpl", "템플릿"), ("guide", "가이드")):
        if key in low:
            topic.append(label)
    return use, topic


def main():
    items, skipped = [], 0
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git/" in str(p):
            continue
        rel = str(p.relative_to(ROOT))
        ext = p.suffix.lower()
        if ext in IMG:
            kind = "이미지"
        elif ext in VID:
            kind = "영상"
        elif ext in FONT:
            kind = "폰트"
        elif ext in VEC:
            kind = "벡터"
        elif ext in DOC:
            kind = "문서"
        else:
            skipped += 1
            continue

        use, topic = classify(rel)
        rec = {"path": rel, "kind": kind, "use": use, "topic": topic,
               "bytes": p.stat().st_size}
        # 규격은 캐릭터·배경·샘플·모션소스·완성물만 잰다(전부 재면 느리다)
        if kind in ("이미지", "영상") and use in (
                "캐릭터", "브랜드배경", "대표샘플", "모션소스", "완성물", "재활용묶음"):
            w, h = dims(p)
            if w:
                rec["w"], rec["h"], rec["ratio"] = w, h, ratio_name(w, h)
        items.append(rec)

    by_use = {}
    for it in items:
        by_use.setdefault(it["use"], {"count": 0, "bytes": 0, "kinds": {}})
        b = by_use[it["use"]]
        b["count"] += 1
        b["bytes"] += it["bytes"]
        b["kinds"][it["kind"]] = b["kinds"].get(it["kind"], 0) + 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(
        {"root": str(ROOT), "total": len(items), "skipped": skipped,
         "by_use": by_use, "items": items},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"색인 {len(items)}개 → {OUT}")
    for k, v in sorted(by_use.items(), key=lambda x: -x[1]["count"]):
        print(f"  {k:8s} {v['count']:5d}개  {v['bytes']/1e6:8.1f}MB  {v['kinds']}")


if __name__ == "__main__":
    main()
