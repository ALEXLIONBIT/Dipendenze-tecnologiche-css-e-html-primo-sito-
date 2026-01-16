from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Funzione per leggere i messaggi salvati
def leggi_commenti():
    try:
        with open("commenti.txt", "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

@app.route('/')
def home():
    messaggi = leggi_commenti()
    return render_template('index.html', commenti=messaggi)

@app.route('/invia', methods=['POST'])
def invia():
    nuovo_messaggio = request.form.get('messaggio')
    if nuovo_messaggio:
        # Salviamo il messaggio nel file .txt
        with open("commenti.txt", "a", encoding="utf-8") as f:
            f.write(nuovo_messaggio + "\n")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=25565)