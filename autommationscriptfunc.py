#!/usr/bin/env python3
# exam_transformer.py
"""
Transform messy/chinese/raw exam text into a polished LaTeX file using a styled template.

Usage:
    python exam_transformer.py INPUT_FILE -o OUTPUT_FILE

Only uses Python stdlib.
"""

import re
import argparse
from pathlib import Path
import html
import sys

# ---------- TEMPLATE (header + footer) ----------
def templateHeader(title, subject):
    
    TEMPLATE_HEADER = rf"""
    \documentclass{{article}}
    \usepackage[a4paper, margin=1in]{{geometry}}
    \usepackage{{graphicx}}
    \usepackage{{amsmath}}
    \usepackage{{amssymb}}
    \usepackage{{xeCJK}}
    \usepackage{{enumitem}}
    \usepackage{{booktabs}}
    \usepackage{{parskip}}
    \usepackage{{fancyhdr}}
    \usepackage{{xcolor}}
    \usepackage{{array}}
    \usepackage{{makecell}}
    \usepackage{{multirow}}
    \usepackage{{mathrsfs}}
    \usepackage{{bigstrut}}

    % Set a Chinese font available on your system (adjust if needed)
    \setCJKmainfont{{SimSun}}

    \definecolor{{questioncolor}}{{RGB}}{{0,102,204}}
    \definecolor{{optioncolor}}{{RGB}}{{153,0,0}}

    \setlist[enumerate]{{label=\arabic*., leftmargin=*, itemsep=1.2em}}
    \setlist[itemize]{{leftmargin=*}}

    \pagestyle{{fancy}}
    \fancyhf{{}}
    \rhead{{{title}}}
    \rfoot{{第~\thepage~页}}

    \newcommand{{\questiontitle}}[1]{{%
        \vspace{{0.5em}}\noindent\textcolor{{questioncolor}}{{\textbf{{#1}}}}\par%
        \noindent\makebox[\linewidth]{{\color{{questioncolor}}\rule{{\paperwidth}}{{0.4pt}}}}\par%
        \vspace{{0.5em}}%
    }}

    \newcommand{{\options}}[4]{{%
        \renewcommand{{\arraystretch}}{{1.6}}%
        \setlength{{\tabcolsep}}{{12pt}}%
        \begin{{tabular}}{{@{{}}p{{0.48\linewidth}}@{{}}p{{0.48\linewidth}}@{{}}}}%
            \textcolor{{optioncolor}}{{A.}}~#1 & \textcolor{{optioncolor}}{{B.}}~#2 \\[4pt]
            \textcolor{{optioncolor}}{{C.}}~#3 & \textcolor{{optioncolor}}{{D.}}~#4
        \end{{tabular}}%
    }}

    \newcommand{{\multichoice}}[1]{{%
        \begin{{itemize}} #1 \end{{itemize}}
    }}

    \newcommand{{\fillblank}}[1][2cm]{{\underline{{\hspace{{#1}}}}}}

    \renewcommand{{\arraystretch}}{{1.4}}
    \setlength{{\extrarowheight}}{{2pt}}
    \allowdisplaybreaks[4]

    \begin{{document}}
    \begin{{center}}
        \Large\textbf{{{title}}}\\
        \vspace{{0.5em}}
        \large\textbf{{{subject}}}
    \end{{center}}
    """
    return TEMPLATE_HEADER

def templateFooter():
    return r"""
\end{document}
"""                               

TEMPLATE_FOOTER = r"""
\end{document}
"""

