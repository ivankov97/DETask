from dash import Dash, html, dash_table, Output, Input
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql://clarkkent:superman@localhost:5432/countriesdb")
query = "SELECT * FROM countries"
df = pd.read_sql(query, engine)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Countries and Flags"),

    dash_table.DataTable(
        id='country-table',
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns if i != 'flag_url'],
        style_table={'height': '400px', 'overflowY': 'scroll'},
        style_cell={'textAlign': 'left'},
        row_selectable='single',
        sort_action = 'native'
    ),

    html.Br(),

    html.Div(id='flag-display')
])

@app.callback(
    Output('flag-display', 'children'),
    Input('country-table', 'selected_rows')
)
def show_flag(selected_rows):
    if selected_rows:
        selected = df.iloc[selected_rows[0]]
        return html.Div([
            html.H3(f"Flag of {selected['name']}"),
            html.Img(src=selected['flag_url'], height='100px')
        ])
    return html.Div("Select a row to see the flag.")

if __name__ == '__main__':
    app.run(debug=True)
