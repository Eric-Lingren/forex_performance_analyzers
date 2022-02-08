from operator import itemgetter
import plotly.graph_objects as go
import plotly.express as px
from chart_generators.utilities import convert_chart_figure_to_jpeg


class HistogramGenerators():

    def generate_2d_histogram_contour(self, chart_params):
        x, y = itemgetter('x', 'y')(chart_params)
        histogram_contour_fig = go.Figure(go.Histogram2dContour(
            x=x, 
            y=y,
            colorscale = 'Jet',
            contours = dict(
                showlabels = True,
                labelfont = dict(
                    family = 'Raleway',
                    color = 'white'
                )
            ),
            hoverlabel = dict(
                bgcolor = 'white',
                bordercolor = 'black',
                font = dict(
                    family = 'Raleway',
                    color = 'black'
                )
            )
        ))
        histogram_contour_jpeg = convert_chart_figure_to_jpeg(histogram_contour_fig)
        return histogram_contour_jpeg



    def generate_histogram(self, chart_params):
        data, x, width, nbins = itemgetter('data', 'x', 'width', 'nbins')(chart_params)
        histogram_fig = px.histogram(
            data, 
            x=x, 
            nbins=nbins
        )
        histogram_jpeg = convert_chart_figure_to_jpeg(histogram_fig, width)
        return histogram_jpeg