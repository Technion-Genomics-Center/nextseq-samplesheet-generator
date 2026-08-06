# NextSeq 2000 SampleSheet Generator

Web app for building **BaseSpace BCL Convert v2** sample sheets for NextSeq 2000 runs, with live validation of sample names and index collisions.

**▶ Open the app: https://technion-genomics-center.github.io/nextseq-samplesheet-generator/**

Single self-contained HTML file — no install, no server, no dependencies. It also works offline: download `index.html` and double-click it.

---

## What it does

1. **Run setup** — project/run name, index kit, index plate ID, and sequencing cycles (Read 1 / Read 2, with Index 1 / Index 2 auto-detected from the chosen indexes and overridable).
2. **Samples** — type them in, or bulk-paste two columns. Barcode numbers, plate wells and well aliases all resolve:

   ```
   Sample ID	Barcode
   1	97
   2	98
   ```

   Accepts `A01`, `A1`, `1A`, `12H`, Smart-seq codes like `U025`, and plate barcode numbers (`97` → well `A01`). A header row is skipped automatically.
3. **Validation (live)**
   - Sample names must be **unique** — duplicates are flagged.
   - Spaces and special characters are converted to `_` (every change is listed).
   - Index sequences must be unique with **Hamming distance ≥ 3** on the combined i7+i5 — identical or too-similar pairs are flagged.
   - If index lengths differ, shorter indexes are padded per the kit's padding rule (NEB 8 bp → 10 bp adds `AT` to i7 and `AC` to i5); if a kit has no padding rule defined, that's an error instead.
   - Invalid or reused wells are caught.
4. **Output**
   - **Copy for BaseSpace** — tab-separated rows to paste straight into the [Run Planning sample table](https://basespace.illumina.com/run-planning/config/1/sample-analysis-setup).
   - **Sample sheet .csv** — BCL Convert v2 file to upload instead.
   - **Records .csv** — full archive table (plate, well, index IDs, raw + final sequences), named `YYYY-MM-DD_Project.csv`.

### Index orientation

Both **Index and Index2 are written in forward orientation**, which is what BaseSpace expects for the NextSeq 2000 — BaseSpace reverse-complements i5 for the instrument itself. A dropdown switches i5 to reverse-complement for legacy workflows.

---

## Built-in index kits

`NEBNext_UDI` · `Nextera_UD_Indexes` · `Smartseq` · `Zymo_RRBS` · `sc10X` · `Qiaseq_miRNA` · `WM_Stubby` · `Lexogen` — 20 plates, 1,600+ index pairs, extracted from the lab's `SampleSheet_generator.xlsx`.

## Adding index plates

Open **➕ Manage index plates** at the bottom of the app.

- **Upload** the vendor's `.csv` / `.tsv` / `.xlsx` plate file — columns are auto-detected (and adjustable), vendor title rows are skipped. Or paste the table directly.
- Saved plates live in **your browser** and are immediately available in the plate dropdown.

### Sharing plates with the whole lab

Local plates stay on one machine. To publish them to everyone:

1. Click **⬇ shared_plates.json (for git)** — it merges the existing lab plates with yours.
2. Commit the downloaded file to the **root of this repository**, replacing `shared_plates.json`.
3. Once GitHub Pages redeploys, every user of the app gets those plates automatically (shown as `lab · <plate>`).

This keeps the lab's plate definitions **version-controlled in git**, with history of who added what.

---

## Repository layout

| Path | Purpose |
|---|---|
| `index.html` | The app — self-contained, what GitHub Pages serves |
| `shared_plates.json` | Lab-shared index plates, loaded by the app at runtime |
| `ss_template.html` | Source template (app code without the embedded dataset) |
| `samplesheet_data.json` | Extracted index dataset |
| `build.py` | Rebuilds `index.html` from the template + dataset |

### Rebuilding

Edit `ss_template.html` (or `samplesheet_data.json`), then:

```bash
python build.py
```

That regenerates `index.html`. Don't hand-edit `index.html` — it's generated.

---

Maintained by the Technion Genomics Center (ATGC).
