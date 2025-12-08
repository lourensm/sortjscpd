# sortjscpd

`sortjscpd` is a small command-line helper that runs the `jscpd` duplicate
code detector and sorts its console output and reformats it.


## Installation

```bash
pip install -e .
```

## Running without installing

```bash
python3 sortjscpd.py --help
```

---

## Usage examples

```bash
python3 sortjscpd.py --by lines *.swift
python3 sortjscpd.py --by tokens *.swift
python3 sortjscpd.py --min-tokens 30 *.swift Util/*.swift
```

---

## Example output

`sortjscpd` supports two output styles.  
Choose the format with `--fmt short` or `--fmt long`.

### • `--fmt short`
One-line, compact format.  
Shows file and start line only (aligned to fixed width):

```
7 lines,  50 tokens — Views/BasketsView.swift:89     - Views/StocksView.swift:63
9 lines,  62 tokens — Views/StocksDataView.swift:46  - Views/StocksView.swift:36
```

### • `--fmt long`
Two-line, detailed format.  
Shows full (line:column) ranges for both files:

```
Views/BasketsView.swift [89:27 - 96:16]                   (7 lines,  50 tokens)
Views/StocksView.swift  [63:11 - 79:03]
```

The statistics table produced by jscpd  is printed after the listing of the duplicates.

___
## Exit codes

| Code | Meaning                             |
|------|-------------------------------------|
| 0    | Normal operation                    |
| 1    | Missing file or invalid jscpd input |
| >1   | Unexpected internal error           |

jspcd probably has different exit codes, code 1 probably means either there are any duplicates or a file is missing
___
## Requirements

- Python 3.11+ (that is what it was tested with)
- `jscpd` installed and on your PATH

Install jscpd via npm:

```bash
npm install -g jscpd
```

## Development notes

All functionality lives in a single Python script:

```
sortjscpd.py
```

The script:
- runs jscpd,
- parses its console output,
- extracts clone blocks,
- sorts them according to command line specification 
- aligns them nicely,
- and prints a readable summary.

## Notes

With hindsight it would have probably been better to try to understand jscpd source (typescript?) and create a branch.
