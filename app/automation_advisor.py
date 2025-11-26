import re
import os

class AutomationAdvisor:
    """
    Formats the raw analysis from Gemini into a readable report and extracts artifacts.
    """

    def __init__(self, output_dir="."):
        self.output_dir = output_dir

    def generate_report(self, raw_text, report_filename="relatorio_processo.md"):
        """
        Saves the raw markdown report and extracts Mermaid diagrams.
        """
        report_path = os.path.join(self.output_dir, report_filename)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(raw_text)
        
        print(f"Report saved to {report_path}")
        
        self._extract_mermaid(raw_text)

    def _extract_mermaid(self, text):
        """
        Finds Mermaid code blocks and saves them to .mmd files.
        """
        pattern = r"```mermaid\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        
        for i, match in enumerate(matches):
            filename = os.path.join(self.output_dir, f"process_flow_{i+1}.mmd")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(match.strip())
            print(f"Mermaid diagram saved to {filename}")

if __name__ == "__main__":
    # Test the advisor
    dummy_text = """
    Here is the process analysis.
    
    ```mermaid
    graph TD;
        A-->B;
        B-->C;
    ```
    
    End of report.
    """
    advisor = AutomationAdvisor()
    advisor.generate_report(dummy_text)
