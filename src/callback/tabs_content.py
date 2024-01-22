# from dash import Input, Output, callback, html, dcc
# from graph_without_callback.graph_function import * 




# tab1_content = [
#     html.Div(className="row align-items-center", children=[
        
#         html.Div(className="col-lg-8", children=[
#             dcc.Graph(id="success-failure-attack", config=dict(displayModeBar=False))
#         ]),
        
#         html.Div(className="col-lg-4", children=[
#             dcc.Graph(config=dict(displayModeBar=False), figure=func_revolution("success"))
#         ])
        
#     ]),
    
#     html.Div(className="row mt-4", children=[
        
#         html.Div(className="col", children=[
#             dcc.Markdown(
#                 "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme.",
                                        
#                 className="preambule_text",
#             ),
    
#         ])
        
#     ]),
    
    
#     html.Div(className="row align-items-center mt-5", children=[
        
#         html.Div(className="col-lg-12", children=[
#             dcc.Graph(config=dict(displayModeBar=False), figure=func("success", 1, 32))
#         ])
#     ]),
    
    
#     html.Div(className="row align-items-center mt-5", children=[
        
#         html.Div(className="mb-4 text-center", children=[
#             html.Div(className="row justify-content-center", children=[
#                 html.Div(className="col-lg-4", children=[
#                     html.Span("Selectionner la cause", className=""),
#                     dcc.Dropdown(
#                         id="dropdown-se",
#                         options=[
#                             {"label": x, "value": y} 
#                             for x, y in zip(["Attacque terroristes réussie", "Attacque terroristes échouées"], [1, 0])
#                         ],
#                         value=1,
#                     )
#                 ])
#             ])
#         ]),
        
#         html.Div(className="col-lg-7", children=[
#             dcc.Graph(id="success-failure-map", config=dict(displayModeBar=True))
#         ]),
#         html.Div(className="col-lg-5", children=[
#             dcc.Markdown(
#                 "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives."
#             ),
#             dcc.Graph(id="success-failure-ranking", config=dict(displayModeBar=False))
#         ])
#     ]),
# ]


# tab2_content = [
#     html.Div(className="row align-items-center", children=[
        
#         html.Div(className="col-lg-8", children=[
#             dcc.Graph(id="success-failure-attack", config=dict(displayModeBar=False))
#         ]),
        
#         html.Div(className="col-lg-4", children=[
#             dcc.Graph(config=dict(displayModeBar=False), figure=func_revolution("suicide"))
#         ])
        
#     ]),
    
#     html.Div(className="row mt-4", children=[
        
#         html.Div(className="col", children=[
#             dcc.Markdown(
#                 "Bienvenue dans notre tableau de bord dédié à l'analyse des données relatives au terrorisme dans le monde. Ce tableau de bord a pour objectif de vous fournir une vue approfondie et dynamique de l'évolution des actes terroristes à travers le temps et l'espace. À travers une série de visualisations interactives et de données actualisées, nous explorerons les tendances, les régions les plus touchées, les groupes terroristes les plus actifs, et bien plus encore. Comprendre le terrorisme.",
                                        
#                 className="preambule_text",
#             ),
    
#         ])
        
#     ]),
    
#     html.Div(className="row align-items-center mt-5", children=[
        
#         html.Div(className="col-lg-6", children=[
#             dcc.Graph(config=dict(displayModeBar=False), figure=func("suicide", 1, 26))
#         ]),
        
#         html.Div(className="col-lg-6", children=[
#             dcc.Graph(config=dict(displayModeBar=False), figure=func("suicide", 0, 26))
#         ])
#     ]),
# ]

# tab3_content = ""

# tab4_content = ""

# @callback(Output("content", "children"), [Input("tabs", "active_tab")])
# def switch_tab(at):
#     if at == "tab-1":
#         return tab1_content
#     elif at == "tab-2":
#         return tab2_content
#     elif at == "tab-3":
#         return tab3_content
#     else:
#         return tab4_content
