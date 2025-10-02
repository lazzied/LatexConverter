import re

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
% Set a Chinese font available on your system (adjust if needed)
\setCJKmainfont{{SimSun}}
\definecolor{{questioncolor}}{{RGB}}{{0,102,204}}
\definecolor{{optioncolor}}{{RGB}}{{153,0,0}}
\setlist[enumerate]{{label=\arabic*., leftmargin=*, itemsep=1.2em}}
\setlist[itemize]{{leftmargin=*}}
\pagestyle{{fancy}}
\fancyhf{{}}
\rhead{{{title}}}
\rfoot{{\thepage}}
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

def escape_latex(text):
    def replace(match):
        s = match.group(0)
        if s.startswith('$') or s.startswith('\\(') or s.startswith('\\['):
            return s  # Don't escape inside math
        # Escape in normal text
        s = s.replace("\\", r"\\")
        s = s.replace("#", r"\#")
        s = s.replace("%", r"\%")
        s = s.replace("_", r"\_")
        s = s.replace("^", r"\^{}")
        s = s.replace("&", r"\&")
        s = s.replace("{", r"\{")
        s = s.replace("}", r"\}")
        return s

    # Regex: match math regions or normal text
    pattern = r"(\\\[.*?\\\]|\\\(.*?\\\)|\\begin\{.*?\}.*?\\end\{.*?\}|\\[a-zA-Z]+|\\.|\\$.*?\\$|\\$.*?\\$|\\$|[^$]+)"
    return re.sub(pattern, replace, text, flags=re.DOTALL)

