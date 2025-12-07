#!/usr/bin/env python3
"""
Utility that runs jscpd and produces aligned clone reports.
"""
import sys
import argparse
import re
import subprocess
from dataclasses import dataclass
from collections.abc import Iterator
from enum import Enum

# ----------------------------------------
# Argument parser
# ----------------------------------------
class Parser:
    DESCRIPTION = "Run jscpd and sort its clone output."

    ARGUMENTS = [
        ("--by", {
            "choices": ["lines", "tokens"],
            "default": "lines",
            "help": "Sort clone blocks by lines or tokens (default: lines)."
        }),
        ("--fmt", {
            "choices": ["short", "long"],
            "default": "short",
            "help": "format of clone output (default: short)."
        }),
        ("--min-tokens", {
            "type": int,
            "default": 20,
            "help": "Minimum token threshold for jscpd (default: 20)."
        }),
        ("files", {
            "nargs": "+",
            "help": "Files or glob patterns to analyze."
        }),
    ]

    @staticmethod
    def build() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description=Parser.DESCRIPTION)
        for name, kwargs in Parser.ARGUMENTS:
            parser.add_argument(name, **kwargs)
        return parser

    @staticmethod
    def parse() -> argparse.Namespace:
        return Parser.build().parse_args()


class JSCPDRunner:
    @staticmethod
    def run(min_tokens: int, files: list[str]) -> str:
        cmd = [
            "jscpd",
            "--reporters", "console,html",
            "--min-tokens", str(min_tokens),
        ] + files

        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            # jscpd returns exit code 1 for duplicates → still valid
            if e.returncode == 1:
                output = e.output
            else:
                raise RuntimeError(
                    f"jscpd failed with exit code {e.returncode}:\n"
                    f"{e.output.decode('utf-8')}"
                ) from e
        text = output.decode("utf-8")
        first = text.partition("\n")[0]
        # Precise ENOENT detection
        m = re.match(r"^Error:\s+ENOENT: no such file or directory, lstat '([^']+)'$", first)
        if m:
            missing = m.group(1)
            raise FileNotFoundError(f"jscpd missing file: \"{missing}\"")
        # Other fatal errors (rare)
        if first.startswith("Error:"):
            raise RuntimeError(f"jscpd error: {first}")
        return text

class LineCol:
    def __init__(self, line: int, col: int):
        self.line = line
        self.col = col

    def __str__(self):
        return f"{self.line}:{self.col}"

    @classmethod
    def from_match(cls, m: re.Match[str], prefix: str):
        return cls(
            int(m.group(f"{prefix}_line")),
            int(m.group(f"{prefix}_col")),
        )


class SnippetPosFormat(Enum):
    SHORT = "short"
    LONG = "long"

    def render(self, info: "CloneFileInfo") -> str:
        match self:
            case SnippetPosFormat.SHORT:
                return f"{info.file}:{info.start.line}"
            case SnippetPosFormat.LONG:
                return f"{info.file} [{info.start} - {info.end}]"
            case _:
                raise ValueError(f"Unknown format {self}")


@dataclass
class CloneFileInfoFormat:
    snippet_spec: SnippetPosFormat
    snippet_width: int

    @staticmethod
    def short() -> "CloneFileInfoFormat":
        return CloneFileInfoFormat(snippet_spec=SnippetPosFormat.SHORT, snippet_width=30)

    @staticmethod
    def long() -> "CloneFileInfoFormat":
        return CloneFileInfoFormat(snippet_spec=SnippetPosFormat.LONG, snippet_width=40)

    def render(self, info: "CloneFileInfo") -> str:
        return f"{self.snippet_spec.render(info):<{self.snippet_width}}"

    def adjust_width(self, clone_infos: list["CloneInfo"]) -> None:
        self.snippet_width = 0
        left_snippet_width = max(len(self.snippet_spec.render(info.info1)) for info in clone_infos)
        right_snippet_width = max(len(self.snippet_spec.render(info.info2)) for info in clone_infos)
        snippet_width = max(left_snippet_width, right_snippet_width)
        self.snippet_width = snippet_width


@dataclass
class CloneInfoFormat:
    file_format: CloneFileInfoFormat
    single_line: bool

    @staticmethod
    def short() -> "CloneInfoFormat":
        return CloneInfoFormat(file_format=CloneFileInfoFormat.short(), single_line=True)

    @staticmethod
    def long() -> "CloneInfoFormat":
        return CloneInfoFormat(file_format=CloneFileInfoFormat.long(), single_line=False)

    @staticmethod
    def from_args(args: argparse.Namespace) -> "CloneInfoFormat":
        if args.fmt == "short":
            return CloneInfoFormat.short()
        elif args.fmt == "long":
            return CloneInfoFormat.long()
        raise RuntimeError(f"Unknown format {args.fmt}")

    # noinspection PyMethodMayBeStatic
    def render_info(self, info: "CloneInfo") -> str:
        return f"{info.lines:3} lines, {info.tokens:3} tokens"

    def render(self, info: "CloneInfo") -> str:
        fmt = self.file_format
        if self.single_line:
            return f"{self.render_info(info)} — {fmt.render(info.info1)} - {fmt.render(info.info2)}"
        else:
            return (
                f"{fmt.render(info.info1)} "
                f"({self.render_info(info)}\n"
                f"{fmt.render(info.info2)}"
                "\n"
            )

    def adjust_width(self, clone_infos: list["CloneInfo"]) -> None:
        self.file_format.adjust_width(clone_infos)


