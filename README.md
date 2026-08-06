# NextSeq 2000 SampleSheet Generator

Web app for building **BaseSpace BCL Convert v2** sample sheets for NextSeq 2000 runs, with live validation of sample names and index collisions.

**▶ Open the app: https://technion-genomics-center.github.io/nextseq-samplesheet-generator/**

Single self-contained HTML file — no install, no server, no dependencies. It also works offline: download `index.html` and double-click it.

---

## What it does

1. **Run setup** — run name and sequencing cycles (Read 1 / Read 2, with Index 1 / Index 2 auto-detected from the chosen indexes and overridable).
2. **Projects** — a run can hold **several projects, each with its own index kit and plate**. Add a project per customer/application; samples are assigned to one. With one project the extra controls stay hidden, so simple runs look exactly as before.
3. **Samples** — type them in, or bulk-paste. Barcode numbers, plate wells and well aliases all resolve:

   ```
   Sample ID	Barcode	Project
   1	97	NaamaG_RNAseq
   2	98	NaamaG_RNAseq
   e1	A01	DoritExome
   ```

   Accepts `A01`, `A1`, `1A`, `12H`, Smart-seq codes like `U025`, and plate barcode numbers (`97` → well `A01`). A header row is skipped automatically.

   **Two ways to load a multi-project run:**
   - **Per project (easiest)** — every project card has its own *"⤓ Paste samples into &lt;project&gt;"* box. Paste that customer's list, click **Add to this project**, and the rows are assigned automatically; nothing to switch by hand. **Replace this project's samples** swaps out just that project's rows and leaves the others alone.
   - **One combined paste** — use the bulk box at the bottom of the Samples card with an optional **third project column**, or pick a target in the *"assign to"* dropdown. A project name that doesn't exist yet is created.
4. **Validation (live)** — always across the **whole run**, since all projects are demultiplexed together:
   - Sample names must be **unique across the entire run**, including between projects.
   - Spaces and special characters are converted to `_` (every change is listed). Project names too — they become the `Sample_Project` folder.
   - Index sequences must be unique with **Hamming distance ≥ 3** on the combined i7+i5 — checked across projects, not just within one.
   - **Mixed index lengths** (e.g. an 8 bp kit beside a 10 bp kit) are reconciled automatically:
     - if the shorter kit has a padding rule, it is padded up (NEB 8 bp → 10 bp adds `AT` to i7, `AC` to i5);
     - otherwise **all indexes are trimmed down to the shortest length**, with a warning. Uniqueness is then re-checked on the trimmed sequences, so any collision that trimming creates is caught as an error.
   - Projects with no name, duplicate project names, and projects with no samples are flagged.
   - Invalid or reused wells are caught.
5. **Output**
   - **Copy for BaseSpace** — tab-separated rows to paste straight into the [Run Planning sample table](https://basespace.illumina.com/run-planning/config/1/sample-analysis-setup).
   - **Sample sheet .csv** — BCL Convert v2 file to upload instead. Multi-project runs get a **`Sample_Project` column**, so BCL Convert writes FASTQs into one folder per project.
   - **Records .csv** — full archive table (project, plate, well, index IDs, raw + final sequences, and whether each index was padded or trimmed), named `YYYY-MM-DD_Run.csv`.

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
