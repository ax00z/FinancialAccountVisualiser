import tkinter
import pandas as panda
import numpy as np
import dash
import webbrowser
from dash import dcc
from dash import html
import plotly.express as express
from tkinter.filedialog import askopenfilename
from threading import Timer
import csv

root = tkinter.Tk()
root.withdraw()

#files = filedialog.askopenfilename()
#data = panda.read_csv(files)
data = panda.read_csv('csv49071.csv')


data['Categories'] = np.where(data['Description 1' or 'Description 2'].str.contains(
    '', case=False), 'Takeout', "")

data['Categories'] += np.where(data['Description 1' or 'Description 2'].str.contains(
    '', case=False), 'Grocery', "")

data['Categories'] += np.where(data['Description 1' or 'Description 2'].str.contains(
    '', case=False), 'Education', "")

data['Categories'] += np.where(data['Description 1' or 'Description 2'].str.match(
    'fee|Fee|FEE', case=False), 'Debit Charges', "")

print(data.values)


Total_Monthly_Expenses_Table = data.groupby(
    'Transaction Date')['Amount'].sum().reset_index(name="sum")
Total_Monthly_Expenses_Chart = express.bar(
    Total_Monthly_Expenses_Table, x="Transaction Date", y="sum", title="Total Monthly Expenses")
Total_Monthly_Expenses_Chart.update_yaxes(
    title="Expenses ($)", visible=True, showticklabels=True)
Total_Monthly_Expenses_Chart.update_xaxes(
    title="Date", visible=True, showticklabels=True)

Expenses_Breakdown_Table = panda.pivot_table(data, values=['Amount'], index=[
                            "Categories",
                            "Transaction Date"], aggfunc=sum).reset_index()
Expenses_Breakdown_Table.columns = [x.upper()
                                    for x in Expenses_Breakdown_Table.columns]
Expenses_Breakdown_Chart = express.line(
    Expenses_Breakdown_Table, 
    x="TRANSACTION DATE", y="AMOUNT", title="Expenses Breakdown", color="CATEGORIES")
Expenses_Breakdown_Chart.update_yaxes(
    title="Expenses ($)", visible=True, showticklabels=True)
Expenses_Breakdown_Chart.update_xaxes(
    title="Date", visible=True, showticklabels=True)


app = dash.Dash()


colours = {
    "background": "#0e1c26",
    "HeadText": "#f6f6f6",
    "SubText": "#e3e3e3"
}

Total_Monthly_Expenses_Chart.update_layout(
    plot_bgcolor=colours["background"],
    paper_bgcolor=colours["background"],
    font_color=colours["SubText"]
)

Expenses_Breakdown_Chart.update_layout(
    plot_bgcolor=colours["background"],
    paper_bgcolor=colours["background"],
    font_color=colours["SubText"]
)


latest_date = Expenses_Breakdown_Table['TRANSACTION DATE'].max()
data_latest_date = Expenses_Breakdown_Table.loc[Expenses_Breakdown_Table['TRANSACTION DATE'] == latest_date]


app.layout = html.Div(style={"backgroundColor": colours["background"]}, 
                      children=[
    html.H1(str(latest_date)+" Total Monthly Expenses ",    
            style={"text-align": "c enter", "color": colours["HeadText"]}),
        dcc.Graph(figure=Total_Monthly_Expenses_Chart),
        dcc.Graph(figure=Expenses_Breakdown_Chart)         
    ])

port = 8050  # default port


def open_website():
    webbrowser.open_new("http://localhost:{}".format(port))


if __name__ == "__main__":
    Timer(1, open_website).start()
    app.run_server(debug=False, port=port, dev_tools_hot_reload=True)
