import re
from classes.myClasses import Question, EssayQuestion

example1 = r"""
### 18. (12分)

记$\triangle ABC$ 的内角A，B，C的对边分别为a，$\pmb{b}$ ，c，已知$\frac{\cos A}{1+\sin A}=\frac{\sin2B}{1+\cos2B}$ 

(1)若$c=\frac{2\pi}{3}$ ，求B;

(2) 求$\frac{a^{2}+b^{2}}{c^{2}}$ 的最小值.

"""

example2 = r"""
2V.（一医疗团队为研究某地的一种地方性疾病与当地居民的卫生习惯（卫生习惯分为良好和不够良好两类)的关系，在己患该疾病的病例中随机调查了100例（称为病例组)，同时在未患该疾病的人群中随机调查了100人（称为对照组），得到如下数据：


(1)能否有99%的把握认为患该疾病群体与未患该疾病群体的卫生习惯有差异?

(2)从该地的人群中任选一人，A表示事件“选到的人卫生习惯不够良好”，B表示事件“选到的人患有该疾病”，$\frac{P(B\mid A)}{P(\overline{B}\mid A)} 与 \frac{P(B\mid\overline{A})}{P(\overline{B}\mid\overline{A})}$ 的比值是卫生习惯不够良好对患该疾病风险程度的一项度量指标，记该指标为R.



(i)证明：$R=\frac{P(A\mid B)}{P(\overline{A}\mid B)}\cdot\frac{P(\overline{A}\mid\overline{B})}{P(A\mid\overline{B})}$ 

（ii）利用该调查数据，给出$P(A\mid B)$ $P(A\mid\overline{B})$ 的估计值，并利用（i）的结果给出R的估计值.



$$K^{2}=\frac{n(ad-bc)^{2}}{(a+b)(c+d)(a+c)(b+d)},\quad\frac{P(K^{2}\geq k)\quad0.050\quad0.010\quad0.001}{k\quad3.841\quad6.635\quad10.828}$$

"""

class EssayQuestionHandler:
    def __init__(self, text):
        self.text = text

    def eqHandler1(self):
        """Handles subquestions like (1), (2) ..."""
        pointsPattern = r'^(?:#+\s*\d+\.\s*)?\((\d+分)\)'
        subQuestionPattern = r'(\d+)\)\s*(.*?)(?=\(\d+\)|$)'

        subQuestions = re.findall(subQuestionPattern, self.text, flags=re.DOTALL)

        # Extract clean subquestions
        subQuestionsList = [sq[1].strip().replace('\n', ' ') for sq in subQuestions]

        # Build Question objects with Description instead of Text
        subQuestionObjects = [Question(Description=sq) for sq in subQuestionsList]

        # Remove subquestions from main description using regex
        questionDescription = re.sub(pointsPattern, '', self.text, flags=re.MULTILINE).strip()
        questionDescription = re.sub(subQuestionPattern, '', questionDescription, flags=re.DOTALL).strip()

        print("Main question found:", questionDescription.strip().replace('\n', ' '))
        print("SubQuestions found:", subQuestionsList)

        return EssayQuestion(
            Description=questionDescription,
            subQuestions=subQuestionObjects
        )

    def eqHandler2(self):
        """Handles subquestions with nested (i), (ii) ..."""
        subQuestionPattern = r'(?ms)^(?:\(\d+\)|（\d+）)[\s\S]*?(?=^(?:\(\d+\)|（\d+）)|\Z)'
        subQuestions = re.findall(subQuestionPattern, self.text, flags=re.MULTILINE | re.DOTALL)

        mainDescription = re.sub(subQuestionPattern, '', self.text).strip()

        subsubPattern = r'^[ \t]*[\(（]([ivx]+)[\)）][ \t]*([\s\S]*?)(?=^[ \t]*[\(（][ivx]+[\)）]|\Z)'

        listOfSubquestions = []
        for subq_text in subQuestions:
            subq_obj = EssayQuestion(Description=subq_text.strip())

            # Extract subsubquestions
            subsubs = re.findall(subsubPattern, subq_text, flags=re.MULTILINE)
            if subsubs:
                subq_obj.SubQuestions = [Question(Description=s[1].strip()) for s in subsubs]
            else:
                subq_obj.SubQuestions = []

            listOfSubquestions.append(subq_obj)

        return EssayQuestion(
            Description=mainDescription,
            subQuestions=listOfSubquestions
        )

    def identify_handler(self):
        """Auto-detect which handler to use"""
        subSubQuestionIndexPattern = r'[\(（][ivxIVX]+[\)）]'
        if re.search(subSubQuestionIndexPattern, self.text, flags=re.MULTILINE):
            return self.eqHandler2
        else:
            return self.eqHandler1
    def eqWrapper(self, question: EssayQuestion):
        """
        Wrap an EssayQuestion into [description, LaTeX enumerate string]
        """
        latexLines = ["\\begin{enumerate}"]
        

        for subq in question.SubQuestions:
            # Add main subquestion
            questionDesc = subq.Description
            latexLines.append(f"    \\item {questionDesc}")

            # Add nested subsubquestions if any
            if isinstance(subq, EssayQuestion) and subq.SubQuestions:
                latexLines.append("    \\begin{enumerate}")
                for ss in subq.SubQuestions:
                    latexLines.append(f"        \\item {ss.Description}")
                latexLines.append("    \\end{enumerate}")

        latexLines.append("\\end{enumerate}")

        latexStr = "\n".join(latexLines)
        return [question.Description, latexStr]


    @staticmethod
    def tester():
        examples = [example1, example2]
        expected = ['eqHandler1', 'eqHandler2']

        for i, example in enumerate(examples, 1):
            testHandlerObject = EssayQuestionHandler(example)
            handler = testHandlerObject.identify_handler()
            handler_name = handler.__name__ if handler else None
            result_obj = handler() if handler else None

            print(f"Example {i}: Using {handler_name}")
            if handler_name == expected[i - 1]:
                print("✓ Correct")
            else:
                print(f"✗ Expected {expected[i - 1]}")
