# LexicalAnalyzer.py
"""
Threaded Lexical Analyzer using a Double-Buffer model.
------------------------------------------------------
Reads a Pascal-like input file and writes recognized tokens
(line by line) into an output file.

Usage:
    python lexer.py input.pas output.txt

Each output line format:
    TOKEN_TYPE    lexeme    line:col
"""

import sys
import threading

BUFFER_CAPACITY = 20  # bytes per buffer

# ---------------- Token Definitions ---------------- #
KEYWORDS = {
    "program", "var", "begin", "end", "function", "procedure", "array", "of",
    "integer", "real", "if", "then", "else", "while", "do", "return",
    "const", "div", "mod", "and", "or", "not", "for", "to", "downto"
}

OPERATORS = {"+", "-", "*", "/", "=", "<", ">", "<=", ">=", "<>", ":=", ":"}
DELIMITERS = {";", ",", ".", "(", ")", "[", "]"}

# ==================================================== #
#               DOUBLE BUFFER IMPLEMENTATION           #
# ==================================================== #
class BufferedReader:
    """Implements a two-buffer system with a background producer thread."""

    def __init__(self, filepath):
        self.path = filepath
        self.file = open(filepath, "rb")

        self.buffers = [bytearray(), bytearray()]
        self.flags = [False, False]  # buffer fill flags
        self.locks = [threading.Condition(), threading.Condition()]

        self.read_index = 0
        self.write_index = 0
        self.cursor = 0

        self.eof = False
        self.closed = False

        # Start producer thread
        threading.Thread(target=self._load_data, daemon=True).start()

    # ---------- Background Thread ---------- #
    def _load_data(self):
        while True:
            idx = self.write_index
            cond = self.locks[idx]
            with cond:
                while self.flags[idx]:
                    cond.wait()

                chunk = self.file.read(BUFFER_CAPACITY)
                if not chunk:
                    self.eof = True
                    self.flags[idx] = False
                    cond.notify_all()
                    break

                self.buffers[idx] = bytearray(chunk)
                self.flags[idx] = True
                cond.notify_all()

            self.write_index = 1 - self.write_index

        self.file.close()
        self.closed = True
        for c in self.locks:
            with c:
                c.notify_all()

    # ---------- Character Retrieval ---------- #
    def get_char(self):
        """Get the next character from buffers; returns '' on EOF."""
        while True:
            idx = self.read_index
            cond = self.locks[idx]
            with cond:
                while not self.flags[idx]:
                    if self.eof:
                        other = 1 - idx
                        with self.locks[other]:
                            if not self.flags[other]:
                                return ''
                    cond.wait(timeout=0.1)

                buf = self.buffers[idx]
                if self.cursor >= len(buf):
                    self.flags[idx] = False
                    cond.notify_all()
                    self.cursor = 0
                    self.read_index = 1 - self.read_index
                    continue

                char = buf[self.cursor]
                self.cursor += 1
                return chr(char)

    def unread_char(self):
        """Move one character back."""
        if self.cursor > 0:
            self.cursor -= 1
            return True
        prev = 1 - self.read_index
        with self.locks[prev]:
            if self.flags[prev] and len(self.buffers[prev]) > 0:
                self.read_index = prev
                self.cursor = len(self.buffers[prev]) - 1
                return True
        return False


# ==================================================== #
#                     LEXER CLASS                      #
# ==================================================== #
class LexicalAnalyzer:
    """State-based lexical analyzer for Pascal-like syntax."""

    def __init__(self, infile, outfile):
        self.buffer = BufferedReader(infile)
        self.outfile = outfile
        self.line = 1
        self.column = 0

    # ------------ Helper functions ------------ #
    def _next(self):
        ch = self.buffer.get_char()
        if ch == '':
            return ''
        if ch == '\n':
            self.line += 1
            self.column = 0
        else:
            self.column += 1
        return ch

    def _peek(self):
        ch = self._next()
        if ch == '':
            return ''
        self.buffer.unread_char()
        if ch == '\n':
            self.line -= 1
        else:
            self.column = max(0, self.column - 1)
        return ch

    def _emit(self, token, lexeme, line, col, writer):
        writer.write(f"{token}\t{lexeme}\t{line}:{col}\n")

    # ------------ Skipping Functions ------------ #
    def _skip_spaces(self):
        while True:
            ch = self._next()
            if ch == '' or not ch.isspace():
                if ch:
                    self.buffer.unread_char()
                return

    def _skip_brace_comment(self):
        while True:
            ch = self._next()
            if ch == '' or ch == '}':
                return

    def _skip_paren_comment(self):
        prev = ''
        while True:
            ch = self._next()
            if ch == '':
                return
            if prev == '*' and ch == ')':
                return
            prev = ch

    # ------------ Main Lexing Routine ------------ #
    def analyze(self):
        with open(self.outfile, "w", encoding="utf-8") as writer:
            while True:
                ch = self._next()
                if ch == '':
                    self._emit("EOF", "<EOF>", self.line, self.column, writer)
                    break
                if ch.isspace():
                    continue

                start_line, start_col = self.line, self.column

                # --- Comments --- #
                if ch == '{':
                    self._skip_brace_comment()
                    continue
                if ch == '(' and self._peek() == '*':
                    self._next()
                    self._skip_paren_comment()
                    continue

                # --- Strings --- #
                if ch == "'":
                    token = "'"
                    while True:
                        c = self._next()
                        if c == '':
                            break
                        token += c
                        if c == "'":
                            if self._peek() == "'":
                                self._next()
                                token += "'"
                                continue
                            break
                    self._emit("STRING", token, start_line, start_col, writer)
                    continue

                # --- Identifiers / Keywords --- #
                if ch.isalpha():
                    word = ch
                    while self._peek().isalnum() or self._peek() == '_':
                        word += self._next()
                    token_type = "KEYWORD" if word.lower() in KEYWORDS else "ID"
                    self._emit(token_type, word, start_line, start_col, writer)
                    continue

                # --- Numbers --- #
                if ch.isdigit():
                    number = ch
                    while self._peek().isdigit():
                        number += self._next()
                    self._emit("NUM", number, start_line, start_col, writer)
                    continue

                # --- Operators / Delimiters --- #
                next_char = self._peek()
                pair = ch + next_char
                if pair in {"<=", ">=", "<>", ":=", ".."}:
                    self._next()
                    self._emit("OP" if pair != ".." else "DELIM", pair, start_line, start_col, writer)
                    continue

                if ch in OPERATORS:
                    self._emit("OP", ch, start_line, start_col, writer)
                    continue

                if ch in DELIMITERS:
                    self._emit("DELIM", ch, start_line, start_col, writer)
                    continue

                self._emit("UNKNOWN", ch, start_line, start_col, writer)


# ==================================================== #
#                    MAIN PROGRAM                      #
# ==================================================== #
def main():
    if len(sys.argv) < 3:
        print("Usage: python lexer.py inputfileName outputfileName")
        return

    infile, outfile = sys.argv[1], sys.argv[2]
    lexer = LexicalAnalyzer(infile, outfile)
    lexer.analyze()
    print(f"Lexical analysis complete. Tokens written to {outfile}")

if __name__ == "__main__":
    main()
