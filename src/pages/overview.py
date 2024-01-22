import dash
from dash import html, dcc

from apps import header, thesis


app_name = "Overview"

dash.register_page(__name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)

layout = html.Div(id=app_name, className="container container-lg layout", children=[
    
    thesis.thesis,
    
    header.navigation,
    
    html.H1("Le Global Terrorism Index (GTI)"),
    
    html.Div(className="preambule mt-3", children=[
        dcc.Markdown(
            """
            Le Global Terrorism Index (GTI) est établi par L’Institute for Economics and Peace (IEP). L’Institute for Economics and Peace est un grand groupe international qui développe des indices afin d’évaluer et de mesurer la paix et la violence dans le monde. Dans cet objectif, depuis trois ans, il se concentre sur l’impact du terrorisme et a développé le GTI qui permet de quantifier le risque terroriste. Il s’agit d’un indice annuel pour chaque pays se présentant sous la forme d’une note allant de 0 pour les pays les moins affectés par le terrorisme, à 10 pour les pays les plus touchés. En 2015, le GTI a été évalué dans 162 pays à partir de la plus grande base de données recensant les actes terroristes : la GTD (présentée dans le chapitre 2). Les variables utilisées pour le calcul sont les suivantes :– Nombre total d’attaques sur l’année– Nombre de morts (nkill)

            """,
                                    
            className="preambule_text",
        )
    ]),
    
])

