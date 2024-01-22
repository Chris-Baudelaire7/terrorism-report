from dash import html


navigation = html.Div(className="nav-scroller shadow-lg mb-5 text-center", children=[
    
    html.Div(className="nav text-center", children=[
        
        html.A(
            "En un clin d'oeil (resumé)", 
            className="nav-link text-dark active", 
            href="/Overview"
        ),
        
        html.A(
            "Étude statistique détaillée et visualisation de données", 
            className="nav-link text-dark active",
            href="/"
        ),
        
        
        html.A(
            "Résumé des chiffres clés", 
            className="nav-link text-dark active",
            href="/resume-des-chiffres-cles"
        ),
        
        html.A(
            "Le terrorisme en France", 
            className="nav-link text-dark active",
            href="/Le-terrorisme-en-France"
        ),
        
        html.A(
            "Autres graphiques", 
            className="nav-link text-dark active", 
            href="/Autre-etude-statistique"
        ),
        
        html.A(
            "Machine learning et prédiction", 
            className="nav-link text-dark active",
            href="/modeles-de-prediction"
        ),
        
        # html.A(
        #     "Sources de données et références", 
        #     className="nav-link text-dark active",
        #     href="/sources-de-donnees-et-references"
        # ),
    ])
    
])