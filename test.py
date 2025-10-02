from testers.fix import LatexMathFixer
from typing import Tuple

test1 =r"""
\documentclass{article}
\usepackage[a4paper, margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{xeCJK}
\usepackage{enumitem}
\usepackage{booktabs}
\usepackage{parskip}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{array}
\usepackage{makecell}
\usepackage{multirow}
% Set a Chinese font available on your system (adjust if needed)
\setCJKmainfont{SimSun}
\definecolor{questioncolor}{RGB}{0,102,204}
\definecolor{optioncolor}{RGB}{153,0,0}
\setlist[enumerate]{label=\arabic*., leftmargin=*, itemsep=1.2em}
\setlist[itemize]{leftmargin=*}
\pagestyle{fancy}
\fancyhf{}
\rhead{Mathematics Exam}
\rfoot{\thepage}

ewcommand{\fillblank}[1][2cm]{\underline{\hspace{#1}}}
\renewcommand{\arraystretch}{1.4}
\setlength{\extrarowheight}{2pt}
\allowdisplaybreaks[4]
\begin{document}
\begin{center}
    \Large\textbf{Mathematics Exam}\\
    \vspace{0.5em}
    \large\textbf{Mathematics}
\end{center}
\section*{一、 选择题：本题共8小题，每小题5分，共40分。在每小题给出的四个选项中，只有一项是符合题目要求的。}
\\begin{enumerate}
\item 若集合$M=\{x\mid\sqrt{x}<4\}$ $N=\{x\mid3x\geqslant1\}$ ，则$M\cap N=$
\begin{itemize}
    \item $\{x\mid0\leqslant x<2\}$
    \item $\{x\mid\frac{1}{3}\leqslant x<2\}$
    \item $\{x\mid3\leqslant x<16\}$
    \item $\{x\mid\frac{1}{3}\leq x<16\}$
\end{itemize}
\item 若$i(1-z)=1$ ，则$z+\overline{z}=$
\begin{itemize}
    \item -2
    \item $-1$
    \item 1
    \item 2
\end{itemize}
\item 在△ABC中，点D在边$AB 上$ $BD=2DA$ .记$\overrightarrow{CA}=m$ ，$\overline{CD}=n$ ，则$\overrightarrow{CB}=$
\begin{itemize}
    \item $}=$
    \item $3m-2m$
    \item $-2m+3n$
    \item $3m+2n$
    \item $2m+3n$
\end{itemize}
\item 南水北调工程缓解了北方一些地区水资源短缺问题，其中一部分水蓄入某水库.已知该水库水位为海拔148.5m时，相应水面的面积为140.0km；水位为海拔157.5m 时，相应水面的面积为$180.0km^2$ 
.将该水库在这两个水位间的形状看作一个棱台，则该水库水位从海拔148.5m上升到157.5m时，增加的水量约为（$\sqrt{7}\approx2.65$
\begin{itemize}
    \item $1.0\times10^{9}m^{3}$
    \item $1.2\times10^{9}m^{3}$
    \item $1.4\times10^{9}m^{3}$
    \item $1.6\times10^{9}m^{3}$
\end{itemize}
\item 从2至8的7个整数中随机取2个不同的数，则这2个数互质的概率为
\begin{itemize}
    \item $\frac{1}{6}$
    \item $\frac{1}{3}$
    \item $\frac{1}{2}$
    \item $\frac{2}{3}$

---

的图像关于点$(\frac{3\pi}{2},2)$ 中心对称，则$f(\frac{\pi}{2})=$
    \item 1
    \item $\frac{3}{2}$
    \item $\frac{5}{2}$
    \item 3
\end{itemize}
\item 设$a=0.1e^{0.1}$ $b=\frac{1}{9},\quad c=-\ln0.9$ ，则
\begin{itemize}
    \item $a<b<c$
    \item $c<b<a$
    \item $c<a<b$
    \item $a<c<b$
\end{itemize}
\item 已知正四棱锥的侧棱长为1，其各顶点都在同一球面上，若该球的体积为36π，且$3\leq1\leq3\sqrt{3}$ ，则该正四棱锥体积的取值范围是
\begin{itemize}
    \item $[18,\frac{81}{4}]$
    \item $[\frac{27}{4},\frac{81}{4}]$
    \item $[\frac{27}{4},\frac{64}{3}]$
    \item [18,27]
\end{itemize}
\\end{enumerate}
\section*{二、选择题：本题共4小题，每小题5分，共20分。在每小题给出的选项中，有多项 符合题目要求。全部选对的得5分，部分选对的得2分，有选错的得0分。}
\\begin{enumerate}
\item 已知正方体$ABCD-A_{1}B_{1}C_{1}D_{1}$ ，则
\begin{itemize}
    \item 直线$BC_{1}$ 与$DA_{1}$ 所成的角为$90^{\circ}$
    \item 直线$BC_{1}$ 与$CA_{1}$ 所成的角为$90^{\circ}$
    \item 直线$BC_{1}$ 与平面$B B_{1}D_{1}D$ 所成的角为450。
    \item 直线$BC_{1}$ 与平面$ABCD$ 所成的角为$45^{\circ}$
\end{itemize}
\item .已知函数$f(x)=x^{3}-x+1$ ，则
\begin{itemize}
    \item $f(x)$ 有两个极值点
    \item $f(x)$ 有三个零点
    \item 点(0,1)是曲线$y=f(x)$ 的对称中心
    \item 直线$y=2x$ 是曲线$y=f(x)$ 的切线
\end{itemize}
\item .已知0为坐标原点，点A(1，1)在抛物线$C:x^{2}=2py(p>0)$ 上，过点$B(0,-1)$ 的直线交C于P，Q两点，则
\begin{itemize}
    \item 于P，Q两点，则
    \item $的准线为$y=-1$
    \item 相切
    \item $\right|^{2}$$
\end{itemize}
\item .已知函数$f(x)$ 及其导函数$f^{\prime}(x)$ 的定义域均为R，记$g(x)=f^{\prime}(x)$ .若$f(\frac{3}{2}-2x)$ $8(2+x)$ 均为偶函数，则
\begin{itemize}
    \item $f(0)=0$
    \item $g(-\frac{1}{2})=0$
    \item $f(-1)=f(4)$
    \item $g(-1)=g(2)$

数学试题第2页（共4页）

---
\end{itemize}
\\end{enumerate}
\section*{三、 填空题：本题共4小题，每小题5分，共20分。}
\\begin{enumerate}
\\\item $(1-\frac{y}{x})(x+y)^{2}$ 的展开式中$x^{2}y^{6}$ 的系数为（用数字作答）。\fillblank\\item 写出与圆$x^{2}+y^{2}=1$ 和$(x-3)^{2}+(y-4)^{2}=16$ 都相切的一条直线的方程\fillblank\\item 若曲线$y=(x+a)e^{x}$ 有两条过坐标原点的切线，则a的取值范围是\fillblank\\item 已知椭圆$C:\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1(a>b>0)$ ，C的上顶点为A，两个焦点为$F_{1},F_{2}$ ，离$ 心$ 率为$\frac{1}{2}$ .过$F_{1}$ 且垂直于$A F_{2}$ 的直线与C交于D，E两点，$|DE|=6$ $\triangle ADE$ 的周长是\fillblank\\\end{enumerate}
\section*{四、 解答题：本题共6小题，共70分。解答应写出文字说明、证明过程或演算步骤。}
\\begin{enumerate}
\item 17.(10分)

记$s_{n}$ 为数列$\{a_{n}\}$ 的前n项和，已知$a_{1}=1$ $\{\frac{S_n}{a_n}\}$ 是公差为$\frac{1}{3}$ 的等差数列.
\begin{enumerate}
    \item 求$\{a_{n}\}$ 的通项公式：
    \item 证明：$\frac{1}{a_{1}}+\frac{1}{a_{2}}+\cdots+\frac{1}{a_{n}}<2$
\end{enumerate}
\item 18. (12分)

记$\triangle ABC$ 的内角A，B，C的对边分别为a，$\pmb{b}$ ，c，已知$\frac{\cos A}{1+\sin A}=\frac{\sin2B}{1+\cos2B}$
\begin{enumerate}
    \item 若$c=\frac{2\pi}{3}$ ，求B;
    \item 求$\frac{a^{2}+b^{2}}{c^{2}}$ 的最小值.
\end{enumerate}
\item 19. (12分)

如图，直三棱柱$ABC-A_{1}B_{1}C_{1}$ 的体积为4，$\triangle A_{1}BC$ 的面积为$2\sqrt{2}$
\begin{enumerate}
    \item 求A到平面$A_{1}BC$ 的距离：
    \item 设D为$A_{1}C$ 的中点，$AA_{1}=AB$ ，平面$A_{1}BC\perp$ 平面$ABB_{1}A_{1}$ ，求二面角$A-BD-C$ 的正弦值.



\includegraphics[width=0.6\textwidth]{imgs/img_in_image_box_811_1302_1138_1559.jpg}


---
\end{enumerate}
\item 2V.（一医疗团队为研究某地的一种地方性疾病与当地居民的卫生习惯（卫生习惯分为良好和不够良好两类)的关系，在己患该疾病的病例中随机调查了100例（称为病例组)，同时在未患该疾病的人 
群中随机调查了100人（称为对照组），得到如下数据：


\begin{tabular}{c | c | c}
\hline
不够良好 & 良好 &  \\
\hline
病例组 & 40 & 60 \\
\hline
对照组 & 10 & 90 \\
\hline
\end{tabular}
\begin{enumerate}
    \item 能否有99%的把握认为患该疾病群体与未患该疾病群体的卫生习惯有差异?
    \item 从该地的人群中任选一人，A表示事件“选到的人卫生习惯不够良好”，B表示事件“选到的人患有该疾病”，$\frac{P(B\mid A)}{P(\overline{B}\mid A)} 与 \frac{P(B\mid\overline{A})}{P(\overline{B}\mid\overline{A})}$ 的比值是卫生习惯不够良好对患该疾病风险程度的一项度量指标，记该指标为R.
\end{enumerate}
\item 21. (12分)

已知点$A(2,1)$ 在双曲线C：$\frac{x^{2}}{a^{2}}-\frac{y^{2}}{a^{2}-1}=1(a>1).$ 上，直线I交C于P，Q两点，直线$\boldsymbol{A}\boldsymbol{P}$ ，AQ的斜率之和为0.
\begin{enumerate}
    \item 求1的斜率；
    \item 若$\tan\angle PAQ=2\sqrt{2}$ ,求$\triangle PAQ$ 的面积.
\end{enumerate}
\item 22. (12分)

已知函数$f(x)=\mathrm{e}^{x}-ax$ 和$g(x)=ax-\ln x$ 有相同的最小值.
\begin{enumerate}
    \item 求a；

（2）证明：存在直线$y=b$ ，其与两条曲线$y=f(x)$ 和$y=8(x)$ 共有三个不同的交点，并且从左到右的三个交点的横坐标成等差数列.



---
\end{enumerate}
\end{enumerate}
\item 22. (12分)

已知函数$f(x)=\mathrm{e}^{x}-ax$ 和$g(x)=ax-\ln x$ 有相同的最小值.
\begin{enumerate}
    \item 求a；

（2）证明：存在直线$y=b$ ，其与两条曲线$y=f(x)$ 和$y=8(x)$ 共有三个不同的交点，并且从左到右的三个交点的横坐标成等差数列.



---
\end{enumerate}
\item 22. (12分)

已知函数$f(x)=\mathrm{e}^{x}-ax$ 和$g(x)=ax-\ln x$ 有相同的最小值.
\begin{enumerate}
    \item 求a；

（2）证明：存在直线$y=b$ ，其与两条曲线$y=f(x)$ 和$y=8(x)$ 共有三个不同的交点，并且从左到右的三个交点的横坐标成等差数列.



---
\end{enumerate}
    \item 求a；

（2）证明：存在直线$y=b$ ，其与两条曲线$y=f(x)$ 和$y=8(x)$ 共有三个不同的交点，并且从左到右的三个交点的横坐标成等差数列.



---
\end{enumerate}
（2）证明：存在直线$y=b$ ，其与两条曲线$y=f(x)$ 和$y=8(x)$ 共有三个不同的交点，并且从左到右的三个交点的横坐标成等差数列.



---
\end{enumerate}


---
\end{enumerate}
\end{enumerate}
\\end{enumerate}

\end{document}
"""

