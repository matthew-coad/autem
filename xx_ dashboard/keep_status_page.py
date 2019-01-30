

# updates battle status based on dropdowns values

# Rating Status
def rating_status(df):
    if df.empty:
        layout = dict(annotations=[dict(text="No results found", showarrow=False)])
        return {"data": [], "layout": layout}

    # Format results
    data = [
        go.Scatter(
            x=df['generation'],
            y=df['max_rating'],
            name='max'
        ),
        go.Scatter(
            x=df['generation'],
            y=df['min_rating'],
            name='min'
        ),
        go.Scatter(
            x=df['generation'],
            y=df['mean_rating'],
            name='mean'
        )
    ]
        
    layout = go.Layout(
        xaxis=dict(showgrid=False),
        margin=dict(l=35, r=25, b=23, t=5, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return {"data": data, "layout": layout}




# Member measure plot
@app.callback(
    Output("member_kpi_plot", "figure"),
    [
        Input("simulation", "value"),
        Input("kpi", "value")
    ],
)
def update_member_kpi_plot(simulation, kpi):

    if simulation is None or kpi is None:
        layout = dict(annotations=[dict(text="No results available", showarrow=False)])
        return {"data": [], "layout": layout}

    simulation_path = config.REPOSITORY_PATH.joinpath(simulation)
    report_manager = genetic.ReportManager(simulation_path)
    df = report_manager.read_member_report()

    # Format results
    data = [
        go.Scatter(
            x=df['generation_prop'],
            y=df[kpi],
            mode='markers',
            name=kpi
        ),
    ]
        
    layout = go.Layout(
        xaxis=dict(showgrid=False),
        margin=dict(l=35, r=25, b=23, t=5, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return {"data": data, "layout": layout}
