from classes.myClasses import *

from questionTypeHandler.eqHandler import *
from questionTypeHandler.mcHandler import *
from questionTypeHandler.fibHandler import *
from questionTypeHandler.sectionsHandler import *

from documentLayoutHandler.displayHandler import *
from documentLayoutHandler.packagesHandler import *






def handle_mc_section(section):
    latex = r'\section*{' + section.Header + r'}' + r'\n\\begin{enumerate}\n'
    mcSection = MultipleChoiceSection(section)
    questions = mcSection.questionsSeperator(section.Body)

    for q in questions:
        handler = multipleChoiceQuestionHandler(q)
        mchandler = handler.identify_handler()
        mcQuestion = mchandler()  # call the function, not tempHandler.mchandler
        mcSection.questionsList.append(mcQuestion)

    for q in mcSection.questionsList:
        handler = multipleChoiceQuestionHandler(q)
        mainQ, Options = handler.mcWrapper(q)
        latex += rf"\item {mainQ}\n{Options}\n"

    latex += r"\\end{enumerate}\n"
    return latex


def handle_fib_section(section):
    latex = r'\section*{' + section.Header + r'}' + r'\n\\begin{enumerate}\n\\'
    fibSection = FillInBlankSection(section)
    # fib is different from them since it's not complicated at all
    handler = fillInBlankQuestionHandler(section.Body)
    questions = handler.fibHandler()
    fibSection.questionsList = questions
    
    for q in fibSection.questionsList:
        handler = fillInBlankQuestionHandler(q)
        latex += handler.fibWrapper(q)


    latex += r"\\end{enumerate}\n"
    return latex


def handle_eq_section(section):
    latex = r'\section*{' + section.Header + r'}' + r'\n\\begin{enumerate}\n'
    eqSection = EssaySection(section)
    questions = eqSection.questionsSeperator(section.Body)

    for q in questions:
        handler = EssayQuestionHandler(q)
        eqhandler = handler.identify_handler()
        eqQ = eqhandler()
        eqSection.questionsList.append(eqQ)

    for q in eqSection.questionsList:
        handler = EssayQuestionHandler(q)
        mainDesc, subqs = handler.eqWrapper(q)
        latex += rf"\item {mainDesc}\n{subqs}\n"

    latex += r"\\end{enumerate}\n"

    return latex


def main():
    filePath = r"C:\Users\user\Desktop\CEE\tex file testing\MATH\MATH1\originaltex.md"
    mathExam = Exam(filePath)
    mathExam.Title = "Mathematics Exam"

    latexOutput = templateHeader(mathExam.Title, "Mathematics")

    examSplitter = examPartitioning(filePath)
    Sections = examSplitter.handleSections()
    mathExam.Sections = Sections
   

    for section in Sections:
        if section.Type == "选择题":  # access .value of Enum
            latexOutput += handle_mc_section(section)
        elif section.Type == "填空题":
            latexOutput += handle_fib_section(section)
        else:
            latexOutput += handle_eq_section(section)

    latexOutput += templateFooter()
    latexOutput = latexOutput.replace(r"\n", "\n")
    
    with open("myfile.txt", "w", encoding="utf-8") as f:
        f.write(latexOutput)

    htmlEditor = HtmlTweaker(filePath)
    htmlEditor.process()
    
    with open("myfile.txt", "r", encoding="utf-8") as f:
        content = f.read()

    print(content)

if __name__ == "__main__":
    main()





 
