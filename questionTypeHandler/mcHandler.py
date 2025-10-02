import re
from classes.myClasses import MultipleChoiceQuestion

# Test examples
testExample = r"""
1.若集合$M=\{x\mid\sqrt{x}<4\}$ $N=\{x\mid3x\geqslant1\}$ ，则$M\cap N=$ 

A.$\{x\mid0\leqslant x<2\}$ 

B.$\{x\mid\frac{1}{3}\leqslant x<2\}$ 

C.$\{x\mid3\leqslant x<16\}$ 

D.$\{x\mid\frac{1}{3}\leq x<16\}$ 

2.若$i(1-z)=1$ ，则$z+\overline{z}=$ 

A.-2B.-1$C.1D.2

3.在△ABC中，点D在边$AB 上$ $BD=2DA$ .记$\overrightarrow{CA}=m$ ，$\overline{CD}=n$ ，则$\overrightarrow{CB}=$ 

A.$3m-2m$ B.$-2m+3n$ C.$3m+2n$ D.$2m+3n$ 

4南水北调工程缓解了北方一些地区水资源短缺问题，其中一部分水蓄入某水库.已知该水库水位为海拔148.5m时，相应水面的面积为140.0km；水位为海拔157.5m 时，相应水面的面积为$180.0km^2$ .将该水库在这两个水位间的形状看作一个棱台，则该水库水位从海拔148.5m上升到157.5m时，增加的水量约为（$\sqrt{7}\approx2.65$ 

A.$1.0\times10^{9}m^{3}$ B.$1.2\times10^{9}m^{3}$ C.$1.4\times10^{9}m^{3}$ D.$1.6\times10^{9}m^{3}$ 

5.从2至8的7个整数中随机取2个不同的数，则这2个数互质的概率为

A.$\frac{1}{6}$ B.$\frac{1}{3}$ C.$\frac{1}{2}$ D.$\frac{2}{3}$ 



的图像关于点$(\frac{3\pi}{2},2)$ 中心对称，则$f(\frac{\pi}{2})=$ 

A.1B.$\frac{3}{2}$ C.$\frac{5}{2}$ D.3

7.设$a=0.1e^{0.1}$ $b=\frac{1}{9},\quad c=-\ln0.9$ ，则

A.$a<b<c$ B.$c<b<a$ C.$c<a<b$ D.$a<c<b$ 

8.已知正四棱锥的侧棱长为1，其各顶点都在同一球面上，若该球的体积为36π，且$3\leq1\leq3\sqrt{3}$ ，则该正四棱锥体积的取值范围是



A.$[18,\frac{81}{4}]$ B.$[\frac{27}{4},\frac{81}{4}]$ C.$[\frac{27}{4},\frac{64}{3}]$ D. [18,27]


9.已知正方体$ABCD-A_{1}B_{1}C_{1}D_{1}$ ，则

A.直线$BC_{1}$ 与$DA_{1}$ 所成的角为$90^{\circ}$ 

B.直线$BC_{1}$ 与$CA_{1}$ 所成的角为$90^{\circ}$ 

C.直线$BC_{1}$ 与平面$B B_{1}D_{1}D$ 所成的角为450。

D.直线$BC_{1}$ 与平面$ABCD$ 所成的角为$45^{\circ}$ 

10.已知函数$f(x)=x^{3}-x+1$ ，则

A.$f(x)$ 有两个极值点B.$f(x)$ 有三个零点

C.点(0,1)是曲线$y=f(x)$ 的对称中心B.直线$y=2x$ 是曲线$y=f(x)$ 的切线

11.已知0为坐标原点，点A(1，1)在抛物线$C:x^{2}=2py(p>0)$ 上，过点$B(0,-1)$ 的直线交C于P，Q两点，则



A.C的准线为$y=-1$ B.直线AB与C相切

C.$\vert O P\vert\cdot\vert O Q\vert>\vert O A\vert^{2}$ 

$$\left|B P\right|\cdot\left|B Q\right|>\left|B A\right|^{2}$$

12.已知函数$f(x)$ 及其导函数$f^{\prime}(x)$ 的定义域均为R，记$g(x)=f^{\prime}(x)$ .若$f(\frac{3}{2}-2x)$ $8(2+x)$ 均为偶函数，则



A.$f(0)=0$ B.$g(-\frac{1}{2})=0$ C.$f(-1)=f(4)$ D.$g(-1)=g(2)$ 

数学试题第2页（共4页）

---

"""

