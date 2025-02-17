from flask import Flask, render_template, request, redirect, url_for
import plotly.graph_objects as go
import plotly.express as px

app = Flask(__name__)

def categorize_anxiety(sum_skåre):
    if 5 <= sum_skåre <= 9:
        return "Mild angst: Dette innebærer symptomer som er merkbare, men som ikke nødvendigvis forstyrrer daglige aktiviteter i stor grad. Du kan føle deg engstelig eller bekymret, men klarer fortsatt å håndtere jobb, skole og sosiale aktiviteter. For mer overskudd og ro i hverdagen finnes det grep du kan gjøre. Se linken for selvhjelpskurs eller se etter tilbud i din kommune for psykisk helsetilbud. Forskning viser at kognitiv eller metakognitiv adferdsterapi er den desidert mest effektive metoden mot angst. Ett gratis lavterskel behandlingstilbud som dette er Rask psykisk helsehjelp. "
    elif 10 <= sum_skåre <= 14:
        return "Moderat angst: Symptomene er mer intense og kan begynne å påvirke din evne til å fungere normalt. Du kan oppleve vedvarende bekymringer, rastløshet, og fysiske symptomer som hjertebank og svette. Dette kan føre til at du unngår visse situasjoner eller oppgaver. Effektiv behandling finnes. Dette kan være er krevende, men ikke farlig å gjøre på egenhånd. Med moderat angst kan det likevel være greit å få støtte fra helsepersonell. Se etter tilbud i din kommune som Rask psykisk helsehjelp eller andre tilbud. Forskning viser at kognitiv adferdsterapi eller metakognitiv terapi er de mest effektive metodene mot spesifikk angst eller bekymringsangst. Konsulter også din fastlege hvis du er i tvil."
    elif 15 <= sum_skåre <= 21:
        return "Alvorlig angst: Symptomene er svært intense og kan være invalidiserende. Du kan oppleve panikkanfall, fysiske symptomer som pustevansker og brystsmerter, og en sterk følelse av frykt eller katastrofetanker. Dette kan gjøre det vanskelig å utføre daglige aktiviteter og opprettholde sosiale relasjoner. Effektiv behandling finnes. Dette kan være er krevende, men ikke farlig å gjøre på egenhånd. Med alvorlig angst kan det likevel være greit å få støtte fra helsepersonell. Ta kontakt med fastlegen for henvisning til behandling og vis skåren din."
    else:
        return "Normale angstreaksjoner som kan gi informasjon om fare eller prioriteringer. Uten at dette påvirker livskvalitet i større grad."
    
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
        "Nervøs, engstelig",
        "Tankekjør bekymringer",
        "Mengde bekymringer",
        "Vansker med å slappe av",
        "Rastløs",
        "Irritasjon",
        "Frykt"
    ]

    fig.update_traces(
        marker_color=['#A2D2DF', '#4A628A', '#4A628A', '#9B7EBD', '#9B7EBD', '#E6C767', 
                      '#E6C767'],  # Endre fargen på stolpene
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

    Kategori = categorize_anxiety(sum_skåre)  if difficulty != "0" else "Du har svart at disse symptomene ikke er vanskelig for deg i din hverdag"
    Livsbelastning = livsbelastning(difficulty)

    anxiety_chart = create_visualization(skåre_visualisering)

    # Samle inn data for bar chart
    data = {}
    for key, value in request.form.items():
        if key.startswith('q'):
            data[key] = float(value)  # Konverter til float hvis verdien finnes

    bar_chart = create_bar_chart(data)  if difficulty != "0" else None

    return render_template('resultat.html', q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, difficulty=difficulty, 
                           sum_skåre=sum_skåre, Kategori=Kategori, Livsbelastning=Livsbelastning, 
                           anxiety_chart=anxiety_chart, bar_chart=bar_chart)

if __name__ == '__main__':
    app.run(debug=True)
