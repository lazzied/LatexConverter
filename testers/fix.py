import re
from typing import List, Tuple, Dict


class LatexMathFixer:
    """
    Universal LaTeX document fixer that detects and repairs common
    math formula inconsistencies across different exam documents.
    """
    
    def __init__(self, latex_text: str):
        self.original_text = latex_text
        self.fixed_text = latex_text
        self.fixes_applied = []
    
    def fix_all(self) -> str:
        """Apply all fixes in sequence"""
        """
        Calls all the fix methods in a specific order:
            Escape characters (\begin, \item, etc.)
            Unbalanced $ signs
            Incomplete braces, brackets, parentheses
            Set notation fixes
            Chinese symbols in math
            Itemize/enumerate structure fixes
            Spacing issues
            Common command typos
            Left-right pairing in math mode
            Text in math mode
            Orphaned \item lines
            Returns the fully fixed LaTeX string.
        """

        self.fix_escape_characters()
        self.fix_unbalanced_math_delimiters()
        self.fix_incomplete_braces()
        self.fix_set_notation()
        self.fix_chinese_symbols_in_math()
        #self.fix_itemize_enumerate_structure()
        self.fix_spacing_issues()
        self.fix_common_command_typos()
        self.fix_leftright_pairing()
        self.fix_text_in_math_mode()
        # self.fix_orphaned_items()
        return self.fixed_text
    
    def fix_escape_characters(self) -> None:

        """Ensures all common LaTeX commands start with a single \.
            Fixes:
            Missing backslashes (e.g., begin{itemize} → \begin{itemize})
            Doubled backslashes (e.g., \\begin → \begin)"""
        
        """Fix missing or doubled backslashes in LaTeX commands"""
        # Pattern: detect common commands without backslash at word boundary
        commands = ['begin', 'end', 'item', 'section', 'subsection', 
                   'frac', 'sqrt', 'sum', 'int', 'lim', 'sin', 'cos', 'tan',
                   'alpha', 'beta', 'gamma', 'theta', 'pi', 'infty']
        
        for cmd in commands:
            # Missing backslash: \begin → \\begin (only if preceded by newline/start)
            pattern = rf'(?:^|(?<=\n))(?<!\\){cmd}\{{'
            if re.search(pattern, self.fixed_text, re.MULTILINE):
                self.fixed_text = re.sub(pattern, rf'\\{cmd}{{', self.fixed_text, flags=re.MULTILINE)
                self.fixes_applied.append(f"Added backslash to {cmd}")
            
            # Doubled backslash: \\begin → \begin
            pattern = rf'\\\\{cmd}(?=\s|\{{)'
            if re.search(pattern, self.fixed_text):
                self.fixed_text = re.sub(pattern, rf'\\{cmd}', self.fixed_text)
                self.fixes_applied.append(f"Fixed doubled backslash in {cmd}")
    
    def fix_unbalanced_math_delimiters(self) -> None:
        """
        Fixes missing $ or extra $ in inline math mode.
            Handles different cases like:
            Formula missing closing $
            Formula missing opening $
            Two formulas in one line missing separation $
        """

        """Fix unbalanced $ signs and other math delimiters"""
        lines = self.fixed_text.split('\n')
        fixed_lines = []
        
        for line_num, line in enumerate(lines, 1):
            original_line = line
        
            # Skip lines that are pure LaTeX commands (no text content)
            if re.match(r'^\s*\\[a-zA-Z]+(\{[^}]*\}|\[[^\]]*\])*\s*$', line):
                fixed_lines.append(line)
                continue
            
            # Count $ signs
            dollar_count = line.count('$')
            
            if dollar_count % 2 != 0:
                # Try to intelligently fix unbalanced $
                
                # Case 1: Formula likely ends but missing closing $
                if re.search(r'\$[^$]+[=><\+\-\*/\)\]\}](?:\s|$)', line) and not line.strip().endswith('$'):
                    line = line.rstrip() + '$'
                    self.fixes_applied.append(f"Line {line_num}: Added missing closing $")
                
                # Case 2: Formula likely starts but missing opening $
                elif re.search(r'(?:^|\s)[a-zA-Z_]\w*\s*[=><].*\$$', line) and not line.lstrip().startswith('$'):
                    line = '$' + line.lstrip()
                    self.fixes_applied.append(f"Line {line_num}: Added missing opening $")
                
                # Case 3: Two separate formulas, one missing $
                elif line.count('$') == 3:
                    # Find pattern: $...$ text $...
                    if re.search(r'\$[^$]+\$\s+[^$]+\$[^$]+', line):
                        # Missing $ before second formula
                        line = re.sub(r'(\$[^$]+\$\s+)([^$\s])', r'\1$\2', line)
                        self.fixes_applied.append(f"Line {line_num}: Added missing $ between formulas")
            
            fixed_lines.append(line)
        
        self.fixed_text = '\n'.join(fixed_lines)
    
    def fix_incomplete_braces(self) -> None:
        """
            Fixes **unbalanced {}, [], ()** inside math mode $...$`.
            Adds missing closing brackets or removes extra closing brackets.
        """
        """Fix unbalanced braces, brackets, and parentheses in math mode"""
        # Find all math mode content
        def fix_braces_in_match(match):
            math_content = match.group(1)
            fixed = math_content
            
            # Count each type of bracket
            brackets = {
                '{': ('{', '}'),
                '(': ('(', ')'),
                '[': ('[', ']'),
            }
            
            for open_br, (o, c) in brackets.items():
                open_count = fixed.count(o)
                close_count = fixed.count(c)
                
                if open_count > close_count:
                    # Add missing closing brackets at the end
                    fixed += c * (open_count - close_count)
                    self.fixes_applied.append(f"Added {open_count - close_count} missing '{c}' in math mode")
                elif close_count > open_count:
                    # Remove extra closing brackets from the end
                    for _ in range(close_count - open_count):
                        if fixed.endswith(c):
                            fixed = fixed[:-1]
                    self.fixes_applied.append(f"Removed {close_count - open_count} extra '{c}' in math mode")
            
            return '$' + fixed + '$'
        
        # Fix inline math mode
        self.fixed_text = re.sub(r'\$([^$]+)\$', fix_braces_in_match, self.fixed_text)
    
    def fix_set_notation(self) -> None:
        """
        Fixes LaTeX set notation, e.g.:
            {x|x>0} → {x\mid x>0}
            Adds missing backslashes or corrects braces.
        """
        """Fix set notation issues (braces and mid/pipe symbols)"""
        # Fix: | should be \mid in set notation
        # Pattern: {x|...} → {x\mid...}
        pattern = r'(\{[^}]*)\|([^}]*\})'
        
        def fix_set(match):
            # Only fix if it looks like set notation (has a variable before |)
            before = match.group(1)
            after = match.group(2)
            
            if re.search(r'[a-zA-Z]$', before.strip()):
                self.fixes_applied.append(f"Fixed set notation: | → \\mid")
                return before + r'\mid' + after
            return match.group(0)
        
        self.fixed_text = re.sub(pattern, fix_set, self.fixed_text)
        
        # Fix missing backslash in set braces: ${x\mid...}$ should have \{ \}
        pattern = r'\$\{([^}]+\\mid[^}]+)\}\$'
        
        def fix_set_braces(match):
            content = match.group(1)
            if not content.startswith(r'\{'):
                self.fixes_applied.append("Fixed set braces: { → \\{")
                return r'$\{' + content + r'\}$'
            return match.group(0)
        
        self.fixed_text = re.sub(pattern, fix_set_braces, self.fixed_text)
    
    def fix_chinese_symbols_in_math(self) -> None:
        """Replace Chinese symbols with proper LaTeX equivalents"""

        """
        Replaces Chinese symbols commonly found in math:
        ， → ,
        。 → ^{\circ} (degree symbol)
        Full-width parentheses → regular parentheses
        Full-width numbers → normal digits
        """

        replacements = [
            # Chinese comma to regular comma in math mode
            (r'\$([^$]*?)，([^$]*?)\$', r'$\1, \2$'),
            
            # Chinese period as degree symbol: 90。→ 90^{\circ}
            (r'(\d+)\s*。', r'\1^{\\circ}'),
            
            # Full-width parentheses to regular
            (r'（', '('),
            (r'）', ')'),
            
            # Chinese colon
            (r'：', ':'),
            
            # Full-width numbers in math mode
            (r'\$([^$]*)[０-９]([^$]*)\$', lambda m: '$' + self._convert_fullwidth_numbers(m.group(0)) + '$'),
        ]
        
        for pattern, replacement in replacements:
            if callable(replacement):
                self.fixed_text = re.sub(pattern, replacement, self.fixed_text)
            else:
                count = len(re.findall(pattern, self.fixed_text))
                if count > 0:
                    self.fixed_text = re.sub(pattern, replacement, self.fixed_text)
                    self.fixes_applied.append(f"Replaced Chinese symbols ({count} instances)")
    
    def _convert_fullwidth_numbers(self, text: str) -> str:
        """Convert full-width numbers to regular numbers"""
        fullwidth = '０１２３４５６７８９'
        regular = '0123456789'
        trans = str.maketrans(fullwidth, regular)
        return text.translate(trans)
    
    def fix_itemize_enumerate_structure(self) -> None:
        """Fix structural issues in itemize/enumerate environments"""
        """
        Fixes structural issues with \item lines:
        Orphaned items outside of \begin{itemize}/\begin{enumerate} are wrapped in itemize.
        Reduces too many items (e.g., more than 4–6) to avoid malformed lists.
        
        """
        # Fix: Multiple \item without proper environment
        lines = self.fixed_text.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Check if we have multiple \item lines without begin/end
            if line.strip().startswith('\\item') and i > 0:
                # Look back to see if we're in an environment
                in_environment = False
                for j in range(i-1, max(-1, i-10), -1):
                    if '\\begin{itemize}' in lines[j] or '\\begin{enumerate}' in lines[j]:
                        in_environment = True
                        break
                    if '\\end{itemize}' in lines[j] or '\\end{enumerate}' in lines[j]:
                        break
                
                # If not in environment, look ahead for more items
                if not in_environment:
                    item_lines = [line]
                    j = i + 1
                    while j < len(lines) and lines[j].strip().startswith('\\item'):
                        item_lines.append(lines[j])
                        j += 1
                    
                    if len(item_lines) >= 2:
                        # Wrap in itemize
                        fixed_lines.append('\\begin{itemize}')
                        fixed_lines.extend(item_lines)
                        fixed_lines.append('\\end{itemize}')
                        self.fixes_applied.append(f"Wrapped {len(item_lines)} orphaned items in itemize")
                        i = j
                        continue
            
            fixed_lines.append(line)
            i += 1
        
        self.fixed_text = '\n'.join(fixed_lines)
        
        # Fix: Items with too much content (likely parsing error)
        pattern = r'(\\begin\{itemize\})(.*?)(\\end\{itemize\})'
        
        def fix_itemize_content(match):
            begin = match.group(1)
            content = match.group(2)
            end = match.group(3)
            
            # Find all items
            items = re.findall(r'\\item\s+([^\n]+)', content)
            
            # Check for malformed items
            cleaned_items = []
            for item in items:
                # Remove multiple \item occurrences within single item
                if '\\item' in item:
                    item = item.split('\\item')[0].strip()
                cleaned_items.append(item)
            
            # Limit to reasonable number (usually 4 for multiple choice)
            if len(cleaned_items) > 6:
                cleaned_items = cleaned_items[:4]
                self.fixes_applied.append(f"Reduced itemize from {len(items)} to 4 items")
            
            # Reconstruct
            new_content = '\n'.join([f'    \\item {item}' for item in cleaned_items])
            return f"{begin}\n{new_content}\n{end}"
        
        self.fixed_text = re.sub(pattern, fix_itemize_content, self.fixed_text, flags=re.DOTALL)
    
    def fix_spacing_issues(self) -> None:
        """Fix spacing issues around operators and symbols"""
        """
        Fixes spaces around symbols, operators, and punctuation.
        Examples:
        Multiple spaces → single space
        Remove spaces before , and .
        Fix spaces around = inside math mode
        
        """
        # Multiple spaces to single space
        self.fixed_text = re.sub(r'  +', ' ', self.fixed_text)
        
        # Space before comma/period
        self.fixed_text = re.sub(r'\s+([,.])', r'\1', self.fixed_text)
        
        # No space around = in math mode
        pattern = r'\$([^$]*)\s*=\s*([^$]*)\$'
        self.fixed_text = re.sub(pattern, r'$\1=\2$', self.fixed_text)
    
    def fix_common_command_typos(self) -> None:
        """Fix common typos in LaTeX commands"""
        """
        Fixes common LaTeX command typos, e.g.:
            \frat{ → \frac{
            \begn{ → \begin{
            Fixes malformed environment names (enumerate, itemize) 
        """
        typos = {
            # Command typos
            r'\\frat\{': r'\\frac{',
            r'\\dfrac\{': r'\\frac{',  # \dfrac is valid but normalize to \frac
            r'\\begn\{': r'\\begin{',
            r'\\ned\{': r'\\end{',
            
            # Symbol typos
            r'\\timse': r'\\times',
            r'\\cdtos': r'\\cdots',
            r'\\lDots': r'\\ldots',
            
            # Environment typos
            r'\\begin\{enumerate\s*\}': r'\\begin{enumerate}',
            r'\\end\{enumerate\s*\}': r'\\end{enumerate}',
            r'\\begin\{itemize\s*\}': r'\\begin{itemize}',
            r'\\end\{itemize\s*\}': r'\\end{itemize}',
            
            # Bold command variations
            r'\\pmb\{': r'\\mathbf{',
            r'\\boldsymbol\{': r'\\mathbf{',
        }
        
        for wrong, correct in typos.items():
            if re.search(wrong, self.fixed_text):
                self.fixed_text = re.sub(wrong, correct, self.fixed_text)
                self.fixes_applied.append(f"Fixed typo: {wrong} → {correct}")
    
    def fix_leftright_pairing(self) -> None:
        """Ensure \left and \right commands are properly paired"""
        """
        Ensures \left and \right are paired properly.
        Adds missing \right or removes extra \right.

        """
        # Find all \left commands
        left_pattern = r'\\left([(\[\{|])'
        right_pattern = r'\\right([)\]\}|])'
        
        # Match opening and closing
        pairs = {
            '(': ')',
            '[': ']',
            '{': r'\}',
            '|': '|',
        }
        
        def fix_leftright_in_math(match):
            content = match.group(1)
            
            # Find all \left
            lefts = [(m.start(), m.group(1)) for m in re.finditer(left_pattern, content)]
            rights = [(m.start(), m.group(1)) for m in re.finditer(right_pattern, content)]
            
            if len(lefts) > len(rights):
                # Add missing \right at the end
                for i in range(len(rights), len(lefts)):
                    bracket = lefts[i][1]
                    closing = pairs.get(bracket, bracket)
                    content += r'\right' + closing
                self.fixes_applied.append(f"Added {len(lefts) - len(rights)} missing \\right")
            
            elif len(rights) > len(lefts):
                # Remove \right without \left (just use regular bracket)
                content = re.sub(r'\\right([)\]\}|])', r'\1', content)
                self.fixes_applied.append(f"Removed {len(rights) - len(lefts)} unpaired \\right")
            
            return '$' + content + '$'
        
        self.fixed_text = re.sub(r'\$([^$]+)\$', fix_leftright_in_math, self.fixed_text)
    
    def fix_text_in_math_mode(self) -> None:

        """
        Wraps actual words in math mode inside \text{}.
        Example: $for x > 0$ → $ \text{for} x > 0 $
        
        """
        """Fix text that should be in \text{} within math mode"""
        # Pattern: detect words (3+ letters) in math mode that should be text
        pattern = r'\$([^$]*[a-zA-Z]{3,}[^$]*)\$'
        
        def fix_text(match):
            content = match.group(1)
            
            # Skip if already has \text or \mathrm or common functions
            if re.search(r'\\(text|mathrm|mathbf|sin|cos|tan|log|ln|exp|lim|max|min)', content):
                return match.group(0)
            
            # Find words that are likely text (not variables)
            # Common indicators: articles, prepositions, etc.
            text_words = ['and', 'or', 'if', 'then', 'where', 'for', 'when', 'the']
            
            for word in text_words:
                if re.search(rf'\b{word}\b', content, re.IGNORECASE):
                    content = re.sub(rf'\b({word})\b', r'\\text{\1}', content, flags=re.IGNORECASE)
                    self.fixes_applied.append(f"Wrapped '{word}' in \\text{{}}")
            
            return '$' + content + '$'
        
        self.fixed_text = re.sub(pattern, fix_text, self.fixed_text)
    """"""
    def fix_orphaned_items(self) -> None:
        """
            Detects \item outside any list environment and removes it.
            Ensures lists only appear inside itemize or enumerate.
        """
        """Fix \item that appears outside of list environments"""
        lines = self.fixed_text.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Check if line has \item
            if '\\item' in line and not line.strip().startswith('%'):
                # Check if we're in an environment
                in_environment = False
                environment_depth = 0
                
                # Look backwards
                for j in range(i-1, -1, -1):
                    if '\\begin{itemize}' in lines[j] or '\\begin{enumerate}' in lines[j]:
                        environment_depth += 1
                    if '\\end{itemize}' in lines[j] or '\\end{enumerate}' in lines[j]:
                        environment_depth -= 1
                
                if environment_depth > 0:
                    in_environment = True
                
                if not in_environment:
                    # This is an orphaned item, remove \item
                    line = line.replace('\\item ', '')
                    self.fixes_applied.append(f"Removed orphaned \\item at line {i+1}")
            
            fixed_lines.append(line)
        
        self.fixed_text = '\n'.join(fixed_lines)
    
    def get_report(self) -> str:
        """Generate a detailed report of all fixes applied"""
        if not self.fixes_applied:
            return "✓ No fixes were needed. Document appears to be well-formed."
        
        report = f"Applied {len(self.fixes_applied)} fixes:\n"
        report += "=" * 60 + "\n"
        
        # Group fixes by type
        fix_groups: Dict[str, List[str]] = {}
        for fix in self.fixes_applied:
            category = fix.split(':')[0] if ':' in fix else "General"
            if category not in fix_groups:
                fix_groups[category] = []
            fix_groups[category].append(fix)
        
        for category, fixes in fix_groups.items():
            report += f"\n{category}:\n"
            for fix in fixes:
                report += f"  • {fix}\n"
        
        return report
    
    def save_fixed_text(self, output_file: str) -> None:
        """Save the fixed text to a file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(self.fixed_text)
        print(f"✓ Fixed LaTeX saved to {output_file}")


# Convenience functions
def fix_latex_file(input_file: str, output_file: str) -> Tuple[str, str]:
    """Fix a LaTeX file and save the result"""
    with open(input_file, 'r', encoding='utf-8') as f:
        latex_text = f.read()
    
    fixer = LatexMathFixer(latex_text)
    fixed_text = fixer.fix_all()
    fixer.save_fixed_text(output_file)
    report = fixer.get_report()
    print(report)
    return fixed_text, report


def fix_latex_string(latex_text: str) -> Tuple[str, str]:
    """Fix LaTeX text provided as string, return fixed text and report"""
    fixer = LatexMathFixer(latex_text)
    fixed_text = fixer.fix_all()
    report = fixer.get_report()
    return fixed_text, report


# Example usage
if __name__ == "__main__":
    # Test with generic patterns
    test_cases = [
        r"$\{x|x>0\}$",  # Set notation
        r"$f(x)=x^2+1",  # Missing closing $
        r"90。",  # Chinese degree
        r"\item Orphaned item",  # Item without environment
        r"$\left(x+1\right)^2$",  # Correct left-right
        r"$\left(x+1$",  # Missing right
    ]
    
    print("Testing generic LaTeX fixes:\n")
    for test in test_cases:
        print(f"Original: {test}")
        fixed, _ = fix_latex_string(test)
        print(f"Fixed:    {fixed}\n")