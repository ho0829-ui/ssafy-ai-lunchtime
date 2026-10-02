#!/usr/bin/env python3
"""학습 자료(.docx / .md / .txt)를 문단 단위 원문 색인으로 변환한다.

사용법:
    python3 extract_source.py <출력폴더> <자료1> [자료2 ...]

출력:
    <출력폴더>/source_index.json  : 문단 ID → 파일·섹션 경로·위치·원문 (검증용, 기계용)
    <출력폴더>/source_numbered.md : [P12] 형식 번호가 붙은 원문 (출제 시 Claude가 읽는 용도)

외부 라이브러리 없이 동작한다(.docx는 zip/XML 직접 파싱).
"""
import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = s.replace(" ", " ").replace("​", "")
    return re.sub(r"[ \t]+", " ", s).strip()


# ---------------------------------------------------------------- markdown / txt
def parse_text(path: Path, markdown: bool):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    blocks = []  # (kind, level, text, line_start, line_end)
    i, n = 0, len(lines)
    buf, buf_start = [], None

    def flush(end):
        nonlocal buf, buf_start
        if buf:
            blocks.append(("para", 0, " ".join(x.strip() for x in buf), buf_start, end))
        buf, buf_start = [], None

    while i < n:
        raw = lines[i]
        s = raw.strip()
        ln = i + 1
        if markdown and s.startswith("```"):
            flush(ln - 1)
            start = ln
            code = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            blocks.append(("code", 0, "\n".join(code), start, min(i + 1, n)))
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s) if markdown else None
        if m:
            flush(ln - 1)
            blocks.append(("heading", len(m.group(1)), m.group(2).strip("# ").strip(), ln, ln))
        elif not s:
            flush(ln - 1)
        elif markdown and (re.match(r"^([-*+]|\d+[.)])\s+", s) or s.startswith("|") or s.startswith(">")):
            flush(ln - 1)
            if s.startswith("|") and re.match(r"^\|?[\s:|-]+\|?$", s):
                pass  # 표 구분선 무시
            else:
                blocks.append(("para", 0, s, ln, ln))
        else:
            if buf_start is None:
                buf_start = ln
            buf.append(s)
        i += 1
    flush(n)
    return blocks


# ---------------------------------------------------------------- docx
def parse_docx(path: Path):
    with zipfile.ZipFile(path) as z:
        doc = ET.fromstring(z.read("word/document.xml"))
        style_names = {}
        if "word/styles.xml" in z.namelist():
            st = ET.fromstring(z.read("word/styles.xml"))
            for s in st.iter(W + "style"):
                sid = s.get(W + "styleId")
                nm = s.find(W + "name")
                if sid and nm is not None:
                    style_names[sid] = nm.get(W + "val", "")

    def heading_level(p):
        ppr = p.find(W + "pPr")
        if ppr is None:
            return 0
        ps = ppr.find(W + "pStyle")
        if ps is not None:
            sid = ps.get(W + "val", "")
            name = style_names.get(sid, sid).lower()
            m = re.search(r"(?:heading|제목)\s*(\d)", name)
            if m:
                return int(m.group(1))
            if name == "title":
                return 1
        ol = ppr.find(W + "outlineLvl")
        if ol is not None:
            return int(ol.get(W + "val", "0")) + 1
        return 0

    def ptext(p):
        out = []
        for el in p.iter():
            if el.tag == W + "t":
                out.append(el.text or "")
            elif el.tag == W + "tab":
                out.append(" ")
            elif el.tag in (W + "br", W + "cr"):
                out.append(" ")
        return "".join(out)

    blocks = []
    body = doc.find(W + "body")
    pno = tno = 0
    for el in body:
        if el.tag == W + "p":
            t = ptext(el)
            if not t.strip():
                continue
            pno += 1  # Word에서 빈 줄을 제외하고 센 문단 순번(제목 포함)
            lv = heading_level(el)
            blocks.append(("heading" if lv else "para", lv, t, f"{pno}번째 문단", None))
        elif el.tag == W + "tbl":
            tno += 1
            for r, tr in enumerate(el.iter(W + "tr"), 1):
                cells = []
                for tc in tr.findall(W + "tc"):
                    cells.append(" ".join(ptext(p) for p in tc.iter(W + "p")).strip())
                if any(cells):
                    blocks.append(("para", 0, "| " + " | ".join(cells) + " |", f"표{tno} {r}행", None))
    return blocks


# ---------------------------------------------------------------- main
def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    entries, md = [], []
    pid = 0
    for f in sys.argv[2:]:
        p = Path(f)
        ext = p.suffix.lower()
        if ext == ".docx":
            blocks = parse_docx(p)
        elif ext in (".md", ".markdown"):
            blocks = parse_text(p, markdown=True)
        elif ext in (".txt", ".text", ""):
            blocks = parse_text(p, markdown=False)
        else:
            print(f"[건너뜀] 지원하지 않는 형식: {p.name} (docx/md/txt만 지원)", file=sys.stderr)
            continue
        md.append(f"\n\n# ===== 파일: {p.name} =====\n")
        path_stack = []
        for kind, lv, text, l1, l2 in blocks:
            text = text if kind == "code" else norm(text)
            if kind == "heading":
                path_stack = path_stack[: lv - 1] + [text]
                md.append(f"\n{'#' * min(lv + 1, 6)} {text}\n")
                continue
            pid += 1
            sec = " > ".join(path_stack)
            lines = None
            if isinstance(l1, str):
                lines = l1
            elif l1:
                lines = f"{l1}행" if l1 == l2 else f"{l1}-{l2}행"
            entries.append({"pid": f"P{pid}", "file": p.name, "section": sec, "lines": lines, "text": text})
            if kind == "code":
                md.append(f"[P{pid}] (코드)\n```\n{text}\n```")
            else:
                md.append(f"[P{pid}] {text}")
        print(f"[완료] {p.name}: 문단 {sum(1 for e in entries if e['file'] == p.name)}개")
    (out / "source_index.json").write_text(json.dumps(entries, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "source_numbered.md").write_text("\n".join(md).strip() + "\n", encoding="utf-8")
    print(f"[저장] {out/'source_index.json'}, {out/'source_numbered.md'} (총 {len(entries)}문단)")


if __name__ == "__main__":
    main()
