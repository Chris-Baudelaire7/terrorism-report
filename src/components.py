from dash import html, dcc, dash_table
import dash_admin_components as dac
from dash import html, dcc
import dash_mantine_components as dmc
from data_preparation import *
from graph_without_callback import *
from data_preparation import *
from utils import *


filtre = html.Div(className="row justify-content-center", children=[

    html.Div(className="col-12", children=[
        html.Span("Zone géographique", className=""),
        dcc.Dropdown(
            id="filter-geo",
            options=[{"label": "Monde", "value": "Monde"}] +

            [{"label": "Continental", "disabled": True, "value": "Monde"}] +

            [{"label": html.Span([x], style={'color': 'rgb(252,187,161)'}), "value": x, }
             for x in sorted(list(df.continent.unique()))] +

            [{"label": "Regional", "disabled": True, "value": "Monde"}] +

            [{"label": html.Span([y], style={'color': 'rgb(254,224,210'}), "value": y}
             for y in sorted(list(df.region.unique()))] +

            [{"label": "Pays les pays touches", "disabled": True, "value": "Monde"}] +

            [{"label": html.Span([z], style={'color': 'rgb(255,245,240)'}), "value": z}
             for z in sorted(countries_most_affected)],
            value="Monde",
            placeholder="Selection",
            searchable=True,
            clearable=True,
            style={"color": "white"}
        )
    ]),

    html.Div(className="col-12 mt-3", children=[
        html.Span("Métrique", className=""),
        dcc.Dropdown(
            id="cause",
            options=[
                {"label": x, "value": y}
                for x, y in zip(["Incidences", "Blessés", "Décès", "Victimes (Blessés + Décès)"], ["size", "nwound", "nkill", "casualties"])
            ],
            value="size",
            placeholder="Selection",
        )
    ]),

    html.Div(className="col-12 mt-3", children=[
        html.Span("Groupe terroriste", className="d-block"),
        dcc.Dropdown(
            id="group",
            options=[
                {"label": x, "value": x} for x in ["All group"] + sorted(terrorist_group)
            ],
            value="All group",
            placeholder="Selection",
        ),
    ]),


    html.Div(className="col-12 mt-3", children=[
        html.Span("Type d'attaque", className="d-block"),
        dcc.Dropdown(
            id="attack",
            options=[
                {"label": x, "value": x} for x in ["All attack type"] + sorted(terrorist_attack)
            ],
            value="All attack type",
        ),
    ]),

    html.Div(className="col-12 mt-3", children=[
        html.Span("Cible visées", className="d-block"),
        dcc.Dropdown(
            id="target",
            options=[
                {"label": x, "value": x} for x in ["All target"] + sorted(terrorist_targtype)
            ],
            value="All target",
        ),
    ]),

    html.Div(className="col-12 mt-3", children=[
        html.Span("Armes utilisées", className="d-block"),
        dcc.Dropdown(
            id="weapon",
            options=[
                {"label": x, "value": x} for x in ["All weapons"] + sorted(terrorist_weaptype)
            ],
            value="All weapons",
        )
    ]),

    html.Div(className="col-12 mt-3", children=[
        html.Div(className="text-enter", children=[
            html.P("Selectionner une plage d'année",
                   className="mb-3"),
        ]),

        dmc.RangeSlider(
            id="range-slider",
            min=list(df.year.unique())[0],
            max=list(df.year.unique())[-1],
            value=[1970, 2020],
            step=1, size=1.5, color="red",
            marks=[
                {"value": 1970, "label": "1970"},
                {"value": 2020, "label": "2020"},
            ],
            labelAlwaysOn=True,
            labelTransition="fade",
            style={
                            "font-family": "serif",
                            "color": "white !importtant",
            }
        )
    ])
])

    
    
def choice_serie_type(id):
    return html.Div(className="selection d-flex justify-content-center mt-2", children=[
        
        dmc.ChipGroup(value="relative", id=id, children=[
            dmc.Chip(x, value=y, size="sm", color="red") 
            for x, y in zip(
                ["Série relative (taux en %)", "Série absolue (données brute)"],
                ["relative", "absolue"]
            )
        ])
    ])
    

    

right_ui = dac.NavbarDropdown(
    id="database",
    badge_label="!",
    badge_color="danger",
    header_text=None,
    footer_text=None,
    menu_icon="database",
)


