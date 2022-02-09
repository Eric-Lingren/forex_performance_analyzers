from operator import itemgetter
import plotly.express as px
from chart_generators.utilities import convert_chart_figure_to_jpeg


class ContourGenerator():

    def generate_density_contour(self, chart_params):
        data, x, y, width = itemgetter('data', 'x', 'y', 'width')(chart_params)
        density_contour_fig = px.density_contour(
            data,     
            x=x, 
            y=y
        )
        density_contour_fig.update_traces(contours_coloring="fill", contours_showlabels = True)
        density_contour_jpeg = convert_chart_figure_to_jpeg(density_contour_fig, width)
        return density_contour_jpeg