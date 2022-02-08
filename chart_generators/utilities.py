from base64 import b64encode

def convert_chart_figure_to_jpeg(figure, width):
    figure_bytes = figure.to_image(format="jpeg", width=width)
    figure_jpeg = b64encode(figure_bytes).decode("utf-8")
    return figure_jpeg