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
