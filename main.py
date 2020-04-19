import logging
import argparse
import datetime

import thl_api
import graphs
import html_utils


logger = logging.getLogger(__name__)

def __init_argparse():
    parser = argparse.ArgumentParser(description="Collect COVID-19 data from the THL API and create graphs & predictions.")
    parser.add_argument("OUTPUT_HTML", help="Output html filename.")
    return parser

if __name__ == "__main__":
    args =__init_argparse().parse_args()
    
    dates, cases = thl_api.total_cases_by_date()
    
    total_cases_fig = graphs.total_cases_graph(dates, cases)
    cumulative_total_cases_fig = graphs.cumulative_total_cases_graph(dates, cases)

    total_cases_div = html_utils.extract_plotly_figure_div(total_cases_fig)
    cumulative_total_cases_div = html_utils.extract_plotly_figure_div(cumulative_total_cases_fig)
    
    cases_by_hdc = thl_api.cases_by_hdc()
    cases_by_hdc_fig = graphs.cases_by_hdc_graph(cases_by_hdc)
    cases_by_hdc_div = html_utils.extract_plotly_figure_div(cases_by_hdc_fig)

    cases_by_hdc_stack_fig = graphs.cases_by_hdc_stack_graph(cases_by_hdc)
    cases_by_hdc_stack_div = html_utils.extract_plotly_figure_div(cases_by_hdc_stack_fig)

    cases_by_age_group = thl_api.total_cases_by_age_group()
    cases_by_age_group_fig = graphs.total_cases_by_age_group_bars(cases_by_age_group)
    cases_by_age_group_div = html_utils.extract_plotly_figure_div(cases_by_age_group_fig)

    dates, tests = thl_api.total_tests_by_date()

    total_tests_fig = graphs.total_tests_graph(dates, tests)
    total_tests_div = html_utils.extract_plotly_figure_div(total_tests_fig)

    cumulative_total_tests_fig = graphs.cumulative_total_tests_graph(dates, tests)
    cumulative_total_tests_div = html_utils.extract_plotly_figure_div(cumulative_total_tests_fig)
    
    with open(args.OUTPUT_HTML, 'w') as out_file:
        out_file.write(html_utils.render_index_html(
            updated=datetime.datetime.now().isoformat(),
            total_cases_div=total_cases_div,
            cumulative_total_cases_div=cumulative_total_cases_div,
            cases_by_hdc_div=cases_by_hdc_div,
            cases_by_hdc_stack_div=cases_by_hdc_stack_div,
            cases_by_age_group_div=cases_by_age_group_div,
            total_tests_div=total_tests_div,
            cumulative_total_tests_div=cumulative_total_tests_div))