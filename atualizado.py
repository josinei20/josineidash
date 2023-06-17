import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from datetime import datetime
import time

while True:
    # import from folders/theme changer
    #from app import *
    from dash_bootstrap_templates import ThemeSwitchAIO

    FONT_AWESOME = ["Bemol.com.br"]
    app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME)
    app.scripts.config.serve_locally = True

    server = app.server
    # ========== Styles ============ #
    tab_card = {'height': '100%'}
    main_config = {
        "hovermode": "x unified",
        "legend": {"yanchor":"top",
                    "y":0.9,
                    "xanchor":"left",
                    "x":0.1,
                    "title": {"text": None},
                    "font" :{"color":"white"},
                    "bgcolor": "rgba(0,0,0,0.5)"},
        "margin": {"l":10, "r":10, "t":10, "b":10}
    }
    config_graph={"displayModeBar": False, "showTips": False}

    template_theme1 = "flatly"
    template_theme2 = "darkly"

    url_theme1 = dbc.themes.FLATLY
    url_theme2 = dbc.themes.DARKLY

    # ===== Reading n cleaning File ====== #
    gd = pd.read_excel('Pasta 29.xlsx')
    df = pd.read_excel('TESTE.xlsx')
    df_cru = df


    # Algumas limpezas

    df = df.drop(['Cod_vendedorr','Vendedor','Unnamed: 11'],axis=1)
    df = df.drop(['Unnamed: 12', 'Unnamed: 17'],axis=1)
    df = df.dropna(how='all', axis=1)
    df = df.dropna(how='all')

    # mudando o nome da coluna

    df = df.rename(columns={'ASDASDASDASDASDSADA': 'Centro'})
    df = df.rename(columns={'Cod_vendedorr': 'Vendedor'})

    # Transformando em int tudo que der
    df['Centro'] = df['Centro'].astype(int)
    df['Valor unitário'] = df['Valor unitário'].astype(int)
    df['Qtd'] = df['Qtd'].astype(int)

    #ajustando a base de dados valores repetidos e errados

    df = df.replace(['Ar_condicionado','Cadeira%Gamer', 'Fone d Ouvido', 'IPHOne', 'iPHONE','SAMSUNG', 'samsungsamsung','XBOX SERIESSSS', 'Amazonas Shoping'], ['Ar condicionado', 'Cadeira Gamer', 'Fone de Ouvido','Iphone', 'Iphone', 'Samsung', 'Samsung' ,'Xbox series s','Amazonas Shopping'])

    # Criando opções pros filtros que virão
    options_month = [{'label': 'Todos os dias', 'value': 0}]
    for i in gd['DIA'].unique():
        options_month.append({'label': i, 'value': i})

    #options_month = sorted(options_month, key=lambda x: x['value'])
    options_team = [{'label': 'Todos os dias', 'value': 0}]
    for i in gd['DIA'].unique():
        options_team.append({'label': i, 'value': i})

    # ========= Função dos Filtros ========= #

    def month_filter(month):

        if month == 0:
            mask = gd['DIA'].isin(gd['DIA'].unique())
        else:
            mask = gd['DIA'].isin([month])
        return mask

    def team_filter(team):

        if team == 0:
            mask = gd['DIA'].isin(gd['DIA'].unique())
        else:
            mask = gd['DIA'].isin([team])
        return mask

    def convert_to_text(month):
        lista1 = ['Todos os dias', 'SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SABADO']
        return lista1[month]

    # =========  Layout  =========== #

    app.layout = dbc.Container(children=[
    # Row 1
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([  
                                html.Legend("Entrega Interior")
                            ], sm=8),
                            dbc.Col([        
                                html.I(className='fa fa-balance-scale', style={'font-size': '300%'})
                            ], sm=4, align="center")
                        ]),
                        dbc.Row([
                            dbc.Col([
                                ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                                html.Legend("GD 2ª Turno")
                            ])
                        ], style={'margin-top': '10px'}),
                        dbc.Row([
                            dbc.Button("Visite o Site da bemol", href="https://www.bemol.com.br/", target="_blank")
                        ], style={'margin-top': '10px'})
                    ])
                ], style=tab_card)
            ], sm=4, lg=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Legend('Rodagem de Boa Vista')
                            ]),
                            dbc.Col([
                                html.Legend('NF Expedidas para Boa Vista'),
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='graph1', className='dbc', config=config_graph)
                            ], sm=12, md=5),
                            dbc.Col([
                                dcc.Graph(id='graph2', className='dbc', config=config_graph)
                            ], sm=12, lg=7)
                        ])
                    ])
                ], style=tab_card)
            ], sm=12, lg=7),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row(
                            dbc.Col([
                                html.H5('Escolha um Dia'),
                                dbc.RadioItems(
                                    id="radio-month",
                                    options=options_month,
                                    value=0,
                                    inline=True,
                                    labelCheckedClassName="text-success",
                                    inputCheckedClassName="border border-success bg-success",
                                ),
                                html.Div(id='month-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                            ])
                        )
                    ])
                ], style=tab_card)
            ], sm=12, lg=3)
        ], className='g-2 my-auto', style={'margin-top': '7px'}),
        # Row 2
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4('Recebimento de Mercado'),
                                dcc.Graph(id='graph3', className='dbc', config=config_graph)
                            ])
                        ], style=tab_card)
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4('Recebimento de Marketplace'),
                                dcc.Graph(id='graph4', className='dbc', config=config_graph)
                            ])
                        ], style=tab_card)
                    ])
                ], className='g-2 my-auto', style={'margin-top': '7px'})
            ], sm=12, lg=5),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph5', className='dbc', config=config_graph)    
                            ])
                        ], style=tab_card)
                    ], sm=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph6', className='dbc', config=config_graph)    
                            ])
                        ], style=tab_card)
                    ], sm=6)
                ], className='g-2'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.H4('Notas enviadas ao CD Porto'),
                            dcc.Graph(id='graph7', className='dbc', config=config_graph)
                        ], style=tab_card)
                    ])
                ], className='g-2 my-auto', style={'margin-top': '7px'})
            ], sm=12, lg=4),
            dbc.Col([
                dbc.Card([
                    html.H4('Caminhoes carregados'),
                    dcc.Graph(id='graph8', className='dbc', config=config_graph)
                ], style=tab_card)
            ], sm=12, lg=3)
        ], className='g-2 my-auto', style={'margin-top': '7px'}),
        # Row 3
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4('Divergencia'),
                        dcc.Graph(id='graph9', className='dbc', config=config_graph)
                    ])
                ], style=tab_card)
            ], sm=14, lg=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Faturamento Terrestre"),
                        dcc.Graph(id='graph10', className='dbc', config=config_graph)
                    ])
                ], style=tab_card)
            ], sm=12, lg=5),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph11', className='dbc', config=config_graph)    
                            ])
                        ], style=tab_card)
                    ], sm=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph12', className='dbc', config=config_graph)    
                            ])
                        ], style=tab_card)
                    ], sm=6)
                ], className='g-2'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.H4('RC RESOLVIDAS'),
                            dcc.Graph(id='graph13', className='dbc', config=config_graph)
                        ], style=tab_card)
                    ])
                ], className='g-2 my-auto', style={'margin-top': '7px'})
            ], sm=12, lg=4),
        ], className='g-2 my-auto', style={'margin-top': '7px'})

    ], fluid=True, style={'height': '100vh'})
    # ======== Callbacks ========== #
    # Graph 1 and 2
    @app.callback(
        Output('graph1', 'figure'),
        Output('graph2', 'figure'),
        Output('month-select', 'children'),
        Input('radio-month', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    )
    def graph1(month, toggle):
        template = template_theme1 if toggle else template_theme2
        mask = month_filter(month)
        gd1 = gd2 = gd.loc[mask]
        gd1 = gd1.groupby(['Expediçao BOA VISTA', 'ORDEM'])['DIA'].sum().reset_index()
        gd1 = gd1.sort_values(by=['ORDEM'],ascending=True)

        gd2 = gd2.groupby(['Rodagem Boa vista', 'ORDEM'])['DIA'].sum().reset_index()
        gd2 = gd2.sort_values(by=['ORDEM'],ascending=False)

        fig2 = fig2 = go.Figure(go.Bar(
            x=gd2['Rodagem Boa vista'],
            y=gd2['DIA'],
            orientation='h',
            textposition='auto',
            text=gd2['Rodagem Boa vista'],
            insidetextfont=dict(family='Times', size=12)))

        fig1 = go.Figure(go.Bar(x=gd1['DIA'], y=gd1['Expediçao BOA VISTA'], textposition='auto', text=gd1['Expediçao BOA VISTA']))
        fig1.update_layout(main_config, height=200, template=template)
        fig2.update_layout(main_config, height=200, template=template, showlegend=False)
        select = html.H1("Todo os dias") if month == 0 else html.H1(month)

        return fig2, fig1, select

    # Graph 3
    @app.callback(

        Output('graph3', 'figure'),
        Input('radio-month', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    )
    def graph3(month, toggle):

        template = template_theme1 if toggle else template_theme2
        mask = month_filter(month)
        gd3 = gd.loc[mask]
        gd3 = gd3.groupby(['DIA', 'ORDEM'])['REC MERCADO'].sum().reset_index()
        gd3 = gd3.sort_values(by=['ORDEM'],ascending=True)
        fig20 = go.Figure(go.Bar(x=gd3['DIA'], y=gd3['REC MERCADO'], textposition='auto', text=gd3['REC MERCADO']))
        fig20.update_layout(main_config, height=200, template=template)
        return fig20

    # Graph 4

    @app.callback(

        Output('graph4', 'figure'),
        Input('radio-month', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    )
    def graph4(month, toggle):
        template = template_theme1 if toggle else template_theme2
        mask = month_filter(month)
        gd07 = gd.loc[mask]

        gd07 = gd07.groupby(['DIA', 'ORDEM'])['REC MARKETPLACE'].sum().reset_index()
        gd07 = gd07.sort_values(by=['ORDEM'],ascending=True)
        fig07 = go.Figure(go.Bar(x=gd07['DIA'], y=gd07['REC MARKETPLACE'], textposition='auto', text=gd07['REC MARKETPLACE']))
        fig07.update_layout(main_config, yaxis={'title': None}, xaxis={'title': None}, height=200, template=template)
        return fig07

    # Indicators 1 and 2 ------ Graph 5 and 6
    @app.callback(

        Output('graph5', 'figure'),
        Output('graph6', 'figure'),
        Input('radio-month', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    )
    def graph5(month, toggle):

        template = template_theme1 if toggle else template_theme2
        mask = month_filter(month)
        gd5 = gd6 = gd.loc[mask]
        
        gd5 = gd5.groupby('DIA')['FLUVIAL'].sum()
        gd5.sort_values(ascending=False, inplace=True)
        gd5 = gd5.reset_index()
        fig5 = go.Figure()
        fig5.add_trace(go.Indicator(mode='number+delta',

            title = {"text": f"<span>{gd5['DIA'].iloc[0]} - TOP DIA</span><br><span style='font-size:70%'>Em envio ao CD Porto</span><br>"},
            value = gd5['FLUVIAL'].iloc[0],
            number = {'prefix': "NF:"},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': gd5['FLUVIAL'].iloc[1]}
        ))

        gd6 = gd6.groupby('DIA')['Expediçao BOA VISTA'].sum()
        gd6.sort_values(ascending=False, inplace=True)
        gd6 = gd6.reset_index()
        fig6 = go.Figure()
        fig6.add_trace(go.Indicator(mode='number+delta',

            title = {"text": f"<span>{gd6['DIA'].iloc[0]} - TOP DIA</span><br><span style='font-size:70%'>Em expediçao - em relação a Boa vista</span><br>"},
            value = gd6['Expediçao BOA VISTA'].iloc[0],
            number = {'prefix': "NF:"},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': gd6['Expediçao BOA VISTA'].iloc[1]}
        ))

        fig5.update_layout(main_config, height=200, template=template)
        fig6.update_layout(main_config, height=200, template=template)
        fig5.update_layout({"margin": {"l":0, "r":0, "t":50, "b":0}})
        fig6.update_layout({"margin": {"l":0, "r":0, "t":50, "b":0}})
        return fig5, fig6

    # Graph 7
    @app.callback(

        Output('graph7', 'figure'),
        Input('radio-month', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    )

    def graph7(month, toggle):

        template = template_theme1 if toggle else template_theme2
        mask = month_filter(month)

        gd7 = gd.loc[mask]
        gd7 = gd7.groupby(['DIA', 'ORDEM'])['FLUVIAL'].sum().reset_index()
        gd7 = gd7.sort_values(by=['ORDEM'],ascending=True)
        fig7 = go.Figure(go.Pie(labels=gd7['DIA'],values=gd7['FLUVIAL'], hole=.6))
        fig7.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20)
        fig7.update_layout(main_config, height=270, template=template)

        return fig7
    # Graph 8

    @app.callback(

        Output('graph8', 'figure'),
        Input('radio-month', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    )
    def graph3(month, toggle):

        template = template_theme1 if toggle else template_theme2
        mask = month_filter(month)
        gd8 = gd.loc[mask]

        gd8 = gd8.groupby(['DIA', 'ORDEM'])['CAMINHÕES'].sum().reset_index()
        gd8 = gd8.sort_values(by=['ORDEM'],ascending=False)

        fig8 = go.Figure(go.Bar(
            x=gd8['CAMINHÕES'],
            y=gd8['DIA'],
            orientation='h',
            textposition='auto',
            text=gd8['CAMINHÕES'],
            insidetextfont=dict(family='Times', size=12)))

        fig8.update_layout(main_config, height=480, template=template)
        return fig8

    # Graph 9

    @app.callback(

        Output('graph9', 'figure'),
        Input('radio-month', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    )
    def graph9(month, toggle):
        template = template_theme1 if toggle else template_theme2
        mask = month_filter(month)
        gd30 = gd.loc[mask]

        gd30 = gd30.groupby(['DIA', 'ORDEM'])['DIVERGÊNCIAS'].sum().reset_index()
        gd30 = gd30.sort_values(by=['ORDEM'],ascending=False)
        fig30 = go.Figure(go.Bar(
            x=gd30['DIVERGÊNCIAS'],
            y=gd30['DIA'],
            orientation='h',
            textposition='auto',
            text=gd30['DIVERGÊNCIAS'],
            insidetextfont=dict(family='Times', size=12)))
        fig30.update_layout(main_config, height=480, template=template)
        return fig30

    # Graph 10

    @app.callback(

        Output('graph10', 'figure'),
        Input('radio-month', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    )

    def graph10(month, toggle):
        template = template_theme1 if toggle else template_theme2
        mask = month_filter(month)
        gd100 = gd.loc[mask]
        gd100 = gd100.groupby(['DIA', 'ORDEM'])['TERRESTRE'].sum().reset_index()
        gd100 = gd100.sort_values(by=['ORDEM'],ascending=True)

        fig100 = go.Figure(go.Scatter(
        x=gd100['DIA'], y=gd100['TERRESTRE'], mode='lines', fill='tonexty'))

        fig100.add_annotation(text=f"Média : {round(gd100['TERRESTRE'].mean())}",
            xref="paper", yref="paper",
            font=dict(
                size=30,
                color='gray'
                ),
            align="center", bgcolor="rgba(0,0,0,0.8)",
                x=0.05, y=0.55, showarrow=False)
        fig100.update_layout(main_config, height=480, template=template)
        return fig100

    # Graph 11

    @app.callback(

        Output('graph11', 'figure'),
        Input('radio-month', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    )
    def graph11(month,toggle):
        template = template_theme1 if toggle else template_theme2
        mask = month_filter(month)
        gd02 = gd.loc[mask]
        gd02 = gd02.loc[mask]
        fig02 = go.Figure()
        fig02.add_trace(go.Indicator(mode='number',

            title = {"text": f"<span style='font-size:150%'>Quantidade Total</span><br><span style='font-size:70%'>De NF enviadas ao CD Porto</span><br>"},
            value = gd02['FLUVIAL'].sum(),
            number = {'prefix': "NF:"}
        ))
        fig02.update_layout(main_config, height=200, template=template)
        return fig02

    #12

    @app.callback(
        Output('graph12', 'figure'),
        Input('radio-month', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    )
    def graph12(month,toggle):

        template = template_theme1 if toggle else template_theme2
        mask = month_filter(month)
        gd03 = gd.loc[mask]
        gd03 = gd03.loc[mask]

        fig03 = go.Figure()
        fig03.add_trace(go.Indicator(mode='number',

            title = {"text": f"<span style='font-size:150%'>Quantidade Total</span><br><span style='font-size:70%'>De NF enviadas para Boa vista</span><br>"},
            value = gd03['Expediçao BOA VISTA'].sum(),
            number = {'prefix': "NF:"}
        ))
        fig03.update_layout(main_config, height=200, template=template)
        return fig03

    # Graph 13
    @app.callback(

        Output('graph13', 'figure'),
        Input('radio-month', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value")
    )

    def graph13(month, toggle):

        template = template_theme1 if toggle else template_theme2
        mask = month_filter(month)
        gd70 = gd.loc[mask]
        
        gd70 = gd70.groupby(['DIA', 'ORDEM'])['RC RESOLVIDAS '].sum().reset_index()
        gd70 = gd70.sort_values(by=['ORDEM'],ascending=True)
        fig70 = go.Figure(go.Pie(labels=gd70['DIA'],values=gd70['RC RESOLVIDAS '], hole=.6))
        fig70.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20)
        fig70.update_layout(main_config, height=270, template=template)
        
        return fig70

    # Run server
    if __name__ == '__main__':
        app.run_server(debug=False)
        
    time.sleep(5)

