from flask import Flask, render_template, request, redirect, url_for
import plotly.graph_objects as go
import os

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
    if 0:
        return "Ikke vanskelig i det hele tatt"
    elif 1:
        return "Litt vanskelig"
    elif 2:
        return "Svært vanskelig"
    elif 3:
        return "Ekstremt vanskelig"
    else: 
        return "Noe gikk galt"


def create_visualization(skåre_visualisering):
    # Definer spørsmålene
    questions = [
        "Følt deg nervøs, engstelig eller på tuppa",
        "Ikke klart å stoppe eller kontrollere bekymringene dine",
        "Bekymret deg for mye om ulike ting",
        "Hatt vansker med å slappe av",
        "Vært så rastløs at det har vært vanskelig å sitte stille",
        "Blitt lett irritert eller ergret deg over ting",
        "Følt deg redd som om noe forferdelig kunne komme til å skje"
    ]

    # Lag et stolpediagram
    fig = go.Figure(data=[
        go.Bar(name='Sum Skåre', x=questions, y=skåre_visualisering)
    ])

    # Oppdater layout
    fig.update_layout(
        title="GAD-7 Sum Skåre Visualisering",
        xaxis_title="Spørsmål",
        yaxis_title="Skåre",
        barmode='group'
    )

    # Lagre figuren som en HTML-fil
     # Lagre figuren som en HTML-fil i static-katalogen
    if not os.path.exists('static'):
        os.makedirs('static')
    fig.write_html("static/gad7_visualization.html")



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():

    
    # Retrieve the form data
    q1 = int(request.form.get('q1'))
    q2 = int(request.form.get('q2'))
    q3 = int(request.form.get('q3'))
    q4 = int(request.form.get('q4'))
    q5 = int(request.form.get('q5'))
    q6 = int(request.form.get('q6'))
    q7 = int(request.form.get('q7'))
    difficulty = request.form.get('difficulty')

    sum_skåre = q1 + q2 + q3 + q4 + q5 + q6 + q7 
    skåre_visualisering = [q1 + q2 + q3 + q4 + q5 + q6 + q7]

    Kategori = categorize_anxiety(sum_skåre)
    Livsbelastning = livsbelastning(difficulty)
    #lage visualiseringer
    create_visualization(skåre_visualisering)



    # Redirect to the results page with the form data
    return render_template('resultat.html', q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, difficulty=difficulty, sum_skåre = sum_skåre, Kategori = Kategori, 
                           Livsbelastning = Livsbelastning, skåre_visualisering=skåre_visualisering)

if __name__ == '__main__':
      app.run(debug=True)