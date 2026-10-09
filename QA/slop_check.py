"""
Audit tulisan "terasa AI" untuk paper (tanpa AI): kosakata & frasa khas AI, em dash, ekor -ing kosong, adverb pengisi,
'not only X but also Y', pembuka 'Moreover/Furthermore', kalimat pasif, kalimat beruntun dengan panjang seragam, heading Title Case.

Aturan diadaptasi dari skill ai-paraphrase (Wikipedia: Signs of AI writing), anti-ai-slop-writing dan stop-slop, disesuaikan
dengan ragam akademik (kontraksi tidak diwajibkan; pasif boleh di bagian metode tetapi dibatasi).

    python QA/slop_check.py "case/outputs/churn_insurance/Warkab_Final Stage 1.pdf"          → isi utama saja (sebelum Appendices)
    python QA/slop_check.py paper.docx --all                                              → termasuk appendix
    python QA/slop_check.py paper.pdf --out SLOP_CHECK.md

Exit code 0 = skor ≥ 80 (aman), 1 = perlu revisi. Setiap temuan menyebut kutipan + saran pengganti.
"""
import argparse
import os
import re
import sys

for _st in (sys.stdout, sys.stderr):
    try:
        _st.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# kata → saran pengganti (ragam akademik)
BANNED = {
    "delve": "examine", "tapestry": "(hapus)", "landscape": "market / situation", "testament": "evidence", "vibrant": "(hapus)",
    "pivotal": "main / decisive", "crucial": "important / necessary", "intricate": "complex", "intricacies": "details",
    "meticulous": "careful", "meticulously": "carefully", "bolster": "support", "bolstered": "supported", "garner": "gain",
    "garnered": "gained", "underscore": "show", "underscores": "shows", "underscoring": "(hapus ekor)", "interplay": "interaction",
    "multifaceted": "(sebut aspeknya)", "foster": "encourage", "fostering": "encouraging", "leverage": "use", "leverages": "uses",
    "leveraging": "using", "utilize": "use", "utilizes": "uses", "utilise": "use", "utilization": "use", "commence": "start",
    "facilitate": "allow / help", "facilitates": "allows", "encompass": "cover", "encompassing": "covering", "paramount": "most important",
    "groundbreaking": "(hapus)", "cutting-edge": "(sebut metodenya)", "game-changing": "(hapus)", "transformative": "(sebut efeknya)",
    "seamless": "(hapus)", "seamlessly": "(hapus)", "comprehensive": "(sebut cakupannya)", "endeavor": "effort", "endeavour": "effort",
    "aforementioned": "this / these", "harnessing": "using", "spearheading": "leading", "navigating": "handling", "showcasing": "showing",
    "showcase": "show", "highlighting": "(hapus ekor)", "emphasizing": "(hapus ekor)", "emphasising": "(hapus ekor)",
    "enhancing": "improving", "enhance": "improve", "enhances": "improves", "unprecedented": "(beri angka)", "remarkable": "(beri angka)",
    "stunning": "(hapus)", "profound": "large", "synergy": "(hapus)", "synergies": "(hapus)", "valuable insights": "(sebut temuannya)",
    "insightful": "(hapus)", "holistic": "(sebut cakupannya)", "nuanced": "(sebut detailnya)", "realm": "field", "align with": "match",
    "aligns with": "matches", "robust": "reliable / stable (kecuali istilah statistik 'robust standard errors')", "streamline": "simplify",
    "empower": "allow", "empowering": "allowing", "elevate": "raise", "invaluable": "useful", "noteworthy": "(beri angka)",
}
PHRASES = [
    r"it is worth noting", r"it'?s worth noting", r"it is important to note", r"it'?s important to note", r"at its core",
    r"in the realm of", r"when it comes to", r"plays? an? (crucial|pivotal|vital|key|important|significant) role", r"serves as a",
    r"stands as", r"in today'?s", r"in conclusion", r"in summary,", r"to sum up", r"this is where", r"at the end of the day",
    r"the bottom line", r"bridge the gap", r"move the needle", r"take .{0,15} to the next level", r"a wide range of", r"a variety of",
    r"valuable insights?", r"deeper understanding", r"shed(s)? light on", r"paves? the way", r"evolving", r"ever-changing",
    r"key takeaways?", r"data-driven insights", r"actionable insights", r"rich (data|insights)",
]
OPENERS = ["Moreover", "Furthermore", "Additionally", "Interestingly", "Notably", "Importantly", "Indeed", "Overall", "Ultimately",
           "In essence", "Essentially", "Crucially", "Firstly", "Secondly", "Thirdly", "Certainly", "Of course"]