class CloneFileInfo:
    file: str
    start: LineCol
    end: LineCol

    def __init__(self, m: re.Match[str]):
        self.file = m.group("file")
        self.start = LineCol.from_match(m, "start")
        self.end = LineCol.from_match(m, "end")


class CloneInfo:
    POS = r'(?P<{name}_line>\d+):(?P<{name}_col>\d+)'
    # regex for the first line
    RE_FIRST = re.compile(
        fr'\s*-\s*(?P<file>\S+)\s*\['
        fr'{POS.format(name="start")}'
        r'\s*-\s*'
        fr'{POS.format(name="end")}'
        r']\s*'
        r'\((?P<lines>\d+)\s+lines?,\s*(?P<tokens>\d+)\s+tokens?\)'
    )

    # regex for the second line
    RE_SECOND = re.compile(
        fr'\s*(?P<file>\S+)\s*\['
        fr'{POS.format(name="start")}'
        r'\s*-\s*'
        fr'{POS.format(name="end")}'
        r']')
    info1: CloneFileInfo
    info2: CloneFileInfo
    lines: int
    tokens: int

    def __init__(self, line1: str, line2: str):
        m1 = self.RE_FIRST.match(line1)
        m2 = self.RE_SECOND.match(line2)
        self.info1 = CloneFileInfo(m1)
        self.info2 = CloneFileInfo(m2)
        self.lines = int(m1.group("lines"))
        self.tokens = int(m1.group("tokens"))

    def sort_key(self, by: str) -> tuple[int, int]:
        return (self.lines, self.tokens) if by == "lines" else (self.tokens, self.lines)


class CloneExtractor:

    def __init__(self):
        self.summary: list[str] = []

    ANSI = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

    @staticmethod
    def strip_ansi(s: str) -> str:
        return CloneExtractor.ANSI.sub('', s)

    def blocks(self, text: str) -> Iterator[list[str]]:
        """Generator that yields each clone block, while storing summary lines."""
        current: list[str] = []
        in_summary = False
        in_block = False
        for raw in text.splitlines(True):
            line = self.strip_ansi(raw)

            # summary table
            if in_summary or line.startswith("┌"):
                in_summary = True
                self.summary.append(raw)
                continue

            # start of block
            if line.startswith("Clone found"):
                in_block = True
                if current:
                    yield current
                    current = []
                continue

            # skip empty
            if not line.strip():
                continue
            if in_block:
                current.append(line)
            else:
                raise ValueError(f"Unexpected input: \"{line}\"")
        if current:
            yield current

    @staticmethod
    def extract_infos(text: str) -> tuple[list[CloneInfo], list[str]]:
        extractor = CloneExtractor()
        clone_infos = []
        for current in extractor.blocks(text):
            if len(current) == 2:
                clone_infos.append(CloneInfo(current[0], current[1]))
            else:
                raise ValueError("unexpected clone block")
        return clone_infos, extractor.summary


class CloneSorter:
    PATTERN: re.Pattern[str] = re.compile(r"\((\d+) lines?, (\d+) tokens?\)")

    @staticmethod
    def metrics(block: str) -> tuple[int, int]:
        m = CloneSorter.PATTERN.search(block)
        return (int(m.group(1)), int(m.group(2))) if m else (0, 0)

    @staticmethod
    def sort_infos(infos: list[CloneInfo], by: str) -> None:
        infos.sort(key=lambda b: b.sort_key(by))

    @staticmethod
    def sort(blocks: list[str], by: str) -> None:
        if by == "lines":
            blocks.sort(key=CloneSorter.metrics)  # (lines, tokens)
        else:
            blocks.sort(key=lambda b: CloneSorter.metrics(b)[::-1])  # secondary: lines


def main():
    try:
        args = Parser.parse()
        raw_text = JSCPDRunner.run(args.min_tokens, args.files)
        clone_infos, summary = CloneExtractor.extract_infos(raw_text)
        CloneSorter.sort_infos(clone_infos, args.by)
        fmt = CloneInfoFormat.from_args(args)
        fmt.adjust_width(clone_infos)
        for info in clone_infos:
            print(fmt.render(info))
        for line in summary:
            print(line, end="")
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e: # pylint: disable=broad-exception-caught
        # fallback for unexpected errors
        print(f"FATAL ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
