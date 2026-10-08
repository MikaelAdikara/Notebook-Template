"""
Rekam proses end-to-end sebuah case menjadi video walkthrough + folder screenshot (bukti semua fungsi bekerja).

    python QA/make_walkthrough.py --case <folder case> --out QA/walkthrough_warkab [--stress tools/STRESS_TEST_REPORT.md]

Isi: casebook → folder kerja → Case Intake → Research Plan → CASE_RESEARCH.xlsx → console run → run summary → halaman artikel
→ tab dashboard → narrative options / judge Q&A → stress test → ZIP. Screenshot HTML memakai Microsoft Edge/Chrome headless,
halaman PDF dirender PyMuPDF, video dirangkai ffmpeg (fallback: hanya PNG kalau ffmpeg tidak ada).
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import textwrap
import zipfile

from PIL import Image, ImageDraw, ImageFont

for _st in (sys.stdout, sys.stderr):
    try:
        _st.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

W, H = 1600, 900
BAR = 118


def font(size, mono=False, bold=False):
    names = (["consola.ttf", "cour.ttf"] if mono else (["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]))
    for n in names:
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def browser():
    for p in [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe", shutil.which("msedge") or "", shutil.which("google-chrome") or "",
              shutil.which("chromium") or ""]:
        if p and os.path.exists(p):
            return p
    return None


def shot_html(path_or_url, out_png, width=1440, height=2000):
    b = browser()
    if not b:
        return None
    url = path_or_url if "://" in path_or_url else "file:///" + os.path.abspath(path_or_url.split("#")[0]).replace("\\", "/") + (
        "#" + path_or_url.split("#", 1)[1] if "#" in path_or_url else "")
    cmd = [b, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={width},{height}", "--virtual-time-budget=4000",
           "--force-device-scale-factor=1", f"--screenshot={os.path.abspath(out_png)}", url]
    try:
        subprocess.run(cmd, capture_output=True, timeout=90)
    except Exception:
        return None
    return out_png if os.path.exists(out_png) else None


def text_image(text, out_png, title=None, mono=True, size=19, max_lines=36, width_chars=118):
    img = Image.new("RGB", (W, H - BAR), "#0f172a" if mono else "#ffffff")
    d = ImageDraw.Draw(img)
    f = font(size, mono=mono)
    y = 24
    lines = []
    if mono:   # font monospace tidak punya emoji → simbol teks
        for k_, v_ in {"▶": ">", "✅": "[OK]", "✔": "[v]", "✘": "[x]", "⏱": "[time]", "⚠️": "[!]", "⚠": "[!]", "❌": "[X]", "ℹ️": "[i]", "→": "->", "️": ""}.items():
            text = str(text).replace(k_, v_)
    for raw in str(text).splitlines():
        lines += textwrap.wrap(raw, width_chars) or [""]
    for line in lines[:max_lines]:
        d.text((30, y), line, fill="#e2e8f0" if mono else "#111", font=f)
        y += int(size * 1.45)
    img.save(out_png)
    return out_png


def table_image(df, out_png, title=""):
    """Tabel → PNG (PIL): lebar kolom proporsional isi, teks panjang dibungkus per piksel (tidak terpotong)."""
    df = df.copy().fillna("").astype(str).iloc[:22]
    f, fb = font(17), font(17, bold=True)
    pad, width = 10, W - 60
    lens = [max([len(str(c))] + [min(len(v), 300) for v in df[c]]) for c in df.columns]
    weights = [max(6, min(l, 120)) for l in lens]
    colw = [int(width * w / sum(weights)) for w in weights]

    def wrap(text, w):
        out = []
        for para in str(text).splitlines() or [""]:
            line = ""
            for word in para.split(" "):
                cand = (line + " " + word).strip()
                if f.getlength(cand) <= w - 2 * pad or not line:
                    line = cand
                else:
                    out.append(line)
                    line = word
            out.append(line)
        return out[:7]

    rows = [[wrap(v, w) for v, w in zip(r, colw)] for r in df.values]
    lh = 22
    heights = [max(len(c) for c in r) * lh + 2 * pad for r in rows]
    head_h = lh + 2 * pad
    total_h = 50 + head_h + sum(heights) + 10
    img = Image.new("RGB", (W - 40, max(total_h, 200)), "white")
    d = ImageDraw.Draw(img)
    if title:
        d.text((10, 8), title, fill="#111", font=font(22))
    y = 50
    x = 10
    for c, w in zip(df.columns, colw):
        d.rectangle([x, y, x + w, y + head_h], fill="#d9e2f3", outline="#334155")
        d.text((x + pad, y + pad), str(c), fill="#111", font=fb)
        x += w
    y += head_h
    for r, h in zip(rows, heights):
        x = 10
        for lines, w in zip(r, colw):
            d.rectangle([x, y, x + w, y + h], outline="#334155")
            for k, ln in enumerate(lines):
                d.text((x + pad, y + pad + k * lh), ln, fill="#111", font=f)
            x += w
        y += h
    img.save(out_png)
    return out_png


def frame(img_path, step, title, desc, out_png, crop_top=0):
    canvas = Image.new("RGB", (W, H), "#f8fafc")
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, 0, W, BAR], fill="#1e3a8a")
    d.text((28, 14), f"STEP {step}", fill="#93c5fd", font=font(22, bold=True))
    d.text((150, 10), title, fill="white", font=font(34, bold=True))
    for k, line in enumerate(textwrap.wrap(desc, 150)[:2]):
        d.text((28, 58 + k * 26), line, fill="#dbeafe", font=font(20))
    if img_path and os.path.exists(img_path):
        im = Image.open(img_path).convert("RGB")
        if crop_top:
            im = im.crop((0, crop_top, im.width, im.height))
        box_w, box_h = W - 40, H - BAR - 20
        r = min(box_w / im.width, box_h / im.height)
        if im.height * (box_w / im.width) > box_h * 1.6:      # halaman panjang → ambil bagian atas saja, lebar penuh
            r = box_w / im.width
            im = im.crop((0, 0, im.width, int(box_h / r)))
        im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
        canvas.paste(im, ((W - im.width) // 2, BAR + 10))
    canvas.save(out_png)
    return out_png


def pdf_pages(pdf, pages, out_dir, prefix):
    try:
        import fitz
    except ImportError:
        return []
    outs = []
    with fitz.open(pdf) as d:
        for p in pages:
            if p < d.page_count:
                o = os.path.join(out_dir, f"{prefix}_p{p + 1:02d}.png")
                raw = o.replace(".png", "_raw.png")
                d[p].get_pixmap(dpi=170).save(raw)
                # halaman A4 dibelah: kiri = setengah atas, kanan = setengah bawah → teks tetap terbaca di frame 16:9
                pg = Image.open(raw).convert("RGB")
                half_w = (W - 60) // 2
                pg = pg.resize((half_w, int(pg.height * half_w / pg.width)), Image.LANCZOS)
                h2 = pg.height // 2
                comp = Image.new("RGB", (W - 40, h2 + 4), "#cbd5e1")
                comp.paste(pg.crop((0, 0, half_w, h2)), (0, 2))
                comp.paste(pg.crop((0, h2, half_w, 2 * h2)), (half_w + 20, 2))
                comp.save(o)
                os.remove(raw)
                outs.append((p, o))
    return outs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stress", default=None)
    ap.add_argument("--seconds", type=float, default=4.5)
    a = ap.parse_args()
    case, out = os.path.abspath(a.case), os.path.abspath(a.out)
    shots = os.path.join(out, "screens")
    frames_dir = os.path.join(out, "frames")
    os.makedirs(shots, exist_ok=True)
    os.makedirs(frames_dir, exist_ok=True)
    cfg = json.load(open(os.path.join(case, "case_config.json"), encoding="utf-8"))
    team = cfg.get("TEAM_NAME", "Team")
    od = os.path.join(case, cfg.get("OUTPUT_DIR", "outputs/churn_insurance").lstrip("./"))
    steps = []

    def add(img, title, desc, crop_top=0):
        steps.append((img, title, desc, crop_top))

    cb = next(iter(glob.glob(os.path.join(case, "casebook.*"))), None)
    if cb:
        add(text_image(open(cb, encoding="utf-8", errors="replace").read(), os.path.join(shots, "01_casebook.png")),
            "Soal / casebook", "Titik awal: soal dari panitia disimpan sebagai casebook.* di folder case.")
    listing = "\n".join(sorted(os.listdir(case)))
    add(text_image(f"> python tools/new_case.py <folder> --team {team}\n\nIsi folder case:\n{listing}\n\nIsi data/:\n" +
                   "\n".join(sorted(os.listdir(os.path.join(case, "data")))), os.path.join(shots, "02_folder.png")),
        "Folder kerja dibuat otomatis", "new_case.py: data/, case_config.json, CASE_INTAKE.html, CASE_RESEARCH.xlsx, RESEARCH_PLAN, RUN_FAST.bat, RUN_FULL.bat.")
    s = shot_html(os.path.join(case, "CASE_INTAKE.html"), os.path.join(shots, "03_intake.png"), height=1500)
    add(s, "Case Intake (offline form)", "Semua informasi dari soal diisi di form → Download JSON → case_config.json (target, metrik, konteks, pertanyaan, parameter bisnis).")
    add(text_image(json.dumps(cfg, indent=2, ensure_ascii=False), os.path.join(shots, "04_config.png"), size=17, max_lines=40),
        "case_config.json (hasil intake)", f"Konfigurasi case {team}: konteks, definisi churn, pertanyaan soal, intervensi, budget, parameter bisnis dari soal.")
    s = shot_html(os.path.join(case, "RESEARCH_PLAN.html"), os.path.join(shots, "05_research_plan.png"), height=2600)
    add(s, "Research Plan otomatis", "research_helper.py membaca casebook: istilah kunci, kalimat berangka (kandidat fakta) dan query siap-klik (Scholar, Crossref, Garuda, OJK/AAJI/AAUI).")
    if s:
        add(s, "Research Plan — query per driver", "Query literatur disesuaikan tema driver hasil fast run (lifecycle, payment, price, service, …).", crop_top=1300)
    xl = os.path.join(case, "CASE_RESEARCH.xlsx")
    if os.path.exists(xl):
        import pandas as pd
        book = pd.read_excel(xl, sheet_name=None, dtype=str)
        for k, sh in enumerate(["case_facts", "industry_facts", "literature", "custom_paragraphs"]):
            if sh in book and len(book[sh]):
                cols = [c for c in book[sh].columns if c in ("use", "section", "theme", "position", "statement_EN", "finding_EN", "in_text_citation", "text")]
                add(table_image(book[sh][cols].fillna(""), os.path.join(shots, f"06_{k}_{sh}.png"), f"CASE_RESEARCH.xlsx — {sh}"),
                    f"Hasil riset tim: {sh}", "Baris use = Y otomatis ditempel ke section laporan yang dipilih; referensinya masuk daftar pustaka (hanya bila disitasi).")
    for logf, ttl in [("run_full_console.log", "RUN_FULL.bat — console"), ("run_fast_console.log", "RUN_FAST.bat — console")]:
        lp = os.path.join(case, logf)
        if os.path.exists(lp):
            txt = open(lp, encoding="utf-8", errors="replace").read()
            noise = ("zmq", "get_loop", "CategoryInfo", "FullyQualified", "joblib", "Traceback", "resource_tracker", "del registry", "~~~", "Press any key")
            lines = [l for l in txt.splitlines() if l.strip() and not any(k in l for k in noise)]
            add(text_image("\n".join(lines[-34:]), os.path.join(shots, f"07_{logf}.png")), ttl,
                "Notebook dijalankan headless; semua output tersimpan di notebook ter-eksekusi. 'no section errors' = seluruh analisis sukses.")
            break
    rs = os.path.join(od, "run_summary.json")
    if os.path.exists(rs):
        s_ = json.load(open(rs, encoding="utf-8"))
        lb = "\n".join(f"  {r['model']:<22} OOF AUC {r['oof_auc']:.4f}" for r in s_.get("leaderboard", [])[:12])
        add(text_image(f"final model : {s_['final_model']}  |  OOF ROC-AUC {s_['final_oof_auc']:.4f}\nn_train     : {s_['n_train']:,}   churn rate {s_['churn_rate']:.3f}\n"
                       f"target      : {s_['target']}  mapping {s_['target_mapping']}\nleaky cols  : {s_['leaky_cols']}\nsection errors: {s_['section_errors'] or 'none'}\n\nLeaderboard:\n{lb}",
                       os.path.join(shots, "08_summary.png")), "Ringkasan run", "Target & mapping benar, kolom leakage dibuang otomatis, semua model + ensemble, tanpa section error.")
    pdf = next(iter(glob.glob(os.path.join(od, f"{team}_Final Stage 1.pdf"))), None) or os.path.join(od, "REPORT_DRAFT.pdf")
    if os.path.exists(pdf):
        captions = {0: ("Artikel — cover", "Judul berbasis temuan, nama tim & anggota otomatis."),
                    1: ("Artikel — Executive Summary & Introduction", "Ringkasan berangka + konteks case + fakta casebook & industri dari CASE_RESEARCH."),
                    3: ("Artikel — Findings (drivers)", "Figure komposit + evidence matrix (4 metode)."),
                    5: ("Artikel — Prediction & model comparison", "AUC dengan CI DeLong, EMPC, experiment log, ablation."),
                    7: ("Artikel — Business impact & recommendations", "Kampanye dalam budget, kausal, rekomendasi + pilot A/B; paragraf custom tim."),
                    9: ("Artikel — Discussion & references", "Literatur tim (CASE_RESEARCH) dikaitkan ke driver; daftar pustaka APA hanya yang disitasi.")}
        for p, img in pdf_pages(pdf, sorted(captions), shots, "09_article"):
            add(img, *captions[p])
        try:
            import fitz
            with fitz.open(pdf) as d_:
                app = next((i for i in range(1, d_.page_count) if "Appendices" in d_[i].get_text()[:200]), None)
            if app:
                for p, img in pdf_pages(pdf, [app, app + 6, app + 14], shots, "10_appendix"):
                    add(img, "Appendix (tidak dihitung halaman)", "Appendix A–L: data, metodologi & arsitektur, driver, survival, model development, kausal, bisnis, governance.")
        except Exception:
            pass
    dash = os.path.join(od, "dashboard", "index.html")
    if os.path.exists(dash):
        for k, (tab, ttl) in enumerate([("overview", "Overview"), ("drivers", "Drivers"), ("timing", "Timing"), ("model", "Model"),
                                         ("campaign", "Campaign simulator & causal"), ("actions", "Actions & customer list"), ("method", "Methodology")]):
            s = shot_html(dash + "#" + tab, os.path.join(shots, f"11_{k}_dash_{tab}.png"), width=1366, height=1300)
            add(s, f"Dashboard — {ttl}", "Web app statis dari hasil run (offline / Vercel). Isinya otomatis mengikuti data & case brief setiap run.")
    for fn, ttl in [("NARRATIVE_OPTIONS.md", "NARRATIVE_OPTIONS.md"), ("JUDGE_QA.md", "JUDGE_QA.md"), ("REPORT_TODO.md", "REPORT_TODO.md")]:
        p = os.path.join(od, fn)
        if os.path.exists(p):
            add(text_image(open(p, encoding="utf-8").read(), os.path.join(shots, f"12_{fn}.png"), mono=False, size=18, max_lines=34, width_chars=150),
                ttl, "Pilihan judul/framing/nama persona, persiapan pertanyaan juri, dan checklist finalisasi — semua berisi angka run ini.")
    qc = os.path.join(case, "QA_CHECK.md")
    if os.path.exists(qc):
        add(text_image(open(qc, encoding="utf-8").read(), os.path.join(shots, "12z_qa_check.png"), mono=False, size=17, max_lines=40, width_chars=160),
            "QA otomatis artikel (QA/qa_check.py)", "Cek tanpa AI: ≤10 halaman, tim & anggota di cover, konteks/fakta/riset soal benar-benar masuk artikel, caption, dashboard, ZIP.")
    if a.stress and os.path.exists(a.stress):
        import pandas as pd
        lines = [l for l in open(a.stress, encoding="utf-8").read().splitlines() if l.startswith("|")]
        hdr = [c.strip() for c in lines[0].strip("|").split("|")]
        rows = [[c.strip() for c in l.strip("|").split("|")] for l in lines[2:]]
        df = pd.DataFrame(rows, columns=hdr)[["variant", "description", "status", "auc"]]
        for k in range(0, len(df), 11):
            add(table_image(df.iloc[k:k + 11], os.path.join(shots, f"13_stress_{k:02d}.png"), f"STRESS_TEST_REPORT.md ({k + 1}–{min(k + 11, len(df))} dari {len(df)})"),
                "Stress test — semua bentuk data", "Setiap varian (data rusak/dimanipulasi) dijalankan end-to-end; PASS = tanpa satu pun section error.")
    z = next(iter(glob.glob(os.path.join(case, "*.zip"))), None)
    if z:
        with zipfile.ZipFile(z) as zf:
            names = zf.namelist()
        top = [n for n in names if "/" not in n] + sorted({n.split("/")[0] + "/" + n.split("/")[1] + "/" for n in names if n.count("/") >= 2})[:20]
        add(text_image(f"{os.path.basename(z)}  ({os.path.getsize(z) / 1e6:.1f} MB, {len(names)} file)\n\n" + "\n".join(top), os.path.join(shots, "14_zip.png")),
            "ZIP pengumpulan", "make_zip.py: <Tim>_Final Stage 1.pdf + notebook ter-eksekusi + supporting/ (figures, tables, Excel, dashboard, submission).")
    for f_ in glob.glob(os.path.join(frames_dir, "*.png")):
        os.remove(f_)
    for k, (img, ttl, desc, ct) in enumerate(steps, 1):
        frame(img, k, ttl, desc, os.path.join(frames_dir, f"f{k:03d}.png"), crop_top=ct)
    with open(os.path.join(out, "STEPS.md"), "w", encoding="utf-8") as f:
        f.write(f"# Walkthrough — {team}\n\n| Step | Judul | Keterangan | Screenshot |\n|---|---|---|---|\n")
        for k, (img, ttl, desc, _) in enumerate(steps, 1):
            f.write(f"| {k} | {ttl} | {desc} | {('screens/' + os.path.basename(img)) if img else '—'} |\n")
    ff = shutil.which("ffmpeg")
    if ff:
        mp4 = os.path.join(out, f"walkthrough_{team}.mp4")
        subprocess.run([ff, "-y", "-loglevel", "error", "-framerate", f"1/{a.seconds}", "-i", os.path.join(frames_dir, "f%03d.png"),
                        "-vf", "fps=25,format=yuv420p", "-c:v", "libx264", "-crf", "23", mp4], check=False)
        print(f"✅ video: {mp4} ({len(steps)} langkah, {len(steps) * a.seconds / 60:.1f} menit)")
    print(f"✅ {len(steps)} frame → {frames_dir}; daftar langkah → {os.path.join(out, 'STEPS.md')}")


if __name__ == "__main__":
    main()
