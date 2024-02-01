import dash
from dash import html, dcc


app_name = "about"

dash.register_page(__name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)

layout = html.Div(id=app_name, className="container-fluid container-md", children=[
        
    html.H1(className="mb-5 fw-bold display-2 fw-bold", children=[
        html.Span("About ",),
        html.Span("Analytics", className="fw-bold"),
        html.Span("Paper", className="fw-bold", style={"color": "red"}),
    ]),
    
    
    html.Div(className="row", children=[
        html.Div(className="col-lg-8", children=[
            
            html.Div(className="app_name", children=[
                html.H4("Description Générale:", className="mb-3 fw-bold"),
                dcc.Markdown(
                    """ 
                    L'Application M3-Analytics (Mathmatics Model and Machine-Learning Analytics) est un outil puissant conçu pour vous aider à tirer le meilleur parti de vos données financières. Que vous gériez une entreprise, un département financier ou que vous cherchiez simplement à comprendre les tendances financières, notre application offre les fonctionnalités et les informations dont vous avez besoin.
                    """
                )
            ]),
            
            
            html.Div(className="mt-4", children=[
                html.H4("Utilité:", className="mb-3 fw-bold"),
                dcc.Markdown(
                    """ 
                    Notre application simplifie le processus d'analyse de données financières complexes en vous offrant une interface conviviale pour explorer, visualiser et tirer des conclusions à partir de vos données de commandes et de livraisons. Elle vous permet de prendre des décisions éclairées pour améliorer l'efficacité opérationnelle, optimiser les coûts et identifier des opportunités.
                    """
                )
            ]),
            
            
            html.Div(className="mt-4", children=[
                html.H4("Fonctionnalités Clés:", className="mb-3 fw-bold"),
                dcc.Markdown(
                    """ 
                    * Visualisation avancée des données financières.
                    
                    * Génération de rapports personnalisés.
                    
                    * Exploration approfondie des données pour identifier des tendances et des anomalies.
                    
                    * Suivi de la performance financière au fil du temps.
                    
                    * Prise en charge de diverses sources de données.
                    """
                )
            ]),
            
            
            html.Div(className="mt-4", children=[
                html.H4("Sources de Données:", className="mb-3 fw-bold"),
                dcc.Markdown(
                    """ 
                    L'application utilise des données de commandes et de livraisons provenant de sources fiables et actualisées. Nos algorithmes de collecte et de mise à jour garantissent que vos données sont toujours à jour et prêtes à être analysées.
                    """
                )
            ]),
            
            
            html.Div(className="mt-4", children=[
                html.H4("Contact:", className="mb-3 fw-bold"),
                dcc.Markdown(
                    """ 
                    Pour toute question, demande d'assistance ou commentaire, n'hésitez pas à nous contacter à l'adresse [chris.baudelaire77@gmail.com].
                    """
                )
            ]),
            
            
            html.Div(className="mt-4", children=[
                html.H4("Crédits et Remerciements:", className="mb-3 fw-bold"),
                dcc.Markdown(
                    """ 
                    Nous tenons à remercier toutes les personnes et organisations qui ont contribué à rendre cette application possible, ainsi que les bibliothèques open source et les ressources que nous utilisons.
                    """
                )
            ]),
    
        ]),
        
        html.Div(className="col-lg-4", children=[
            
            html.Div(className="mt-4 text-center", children=[
                html.H4("About author:", className="mb-2 fw-bold"),
                html.Div(className="", children=[
                    html.Img(
                        src=dash.get_asset_url('cccb-6.png'),
                        className="div-img img-responsive rounded-circle mb-2",
                        style={
                            "height": "170px", 
                            "width": "180px",
                        }
                    ),
                ]),
                dcc.Markdown(
                    """ 
                    Cette application a été développée par [Votre Nom], un expert en analyse de données financières avec plus de [X années] d'expérience dans le domaine. [Votre Nom] est passionné par l'utilisation de la technologie pour faciliter la prise de décision basée sur les données et a travaillé dur pour créer une application qui répond à vos besoins

                    Cette application a été développée par [Votre Nom], un expert en analyse de données financières avec plus de [X années] d'expérience dans le domaine. [Votre Nom] est passionné par l'utilisation de la technologie pour faciliter la prise de décision basée sur les données et a travaillé dur pour créer une application qui répond à vos besoins
                    
                    
                    #### Autre tableaux de bord:
                    
                    ###### [Catastrophes naturelles: Analyse de données]
                    ###### [Terrorism data application]
                    ###### [Covid Tracker]
                    ###### [Réchauffement climatique]
                    ###### [Dashboard analytique] 
                    ###### [Daily Transactions Dataset](https://www.kaggle.com/datasets/prasad22/daily-transactions-dataset) 
                    ###### [Tornados: 1950 - 2022](https://www.kaggle.com/code/mikedelong/investigate-tornado-datas-with-scatter-maps)
                    
                    """
                )
            ]),   

            
        ]),
    ])
    
])

