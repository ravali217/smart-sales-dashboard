import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import services
from db import create_tables

create_tables()

app = Dash(__name__)
server = app.server  # for deployment if needed

def build_dataframes():
    products = pd.DataFrame(services.list_products())
    report = pd.DataFrame(services.get_sales_report())
    return products, report

app.layout = html.Div([
    html.H1("📊 Smart Sales Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.H3("Profit per Salesperson"),
            dcc.Graph(id="profit-salesperson")
        ], style={"width": "48%", "display": "inline-block"}),

        html.Div([
            html.H3("Top Products (by item_total)"),
            dcc.Graph(id="top-products")
        ], style={"width": "48%", "display": "inline-block", "float": "right"})
    ]),

    html.Div([
        html.H3("Sales Transactions"),
        dcc.Graph(id="sales-table")
    ]),

    dcc.Interval(id="interval", interval=5 * 1000, n_intervals=0)  # refresh every 5s
])

@app.callback(
    [Output("profit-salesperson", "figure"),
     Output("top-products", "figure"),
     Output("sales-table", "figure")],
    [Input("interval", "n_intervals")]
)
def update_graphs(n):
    products_df, report_df = build_dataframes()

    if report_df.empty:
        fig1 = px.bar(pd.DataFrame({"Salesperson": [], "Profit": []}), x="Salesperson", y="Profit")
        fig2 = px.bar(pd.DataFrame({"Product": [], "ItemTotal": []}), x="Product", y="ItemTotal")
        fig3 = px.scatter()
        return fig1, fig2, fig3

    # Profit per Salesperson
    profit_per_sp = report_df.groupby("salesperson")["item_total"].sum().reset_index().rename(columns={"item_total": "Profit"})
    fig1 = px.bar(profit_per_sp, x="salesperson", y="Profit", text="Profit")
    fig1.update_layout(xaxis_title="Salesperson", yaxis_title="Profit")

    # Top Products
    top_products = report_df.groupby("product_name")["item_total"].sum().reset_index().sort_values("item_total", ascending=False).head(10)
    fig2 = px.bar(top_products, x="product_name", y="item_total", text="item_total")
    fig2.update_layout(xaxis_title="Product", yaxis_title="Revenue")

    # Recent Sales
    fig3 = px.scatter(report_df, x="order_date", y="item_total", hover_data=["salesperson", "product_name", "quantity", "order_id"])
    fig3.update_layout(title="Recent Sales (dot = item revenue)")

    return fig1, fig2, fig3

if __name__ == "__main__":
    app.run_server(debug=True)
