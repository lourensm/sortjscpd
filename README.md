# sortjscpd

`sortjscpd` is a small command-line helper around the `jscpd` duplicate-code detector.  
It runs `jscpd`, parses its text output, sorts the clone blocks according to command-line
options, formats them into either compact or detailed form, and then copies the original
`jscpd` summary table.

---
## Installation

```bash
pip install -e .
```
This installs `sortjscpd` as a stand-alone program.

---

## Running without installing

```bash
python3 sortjscpd.py --help
```

---

## Usage

```bash
sortjscpd *.swift
sortjscpd --by lines *.swift
sortjscpd --by tokens *.swift
sortjscpd --min-tokens 30 *.swift Util/*.swift
```

Options:

- `--by {lines|tokens}` — choose the sort key (default: `lines`)
- `--fmt {short|long}` — choose output format (default: `short`)
- `--min-tokens N` — minimum token threshold passed to `jscpd` (default: `20`)

---

## Example outputs

### `--fmt short`
One-line, compact format.  
Shows file and start line only (aligned to fixed width):

```
...
7 lines,  50 tokens — Views/BasketsView.swift:89     - Views/StocksView.swift:63
9 lines,  62 tokens — Views/StocksDataView.swift:46  - Views/StocksView.swift:36
...
```

### `--fmt long`
Two-line, detailed format.  
Shows full (line:column) ranges for both files:

```
...
Views/BasketsView.swift [89:27 - 96:16]                   (7 lines,  50 tokens)
Views/StocksView.swift  [63:11 - 79:03]

Views/MultiDataView.swift [33:19 - 40:13]                 (7 lines,  51 tokens)
Views/WindowSettingsView.swift [17:20 - 24:2]

...
```

After the duplicate listing, the statistics table printed by `jscpd` follows unchanged.

---

## Requirements

- Python 3.10+ (tested with Python 3.11)
- `jscpd` installed and on your PATH

Install jscpd via npm:

```bash
npm install -g jscpd
```

## How it works

Everything lives in a single Python script:

```
sortjscpd.py
```

It:

- runs `jscpd` as a subprocess,
- captures and parses its console output,
- extracts clone blocks,
- sorts them based on the chosen criterion,
- formats them (short or long),
- and finally copies the `jscpd` provided summary.

___

## Remarks

With hindsight, it might have been cleaner to study the `jscpd` source (TypeScript)
and implement this as an internal formatter or extension. For now, this tool
operates purely on the textual output of `jscpd`.

--- 
## Exit codes

| Code | Meaning                             |
|------|-------------------------------------|
| 0    | Normal operation                    |
| 1    | Missing file or invalid jscpd input |
| >1   | Unexpected internal error           |