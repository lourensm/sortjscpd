# sortjscpd

`sortjscpd` is a small command-line helper around the `jscpd` duplicate-code detector.  
It runs `jscpd`, parses its console output, sorts the clone blocks according to command-line
options, formats them into either compact or detailed form, and then copies the original
`jscpd` summary table.


---
## Installation

```shell
pip install -e .
```
This installs `sortjscpd` as a stand-alone program.

---

## Running without installing

```shell
python3 sortjscpd.py --help
```

---

## Usage

```shell
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

```shell
npm install -g jscpd
```

## How it works

Everything lives in a single Python script:

```
sortjscpd.py
```

It:

- runs `jscpd` as a subprocess, with option `--reporters console` and the trailing arguments as files
- captures and parses its console output,
- extracts clone blocks,
- sorts them based on the chosen criterion,
- formats them (short or long),
- and finally copies the `jscpd` provided summary.

___

### Limitations and future improvements

This tool parses the console output of `jscpd`.

`sortjscpd` expects a list of files to be passed on to `jscpd`. `jscpd` allows other kinds of input,
e.g. directories, no `files`..

In retrospect, a more robust design would have been to:

- integrate sorting directly into `jscpd`’s source (TypeScript), or  
- use the `--reporters json` output and process the structured data instead of console text.

At the time of writing, the console output was the quickest approach for a
drop-in helper tool. Future versions may switch to consuming `jscpd`’s JSON
reporter or supporting additional reporter formats.


--- 
## Exit codes

| Code | Meaning                             |
|------|-------------------------------------|
| 0    | Normal operation                    |
| 1    | Missing file or invalid jscpd input |
| >1   | Unexpected internal error           |

## TODO

Have a look at jscpd documentation!

Explore other jscpd functionality, specifically the --reporters json

`sortjscpd` doesn't follow `jscpd` conventions enough:

* `jscpd` without arguments seems to recursively analyse the current directory.
* `jscpd` without `--reporters` options does report, probably to `console` 
* An unsupported --reporters option probably looks for an installed package named `@jscpd/aap-reporter` or 
  `jscpd-aap-reporter` but then still outputs clones, but probably not the table.
