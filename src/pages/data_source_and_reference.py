import dash
from dash import html, dcc

from apps import header, thesis


app_name = "sources-de-donnees-et-references"

dash.register_page(__name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)

layout = html.Div(id=app_name, className="container container-lg layout", children=[
    
    html.H1("Source de données"),
    
    html.Div(className="data-source mb-5", children=[
        html.A(
            "https://fr.wikipedia.org/wiki/Terrorisme#Situation_dans_l'Union_européenne", 
            href="https://fr.wikipedia.org/wiki/Terrorisme#Situation_dans_l'Union_européenne",
            className="d-block"
        ),
        
        html.A(
            "https://fr.wikipedia.org/wiki/Terrorisme#Situation_dans_l'Union_européenne", 
            href="https://fr.wikipedia.org/wiki/Terrorisme#Situation_dans_l'Union_européenne",
            className="d-block"
        ),
        
        html.A(
            "https://fr.wikipedia.org/wiki/Terrorisme#Situation_dans_l'Union_européenne", 
            href="https://fr.wikipedia.org/wiki/Terrorisme#Situation_dans_l'Union_européenne",
            className="d-block"
        ),
    ]),
    
    
     html.H1("Références"),
    
    html.Div(className="reference", children=[
        html.A(
            "https://fr.wikipedia.org/wiki/Terrorisme#Situation_dans_l'Union_européenne", 
            href="https://fr.wikipedia.org/wiki/Terrorisme#Situation_dans_l'Union_européenne",
            className="d-block"
        ),
        
        html.A(
            "https://mavenanalytics.io/project/908", 
            href="https://mavenanalytics.io/project/908",
            className="d-inline-block"
        ),
        
        html.A(
            "https://www.novypro.com/project/global-terrorism-analysis-2", 
            href="https://www.novypro.com/project/global-terrorism-analysis-2",
            className="d-block"
        ),
        
        html.A(
            "https://app.powerbi.com/view?r=eyJrIjoiNjhmMGE3ZTMtYTQ2MS00NTg0LWI4ZjgtZGJkZmEzOTQxNmY2IiwidCI6IjlmMTA3ZWExLWI5YmYtNDgxMi1hM2I5LWNjZGZlNWU0OTJlNSJ9", 
            href="https://app.powerbi.com/view?r=eyJrIjoiNjhmMGE3ZTMtYTQ2MS00NTg0LWI4ZjgtZGJkZmEzOTQxNmY2IiwidCI6IjlmMTA3ZWExLWI5YmYtNDgxMi1hM2I5LWNjZGZlNWU0OTJlNSJ9",
            className="d-block"
        ),
        
    ]),
    
])