ADVERBS = ["really", "just", "literally", "genuinely", "honestly", "simply", "actually", "deeply", "truly", "fundamentally",
           "inherently", "inevitably", "interestingly", "importantly", "crucially", "significantly", "notably", "clearly",
           "highly", "extremely", "incredibly", "particularly", "remarkably", "substantially", "seamlessly", "effectively", "ultimately"]
ING_TAIL = r",\s+(highlighting|underscoring|emphasizing|emphasising|ensuring|reflecting|showcasing|fostering|enhancing|contributing to|" \
           r"demonstrating|illustrating|signalling|signaling|indicating that|suggesting that|making it|thereby)\b"
NOT_BUT = r"\bnot (only|just|merely)\b[^.]{0,80}\bbut( also)?\b|\bisn'?t (just|only)\b"
PASSIVE = r"\b(is|are|was|were|be|been|being)\s+(\w+ly\s+)?(\w+ed|built|done|made|shown|found|seen|given|taken|known|drawn|run|set|kept|held|put|met)\b"


def read_text(path, include_appendix):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz
        with fitz.open(path) as d:
            pages = [p.get_text() for p in d]
        if not include_appendix:
            cut = next((i for i, t in enumerate(pages) if re.search(r"^\s*Appendices\s*$", t, re.M)), len(pages))
            pages = pages[1:cut] if cut > 1 else pages              # halaman 1 = cover
        txt = "\n".join(pages)
    elif ext == ".docx":
        import docx
        paras = [p.text for p in docx.Document(path).paragraphs]
        if not include_appendix and "Appendices" in paras:
            paras = paras[:paras.index("Appendices")]
        txt = "\n".join(paras)
    else:
        txt = open(path, encoding="utf-8", errors="replace").read()
    if not include_appendix:
        txt = re.split(r"\n\s*References\s*\n", txt)[0]            # daftar pustaka tidak diaudit
    # gabungkan baris PDF yang terpotong
    txt = re.sub(r"-\n(?=[a-z])", "", txt)
    txt = re.sub(r"(?<![.:!?\n])\n(?![\n•\d])", " ", txt)
    return txt


def sentences(txt):
    flat = re.sub(r"\s+", " ", txt)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(])", flat)
    return [p.strip() for p in parts if len(p.split()) >= 4 and not re.match(r"^(Figure|Table) [A-Z]?\.?\d", p)]


