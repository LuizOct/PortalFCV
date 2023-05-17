# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from datetime import date



# importando meus dados

df = pd.read_excel('dados.xlsx')

# Variáveis
rows = df.shape[0]


df['ESTADIAM'] = df['ESTADIAM'].replace(['0A'], 0)
df['ESTADIAM'] = df['ESTADIAM'].replace(['1'], 'I')
df['ESTADIAM'] = df['ESTADIAM'].replace(['2'], 'II')
df['ESTADIAM'] = df['ESTADIAM'].replace(['3'], 'III')
df['ESTADIAM'] = df['ESTADIAM'].replace(['4'],'IV')

df['OBITOPORCANCER'].fillna('Sem Informação', inplace=True)
df['OBITOPORCANCER'] = df['OBITOPORCANCER'].replace(['Sim'], 'Óbito por Câncer')
df['OBITOPORCANCER'] = df['OBITOPORCANCER'].replace(['Não'], 'Óbito por Outras Causas')

df['ALCOOLIS'] = df['ALCOOLIS'].replace(['Sim'], 'Consumidor')
df['TABAGISM'] = df['TABAGISM'].replace(['Sim'], 'Fumante')

df['CIDADE'].fillna('Sem Informação', inplace=True)
df = df[df['CIDADE'] != 'Sem Informação']
sexoNumber = df['SEXO'].value_counts()


# Variáveis de filtro
sexos = df["SEXO"].sort_values().unique()
cidades = df["CIDADE"].sort_values().unique()
anos = df['ANO'].sort_values().unique()
tiposDeCancer = df['LocalTumorLegendado'].sort_values().unique()


# inicializando app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', {
    'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
    'crossorigin': 'anonymous'
}]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div(className='corpo-site', children=[

    # Título
    html.Div(className='header-title', children=[
        html.Div(className='logo', children=[
            html.Img(src='assets/imgs/vetorFCV.png',
                     alt='logo fundação cristiano varella')
        ]),
        html.H1(className='title', children='Portal Informativo do Câncer'),
        
        html.P(className='sub-title',
               children='Dados epdemiológicos do RHC coletados no período de 2010 a 2021')
    ]),


    html.Br(),
    html.Br(),

    # Filtro
    html.Div(className='filtro',
             
             children=[
                 
                html.Div(
                     children=[
                         html.Div(children="Cidade", className="menu-title"),
                         dcc.Dropdown(
                             id="cidade-filter",
                             options=[{'label': 'Selecione todos', 'value': 'all'}]+[
                                 {
                                     "label": cidade,
                                     "value": cidade
                                 }
                                 for cidade in cidades
                             ],
                             value="all",
                             clearable=False,
                             searchable=True,
                             className="dropdown",
                         ),
                     ],
                 ),

                 html.Div(children="Sexo", className="menu-title"),
                 dcc.Dropdown(
                     id="sexo-filter",
                     options=[{'label': 'Selecione todos', 'value': 'all'}]+[
                         {"label": sexo, "value": sexo}
                         for sexo in sexos],
                     value="all",
                     clearable=False,
                     className="dropdown",
                 ),

                 
                 html.Div(
                     children=[
                         html.Div(children="Local do Tumor", className="menu-title"),
                         dcc.Dropdown(
                             id="tipoDeCancer-filter",
                             options=[{'label': 'Selecione todos', 'value': 'all'}]+[
                                 {
                                     "label": cancer,
                                     "value": cancer
                                 }
                                 for cancer in tiposDeCancer
                             ],
                             value="all",
                             clearable=False,
                             searchable=True,
                             className="dropdown",
                         ),
                     ],
                 ),
                 html.Div(
                     children=[
                         html.Div(
                             children="Selecionar Data", className="menu-title"
                         ),
                         dcc.RangeSlider(
                             id="date-range",
                             min=df["ANO"].min(),
                             max=df["ANO"].max(),
                             marks={2010: '2010', 2011: '2011', 2012: '2012', 2013: '2013', 2014: '2014', 2015: '2015', 2016: '2016',
                                    2017: '2017', 2018: '2018', 2019: '2019', 2020: '2020', 2021: '2021'},
                             value=[2010, 2021],
                             tooltip={"placement": "bottom",
                                      "always_visible": True}
                         ),
                     ]
                 ),
             ]
             ),

    html.Br(),
    html.Br(),
    #CARDS CONTANDO O NÙMERO DE PESSOAS 
    html.Div(className='row', children=[

        html.Div(className='three columns', children=[
            html.Div(className='cardTotalPessoas', children=[
                 html.Div(className='row', children=[
                     'Número de Casos',
                     html.Div(id='numeroPessoasValue')
                 ])
            ]),
        ]),
        html.Div(className='three columns', children=[
            html.Div(className='cardTotalMasculino', children=[
                 html.Div(className='row', children=[
                     'Número de Pacientes Masculinos',
                     html.Div(id='numeroMasculinoValue')
                 ])
            ]),
        ]),
        html.Div(className='three columns', children=[
            html.Div(className='cardTotalFeminino', children=[
                 html.Div(className='row', children=[
                     'Número de Pacientes Femininos',
                     html.Div(id='numeroFemininoValue')
                 ])
            ]),
        ]),
        html.Div(className='three columns', children=[
            html.Div(className='cardTotalMenor', children=[
                 html.Div(className='row', children=[
                     'Número de Pacientes Menor de Idade',
                     html.Div(id='numeroMenorValue')
                 ])
            ]),
        ])
    ]),

    

    html.Br(),
    html.Div(className='row', children=[
        html.Div( children=[
            dcc.Graph(
                id='casosPorAno'
            )
        ]),
    ]),
    html.Br(),

    html.Div(className='row', children=[
        
        html.Div(className='six columns', children=[
            dcc.Graph(
                id='escolaridade'
            )
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(
                id='idade'
            )
        ]),
    ]),

    html.Br(),
    #Gráficos de hábitos e raça
    html.Div(className='row', children=[
        html.Div(className='four columns', children=[
            dcc.Graph(id='raca')
        ]),
        html.Div(className='four columns', children=[
            dcc.Graph(id='consumoBebidaAlcoolica')
        ]),
        html.Div(className='four columns', children=[
            dcc.Graph(id='consumoTabaco')
        ]),
        
    ]),

    html.Br(),

    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Graph(
                id='obitos',
            )
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(
                id='estadiamento'
            )
        ])
    ]),

    html.Br(),

])