navbar = dac.Navbar(
    className="nav-bar",
    fixed=True, 
    color="white",
    text="Statistical Report and Data Visualization on Terrorism", 
    children=[right_ui]
)


subitems = [dac.SidebarMenuSubItem(id='tab_gallery_1',
                                   label='Gallery 1',
                                   icon='arrow-circle-right',
                                   badge_label='Soon',
                                   badge_color='success'),
            dac.SidebarMenuSubItem(id='tab_gallery_2',
                                   label='Gallery 2',
                                   icon='arrow-circle-right',
                                   badge_label='Soon',
                                   badge_color='success')
            ]

sidebar = dac.Sidebar(
    dac.SidebarMenu(
        [
            dac.SidebarHeader(children="Tableau De Bord"),
            
            dac.SidebarHeader(children="Tendances Générales"),
            
            dcc.Link(href="/", className="nav_link", children=[
                dac.SidebarMenuItem(label="Généralités", icon='box')
            ]),
        
                        
            dac.SidebarHeader(children="En détail"),
            
            dcc.Link(href="/tracker", className="nav_link", children=[
                dac.SidebarMenuItem(label="tracker", icon='box')
            ]),
            
            dcc.Link(href="/the-course-of-a-year", className="nav_link", children=[
                dac.SidebarMenuItem(label="Dans l'année", icon='box')
            ]),
            dcc.Link(href="/high-level-trends", className="nav_link", children=[
                dac.SidebarMenuItem(label="Tendance de haut niveau", icon='box')
            ]),
            dcc.Link(href="/major-terrorist-groups", className="nav_link", children=[
                dac.SidebarMenuItem(label="Les groupes terroristes", icon='box')
            ]),
            dcc.Link(href="/comparative-analysis", className="nav_link", children=[
                dac.SidebarMenuItem(label="Analyse comparative", icon='box')
            ]),
            dcc.Link(href="/economic-impact", className="nav_link", children=[
                dac.SidebarMenuItem(label="Impact économique", icon='desktop')
            ]),
            
                        
            dac.SidebarHeader(children="Analyse Par Pays"),
            
            dcc.Link(href="/situation-by-country", className="nav_link", children=[
                dac.SidebarMenuItem(
                    label="Tracker", icon='desktop')
            ]),


            dac.SidebarHeader(children="Chiffres Clés"),
            
            dcc.Link(href="/summury-country", className="nav_link", children=[
                dac.SidebarMenuItem(label="Résumé des chiffres clés", icon='desktop')
            ]),
            

            dac.SidebarHeader(children="Autres Graphiques"),
            dac.SidebarMenuItem(label='Galleries',
                                icon='cubes', children=subitems),

        ]
    ),
    title='Chris Baudelaire .K',
   	skin="light",
    color="danger",
   	brand_color="light-grey",
    url="/about",
    src='/assets/cccb-6.png',
    elevation=3,
    opacity=0.9
)



controlbar = dac.Controlbar(
    title="Bar Latérale | Filtre",
    skin="light",
    className="rightsidebar",
    children=[
        html.Br(),
        html.H4("Selection de données", className="mb-4"),
        filtre
    ],
)

# Footer
footer = dac.Footer(right_text="2024", children=[
    html.Small(className="fw-bold", children=[
        html.Span("@"),
        html.Span("Analytics"),
        html.Span("Paper", className="text-danger"),
        html.Span(" | Powered By Plotly/Dash", className="text")
    ])
])


def table(idx):
    return dash_table.DataTable(
        id=idx,
        style_cell={'font-family': 'Montserrat'},
        style_data_conditional=[
            {
                'if': {'column_id': 'intitule'},
                'textAlign': 'left'
            }] + [
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    )


affix = dmc.Affix(
    html.Div(id="minimap", className="carte"), position={"bottom": 20, "right": 20}
)


social_cards_tab = dac.TabItem(id='content_social_cards', 
                              
    children=html.Div(
        [
            dac.UserCard(
              src = "https://adminlte.io/themes/AdminLTE/dist/img/user1-128x128.jpg",
              color = "info",
              title = "User card type 1",
              subtitle = "a subtitle here",
              elevation = 4,
              children="Any content here"
            ),
            dac.UserCard(
              type = 2,
              src = "https://adminlte.io/themes/AdminLTE/dist/img/user7-128x128.jpg",
              color = "success",
              image_elevation = 4,
              title = "User card type 2",
              subtitle = "a subtitle here",
              children="Any content here"
            )
        ], 
        className='row'
    )
)