import os
import re
import markdown
import html
from datetime import datetime

class ReportService:
    """
    Generates professional HTML reports from Gemini analysis.
    """

    def __init__(self, output_dir="."):
        self.output_dir = output_dir

    def generate_report(self, raw_text, report_filename=None):
        """
        Converts the raw markdown analysis into a styled HTML report.
        Parses JSON flowchart steps and renders them as HTML.
        """
        if not report_filename:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            report_filename = f"Relatorio_Processo_{timestamp}.html"
        
        report_path = os.path.join(self.output_dir, report_filename)
        
        # 1. Extract JSON Flowchart
        flowchart_html = ""
        json_match = re.search(r'### FLOWCHART_JSON\s*(\[.*?\])', raw_text, re.DOTALL)
        
        if json_match:
            try:
                import json
                json_str = json_match.group(1).strip()
                steps = json.loads(json_str)
                flowchart_html = self._generate_flowchart_html(steps)
                # Remove the JSON block from the text to be rendered
                raw_text = raw_text.replace(json_match.group(0), "")
            except Exception as e:
                print(f"Error parsing flowchart JSON: {e}")
                flowchart_html = f"<div class='error'>Erro ao gerar fluxograma: {e}</div>"
        
        # 2. Convert Markdown to HTML
        html_content = markdown.markdown(raw_text, extensions=['fenced_code', 'tables'])
        
        # Insert Flowchart (heuristic: put it before "Sugestões" or at the end)
        # CORREÇÃO: A lógica de inserção estava quebrada. Aqui inserimos o fluxo no HTML processado.
        if flowchart_html:
            if "Sugestões" in html_content:
                # Tenta inserir antes do título "Sugestões" (assumindo que o markdown gerou um <h2> ou similar, ajustamos apenas a string)
                html_content = html_content.replace("Sugestões", f"{flowchart_html}\n<h2>Sugestões", 1)
            else:
                html_content += flowchart_html

        # CORREÇÃO PRINCIPAL: O HTML precisa ser atribuído à variável 'full_html' usando f-string (f""")
        full_html = f"""<!DOCTYPE html>
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
            max-width: 900px;
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
        /* Flowchart Styles */
        .flowchart-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 30px 0;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
        }}
        .flow-step {{
            background-color: #fff;
            border: 2px solid #3498db;
            border-radius: 8px;
            padding: 15px 25px;
            margin: 10px 0;
            text-align: center;
            font-weight: 500;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            max-width: 80%;
            position: relative;
        }}
        .flow-step.decision {{
            border-color: #e67e22;
            border-radius: 20px;
        }}
        .flow-arrow {{
            font-size: 24px;
            color: #7f8c8d;
            margin: -5px 0;
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
</body>
</html>
"""
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        
        print(f"Report saved to {report_path}")
        return report_path

    def _generate_flowchart_html(self, steps):
        """Generates HTML for the flowchart from steps list."""
        html_output = '<div class="flowchart-container">\n<h3>Fluxo do Processo</h3>\n'
        
        # Create a map for easy lookup if needed, though simple list iteration is usually enough for linear
        # For complex branching, we might need a graph lib, but for this "fast" version, we'll assume a linear-ish sequence
        # or just render them in order of the list.
        
        for i, step in enumerate(steps):
            step_type = step.get("type", "process")
            label = step.get("label", "")
            
            css_class = "flow-step"
            if step_type == "decision":
                css_class += " decision"
            
            html_output += f'<div class="{css_class}">{html.escape(label)}</div>\n'
            
            # Add arrow if not the last step
            if i < len(steps) - 1:
                html_output += '<div class="flow-arrow">↓</div>\n'
                
        html_output += '</div>'
        return html_output