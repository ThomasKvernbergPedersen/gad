from flask import Flask, render_template, request, redirect, url_for
import plotly.graph_objects as go
import plotly.express as px

app = Flask(__name__)

def categorize_anxiety(sum_skåre):
    if 5 <= sum_skåre <= 9:
        return "Mild angst"
    elif 10 <= sum_skåre <= 14:
        return "Moderat angst"
    elif 15 <= sum_skåre <= 21:
        return "Alvorlig angst"
    else:
        return "Normal angst"
    
def livsbelastning(difficulty):
    if difficulty == "0":
        return "Ikke vanskelig i det hele tatt"
    elif difficulty == "1":
        return "Litt vanskelig"
    elif difficulty == "2":
        return "Svært vanskelig"
    elif difficulty == "3":
        return "Ekstremt vanskelig"
    else: 
        return "Noe gikk galt"

def create_visualization(skåre_visualisering):
    questions = [
        "Følt deg nervøs, engstelig eller på tuppa",
        "Ikke klart å stoppe eller kontrollere bekymringene dine",
        "Bekymret deg for mye om ulike ting",
        "Hatt vansker med å slappe av",
        "Vært så rastløs at det har vært vanskelig å sitte stille",
        "Blitt lett irritert eller ergret deg over ting",
        "Følt deg redd som om noe forferdelig kunne komme til å skje"
    ]

    fig = go.Figure(data=[
        go.Bar(name='Sum Skåre', x=questions, y=skåre_visualisering)
    ])

    fig.update_layout(
        title="GAD-7 Sum Skåre Visualisering",
        xaxis_title="Spørsmål",
        yaxis_title="Skåre",
        barmode='group'
    )

    return fig.to_html(full_html=False)

def create_bar_chart(data):
    data_list = [{'Domain': key, 'Score': value} for key, value in data.items()]
    
    fig = px.bar(data_list, x='Domain', y='Score', title='Total Score per Domain')
    new_x_labels = [
        'Suitable Items', 'Feasible Agenda', 'Coherent and dynamic formulation', 'Appropriate Intervention Targets', 
        'Choosing Suitable Interventions', 'Rationale for Interventions', 'Implementing Interventions', 
        'Reviewing Interventions', 'Reviewing Homework', 'Choosing Suitable Homework', 'Rationale for Homework', 
        'Planning Homework', 'Choosing Suitable Measures', 'Implementing Measures', 'Pace', 'Time Management', 
        'Maintained Focus', 'Interpersonal style', 'Empathic Understanding', 'Collaboration', 'Patient Feedback', 
        'Reflective Summaries'
    ]

    fig.update_traces(
        marker_color=['#A2D2DF', '#A2D2DF', '#4A628A', '#9B7EBD', '#9B7EBD','#9B7EBD','#9B7EBD','#9B7EBD', '#E6C767', 
                      '#E6C767','#E6C767','#E6C767','#898121','#898121', '#F87A53','#F87A53','#F87A53','#0D92F4','#0D92F4',
                      '#0D92F4', '#54473F','#54473F'],  # Endre fargen på stolpene
        texttemplate='%{x}: %{y}',  # Legg til tekst på stolpene
        textposition='outside'  # Plasser teksten utenfor stolpene
    )

    fig.update_xaxes(
        tickvals=list(data.keys()),  # Originale verdier
        ticktext=new_x_labels  # Nye navn
    )

    fig.update_layout(
        xaxis_title='See your item spesific score in the color separated domains.',
        yaxis_title='Item score',
        title='Total score per Domene',
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    return fig.to_html(full_html=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    q1 = int(request.form.get('q1'))
    q2 = int(request.form.get('q2'))
    q3 = int(request.form.get('q3'))
    q4 = int(request.form.get('q4'))
    q5 = int(request.form.get('q5'))
    q6 = int(request.form.get('q6'))
    q7 = int(request.form.get('q7'))
    difficulty = request.form.get('difficulty')

    sum_skåre = q1 + q2 + q3 + q4 + q5 + q6 + q7 
    skåre_visualisering = [q1, q2, q3, q4, q5, q6, q7]

    Kategori = categorize_anxiety(sum_skåre)
    Livsbelastning = livsbelastning(difficulty)

    anxiety_chart = create_visualization(skåre_visualisering)

    # Samle inn data for bar chart
    data = {}
    for key, value in request.form.items():
        if key.startswith('q'):
            data[key] = float(value)  # Konverter til float hvis verdien finnes

    bar_chart = create_bar_chart(data)

    return render_template('resultat.html', q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, difficulty=difficulty, 
                           sum_skåre=sum_skåre, Kategori=Kategori, Livsbelastning=Livsbelastning, 
                           anxiety_chart=anxiety_chart, bar_chart=bar_chart)

if __name__ == '__main__':
    app.run(debug=True)