class multipleChoiceQuestionHandler:
    def __init__(self, text):
        self.text = text

    def mchandler(self):
        """Handles questions with options on separate lines"""
        OptionsPattern = r'^[A-D][\.、]?\s*(.+)$'
        questionPattern = r'(^\d+\.)(.*?)(?=^[A-D][\.、])'
        options = re.findall(OptionsPattern, self.text, flags=re.MULTILINE)
        question_match = re.search(questionPattern, self.text, flags=re.MULTILINE | re.DOTALL)
        question = question_match.group(2).strip() if question_match else ""
        print("Options found:", options)
        print("Question found:", question)
        return MultipleChoiceQuestion(
            Description=self.text,
            options=options,
            mainQuestion=question
        )

    def mchandler2(self):
        """Handles inline options with proper extraction"""
        OptionsPattern = r'([A-D])[\.、]?\s*([^A-D]+?)(?=[A-D][\.、]|$)'
        questionPattern = r'^\d+\.(.+?)(?=[A-D][\.、])'
        Options = re.findall(OptionsPattern, self.text, flags=re.DOTALL)
        question_match = re.search(questionPattern, self.text, flags=re.DOTALL)
        question = question_match.group(1).strip() if question_match else ""
        Options = [opt[1].strip() for opt in Options]
        
        # Clean Options
        cleaned_Options = []
        for opt in Options:
            opt = opt.strip()
            if opt and opt[-1] == '$' and opt[0] != '$':
                opt = '$' + opt
            cleaned_Options.append(opt)
        
        print("Options found:", cleaned_Options)
        print("Question found:", question)
        return MultipleChoiceQuestion(
            Description=self.text,
            options=cleaned_Options,
            mainQuestion=question
        )

    def mchandler3(self):
        """Handles inline options on a single line"""
        OptionsPattern = r'(?:^|\s)([A-D])[\.、]?\s*(.*?)(?=\s+[A-D][\.、]|$)'
        questionPattern = r'^\d+\.(.+?)(?=\s+[A-D][\.、])'
        Options = re.findall(OptionsPattern, self.text, flags=re.DOTALL)
        question_match = re.search(questionPattern, self.text, flags=re.DOTALL)
        question = question_match.group(1).strip() if question_match else ""
        Options = [opt[1].strip() for opt in Options]

        cleaned_Options = []
        for opt in Options:
            opt = opt.strip()
            if opt and opt[-1] == '$' and opt[0] != '$':
                opt = '$' + opt
            cleaned_Options.append(opt)

        print("Options found:", cleaned_Options)
        print("Question found:", question)
        return MultipleChoiceQuestion(
            Description=self.text,
            options=cleaned_Options,
            mainQuestion=question
        )


    def mchandler4(self):
        """Handles questions without period after number"""
        OptionsPattern = r'([A-D])[\.、]?\s*([^A-D]+?)(?=[A-D][\.、]|$)'
        questionPattern = r'^\d+\s*(.+?)(?=[A-D][\.、])'
        Options = re.findall(OptionsPattern, self.text, flags=re.DOTALL)
        Options = [opt[1].strip() for opt in Options]
        question_match = re.search(questionPattern, self.text, flags=re.DOTALL)
        question = question_match.group(1).strip() if question_match else ""
        
        cleaned_Options = []
        for opt in Options:
            opt = opt.strip()
            if opt and opt[-1] == '$' and opt[0] != '$':
                opt = '$' + opt
            cleaned_Options.append(opt)
        
        print("Options found:", cleaned_Options)
        print("Question found:", question)
        return MultipleChoiceQuestion(
            Description=self.text,
            options=cleaned_Options,
            mainQuestion=question
        )

    def mchandler5(self):
        """Handles questions without number prefix"""
        OptionsPattern = r'([A-D])[\.、]?\s*([^A-D]+?)(?=[A-D][\.、]|$)'
        Options = re.findall(OptionsPattern, self.text, flags=re.DOTALL)
        Options = [opt[1].strip() for opt in Options]
        
        questionPattern = r'[A-D][\.、]?\s*[^A-D]+'
        question = re.sub(questionPattern, '', self.text, flags=re.DOTALL).strip()
        
        cleaned_Options = []
        for opt in Options:
            opt = opt.strip()
            if opt and opt[-1] == '$' and opt[0] != '$':
                opt = '$' + opt
            cleaned_Options.append(opt)
        
        print("Options found:", cleaned_Options)
        print("Question found:", question)
        return MultipleChoiceQuestion(
            Description=self.text,
            options=cleaned_Options,
            mainQuestion=question
        )

    def mchandler6(self):
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
        return MultipleChoiceQuestion(
            Description=self.text,
            mainQuestion=question,
            options=options
        )


    def identify_handler(self):
        """Identifies which handler to use based on question format"""
        self.text = self.text.strip()
        lines = [line.strip() for line in self.text.split('\n') if line.strip()]

        if not lines:
            return None

        question_line = lines[0]

        # Fix: Only select mchandler4 if number is NOT followed by a dot or digit (like "4南水北调")
        match = re.match(r'^(\d+)[^\.\d]', question_line)
        if match:
            print("DEBUG: Selected handler = mchandler4 (no dot after number)")
            return self.mchandler4

        # Check if question has no number prefix
        if not re.match(r'^\d+', question_line):
            print("DEBUG: Selected handler = mchandler5 (no number prefix)")
            return self.mchandler5

        # Count unique option letters (A-D)
        option_letters = set(re.findall(r'[A-D](?=[\.、])', self.text))
        if len(option_letters) < 4:
            print("DEBUG: Selected handler = mchandler6 (less than 4 unique option markers)")
            return self.mchandler6

        # Find where options start
        Options_start = None
        for i, line in enumerate(lines):
            if re.search(r'^[A-D][\.、]', line):
                Options_start = i
                break

        if Options_start is None:
            Options_start = len(lines)

        # Check if options are on separate lines
        option_lines = lines[Options_start:]
        starts_with_options = [line for line in option_lines if re.match(r'^[A-D][\.、]', line)]
        separate_lines = len(starts_with_options) >= 4 and all(
            len(re.findall(r'^[A-D][\.、]', line)) == 1 for line in starts_with_options[:4]
        )

        if separate_lines:
            print("DEBUG: Selected handler = mchandler (options on separate lines)")
            return self.mchandler

        # Check for inline options (multiple options on one line)
        has_inline = any(len(re.findall(r'[A-D][\.、]', line)) > 1 for line in lines)

        if has_inline:
            question_text = ' '.join(lines[:max(1, Options_start)])
            # Remove actual option patterns from question
            question_cleaned = re.sub(r'[A-D][\.、]\s*[^A-D]*', '', question_text)
            has_ad_in_question = bool(re.search(r'[A-D]', question_cleaned))

            if has_ad_in_question:
                print("DEBUG: Selected handler = mchandler3 (inline options + A-D in question)")
                return self.mchandler3
            else:
                print("DEBUG: Selected handler = mchandler2 (clean inline options)")
                return self.mchandler2

        print("DEBUG: Defaulting to mchandler (fallback)")
        return self.mchandler




    def mcWrapper(self, question: MultipleChoiceQuestion):
        """Wraps the question in LaTeX itemize format"""
        Options = question.Options
        mainQuestion = question.MainQuestion
        result = "\\begin{itemize}\n"
        for option in Options:
            result += f"    \\item {option}\n"
        result += "\\end{itemize}"
        return [mainQuestion, result]

    @staticmethod
    def tester():
        """Test the handler identification"""
        examples = [testExample]
        expected = ['mchandler']
        
        for i, example in enumerate(examples, 1):
            print(f"\n{'='*60}")
            print(f"TESTING EXAMPLE {i}")
            print('='*60)
            testHandlerObject = multipleChoiceQuestionHandler(example)
            handler = testHandlerObject.identify_handler()
            handler_name = handler.__name__ if handler else None
            
            print(f"\nIdentified handler: {handler_name}")
            
            if handler:
                try:
                    result_obj = handler()
                    print(f"\n✓ Handler executed successfully")
                    print(f"Main Question: {result_obj.MainQuestion[:100]}...")
                    print(f"Number of options: {len(result_obj.Options)}")
                except Exception as e:
                    print(f"\n✗ Handler execution failed: {e}")
            
            if handler_name == expected[i-1]:
                print(f"\n✓ Correct handler identified")
            else:
                print(f"\n✗ Expected {expected[i-1]}, got {handler_name}")


