# sortjscpd

**sortjscpd** is a lightweight command-line helper that runs **jscpd** (duplicate
code detector) and formats its console output into clean, aligned,
human-scannable clone summaries.

It does *not* change jscpd’s detection logic — it only reorganizes the
textual console output.

---

## Installation

### From source

Clone and install locally:

```bash
git clone https://github.com/<yourname>/sortjscpd.git
cd sortjscpd
pip install -e .
```

### Or install from a wheel (if you build one)

```bash
pip install dist/sortjscpd-*.whl
```

### Exposes a `sortjscpd` CLI

After installation you get:

```bash
sortjscpd --help
```

---

## Run without Installing

```bash
python3 sortjscpd.py --help
```

---

## Usage Examples

```bash
sortjscpd --by lines *.swift
sortjscpd --by tokens *.swift
sortjscpd --min-tokens 30 *.swift Util/*.swift
```

---

## Example Output

```
7 lines,  50 tokens — Views/BasketsView.swift:89     - Views/StocksView.swift:63
9 lines,  62 tokens — Views/StocksDataView.swift:46  - Views/StocksView.swift:36
```

---

## Exit Codes

| Code | Meaning                            |
|------|------------------------------------|
| 0    | Normal operation                   |
| 1    | Missing file or invalid jscpd input |
| >1   | Unexpected internal error          |

---

## Requirements

- Python 3.11+
- `jscpd` installed and available on `$PATH`

### Install jscpd

```bash
npm install -g jscpd
```

---

## Development

Sources are organized as:

```
sortjscpd/
    src/sortjscpd/
        cli.py
        ...
    pyproject.toml
    README.md
```

Build distribution artifacts:

```bash
python3 -m build
```

Run tests or static analysis as you prefer.

---

## License

MIT License

---

## Notes

sortjscpd only uses the textual console output of **jscpd**.
It is intentionally simple and intended as a helper for scanning clone
reports or integrating clone summary output into larger build pipelines.