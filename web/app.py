import os
from flask import Flask, request, render_template_string
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database import get_engine


from queries import (
    q1_revenue_recurrent_customers,
    q2_margin_variance_products,
    q3_market_basket,
    q4_cohort_analysis
)

engine = get_engine()

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<title> AdventureWorks</title>

<style>

body {
    font-family: Arial, sans-serif;
    margin: 30px;
    background: #f4f6f8;
}

h1 {
    color: #2c3e50;
}

.card {
    background: white;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

button {
    padding: 8px 16px;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background: #2980b9;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin-top: 15px;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
}

th {
    background: #f2f2f2;
}

tr:nth-child(even) {
    background: #fafafa;
}

.empty {
    color: #777;
    margin-top: 10px;
}

</style>

</head>

<body>

<h1>Análisis AdventureWorks</h1>


<div class="card">
<h2>Q1 – Revenue (Clientes frecuentes VS Clientes no frecuentes)</h2>

<form>
<input type="hidden" name="view" value="q1"/>
<button type="submit">Run Query</button>
</form>
</div>


<div class="card">
<h2>Q2 – Productos con mayor margen de varianza</h2>

<form>
<input type="hidden" name="view" value="q2"/>
<button type="submit">Run Query</button>
</form>
</div>


<div class="card">
<h2>Q3 – 10 parejas de productos que tienen mayor ocurrencia de comprarse juntos.</h2>

<form>
<input type="hidden" name="view" value="q3"/>
<button type="submit">Run Query</button>
</form>
</div>


<div class="card">
<h2>Q4 – Análisis cohortes</h2>

<form>
<input type="hidden" name="view" value="q4"/>
<button type="submit">Run Query</button>
</form>
</div>


{% if rows %}

<div class="card">

<table>

<thead>
<tr>
{% for col in columns %}
<th>{{ col }}</th>
{% endfor %}
</tr>
</thead>

<tbody>
{% for r in rows %}
<tr>
{% for c in r %}
<td>{{ c }}</td>
{% endfor %}
</tr>
{% endfor %}
</tbody>

</table>

</div>

{% elif rows is not none %}

<p class="empty">No results returned.</p>

{% endif %}

</body>
</html>
"""

QUERY_MAP = {
    "q1": q1_revenue_recurrent_customers,
    "q2": q2_margin_variance_products,
    "q3": q3_market_basket,
    "q4": q4_cohort_analysis,
}


@app.route("/")
def index():

    view = request.args.get("view")

    rows = []
    columns = []

    if view in QUERY_MAP:
        with Session(engine) as session:

            stmt = QUERY_MAP[view]()   # obtener statement

            result = session.execute(stmt)

            columns = result.keys()
            rows = result.fetchall()

    return render_template_string(
        HTML,
        rows=rows,
        columns=columns
    )

if __name__ == "__main__":
    app.run(debug=True)