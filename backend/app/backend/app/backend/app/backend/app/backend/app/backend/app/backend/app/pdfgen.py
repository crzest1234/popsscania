from jinja2 import Template
import pdfkit
import os

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; }
    .header { display:flex; justify-content:space-between; align-items:center; }
    .photos img{ max-width:200px; margin:5px; }
    .section { margin-top:20px; }
    table { width:100%; border-collapse: collapse; }
    th,td{ border:1px solid #ddd; padding:8px; text-align:left;}
  </style>
</head>
<body>
  <div class="header">
    <h1>PropScan AI — Rapport</h1>
    <div>{{analysis.created_at}}</div>
  </div>
  <h2>Source</h2>
  <p>{{analysis.source_url}}</p>

  <div class="section">
    <h3>Défauts détectés</h3>
    <ul>
    {% for k,v in ml.defects.items() %}
      <li><strong>{{k}}:</strong> {{v}}</li>
    {% endfor %}
    </ul>
    <p>Score global : {{ml.global_state_score}}</p>
  </div>

  <div class="section">
    <h3>Estimation travaux</h3>
    <p>Fourchette : {{estimated.min}} € — {{estimated.max}} €</p>
  </div>

  <div class="section">
    <h3>Rentabilité</h3>
    <table><tr><th>Loyer estimé</th><th>Gross yield</th><th>Net yield</th></tr>
    <tr><td>{{rent.estimated_rent}} €</td><td>{{rent.gross_yield}}%</td><td>{{rent.net_yield}}%</td></tr></table>
  </div>
</body>
</html>
"""

def generate_pdf(analysis: dict, ml: dict, estimated: dict, rent: dict, out_path: str):
    tpl = Template(HTML_TEMPLATE)
    html = tpl.render(analysis=analysis, ml=ml, estimated=estimated, rent=rent)
    # pdfkit requires wkhtmltopdf on host or a docker image that contains it
    options = {"enable-local-file-access": None}
    pdfkit.from_string(html, out_path, options=options)
    return out_path
