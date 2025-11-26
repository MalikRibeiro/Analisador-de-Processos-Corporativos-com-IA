import os
import re
import markdown
from datetime import datetime

class AutomationAdvisor:
    """
    Generates professional HTML reports from Gemini analysis.
    """

    def __init__(self, output_dir="."):
        self.output_dir = output_dir

    def generate_report(self, raw_text, report_filename=None):
        """
        Converts the raw markdown analysis into a styled HTML report.
        """
        if not report_filename:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            report_filename = f"Relatorio_Processo_{timestamp}.html"
        
        report_path = os.path.join(self.output_dir, report_filename)
        
        # Extract Mermaid code blocks
        mermaid_blocks = []
        def replace_mermaid(match):
            code = match.group(1)
            mermaid_blocks.append(code)
            return f'<div class="mermaid">\n{code}\n</div>'
        
        # Regex to find mermaid blocks: ```mermaid ... ```
        processed_text = re.sub(r'```mermaid\n(.*?)```', replace_mermaid, raw_text, flags=re.DOTALL)
        
        # Convert Markdown to HTML
        html_content = markdown.markdown(processed_text, extensions=['fenced_code', 'tables'])
        
        # Create full HTML document
        full_html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Análise de Processo</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max_width: 900px;
            margin: 0 auto;
            background: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        h1 {{
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 4px;
            font-family: 'Courier New', Courier, monospace;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        .mermaid {{
            text-align: center;
            margin: 20px 0;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            font-size: 0.9em;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Relatório de Análise de Processo</h1>
        <p><strong>Data da Análise:</strong> {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
        <hr>
        
        {html_content}
        
        <div class="footer">
            <p>Gerado por Corporate Process Analyzer AI</p>
        </div>
    </div>

    <!-- Mermaid JS Integration -->
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true }});
    </script>
</body>
</html>
"""
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        
        print(f"Report saved to {report_path}")
        return report_path

if __name__ == "__main__":
    # Test
    advisor = AutomationAdvisor()
    advisor.generate_report("# Teste\nIsso é um teste.\n```mermaid\ngraph TD;A-->B;```")
