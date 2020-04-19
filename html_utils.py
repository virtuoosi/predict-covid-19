import tempfile
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = "templates"

def extract_plotly_figure_div(figure):
    full_html = figure.to_html(include_plotlyjs='cdn')
    html_lines = full_html.split("\n")
    # TODO: this solution may not work for all plotly output types,
    # keep an eye on it.
    div_lines = html_lines[7:len(html_lines) - 3]
    return "\n".join(div_lines)
    


def render_index_html(**kwargs):
    template_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = template_env.get_template("index.html")
    return template.render(**kwargs)