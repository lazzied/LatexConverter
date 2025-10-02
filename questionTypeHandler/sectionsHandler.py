import re
from utilityFunctions import escape_latex
from classes.myClasses import Section

class examPartitioning:
    def __init__(self, file):
        self.file = file
        self.sections=[] # list of tuples; each tuple is a header and body


# in the handleSections; i want a function, that returns a list of section objects; each section object contains; section number; section header;
    def handleSections(self):

        with open(self.file, "r", encoding="utf-8") as file:
            content = file.read()
        # Robust pattern for markdown headers with Chinese numerals and section name; not the whole section name but only the keyword !!! 
        section_pattern = (
            r'(^#+\s*[一二三四五六七八九十]+[、。]\s*.*?[题：].*?$)([\s\S]*?)(?=^#+\s*[一二三四五六七八九十]+[、。]|\Z)'
        )
        matches = re.findall(section_pattern, content, flags=re.MULTILINE | re.DOTALL)
        if not matches:
            print("No matching section found.")
            return
        
        def clean_header(header):
            # Remove leading # and whitespace
            return re.sub(r'^#+\s*', '', header)
        def extractNumber(header):
            match = re.search(r'([一二三四五六七八九十]+)', header)
            numberStr = match.group(1) if match else ""  # returns the captured numeral as a string, or empty string if no match
            return numberStr
        def extractType(header):
            match = re.search(r'(选择题|填空题|解答题)', header)
            typeStr = match.group(1) if match else ""
            return typeStr

        try:
            Sections = [
                Section(
                    self.file,
                    text=header + "\\" + body,
                    header=clean_header(header),
                    body=body.strip(),
                    number=extractNumber(header),
                    type=extractType(header)
                )
                for header, body in matches
            ]
        except Exception as e:
            print("Error creating Section objects:", e)
            Sections = []

        return Sections


    