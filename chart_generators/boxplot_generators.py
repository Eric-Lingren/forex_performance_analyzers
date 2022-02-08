import plotly.express as px

from operator import itemgetter
from chart_generators.utilities import convert_chart_figure_to_jpeg

class BoxplotGenerators():

    def generate_boxplot_chart(self, chart_params):
        data, title, x, y, labels, showlegend, width, colorseperator = itemgetter('data', 'title', 'x', 'y', 'labels', 'showlegend', 'width', 'colorseperator')(chart_params)
        boxplot_fig = px.box(
            data, 
            title=title,
            x=x, 
            y=y, 
            labels=labels, 
            color=colorseperator
        )
        boxplot_fig.update_layout(barmode='relative')
        boxplot_fig.update_layout(showlegend=showlegend)
        bar_chart_jpeg = convert_chart_figure_to_jpeg(boxplot_fig, width)
        return bar_chart_jpeg