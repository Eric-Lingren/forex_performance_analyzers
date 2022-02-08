import plotly.express as px
from operator import itemgetter
from chart_generators.utilities import convert_chart_figure_to_jpeg

class BarGenerators():

    def generate_bar_chart(self, chart_params):
        data, title, x, y, labels, showlegend, width, colorseperator = itemgetter('data', 'title', 'x', 'y', 'labels', 'showlegend', 'width', 'colorseperator')(chart_params)
        bar_fig = px.bar(
            data, 
            title=title,
            x=x, 
            y=y, 
            text_auto=True,
            labels=labels, 
            color=colorseperator
        )
        bar_fig.update_layout(barmode='relative')
        bar_fig.update_layout(showlegend=showlegend)
        bar_chart_jpeg = convert_chart_figure_to_jpeg(bar_fig, width)
        return bar_chart_jpeg