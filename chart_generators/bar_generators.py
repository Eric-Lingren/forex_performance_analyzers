import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from operator import itemgetter
from chart_generators.utilities import convert_chart_figure_to_jpeg

class BarGenerators():

    def generate_bar_chart(self, chart_params):
        data, title, x, y, labels, showlegend, width, colorseperator, barmode = itemgetter('data', 'title', 'x', 'y', 'labels', 'showlegend', 'width', 'colorseperator', 'barmode')(chart_params)
        bar_fig = px.bar(
            data, 
            title=title,
            x=x, 
            y=y, 
            text_auto=True,
            labels=labels, 
            color=colorseperator,
            barmode=barmode
        )
        bar_fig.update_layout(barmode='relative')
        bar_fig.update_layout(showlegend=showlegend)
        bar_chart_jpeg = convert_chart_figure_to_jpeg(bar_fig, width)
        return bar_chart_jpeg


    def generate_custom_multibar_chart(self, chart_params):
        data, title, x, y, y2, y3, labels, showlegend, width, colorseperator, barmode = itemgetter('data', 'title', 'x', 'y', 'y2', 'y3', 'labels', 'showlegend', 'width', 'colorseperator', 'barmode')(chart_params)
        
        fig = go.Figure(
            data=[
                go.Bar(
                    name="Total Trades",
                    x=x,
                    y=y,
                    offsetgroup=0,
                    text = y
                ),
                go.Bar(
                    name="Trades > 1 SD",
                    x=x,
                    y=y2,
                    offsetgroup=1,
                    text = y2
                ),
                go.Bar(
                    name="Trades > Mean",
                    x=x,
                    y=y3,
                    offsetgroup=2,
                    text = y3
                )
            ],
            layout=go.Layout(
                title=title,
                yaxis_title="Trade Count"
            )
        )

        bar_chart_jpeg = convert_chart_figure_to_jpeg(fig, width)
        return bar_chart_jpeg