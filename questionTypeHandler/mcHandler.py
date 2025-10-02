import re
from classes.myClasses import MultipleChoiceQuestion

# Test examples
testExample = r"""
1.若集合$M=\{x\mid\sqrt{x}<4\}$ $N=\{x\mid3x\geqslant1\}$ ，则$M\cap N=$
A.$\{x\mid0\leqslant x<2\}$
B.$\{x\mid\frac{1}{3}\leqslant x<2\}$
C.$\{x\mid3\leqslant x<16\}$
D.$\{x\mid\frac{1}{3}\leq x<16\}$
"""

class multipleChoiceQuestionHandler:
    def __init__(self, text):
        self.text = text

    def mchandler(self):
        OptionsPattern = r'^[A-D][\.、]?\s*(.+)$'
        questionPattern = r'(^\d+\.)(.*?$)'
        options = re.findall(OptionsPattern, self.text, flags=re.MULTILINE)
        question = re.findall(questionPattern, self.text, flags=re.MULTILINE)[0][1]
        print("Options found:", options)
        print("Questions found:", question)
        return MultipleChoiceQuestion(
            Description=self.text,
            options=options,
            mainQuestion=question
        )

    def mchandler2(self):
        OptionsPattern = r'([A-D])[\.、]?\s*([^A-D]+)'
        questionPattern = r'(^\d+\.)(.*?$)'
        Options = re.findall(OptionsPattern, self.text)
        question = re.findall(questionPattern, self.text, flags=re.MULTILINE)[0][1]
        Options = [opt[1] for opt in Options]
        # Clean Options
        cleaned_Options = []
        for opt in Options:
            if opt and opt[-1] == '$' and opt[0] != '$':
                opt = '$' + opt
            opt = opt.rstrip('\n').rstrip()
            cleaned_Options.append(opt)
        print("Options found:", cleaned_Options)
        print("Questions found:", question)
        return MultipleChoiceQuestion(
            Description=self.text,
            options=cleaned_Options,
            mainQuestion=question
        )

    def mchandler3(self):
        OptionsPattern = r'(^[A-D])[\.、]?\s*([^A-D]+)+([A-D])[\.、]?\s*([^A-D]+)+([A-D])[\.、]?\s*([^A-D]+)+([A-D])[\.、]?\s*([^A-D]+)'
        questionPattern = r'(^\d+\.)(.*?$)'
        Options = re.findall(OptionsPattern, self.text, flags=re.MULTILINE)
        question = re.findall(questionPattern, self.text, flags=re.MULTILINE)[0][1]
        Options = [opt[i] for opt in Options for i in range(1, 8, 2)]
        cleaned_Options = []
        for opt in Options:
            if opt and opt[-1] == '$' and opt[0] != '$':
                opt = '$' + opt
            opt = opt.rstrip('\n').rstrip()
            cleaned_Options.append(opt)
        print("Options found:", cleaned_Options)
        print("Questions found:", question)
        return MultipleChoiceQuestion(
            Description=self.text,
            options=cleaned_Options,
            mainQuestion=question
        )

    def mchandler4(self):
        OptionsPattern = r'(^[A-D])[\.、]?\s*([^A-D]+)+([A-D])[\.、]?\s*([^A-D]+)+([A-D])[\.、]?\s*([^A-D]+)+([A-D])[\.、]?\s*([^A-D]+)'
        questionPattern = r'(^\d)(.*?$)'
        Options = re.findall(OptionsPattern, self.text, flags=re.MULTILINE)
        Options = [opt[i] for opt in Options for i in range(1, 8, 2)]
        question = re.findall(questionPattern, self.text, flags=re.MULTILINE)[0][1]
        cleaned_Options = []
        for opt in Options:
            if opt and opt[-1] == '$' and opt[0] != '$':
                opt = '$' + opt
            opt = opt.rstrip('\n').rstrip()
            cleaned_Options.append(opt)
        print("Options found:", cleaned_Options)
        print("Questions found:", question)
        return MultipleChoiceQuestion(
            Description=self.text,
            options=cleaned_Options,
            mainQuestion=question
        )

    def mchandler5(self):
        OptionsPattern = r'([A-D])[\.、]?\s*([^A-D]+)'
        Options = re.findall(OptionsPattern, self.text)
        Options = [opt[1] for opt in Options]
        questionPattern = r'[A-D][\.、]?\s*[^A-D]+'
        question = re.sub(questionPattern, '', self.text).strip()
        cleaned_Options = []
        for opt in Options:
            if opt and opt[-1] == '$' and opt[0] != '$':
                opt = '$' + opt
            opt = opt.rstrip('\n').rstrip()
            cleaned_Options.append(opt)
        print("Options found:", cleaned_Options)
        print("Questions found:", question)
        return MultipleChoiceQuestion(
            Description=self.text,
            options=cleaned_Options,
            mainQuestion=question
        )

    def mchandler6(self):
        questionPattern = r'(^\d+.)(.*?$)'
        OptionsPattern = r'([A-D][\.、]\s*.*?)(?=\s*[A-D][\.、]|$)'
        options = re.findall(OptionsPattern, self.text, flags=re.MULTILINE)
        question = re.findall(questionPattern, self.text, flags=re.MULTILINE)[0][1]
        print("Questions found:", question)
        print("Options found:", options)
        if len(options) != 4:
            print("Error: Expected 4 Options, found", len(options))
            onlyOptions = re.sub(questionPattern, '', self.text, flags=re.MULTILINE).strip()
            for opt in options:
                onlyOptions = onlyOptions.replace(opt, '')
            lines = [line.strip() for line in onlyOptions.split('\n') if line.strip()]
            missingOption = lines[-1] if lines else ''
            options.append(missingOption)
        return MultipleChoiceQuestion(
            Description=self.text,
            options=options,
            mainQuestion=question
        )

    def identify_handler(self):
        self.text = self.text.strip()
        lines = [line.strip() for line in self.text.split('\n') if line.strip()]
        if not lines:
            return None
        question_line = lines[0]
        match = re.match(r'^\d+', question_line)
        if match and (match.end() == len(question_line) or question_line[match.end()] != '.'):
            return self.mchandler4
        if not re.match(r'^\d+\.', question_line):
            return self.mchandler5
        option_letters = set(re.findall(r'([A-D])[\.、]', self.text))
        if len(option_letters) < 4:
            return self.mchandler6
        Options_start = None
        for i, line in enumerate(lines):
            if re.search(r'[A-D][\.、]', line):
                Options_start = i
                break
        question = ' '.join(lines[:Options_start])
        has_ad_in_question = re.search(r'[A-D]', question)
        option_lines = lines[Options_start:]
        separate_lines = all(re.match(r'^[A-D][\.、]', line) for line in option_lines)
        if separate_lines and len(option_lines) == 4:
            return self.mchandler
        inline = any(len(re.findall(r'[A-D][\.、]', line)) > 1 for line in option_lines)
        if inline:
            if has_ad_in_question:
                return self.mchandler3
            else:
                if re.search(r'[A-D][\.、]?\s*\$', self.text):
                    return self.mchandler
                else:
                    return self.mchandler2
        return self.mchandler

    def mcWrapper(self, question: MultipleChoiceQuestion):
        Options = question.Options
        mainQuestion = question.MainQuestion
        result = "\\begin{itemize}\n"
        for option in Options:
            result += f"    \\item {option}\n"
        result += "\\end{itemize}"
        return [mainQuestion, result]

    @staticmethod
    def tester():
        examples = [testExample]  # add other examples if needed
        expected = ['mchandler']
        for i, example in enumerate(examples, 1):
            testHandlerObject = multipleChoiceQuestionHandler(example)
            handler = testHandlerObject.identify_handler()
            handler_name = handler.__name__ if handler else None
            result_obj = handler() if handler else None
            print(f"Example {i}: Using {handler_name}")
            if handler_name == expected[i-1]:
                print("✓ Correct")
            else:
                print(f"✗ Expected {expected[i-1]}")