# ---------- Utility functions ----------
def remove_html_tags(text: str) -> str:
    """Remove simple HTML tags but keep content; convert <br> to newline"""
    text = html.unescape(text)
    # Replace common tags with newline equivalents
    text = re.sub(r'(?i)<br\s*/?>', '\n', text)
    text = re.sub(r'(?is)<div[^>]*>.*?</div>', lambda m: re.sub(r'(?i)<.*?>', '', m.group(0)), text)
    # Convert <table> simple HTML to a placeholder (we'll convert later)
    # Remove remaining tags
    text = re.sub(r'(?s)<(script|style).*?>.*?</\1>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    return text

def normalize_whitespace(text: str) -> str:
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # collapse multiple newlines but keep some separation
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'

def extract_images(text: str):
    """
    Convert common markdown/html <img src="..."> occurrences left in original into \includegraphics.
    This tries to handle: <img src="imgs/..."> and markdown ![...](...)
    """
    # markdown images: ![alt](path)
    text = re.sub(r'!\[[^\]]*\]\(([^)]+)\)', lambda m: r'\includegraphics[width=0.6\textwidth]{' + m.group(1).strip() + '}', text)
    # html img: src="..."
    text = re.sub(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', lambda m: r'\includegraphics[width=0.6\textwidth]{' + m.group(1).strip() + '}', text)
    return text

def convert_html_table_to_latex(table_html: str) -> str:
    """
    A tiny converter: table_html should be already stripped of tags; we'll attempt to parse a simple ASCII table
    If it's not recognized, return original inside verbatim.
    """
    # Try to find rows by splitting on newlines that likely came from <tr>
    rows = [r.strip() for r in table_html.splitlines() if r.strip()]
    if not rows:
        return '\\begin{verbatim}\n' + table_html + '\n\\end{verbatim}\n'
    # Each row might be like "病例组 40 60"
    cells = [re.split(r'\s{2,}|\t|\|', r) for r in rows]
    # Determine max cols
    maxc = max(len(c) for c in cells)
    colspec = '|'.join(['c'] * maxc)
    out = ['\\begin{center}', '\\begin{tabular}{|' + colspec + '|}', '\\hline']
    for c in cells:
        # sanitize
        c = [ci.strip() for ci in c if ci.strip() != '']
        # pad
        while len(c) < maxc:
            c.append('')
        out.append(' & '.join(c) + r' \\ \hline')
    out.append('\\end{tabular}')
    out.append('\\end{center}\n')
    return '\n'.join(out)

# ---------- Parsing logic ----------
def parse_sections(text: str):
    """Convert heading marks (#, ##, Chinese markers) to LaTeX sections and keep the rest"""
    # Common patterns: "# 2022年..." or "## 一、 选择题" or "### 四、 解答题"
    # Normalize header tokens
    text = re.sub(r'(?m)^\s*#{1}\s*(.+)$', lambda m: r'\begin{center}\n\Large\textbf{' + m.group(1).strip() + r'}\\' + '\n\\end{center}\n', text)
    text = re.sub(r'(?m)^\s*#{2,}\s*(.+)$', lambda m: r'\section*{' + m.group(1).strip() + '}\n', text)
    # Chinese style headings like "## 一、 选择题" or "三、 填空题："
    text = re.sub(r'(?m)^\s*(第?\s?[一二三四五六七八九十]+、\s*.*)$', lambda m: r'\section*{' + m.group(1).strip() + '}\n', text)
    text = re.sub(r'(?m)^\s*([一二三四五六七八九十]+、\s*[\u4e00-\u9fff].*)$', lambda m: r'\section*{' + m.group(1).strip() + '}\n', text)
    # explicit Chinese patterns like "一、选择题："
    text = re.sub(r'(?m)^\s*(一、\s*选择题[:：]?.*)$', lambda m: r'\section*{' + m.group(1).strip() + '}\n', text)
    return text

def split_into_question_blocks(text: str):
    """
    Split text into numbered question blocks. Return list of (number, content).
    Pattern: lines starting with "1." or "1 . " or "1．" (Chinese full stop)
    """
    # Standardize numbering token: convert "1．" to "1." etc.
    text = re.sub(r'(?m)^(\d+)[\.\uFF0E\u3002]\s*', r'\n\1. ', text)
    # Ensure there's a leading newline for easier splitting
    if not text.startswith('\n'):
        text = '\n' + text
    # Split on newline followed by a number and dot and optional spaces then some text
    parts = re.split(r'(?m)\n(?=\d+\.\s)', text)
    blocks = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        m = re.match(r'^(\d+)\.\s*(.*)', p, re.S)
        if m:
            num = int(m.group(1))
            content = m.group(2).strip()
            blocks.append((num, content))
        else:
            # this might be a preface or header
            blocks.append((None, p))
    return blocks

def extract_options_from_block(content: str):
    """
    Try to extract options (A/B/C/D) from a question content.
    Return (stem, options_dict) where options_dict is {'A':..., 'B':..., ...} or None if no 4-option set found.
    """
    # Normalize option separators: accept "A. B. C. D.", "A、", "A．", "A："
    # make a pattern that matches A. text B. text C. text D. text
    opt_label = r'([A-D])[\.\uFF0E\u3002\u3001:：]\s*'
    pattern = re.compile(
        r'^(?P<stem>.*?)'  # question stem (non-greedy)
        + r'(?:' + opt_label + r')'  # A.
        + r'(?P<A>.*?)'
        + r'(?:' + opt_label + r')'  # B.
        + r'(?P<B>.*?)'
        + r'(?:' + opt_label + r')'  # C.
        + r'(?P<C>.*?)'
        + r'(?:' + opt_label + r')'  # D.
        + r'(?P<D>.*)$',
        flags=re.S
    )
    m = pattern.match(content)
    if m:
        stem = m.group('stem').strip()
        opts = {
            'A': m.group('A').strip(),
            'B': m.group('B').strip(),
            'C': m.group('C').strip(),
            'D': m.group('D').strip(),
        }
        return stem, opts
    # No 4-option. Try to detect multiple options across lines like:
    # A.xxx
    # B.xxx
    # C.xxx
    # D.xxx
    lines = content.splitlines()
    # find lines starting with A. etc
    opt_lines = {}
    for i, ln in enumerate(lines):
        m = re.match(r'^\s*([A-D])[\.\uFF0E\u3002\u3001:：]\s*(.*)', ln)
        if m:
            lbl = m.group(1)
            opt_lines[lbl] = (i, m.group(2))
    if opt_lines and all(k in opt_lines for k in ['A', 'B', 'C', 'D']):
        # build option text by taking from each label line until next label line
        stem_lines = []
        # lines before first option label are stem
        first_idx = min(opt_lines[k][0] for k in opt_lines)
        stem_lines = lines[:first_idx]
        stem = '\n'.join(stem_lines).strip()
        opts = {}
        ordered = sorted((k, opt_lines[k][0]) for k in opt_lines)
        for idx, (lbl, start) in enumerate(ordered):
            end = ordered[idx + 1][1] if idx + 1 < len(ordered) else len(lines)
            # join lines from start line (we already captured remainder in that line)
            part = [lines[i] for i in range(start, end)]
            # remove the leading "A." from first line
            part[0] = re.sub(r'^\s*[A-D][\.\uFF0E\u3002\u3001:：]\s*', '', part[0])
            opts[lbl] = '\n'.join(part).strip()
        return (stem, opts)
    return (content, None)

def render_block_to_latex(number, stem, opts):
    """
    Return a LaTeX string for the question.
    If opts is None -> leave as plain \item with stem, possibly a verbatim chunk for complex content.
    If opts present and 4 options -> use \options{...}{...}{...}{...}
    """
    out = []
    if number is None:
        # Not a numbered question — return raw
        out.append('\\begin{verbatim}\n' + stem + '\n\\end{verbatim}\n')
        return '\n'.join(out)
    out.append(f'\\item {stem}')
    if opts:
        # sanitize braces inside options
        def safe(s):
            s = s.replace('\n', ' ')
            s = s.strip()
            # escape underscores (common in LaTeX)
            s = s.replace('_', r'\_')
            return s
        A = safe(opts.get('A', ''))
        B = safe(opts.get('B', ''))
        C = safe(opts.get('C', ''))
        D = safe(opts.get('D', ''))
        out.append('\\vspace{0.3em}')
        out.append('\\options{' + A + '}{' + B + '}{' + C + '}{' + D + '}')
    else:
        out.append('% (no A/B/C/D detected; please inspect)')
    return '\n'.join(out) + '\n\n'

def process_fill_in_section(blocks_text: str):
    """
    For a fill-in-the-blank section text, attempt to convert lines like
    "13. .... 的系数为（用数字作答）。" into \item ... \fillblank
    We'll use a heuristic: if a line ends with '（用数字作答）' or similar, put fillblank.
    """
    lines = blocks_text.splitlines()
    out_lines = []
    for ln in lines:
        ln_strip = ln.strip()
        m = re.match(r'^(\d+)\.\s*(.*?)(（.*?作答.*?）|：|:)?\s*$', ln_strip)
        if m and ('作答' in (m.group(3) or '') or '填空' in ln_strip or '答案' in ln_strip):
            idx = m.group(1)
            stem = m.group(2)
            out_lines.append(f'\\item {stem} \\fillblank')
        else:
            out_lines.append(ln)
    return '\n'.join(out_lines)

# ---------- Main conversion pipeline ----------
def transform_raw_to_polished(raw_text: str) -> str:
    text = raw_text
    text = remove_html_tags(text)
    text = extract_images(text)
    text = normalize_whitespace(text)
    text = parse_sections(text)

    # Find and convert simple HTML-like tables (we will detect lines that look like "病例组 40 60")
    # First, try to find original table blocks by heuristics (rows with many columns separated by multiple spaces)
    # We will convert any block that looks like a table (has at least 2 rows with 2+ whitespace-separated columns)
    blocks = re.split(r'\n{2,}', text)
    transformed_blocks = []
    for block in blocks:
        rows = [r for r in block.splitlines() if r.strip()]
        # detect table: multiple rows with columns separated by 2+ spaces or tabs or pipes
        table_like = sum(1 for r in rows if re.search(r'(\s{2,}|\t|\|)', r)) >= 2 and len(rows) >= 2
        if table_like:
            latex_table = convert_html_table_to_latex(block)
            transformed_blocks.append(latex_table)
            continue
        transformed_blocks.append(block)
    text = '\n\n'.join(transformed_blocks)

    # Now split into question-numbered blocks and process each
    blocks = split_into_question_blocks(text)
    # We'll build output enumerates by detecting first big section "一、选择题" etc.
    out = [TEMPLATE_HEADER]

    # We'll output every numbered block as \begin{enumerate} ... \end{enumerate} in large sweeps.
    # Strategy: accumulate items until we see a section marker like "二、" in original (already converted to \section*).
    # Simpler: put all numbered items into one big enumerate (user can post-process).
    out.append('\\begin{enumerate}\n')

    for number, content in blocks:
        # If content starts with \section* or other latex markup, insert it as-is (close enumerate first)
        if isinstance(content, str) and content.strip().startswith('\\section*'):
            out.append('\\end{enumerate}\n')
            out.append(content + '\n')
            out.append('\\begin{enumerate}\n')
            continue
        # Try to extract options
        stem, opts = extract_options_from_block(content)
        # handle images inside stem (already converted)
        # handle fill-in heuristics when in "填空" area: if a nearby section title includes '填空', try to fill blanks
        # For now: if options missing and the content contains '（用数字作答' or '填空', create a fillblank
        if opts is None and (re.search(r'用数字作答|填空|填\s*空|写出|写出与', content) or re.search(r'相切', content) and '相切的一条直线' in content):
            # crude transformation: if the content ends with ')，' or '：' etc, add \fillblank
            # We will just render as item and append \fillblank
            clean_stem = content.replace('\n', ' ').strip()
            out.append(f'\\item {clean_stem} \\fillblank\n\n')
            continue
        # normal MCQ rendering
        out.append(render_block_to_latex(number, stem, opts))

    out.append('\\end{enumerate}\n')
    out.append(TEMPLATE_FOOTER)
    return '\n'.join(out)

# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description='Transform raw exam text to polished LaTeX.')
    parser.add_argument('input', type=Path, help='Input raw text / tex file')
    parser.add_argument('-o', '--output', type=Path, required=True, help='Output .tex file')
    parser.add_argument('--dry-run', action='store_true', help='Print transformed text to stdout instead of writing file')
    args = parser.parse_args()

    if not args.input.exists():
        print('Input file not found:', args.input)
        sys.exit(2)

    raw = args.input.read_text(encoding='utf-8')
    print('Parsing input file...')

    polished = transform_raw_to_polished(raw)

    if args.dry_run:
        print('----- TRANSFORMED OUTPUT START -----')
        print(polished)
        print('----- TRANSFORMED OUTPUT END -----')
    else:
        args.output.write_text(polished, encoding='utf-8')
        print('Wrote polished TeX to', args.output)

if __name__ == '__main__':
    main()