class examPartitioning:
    def __init__(self, file):
        self.file = file
    
    def handleSections(self):
        with open(self.file, "r", encoding="utf-8") as file:
            content = file.read()
        # Robust pattern for markdown headers with Chinese numerals and section name
        section_pattern = (
            r'(^#+\s*[一二三四五六七八九十]+[、.，]?\s*.*?(?:选择题|填空题|解答题).*?$)'
            r'([\s\S]*?)(?=^#+\s*[一二三四五六七八九十]+[、.，]?|\Z)'
        )
        match = re.search(section_pattern, content, flags=re.MULTILINE | re.DOTALL)
        if not match:
            print("No matching section found.")
            return
        section_header = match.group(1)
        try:
            def clean_header(header):
                # Remove leading # and whitespace
                return re.sub(r'^#+\s*', '', header)
            replacement = lambda m: (
                r"\section*{" + escape_latex(clean_header(m.group(1))) + "}\n" + m.group(2)
            )
            result = re.sub(section_pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
            with open(self.file, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"Section replaced successfully: '{clean_header(section_header)}'")
        except Exception as e:
            print(f"Error processing section '{section_header}': {e}")



    def getSection(self, sectionName):
        with open(self.file, "r", encoding="utf-8") as file:
            content = file.read()

        print(f"Looking for section: {sectionName}")
        # Robust pattern for markdown headers with Chinese numerals and section name
        section_pattern = (
            r'(\\section\*\{[一二三四五六七八九十]+[、.，]?\s*.*?(?:选择题|填空题|解答题).*?\})'
            r'([\s\S]*?)(?=\\section\*\{[一二三四五六七八九十]+[、.，]?|\Z)'
        )

        match = re.search(section_pattern, content, flags=re.MULTILINE | re.DOTALL)
        if not match:
            print(f"Section '{sectionName}' not found in the file.")
            return None, None
        else:
            print(f"Section '{sectionName}' found.")
            
        section_header = match.group(1)
        section_body = match.group(2)

        return section_header, section_body

    def mcHandler(self):
        with open(self.file, "r", encoding="utf-8") as file:
            content = file.read()

        section_header, section_body = self.getSection("选择题")
        if section_header is None or section_body is None:
            print("Error: '选择题' section not found.")
            return

        print("Processing '选择题' section...")

        # Split the content into questions (each starting with a number)
        questions = re.split(r'(?=\d+\.)', section_body)

        latex_items = []
        for q in questions:
            if not q.strip():
                continue

            # Split into lines and clean them
            lines = [line.strip() for line in q.split('\n') if line.strip()]
            if not lines:
                continue

            # First line is the question
            question_text = escape_latex(lines[0])

            # The rest are options
            options = []
            current_option = ""
            for line in lines[1:]:
                # Check if line starts with an option marker (A-D.)
                if re.match(r'^[A-D]\.', line):
                    # If we have a current option being built, save it
                    if current_option:
                        options.append(escape_latex(current_option.strip()))
                        current_option = ""
                    # Start new option
                    current_option = re.sub(r'^[A-D]\.\s*', '', line)
                else:
                    # Continue building the current option
                    if current_option:
                        current_option += " " + line

            # Add the last option if it exists
            if current_option:
                options.append(escape_latex(current_option.strip()))

            # Ensure we have exactly 4 options
            while len(options) < 4:
                options.append('')
            options = options[:4]  # Take only first 4 options

            print(f"Question: {question_text}")
            print(f"Options: {options}")

            # Create LaTeX output for this question
            latex_item = f"\\item {question_text}\n\\options\n"
            for opt in options:
                latex_item += f"{{{opt}}}\n"
            latex_items.append(latex_item)

        # Create the final LaTeX output
        latex_output = "\\begin{enumerate}\n" + ''.join(latex_items) + "\\end{enumerate}\n"
        new_content = content.replace(section_body, latex_output)

        with open(self.file, "w", encoding="utf-8") as file:
            file.write(new_content)





    def fibHandler(self):
        with open(self.file, "r", encoding="utf-8") as file:
            content = file.read()

        section_header, section_body = self.getSection("填空题")
        if section_body is None:
            print("Error: '填空题' section body not found.")
            return

        question_block_pattern = r'(?:^|\n)(\d+)[\.、]?\s*([\s\S]*?)(?=\n\d+[\.、]|$)'
        blocks = re.findall(question_block_pattern, section_body, flags=re.MULTILINE)
        if not blocks:
            print("No question blocks found in '填空题' section.")
            return

        latex_items = []
        for qnum, block in blocks:
            question_text = block.strip()
            question_text = escape_latex(question_text)

            if not question_text.endswith("_______________"):
                question_text += " _______________"

            latex_item = f"\\item {question_text}\n"
            latex_items.append(latex_item)

        latex_output = "\\begin{enumerate}[resume]\n" + ''.join(latex_items) + "\\end{enumerate}\n"
        new_content = content.replace(section_body, latex_output)

        with open(self.file, "w", encoding="utf-8") as file:
            file.write(new_content)

    def aqHandler(self):
        with open(self.file, "r", encoding="utf-8") as file:
            content = file.read()

        section_header, section_body = self.getSection("解答题")
        if section_body is None:
            print("Error: '解答题' section body not found.")
            return

        question_block_pattern = r'(?:^|\n)(###\s*\d+[\.、]?[^\n]*\n(?:.*\n)*?)(?=###\s*\d+[\.、]|---|$)'
        blocks = re.findall(question_block_pattern, section_body, flags=re.MULTILINE)
        if not blocks:
            print("No question blocks found in '解答题' section.")
            return

        latex_items = []
        for block in blocks:
            question_lines = block.strip().split('\n')
            question_text = question_lines[0].strip()
            question_text = escape_latex(question_text)

            sub_questions = question_lines[1:]
            sub_latex_items = []

            for sub in sub_questions:
                m = re.match(r'^\s*\((\d+|[iv]+)\)[\.、：]?\s*(.*)', sub)
                if m:
                    sub_qnum = m.group(1)
                    sub_qtext = m.group(2).strip()
                    sub_qtext = escape_latex(sub_qtext)
                    sub_latex_items.append(f"\\item {sub_qtext}\n")

            if sub_latex_items:
                latex_item = f"\\item {question_text}\n\\begin{{enumerate}}\n{''.join(sub_latex_items)}\\end{{enumerate}}\n"
            else:
                latex_item = f"\\item {question_text}\n"

            latex_items.append(latex_item)

        latex_output = "\\begin{enumerate}[resume]\n" + ''.join(latex_items) + "\\end{enumerate}\n"
        new_content = content.replace(section_body, latex_output)

        with open(self.file, "w", encoding="utf-8") as file:
            file.write(new_content)

class htmlTweaker:
    def __init__(self, file):
        self.file = file
        self.divs = {}

    def htmlIdentifier(self):
        with open(self.file, "r", encoding="utf-8") as file:
            content = file.read()
            div_elements = re.findall(r'<div[^>]*>.*?</div>', content, re.DOTALL)
            for div_element in div_elements:
                if re.search(r'<img[^>]*>', div_element):
                    self.divs[div_element] = "image"
                elif re.search(r'<table[^>]*>', div_element):
                    self.divs[div_element] = "table"
                elif re.search(r'(i?)page', div_element, re.IGNORECASE):
                    self.divs[div_element] = "page"

    def htmlExtractor(self):
        divsType = {}
        for key, value in self.divs.items():
            if value == "image":
                match = re.search(r'<img[^>]*src="([^"]*)"', key)
                if match:
                    divsType[key] = match.group(1)
            elif value == "table":
                rows = re.findall(r'<tr>(.*?)</tr>', key, re.DOTALL)
                table_cells = [re.findall(r'<td>(.*?)</td>', row, re.DOTALL) for row in rows]
                num_rows = len(table_cells)
                num_cols = len(table_cells[0]) if num_rows > 0 else 0
                divsType[key] = {"num_rows": num_rows, "num_cols": num_cols, "cells": table_cells}
            else:
                divsType[key] = None
        return divsType

    def htmlReplacement(self, divsType):
        with open(self.file, "r", encoding="utf-8") as file:
            content = file.read()
        for key, value in divsType.items():
            if self.divs[key] == "image":
                replacement = r'\includegraphics[width=0.6\textwidth]{' + value + '}'
                content = content.replace(key, replacement)
            elif self.divs[key] == "table":
                table_info = value
                latex_table = r"\begin{tabular}{" + " | ".join(["c"] * table_info["num_cols"]) + r"}\n\hline\n"
                for row in table_info["cells"]:
                    latex_row = " & ".join(row) + r" \\ \n\hline\n"
                    latex_table += latex_row
                latex_table += r"\end{tabular}"
                content = content.replace(key, latex_table)
            else:
                content = content.replace(key, "")
        with open(self.file, "w", encoding="utf-8") as file:
            file.write(content)

def processFile(file_path, output_path=None):
    from shutil import copyfile
    from pathlib import Path
    original = Path(file_path)
    stem = original.stem
    suffix = original.suffix
    counter = 1
    while True:
        new_stem = f"{stem}_{counter}"
        output_path = original.parent / f"{new_stem}{suffix}"
        if not output_path.exists():
            break
        counter += 1

    copyfile(file_path, output_path)

    htmlEngine = htmlTweaker(output_path)
    htmlEngine.htmlIdentifier()
    divsType = htmlEngine.htmlExtractor()
    htmlEngine.htmlReplacement(divsType)

    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()

    title = "2022年普通高等学校招生全国统一考试"
    subject = "数学"
    header = templateHeader(title, subject)
    content = header + content

    partitioner = examPartitioning(output_path)
    partitioner.handleSections()
    
    partitioner.mcHandler()
    """
    partitioner.fibHandler()
    partitioner.aqHandler()
    """
    

    with open(output_path, "r", encoding="utf-8") as f:
        final_content = f.read()
    final_content += templateFooter()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"Processed file saved as: {output_path}")

if __name__ == "__main__":
    filePath = r"C:\Users\user\Desktop\CEE\tex file testing\MATH\MATH1\originaltex.md"
    outputPath = r"C:\Users\user\Desktop\CEE\tex file testing\MATH\Math tex automation script\tex scripts trials"
    processFile(filePath, outputPath)
