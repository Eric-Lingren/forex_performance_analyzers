from operator import itemgetter
import plotly.express as px
from chart_generators.utilities import convert_chart_figure_to_jpeg


class ScatterGenerators():

    def generate_scatter_plot(self, chart_params):
        data, title, x, y, width, colorseperator, showlegend = itemgetter('data', 'title', 'x', 'y', 'width', 'colorseperator', 'showlegend')(chart_params)
        scatter_plot_fig = px.scatter(
            data, 
            title=title,
            x=x, 
            y=y, 
            color=colorseperator,
        )
        scatter_plot_fig.update_layout(showlegend=showlegend)
        scatter_plot_jpeg = convert_chart_figure_to_jpeg(scatter_plot_fig, width)
        return scatter_plot_jpeg