def fix_latex_string(latex_text: str) -> Tuple[str, str]:
    """Fix LaTeX text provided as string, return fixed text and report"""
    fixer = LatexMathFixer(latex_text)
    fixed_text = fixer.fix_all()
    report = fixer.get_report()
    return fixed_text, report


import re
from classes.myClasses import MultipleChoiceQuestion

def extract_options(self):
    """Extract options line by line - collect A, B, C, then remaining becomes D"""
    questionPattern = r'(^\d+\.)(.*?)(?=^[A-D][\.、]|$)'
    question_match = re.search(questionPattern, self.text, flags=re.MULTILINE | re.DOTALL)
    question = question_match.group(2).strip() if question_match else ""
    options = []
    lines = [line.strip() for line in self.text.split('\n') if line.strip()]
    
    print(f"DEBUG: All lines: {lines}")  # Debug line
    
    # Find where options start
    option_start_idx = -1
    for i, line in enumerate(lines):
        if re.match(r'^[A-D][\.、]', line):
            option_start_idx = i
            break
    
    if option_start_idx == -1:
        return []  # No options found
    
    print(f"DEBUG: Options start at line {option_start_idx}: {lines[option_start_idx]}")  # Debug line
    
    # Process the option lines
    option_lines = lines[option_start_idx:]
    
    # First, split lines that contain multiple options (like "A. text B. text")
    split_option_lines = []
    for line in option_lines:
        # Split line by A., B., C., D. markers
        parts = re.split(r'([A-D][\.、])', line)
        if len(parts) > 1:
            # Reconstruct the split options
            for i in range(1, len(parts), 2):
                option_marker = parts[i]  # A., B., etc.
                option_content = parts[i+1].strip() if i+1 < len(parts) else ""
                split_option_lines.append(f"{option_marker} {option_content}")
        else:
            split_option_lines.append(line)
    
    print(f"DEBUG: Split option lines: {split_option_lines}")
    
    # Simple approach: find A, B, C explicitly, then everything else is D
    a_content = None
    b_content = None
    c_content = None
    d_content = []
    
    for line in split_option_lines:
        if line.startswith('A.') or line.startswith('A、'):
            a_content = line
        elif line.startswith('B.') or line.startswith('B、'):
            b_content = line
        elif line.startswith('C.') or line.startswith('C、'):
            c_content = line
        else:
            # This line doesn't start with A, B, or C - it's part of D
            d_content.append(line)
    
    # Build options array
    if a_content:
        options.append(a_content)
    if b_content:
        options.append(b_content)
    if c_content:
        options.append(c_content)
    
    # For D: combine all the remaining lines
    if d_content:
        d_option = "D. " + " ".join(d_content)
        options.append(d_option)
    
    print(f"DEBUG: Final options: {options}")  # Debug line
    return  MultipleChoiceQuestion(
        Description=self.text,
        mainQuestion=question,
        options=options
    )

