sortjscpd

sortjscpd is a command-line tool that runs jscpd (duplicate code detector) and produces clean, aligned, sortable clone reports. It converts the messy jscpd console output into readable and diff-friendly output.

Installation:

Clone the project and install it in editable mode:
pip install -e .

Install jscpd using Node.js:
npm install -g jscpd

Usage:
sortjscpd [OPTIONS] FILES...

Options:
--by lines|tokens      Sort clones by lines or tokens (default: lines)
--fmt short|long       Output format for file positions (default: short)
--min-tokens N         Minimum token threshold for jscpd (default: 20)
FILES...               File list or glob patterns

Example:
sortjscpd --by tokens --fmt long Src/**/*.swift

What it does:

1. Runs jscpd on the provided files.
2. Detects missing files (because jscpd does not consistently error out).
3. Parses clone report blocks.
4. Sorts clones by the requested criteria.
5. Prints aligned one-line summaries, for example:

  7 lines, 50 tokens — Views/BasketsView.swift:89 - Views/StocksView.swift:63
  8 lines, 52 tokens — Views/MultiDataView.swift:43 - Views/WindowSettingsView.swift:36
  9 lines, 62 tokens — Views/StocksDataView.swift:46 - Views/StocksView.swift:36

Error handling:

Missing files result in FileNotFoundError with a clean error message.
Unexpected jscpd internal failures are shown as fatal errors.
Unexpected output format yields ValueError.

Exit codes:
0 = success
1 = expected user error (missing file, bad input)
2 = unexpected internal error

Development:

Run the script manually:
python sortjscpd.py FILES...

Linting:
make p
make pycodestyle
make mypy

Requirements:
Python 3.10 or newer
Node.js 18 or newer
jscpd installed globally

License:
Private project.