@app.callback(
    Output("consumoTabaco", "figure"),
    Output("consumoBebidaAlcoolica", "figure"),
    Output("raca", 'figure'),
    Output("casosPorAno", 'figure'),
    Output("escolaridade", 'figure'),
    Output("idade", 'figure'),
    Output("estadiamento", 'figure'),
    Output("obitos", 'figure'),
    Output('numeroPessoasValue', 'children'),
    Output('numeroMasculinoValue', 'children'),
    Output('numeroFemininoValue', 'children'),
    Output('numeroMenorValue', 'children'),
    Input("cidade-filter", "value"),
    Input("sexo-filter", "value"),
    Input("tipoDeCancer-filter", "value"),
    Input("date-range", "value"),

)
def update_charts( cidade, sexo, cancer, value):
    #Retirando dados que não desejamos em alguns gráficos
    dadosNDesejáveis= ['Sem informação','Sem Informação','Não se Aplica','Não Avaliado','']
    paletaDeCores= ['#0f3376','#00BF63','#FF3131','#8C52FF','#EFBC33']

    #GARANTINDO QUE OS FILTROS FUNCIONEM
    if (sexo == 'all' and cidade == 'all' and cancer =='all'):
        filtered_data = df.query('ANO >= @value[0] and ANO<= @value[1]')
    elif (sexo == 'all' and cancer =='all'):
        filtered_data = df.query(
            "CIDADE == @cidade and ANO >= @value[0] and ANO<= @value[1]")
    elif (sexo == 'all' and cidade == 'all'):
        filtered_data = df.query(
            'LocalTumorLegendado == @cancer and ANO >= @value[0] and ANO<= @value[1]')
    elif (cidade == 'all' and cancer == 'all'):
        filtered_data = df.query(
            'SEXO == @sexo and ANO >= @value[0] and ANO<= @value[1]')    
    elif(sexo=='all'):
        filtered_data = df.query(
            "CIDADE == @cidade and LocalTumorLegendado == @cancer and ANO >= @value[0] and ANO<= @value[1]"
        )
    elif(cidade=='all'):
        filtered_data = df.query(
            "SEXO == @sexo and LocalTumorLegendado == @cancer and ANO >= @value[0] and ANO<= @value[1]"
        )
    elif(cancer=='all'):
        filtered_data = df.query(
            "SEXO == @sexo and CIDADE == @cidade and ANO >= @value[0] and ANO<= @value[1]"
        )            
    else:
        filtered_data = df.query(
            "CIDADE == @cidade and SEXO == @sexo and LocalTumorLegendado == @cancer and ANO >= @value[0] and ANO<= @value[1]")
    #PLOTANDO OS GRÁFICOS DE ACORDO COM O FILTRO
    consumoTabaco = px.pie(
        filtered_data[-filtered_data['TABAGISM'].isin(dadosNDesejáveis)], values='COUNT',names='TABAGISM', hole=.3, title='Tabagismo',color_discrete_sequence=paletaDeCores)
    consumoTabaco.update_traces(
        hoverinfo='label+value', textinfo='percent', textfont_size=15)

    consumoBebidaAlcoolica = px.pie(
        filtered_data[-filtered_data['ALCOOLIS'].isin(dadosNDesejáveis)], values='COUNT', names='ALCOOLIS', hole=.3, title='Etilismo',color_discrete_sequence=paletaDeCores)
    consumoBebidaAlcoolica.update_traces(
        hoverinfo='label+value', textinfo='percent', textfont_size=15)

    raca = px.pie(
        filtered_data[-filtered_data['RACACOR'].isin(dadosNDesejáveis)], values='COUNT',names='RACACOR', hole=.3, title='Etnia',color_discrete_sequence=paletaDeCores)
    raca.update_traces(hoverinfo='label+value',textinfo='percent', textfont_size=15)

    casosPorAno = px.histogram(filtered_data, x='ANO', y='COUNT', title='Número de casos por ano',text_auto=True,color_discrete_sequence=['#0f3376'])
    casosPorAno.update_layout(bargap=0.2,yaxis_title='Novos Casos',xaxis_title='Ano', xaxis=dict(tickmode='linear',tick0=2010,dtick=1))
    
        

    idade = px.histogram(filtered_data,x='Cortes_Idade',y='COUNT',title='Idade',histnorm='percent',text_auto='.2f',color_discrete_sequence=['#0f3376'])
    idade.update_layout(bargap=0.2,yaxis_title='Porcentagem(%)',xaxis_title='Faixa Etária' )
    idade.update_xaxes(categoryorder='array', categoryarray=['0','1-10','11-20','21-30','31-40','41-50','51-60','61-70','71-80','81-90','91+'])
   
    

    escolaridade = px.histogram(filtered_data[-filtered_data['INSTRUC'].isin(dadosNDesejáveis)],x='COUNT',y='INSTRUC',title='Escolaridade',histnorm='percent',text_auto='.2f',labels={
        'INSTRUC':'',
       },
       color_discrete_sequence=['#0f3376'])
    escolaridade.update_layout(bargap=0.2,xaxis_title='Porcentagem(%)')
    escolaridade.update_yaxes(categoryorder='array' , categoryarray = ['Analfabeto','Fundamental Incompleto','Fundamental Completo','Nível Médio','Nível Superior Incompleto','Nível Superior Completo'])

    estadiamento = px.histogram(filtered_data[-filtered_data['ESTADIAM'].isin(dadosNDesejáveis)],color='ESTADIAM',x='ANO',title='Estadiamento do Tumor',barnorm = "percent",category_orders={
        'ESTADIAM': ['0','I','II','III','IV']},
        color_discrete_map={'0':'#0f3376','I':'#2d8a87','II':'#EFBC33','III':'#FF66C4','IV':'#FF3131'})
    estadiamento.update_layout(bargap=0.2,legend_title_text='',yaxis_title='Estadiamento(%)', xaxis_title='Ano',xaxis=dict(tickmode='linear',tick0=2010,dtick=1))

    
    obitos = px.pie(filtered_data[(-filtered_data['OBITOPORCANCER'].isin(dadosNDesejáveis))],values='COUNT',names='OBITOPORCANCER',title='Óbitos por Câncer',hole=.3 ,color_discrete_sequence=paletaDeCores)
    obitos.update_traces(sort=False)

    #CRIANDO OS CARDS DE ACORDO COM O FILTRO

    numeroPessoasValue = html.Div(children=[
        filtered_data.shape[0]
    ])
     
    masc='Masculino'
    fem='Feminino'
    masculino=filtered_data.query('SEXO == @masc and IDADE > 17')
    feminino=filtered_data.query('SEXO == @fem and IDADE > 17')
    menor = filtered_data.query('IDADE < 18')
    numeroMasculinoValue = html.Div(children=[        
        masculino.shape[0]
    ])
    numeroFemininoValue = html.Div(children=[
        feminino.shape[0]
    ])
    numeroMenorValue = html.Div(children=[
        menor.shape[0]
    ])

    return consumoTabaco, consumoBebidaAlcoolica, raca, casosPorAno, escolaridade, idade, estadiamento, obitos, numeroPessoasValue, numeroMasculinoValue, numeroFemininoValue, numeroMenorValue


def update_others_charts():
    return


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

