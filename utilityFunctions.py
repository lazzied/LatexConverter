def escape_latex(text):
    def replace(match):
        s = match.group(0)
        if s.startswith('$') or s.startswith('\\(') or s.startswith('\\['):
            return s  # Don't escape inside math
        # Escape in normal text
        s = s.replace("\\", r"\\")
        s = s.replace("#", r"\#")
        s = s.replace("%", r"\%")
        s = s.replace("_", r"\_")
        s = s.replace("^", r"\^{}")
        s = s.replace("&", r"\&")
        s = s.replace("{", r"\{")
        s = s.replace("}", r"\}")
        return s
    
