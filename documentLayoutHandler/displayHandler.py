import re
from classes.myClasses import Table, Image
from typing import List, Dict, Union

class HtmlTweaker:
    """
    Processes HTML files to identify div elements containing images or tables,
    and converts them to LaTeX format.
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.elements: Dict[str, Union[Image, Table]] = {}
    
    def identify_elements(self) -> None:
        """
        Parse the HTML file and identify div elements containing images or tables.
        Stores the identified elements in self.elements.
        """
        content = self._read_file()
        div_elements = re.findall(r'<div[^>]*>.*?</div>', content, re.DOTALL)
        
        for div_element in div_elements:
            element = self._parse_div_element(div_element)
            if element:
                self.elements[div_element] = element
    
    def _parse_div_element(self, div_text: str) -> Union[Image, Table, None]:
        """
        Parse a single div element and return the appropriate object.
        
        Args:
            div_text: The HTML text of the div element
            
        Returns:
            Image, Table, or None if the div doesn't contain a supported element
        """
        if re.search(r'<img[^>]*>', div_text):
            return self._extract_image(div_text)
        elif re.search(r'<table[^>]*>', div_text):
            return self._extract_table(div_text)
        return None
    
    def _extract_image(self, div_text: str) -> Union[Image, None]:
        """Extract image information from a div element."""
        match = re.search(r'<img[^>]*src="([^"]*)"', div_text)
        if match:
            return Image(src=match.group(1), div_text=div_text)
        return None
    
    def _extract_table(self, div_text: str) -> Union[Table, None]:
        """Extract table information from a div element."""
        rows = re.findall(r'<tr>(.*?)</tr>', div_text, re.DOTALL)
        table_cells = [re.findall(r'<td>(.*?)</td>', row, re.DOTALL) for row in rows]
        
        num_rows = len(table_cells)
        num_cols = len(table_cells[0]) if num_rows > 0 else 0
        
        if num_rows > 0 and num_cols > 0:
            return Table(
                num_rows=num_rows,
                num_cols=num_cols,
                cells=table_cells,
                div_text=div_text
            )
        return None
    
    def convert_to_latex(self) -> None:
        """
        Replace all identified HTML elements with their LaTeX equivalents
        and write the result back to the file.
        """
        content = self._read_file()
        
        for element in self.elements.values():
            latex_code = element.to_latex()
            content = content.replace(element.div_text, latex_code)
        
        self._write_file(content)
    
    def _read_file(self) -> str:
        """Read the HTML file content."""
        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.read()
    
    def _write_file(self, content: str) -> None:
        """Write content back to the HTML file."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(content)
    
    def process(self) -> None:
        """
        Main processing method. Identifies elements and converts them to LaTeX.
        """
        self.identify_elements()
        self.convert_to_latex()