def audit(txt):
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", txt)
    n_words = max(len(words), 1)
    low = txt.lower()
    F = []

    def add(cat, quote, fix, weight):
        F.append((cat, re.sub(r"\s+", " ", quote).strip()[:110], fix, weight))

    for w, fix in BANNED.items():
        for m in re.finditer(r"\b" + re.escape(w) + r"\b", low):
            ctx = txt[max(0, m.start() - 40): m.end() + 40]
            if w == "robust" and (re.search(r"robust (standard|variance|regression|estimator|to)", low[m.start():m.end() + 25])
                                  or low[max(0, m.start() - 7):m.start()] == "doubly "):
                continue
            add("D Kosakata khas AI", ctx, f"'{w}' → {fix}", 2)
    for p in PHRASES:
        for m in re.finditer(p, low):
            add("A/H Frasa klise", txt[max(0, m.start() - 30): m.end() + 30], "tulis faktanya langsung / hapus", 2)
    for s in sentences(txt):
        for o in OPENERS:
            if s.startswith(o + ",") or s.startswith(o + " "):
                add("E Pembuka transisi", s, f"hapus '{o}' atau sambungkan dengan kalimat sebelumnya", 1)
    for m in re.finditer(ING_TAIL, txt, re.I):
        add("B Ekor -ing kosong", txt[max(0, m.start() - 50): m.end() + 30], "pecah jadi kalimat dengan subjek, atau hapus ekornya", 2)
    for m in re.finditer(NOT_BUT, txt, re.I):
        add("E Paralelisme 'not X but Y'", txt[max(0, m.start() - 10): m.end() + 30], "nyatakan Y langsung", 2)
    for a in ADVERBS:
        for m in re.finditer(r"\b" + a + r"\b", low):
            if a == "significantly" and re.search(r"\bp\s*[<=]?\s*[0-9<]|delong|p-value|q-value", low[m.end():m.end() + 60]):
                continue                                         # klaim uji statistik yang sah
            add("Adverb pengisi", txt[max(0, m.start() - 35): m.end() + 35], f"hapus '{a}' atau ganti angka", 1)
    em = [m for m in re.finditer(r"(?<=[A-Za-z)',])\s?—\s?(?=[A-Za-z('])", txt)]      # em dash dalam kalimat, bukan sel tabel kosong
    em_limit = max(1, n_words // 500)
    if len(em) > em_limit:
        for m in em[em_limit:]:
            add("F Em dash berlebih", txt[max(0, m.start() - 40): m.end() + 40], "ganti koma, titik dua, kurung atau titik", 1)
    sents = sentences(txt)
    n_pass = 0
    for s in sents:
        if re.search(PASSIVE, s):
            n_pass += 1
    pass_share = n_pass / max(len(sents), 1)
    if pass_share > 0.35:
        ex = [s for s in sents if re.search(PASSIVE, s)][:3]
        for s in ex:
            add("Pasif dominan", s, f"{pass_share:.0%} kalimat pasif (batas 35%) → jadikan 'we …' / subjek pelaku", 1)
    lens = [len(s.split()) for s in sents]
    for i in range(len(lens) - 2):
        a, b, c = lens[i:i + 3]
        if max(a, b, c) - min(a, b, c) <= 3 and min(a, b, c) >= 8:
            add("Ritme seragam", sents[i + 1], f"3 kalimat berturut {a}/{b}/{c} kata → pendekkan atau gabungkan salah satu", 1)
    for m in re.finditer(r"^(\d+(\.\d+)*\.?\s+)?([A-Z][a-z]+(\s+(and|of|the|for|in|to|a|an|by|vs\.?|&|[A-Z][a-z]+)){2,})\s*$", txt, re.M):
        line = m.group(0).strip()
        caps = [w for w in line.split() if w[:1].isupper() and len(w) > 3]
        if len(caps) >= 3 and not line.isupper():
            add("F Heading Title Case", line, "pakai sentence case: hanya huruf pertama kapital", 0.5)
    pen = sum(w for *_, w in F)
    score = max(0.0, 100 - 100 * pen / (n_words / 40))
    return F, score, n_words, pass_share, len(em)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--all", action="store_true", help="termasuk appendix & referensi")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    txt = read_text(a.path, a.all)
    F, score, n_words, pass_share, n_em = audit(txt)
    cats = {}
    for cat, q, fix, w in F:
        cats.setdefault(cat, []).append((q, fix))
    lines = [f"# SLOP CHECK — {os.path.basename(a.path)}", "",
             f"Kata dianalisis: {n_words:,} | temuan: {len(F)} | em dash: {n_em} | kalimat pasif: {pass_share:.0%} | "
             f"**skor: {score:.0f}/100** ({'aman' if score >= 80 else 'perlu revisi'})", "",
             "| Kategori | Jumlah | Contoh (kutipan) | Saran |", "|---|---|---|---|"]
    for cat, items in sorted(cats.items(), key=lambda kv: -len(kv[1])):
        for k, (q, fix) in enumerate(items[:3]):
            lines.append(f"| {cat if k == 0 else ''} | {len(items) if k == 0 else ''} | …{q.replace('|', '/')}… | {fix} |")
    lines += ["", "Catatan: tanda di atas adalah indikator, bukan bukti. Jangan sekadar ganti sinonim; tulis fakta/angka spesifik. "
              "Jangan menyentuh angka, nama, kutipan, sitasi dan istilah statistik baku (mis. 'robust standard errors', 'statistically significant')."]
    out = "\n".join(lines)
    print(out)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(out + "\n")
    return 0 if score >= 80 else 1


if __name__ == "__main__":
    sys.exit(main())