def mchandler_universal(self):
    """Universal handler that works for most cases"""
    cleaned_text = self.clean_text()
    
    # Extract question number and text
    question_number, main_question = self.extract_question_number_and_text(cleaned_text)
    
    # Extract options
    options = extract_options(cleaned_text)
    
    # Clean the main question by removing any option-like patterns
    main_question = re.sub(r'[A-D][\.、]\s*[^A-D]*$', '', main_question, flags=re.MULTILINE).strip()
    
    print(f"Question {question_number}:")
    print(f"  Main: {main_question[:100]}...")
    print(f"  Options: {options}")
    print(f"  Options count: {len(options)}")
    
    return MultipleChoiceQuestion(
        Description=cleaned_text,
        mainQuestion=main_question,
        options=options
    )
questionEx=r""" 11.已知0为坐标原点，点A(1，1)在抛物线$C:x^{2}=2py(p>0)$ 上，过点$B(0,-1)$ 的直线交C于P，Q两点，则



A.C的准线为$y=-1$ B.直线AB与C相切

C.$\vert O P\vert\cdot\vert O Q\vert>\vert O A\vert^{2}$ 

$$\left|B P\right|\cdot\left|B Q\right|>\left|B A\right|^{2}$$"""


testExample="""
3.在△ABC中，点D在边$AB 上$ $BD=2DA$ .记$\overrightarrow{CA}=m$ ，$\overline{CD}=n$ ，则$\overrightarrow{CB}=$ 

A.$3m-2m$ B.$-2m+3n$ C.$3m+2n$ D.$2m+3n$ 

"""



from questionTypeHandler.mcHandler import multipleChoiceQuestionHandler
handler = multipleChoiceQuestionHandler(testExample)
mchandler = handler.identify_handler()
object = mchandler()

print(object.Options)