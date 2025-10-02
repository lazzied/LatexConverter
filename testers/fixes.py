# brute forcing solution; when scaling i'll fix them in the other functions
# issue 1 : ewcommand au lieu de \newcommand ; there's also a command named: \renewcommand ; so don't mix them up
# issue 2: \\begin{enumerate} au lieu de \begin{enumerate}
# issue 3: \\end{enumerate} au lieu de \end{enumerate}
#issue 4: \\ avant \item dans les listes
#issue 5: delete --- dans les options de question
# fix math: $\right|^{2}$ ; $\pmb{b}$ ; 
# text inside math equation : 与 \text{ et }
# $\boldsymbol{A}\boldsymbol{P}$ rreur : Utilisation de \boldsymbol pour des lettres simples. Correction : Remplacez par $AP$.
# 	      数学试题第2页（共4页）: Mathematics Test Page 2 (of 4) ; remove page numbering
##\item 22. (12分) couldn't detect (2)
textdz= r"""
已知函数$f(x)=\mathrm{e}^{x}-ax$ 和$g(x)=ax-\ln x$ 有相同的最小值.
\begin{enumerate}
	\item 求a；
	      
	      （2）证明：存在直线$y=b$ ，其与两条曲线$y=f(x)$ 和$y=8(x)$ 共有三个不同的交点，并且从左到右的三个交点的横坐标成等差数列.
"""
import re

def replace(text: str) -> str:
    changes = {
        r"\\begin": r"\begin",
        r"\\end": r"\end", 
        r"\\item": r"\item",
        r"---": "",
        r"ewcommand\{\\fillblank\}": r"\newcommand{\fillblank}",
    }
    
    for pattern, replacement in changes.items():
        # Escape the pattern for regex
        escaped_pattern = re.escape(pattern)
        # For replacement, we need to handle backslashes carefully
        # Replace single backslash with double backslash in replacement
        safe_replacement = replacement.replace('\\', '\\\\')
        text = re.sub(escaped_pattern, safe_replacement, text)
    
    return text

# Alternative simpler approach without regex:
def replace_simple(text: str) -> str:
    changes = {
        r"\\begin": r"\begin",
        r"\\end": r"\end",
        r"\\item": r"\item", 
        r"---": "",
    }
    
    for old, new in changes.items():
        text = text.replace(old, new)
    
    return text

text = r"""\end{enumerate}
\section*{二、选择题：本题共4小题，每小题5分，共20分。在每小题给出的选项中，有多项 符合题目要求。全部选对的得5分，部分选对的得2分，有选错的得0分。}
\\begin{enumerate}
\item 已知正方体$ABCD-A_{1}B_{1}C_{1}D_{1}$ ，则
"""

# Using the simple version is actually better for this case
fixed_text = replace_simple(text)
print(fixed_text)

"""
The key issues in your original code were:

In the changes dictionary: You had r"\\begin": r"\\begin" which means you were replacing \\begin with \\begin (no change), when you wanted to replace \\begin with \begin.

Backslash handling: In regex replacements, backslashes need special handling. The simpler string .replace() method avoids these issues.
Escaping regex special characters

Curly braces {} and backslashes \ in LaTeX commands are special in regex.

Fixed by using \{, \}, and \\ in regex patterns.

Use .items() to iterate dictionaries

Original code: for key, value in changes: → wrong.

Fixed: for key, value in changes.items():.

Assign re.sub result back to text

re.sub() does not modify the string in-place.

Fixed: text = re.sub(key, value, text).

Use raw strings (r"") for patterns and replacements

Prevent Python from interpreting \n, \t, \b as special characters.

Double backslashes in replacement strings

\newcommand → \\newcommand to avoid bad escape \e error in re.sub().

Removed unnecessary if re.search() check

re.sub() already does nothing if no match; the check is redundant.
 """

