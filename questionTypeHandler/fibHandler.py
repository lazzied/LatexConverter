import re
from utilityFunctions import escape_latex
from classes.myClasses import Question

class fillInBlankQuestionHandler:
    def __init__(self, text):
        self.text = text
    def fibHandler(self):
        # Pattern to capture fill-in-the-blank questions
         questionPattern = r'(?:^|\n)(\d+)[\.、]?\s*([\s\S]*?)(?=\n\d+[\.、]|$)'
         questions = re.findall(questionPattern, self.text, flags=re.MULTILINE)
         questionsList = [Question(Description=q[1].strip().replace('\n', ' ')) for q in questions]
         return questionsList

    # i want to keep it uniform acroos the other handlers, so this wrapper function will take a question 
    def fibWrapper(self, question:Question):
            return f"\\item {question.Description}" + "\\fillblank"+ "\\"
