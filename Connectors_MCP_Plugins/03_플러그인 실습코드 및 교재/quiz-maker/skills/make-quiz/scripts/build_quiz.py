#!/usr/bin/env python3
"""quiz.json을 검증한 뒤 문제지·정답지 Markdown 2개로 분리 출력한다.

사용법:
    python3 build_quiz.py <quiz.json> <source_index.json> <출력폴더>

검증 실패(오류)가 하나라도 있으면 파일을 만들지 않고 종료코드 1을 반환한다.
경고는 출력만 하고 파일은 생성한다.
"""
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

CIRCLED = "①②③④⑤"
QUOTE_MAP = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", " ": " ", "​": ""})


def cmp_norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s).translate(QUOTE_MAP)
    return re.sub(r"\s+", " ", s).strip()


def location(e: dict) -> str:
    parts = [e["file"]]
    if e.get("section"):
        parts.append(e["section"])
    parts.append(e["lines"] if e.get("lines") else e["pid"])
    return " › ".join(parts)


def validate(quiz, index):
    errors, warns = [], []
    qs = quiz.get("questions") or []
    if not qs:
        errors.append("questions가 비어 있음")
    for i, q in enumerate(qs, 1):
        tag = f"{i}번"
        if q.get("id") != i:
            errors.append(f"{tag}: id가 {q.get('id')} (1부터 순서대로여야 함)")
        t = q.get("type")
        if not str(q.get("stem", "")).strip():
            errors.append(f"{tag}: stem(문제 본문) 없음")
        if t == "mc":
            ch = q.get("choices") or []
            if not 4 <= len(ch) <= 5:
                errors.append(f"{tag}: 선택지 {len(ch)}개 (4~5개여야 함)")
            if len({cmp_norm(c) for c in ch}) != len(ch):
                errors.append(f"{tag}: 중복 선택지 존재")
            a = q.get("answer")
            if not isinstance(a, int) or not 1 <= a <= len(ch):
                errors.append(f"{tag}: answer는 1~{len(ch)} 사이 정수여야 함 (현재 {a!r})")
            for c in ch:
                if re.search(r"모두\s*(정답|옳|맞)|정답\s*없음|해당\s*없음", c):
                    warns.append(f"{tag}: '모두 정답/정답 없음'류 선택지 — 변별력 확인 필요: {c}")
        elif t == "short":
            a = str(q.get("answer", "")).strip()
            if not a:
                errors.append(f"{tag}: 단답형 answer 없음")
            elif cmp_norm(a) in cmp_norm(q.get("stem", "")):
                warns.append(f"{tag}: 정답 '{a}'가 문제 본문에 그대로 노출됨")
        else:
            errors.append(f"{tag}: type은 'mc' 또는 'short' (현재 {t!r})")
        ev = q.get("evidence") or []
        if not ev:
            errors.append(f"{tag}: evidence(원문 근거) 없음")
        for j, e in enumerate(ev, 1):
            pid, quote = e.get("pid"), str(e.get("quote", ""))
            src = index.get(pid)
            if src is None:
                errors.append(f"{tag} 근거{j}: 존재하지 않는 문단 {pid!r}")
                continue
            if len(cmp_norm(quote)) < 5:
                errors.append(f"{tag} 근거{j}: 인용이 너무 짧음 (5자 이상)")
            elif cmp_norm(quote) not in cmp_norm(src["text"]):
                hit = [p for p, s in index.items() if cmp_norm(quote) in cmp_norm(s["text"])]
                hint = f" → 실제 위치: {', '.join(hit[:3])}" if hit else " → 원문 어디에도 없음(의역·변형 금지)"
                errors.append(f"{tag} 근거{j}: 인용이 {pid} 원문과 불일치{hint}\n      인용: {quote}")
    mc = [q for q in qs if q.get("type") == "mc" and isinstance(q.get("answer"), int)]
    if len(mc) >= 5:
        cnt = Counter(q["answer"] for q in mc)
        top, n = cnt.most_common(1)[0]
        if n / len(mc) > 0.4:
            warns.append(f"객관식 정답이 {CIRCLED[top-1]}번에 {n}/{len(mc)}개 몰림 — 위치 분산 권장 (분포: {dict(sorted(cnt.items()))})")
    return errors, warns


