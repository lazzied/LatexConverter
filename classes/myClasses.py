import re
from typing import List, Optional
from enum import Enum


class SectionType(Enum):
    MCQ = "选择题"
    FIB = "填空题"
    ESSAY = "解答题"


class Exam:
    def __init__(self, file: str, title: str = ""):
        self.File = file
        self.Sections: List["Section"] = []
        self.TotalPoints = 0
        self.TotalQuestions = 0
        self.Title = title

    def addSection(self, section: "Section"):
        self.Sections.append(section)


class Section:
    def __init__(self, file: str, text: str, body: str, header: str, number: int, type: SectionType):
        self.ExamFile = file
        self.Text = text
        self.Body = body
        self.Header = header
        self.Number = number
        self.Type = type
        self.Points = 0

    def questionsSeperator(self, text: str) -> List[str]:
        pattern = r'(?ms)^\s*(\d+\.?.*?)(?=^\s*\d+\.?|\Z)'
        return [q.strip() for q in re.findall(pattern, text)]


# -------------------------
# Typed Section Wrappers
# -------------------------
class MultipleChoiceSection(Section):
    def __init__(self, baseSection: Section):
        super().__init__(
            file=baseSection.ExamFile,
            text=baseSection.Text,
            body=baseSection.Body,
            header=baseSection.Header,
            number=baseSection.Number,
            type=SectionType.MCQ
        )
        self.questionsList: List[MultipleChoiceQuestion] = []

    def questionsSeperator(self, text: str) -> List[str]:
        pattern = r'(?ms)^\s*(\d+\.?.*?)(?=^\s*\d+\.?|\Z)'
        return [q.strip() for q in re.findall(pattern, text)]


class FillInBlankSection(Section):
    def __init__(self, baseSection: Section):
        super().__init__(
            file=baseSection.ExamFile,
            text=baseSection.Text,
            body=baseSection.Body,
            header=baseSection.Header,
            number=baseSection.Number,
            type=SectionType.FIB
        )
        self.questionsList: List[Question] = []


class EssaySection(Section):
    def __init__(self, baseSection: Section):
        super().__init__(
            file=baseSection.ExamFile,
            text=baseSection.Text,
            body=baseSection.Body,
            header=baseSection.Header,
            number=baseSection.Number,
            type=SectionType.ESSAY
        )
        self.questionsList: List[EssayQuestion] = []

    def questionsSeperator(self, text: str) -> List[str]:
        pattern = r'(?ms)^\s*(?:#+\s*)?((?:\d+|2V)\..*?)(?=^\s*(?:#+\s*)?(?:\d+|2V)\.|\Z)'
        return [q.strip() for q in re.findall(pattern, text)]


# -------------------------
# Question Hierarchy
# -------------------------
class Question:
    def __init__(self, Description: str, points=0):
        self.Description = Description
        self.Points = points


class MultipleChoiceQuestion(Question):
    def __init__(self, Description: str, mainQuestion: str, options: List[str], points: int = 0):
        super().__init__(Description, points)  # HERE DESCRIPTION TAKES THE WHOLE QUESTION 
        self.MainQuestion = mainQuestion
        self.Options = options


class FillInBlankQuestion(Question):
    def __init__(self, Description: str, blanks: Optional[List[str]] = None, points: int = 0):
        super().__init__(Description, points)
        self.Blanks = blanks or []


class EssayQuestion(Question):
    def __init__(self, Description: str, subQuestions: Optional[List["EssayQuestion"]] = None, points: int = 0):
        super().__init__(Description, points) # HERE THE DESCRIPTION IS THE 
        self.SubQuestions = subQuestions


# -------------------------
# Other Elements
# -------------------------
class Image:
    """Represents an image element found in HTML."""
    
    def __init__(self, src: str, div_text: str):
        self.src = src
        self.div_text = div_text
    
    def to_latex(self) -> str:
        """Convert the image to LaTeX format."""
        return rf'\includegraphics[width=0.6\textwidth]{{{self.src}}}'


class Table:
    """Represents a table element found in HTML."""
    
    def __init__(self, num_rows: int, num_cols: int, cells: List[List[str]], div_text: str):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cells = cells
        self.div_text = div_text
    
    def to_latex(self) -> str:
        """Convert the table to LaTeX format."""
        column_spec = " | ".join(["c"] * self.num_cols)
        latex_table = rf"\begin{{tabular}}{{{column_spec}}}" + "\n\\hline\n"
        
        for row in self.cells:
            latex_row = " & ".join(row) + r" \\ " + "\n\\hline\n"
            latex_table += latex_row
        
        latex_table += r"\end{tabular}"
        return latex_table