import dash_leaflet as dl
from dash import Dash, html, Output, Input
from dash_extensions.javascript import assign
import simplekml
from flask import Flask, send_from_directory
import os 
import dash_bootstrap_components as dbc



# How to render geojson.
point_to_layer = assign("""function(feature, latlng, context){
    const p = feature.properties;
    if(p.type === 'circlemarker'){return L.circleMarker(latlng, radius=p._radius)}
    if(p.type === 'circle'){return L.circle(latlng, radius=p._mRadius)}
    return L.marker(latlng);
}""")


# Create example app.
app = Dash(external_stylesheets=[dbc.themes.SUPERHERO])
server = app.server

app.layout = html.Div([
    # Setup a map with the edit control.
    dbc.Container([ 
    dbc.Row(
            [
            html.H1("Bounding Box Tool")
            ], justify="center", align="center"
            ),
    dbc.Row(dl.Map(center=[56, 10], zoom=4, children=[
        dl.TileLayer(), dl.FeatureGroup([
            dl.EditControl(id="edit_control")]),
    ]), justify="center", align="center", style={'width': '50%', 'height': '50vh', 'margin': "auto", "display": "inline-block"}, id="map"),
    # Setup another map to that mirrors the edit control geometries using the GeoJSON component.
    
    dbc.Row(html.Div([
        "Bounding Box: ",
        html.Div(id='my-output')
    ])),
    dbc.Row(html.Div([
        "Polygon: ",
        html.Div(id='my-output2')
    ])),
    #dbc.Row(html.Div([html.Button("Download", id="btn"), Download(id="download")]))
])])



@app.callback(Output(component_id='my-output', component_property='children'), Input("edit_control", "geojson"))
def update_bbox(x):
    if not x:
        return 'No Rectangle Created'
    else:
        for val in x['features']:
            if val['type'] == 'Feature' and val['properties']['type'] == 'rectangle':
                return str([val['properties']['_bounds'][0]['lat'], val['properties']['_bounds'][0]['lng'], val['properties']['_bounds'][1]['lat'], val['properties']['_bounds'][1]['lng']])
        
    
@app.callback(Output(component_id='my-output2', component_property='children'), Input("edit_control", "geojson"))
def update_polygon(x):
    if not x:
        return 'No Rectangle Created'
    else:
        for val in x['features']:
            if val['type'] == 'Feature' and val['properties']['type'] == 'rectangle':
                return str(val['geometry']['coordinates'])


if __name__ == '__main__':
    app.run_server()