def render(quiz, index):
    title = quiz.get("title", "퀴즈")
    qs = quiz["questions"]
    n_mc = sum(q["type"] == "mc" for q in qs)
    n_sa = len(qs) - n_mc
    srcs = ", ".join(quiz.get("source_files") or sorted({e["file"] for e in index.values()}))
    kinds = " · ".join(x for x in [f"객관식 {n_mc}" if n_mc else "", f"단답형 {n_sa}" if n_sa else ""] if x)

    # ---- 문제지
    P = [f"# {title} — 문제지", "", f"- 문항 수: {len(qs)}문항 ({kinds})", f"- 출제 범위: {srcs}"]
    if quiz.get("instructions"):
        P.append(f"- 안내: {quiz['instructions']}")
    P += ["", "이름: ____________ 　 점수: ______ / " + str(len(qs)), "", "---", ""]
    for q in qs:
        label = "객관식" if q["type"] == "mc" else "단답형"
        P.append(f"**{q['id']}.** [{label}] {q['stem'].strip()}")
        P.append("")
        if q.get("code"):
            P += ["```" + q.get("code_lang", ""), q["code"].rstrip(), "```", ""]
        if q["type"] == "mc":
            for k, c in enumerate(q["choices"]):
                P.append(f"{CIRCLED[k]} {c}  ")
        else:
            P.append("답: ______________________")
        P += ["", ""]

    # ---- 정답지
    A = [f"# {title} — 정답지", "", f"- 문항 수: {len(qs)}문항 ({kinds})", f"- 출제 범위: {srcs}", "", "## 빠른 정답표", "",
         "| 번호 | 유형 | 정답 |", "|---:|:---:|---|"]
    for q in qs:
        if q["type"] == "mc":
            A.append(f"| {q['id']} | 객관식 | {CIRCLED[q['answer']-1]} |")
        else:
            acc = q.get("accept") or []
            extra = f" (인정: {', '.join(acc)})" if acc else ""
            A.append(f"| {q['id']} | 단답형 | {q['answer']}{extra} |")
    A += ["", "## 문항별 정답·해설·근거", ""]
    for q in qs:
        A.append(f"### {q['id']}. {q['stem'].strip().splitlines()[0]}")
        A.append("")
        if q["type"] == "mc":
            A.append(f"**정답: {CIRCLED[q['answer']-1]} {q['choices'][q['answer']-1]}**")
        else:
            acc = f" (인정: {', '.join(q['accept'])})" if q.get("accept") else ""
            A.append(f"**정답: {q['answer']}**{acc}")
        A.append("")
        if q.get("explanation"):
            A += [f"해설: {q['explanation'].strip()}", ""]
        for e in q["evidence"]:
            src = index[e["pid"]]
            A.append(f"> 📌 근거 — {location(src)}  ")
            A.append(f"> “{e['quote'].strip()}”")
            A.append("")
        A += ["---", ""]
    return "\n".join(P).rstrip() + "\n", "\n".join(A).rstrip() + "\n"


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    quiz = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    index = {e["pid"]: e for e in json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))}
    out = Path(sys.argv[3])
    errors, warns = validate(quiz, index)
    for w in warns:
        print(f"[경고] {w}")
    if errors:
        for e in errors:
            print(f"[오류] {e}")
        print(f"\n검증 실패: 오류 {len(errors)}건 — 파일을 생성하지 않았습니다. quiz.json을 고친 뒤 다시 실행하세요.")
        sys.exit(1)
    out.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r'[\\/:*?"<>|\s]+', "_", quiz.get("title", "퀴즈")).strip("_") or "퀴즈"
    pq, pa = out / f"{safe}_문제지.md", out / f"{safe}_정답지.md"
    q_md, a_md = render(quiz, index)
    pq.write_text(q_md, encoding="utf-8")
    pa.write_text(a_md, encoding="utf-8")
    print(f"[검증 통과] {len(quiz['questions'])}문항, 근거 {sum(len(q['evidence']) for q in quiz['questions'])}건 모두 원문 일치")
    print(f"[저장] {pq}\n[저장] {pa}")


if __name__ == "__main__":
    main()
