import plotly.express as px


def format_line_figure(fig):
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        legend_title_text='',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.0,
            xanchor="center",
            x=0.5
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        font=dict(color='#FDFBF9')
    )
    fig.update_xaxes(
        tickangle=45,
        tickmode='array',
        # showgrid=False
    )
    fig.update_traces(patch={"line": {"color": "#FDFBF9", "width": 2, "dash": 'dot'}}, selector={
                      "legendgroup": "Neutral"})
    fig = figure_color(fig)

    return fig


def figure_color(fig):
    fig.update_layout(
        paper_bgcolor='#404040',
        plot_bgcolor='#404040',
        font=dict(color='#FDFBF9')
    )
    return fig


def multi_line_plot(name, data, intersections):
    """Expects Dataset object"""
    fig = px.line(data, x=data.index, y=data.columns[:3])
    for date, row in intersections.iterrows():
        if row['decision'] == 'sell':
            line_color = "red"
        elif row['decision'] == 'buy':
            line_color = "green"

        fig.add_vline(x=date, line_width=3, line_dash="dash",
                      line_color=line_color)

    fig.update_layout(
        title=f"{name} Chart",
    )

    fig = format_line_figure(fig)

    return fig
