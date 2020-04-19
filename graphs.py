import plotly.graph_objects as go
import numpy as np


GRAPH_LAYOUT = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(211,233,247,0.5)',
    margin = { 't': 40, 'b': 0 },
    xaxis = { 
        'tickformat': '%Y-%m-%d'
    }
)


def total_cases_graph(dates, cases):
    fig = go.Figure(layout=GRAPH_LAYOUT)
    fig.add_trace(go.Scatter(x=dates, y=cases, mode='lines+markers', name='New cases'))
    return fig

def total_tests_graph(dates, tests):
    fig = go.Figure(layout=GRAPH_LAYOUT)
    fig.add_trace(go.Scatter(x=dates, y=tests, mode='lines+markers', name='Tests'))
    return fig

def cumulative_total_cases_graph(dates, cases):
    fig = go.Figure(layout=GRAPH_LAYOUT)
    cumulative_cases = np.cumsum(cases)
    fig.add_trace(go.Scatter(x=dates, y=cumulative_cases, mode='lines', name='Cumulative cases'))
    return fig

def cases_by_hdc_graph(data):
    fig = go.Figure(layout=GRAPH_LAYOUT)
    
    for (hdc, xy) in data.items():
        fig.add_trace(go.Scatter(x=xy[0], y=xy[1], mode='lines', name=hdc, stackgroup='hdcs'))
    
    return fig

def cases_by_hdc_stack_graph(data):
    fig = go.Figure(layout=GRAPH_LAYOUT)
    
    for (hdc, xy) in data.items():
        cumulative_cases = np.cumsum(xy[1])
        fig.add_trace(go.Scatter(x=xy[0], y=cumulative_cases, mode='lines', name=hdc, stackgroup='hdcs'))
    
    return fig

def total_cases_by_age_group_bars(data):
    fig = go.Figure(layout=GRAPH_LAYOUT)
    grps_arr = np.array(list(map(lambda group: " → ".join(group.split("-")), data.keys())))
    vals_arr = np.array(list(data.values()))
    fig.add_trace(go.Bar(x=grps_arr, y=vals_arr, name="Age groups"))
    return fig

def cumulative_total_tests_graph(dates, tests):
    fig = go.Figure(layout=GRAPH_LAYOUT)
    cumulative_tests = np.cumsum(tests)
    fig.add_trace(go.Scatter(x=dates, y=cumulative_tests, mode='lines', name='Cumulative tests'))
    return fig