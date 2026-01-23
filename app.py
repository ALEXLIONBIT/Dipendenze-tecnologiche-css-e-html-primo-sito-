from flask import Flask, render_template, request, redirect, url_for
import requests
#code by Alessandro Bitti - GitHub:https://github.com/ALEXLIONBIT
app = Flask(__name__)


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

@app.route('/scuse', methods=['GET', 'POST'])
def genera_scuse():
    scusa_generata = ""
    argomento = ""

    if request.method == 'POST':
        argomento = request.form.get('argomento')
        
        
        prompt = (
    f"Sei un assistente che aiuta le persone a staccarsi dai social e dai videogiochi. "
    f"Inventa una scusa divertente, brevissima (max 10 parole) e piena di emoji per spiegare "
    f"che non puoi stare al PC/telefono perché devi fare altro con: {argomento}. "
    f"Esempio se l'argomento è 'Cane': 'Lascio Brawl Stars, il mio cane vuole sfidarmi a nascondino! 🐶🎾' "
    f"Rispondi solo con la scusa in italiano."
)
        
        try:
            url = "http://localhost:11434/api/generate"
            payload = {
                "model": "gemma3:4b",  
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7, 
                    "top_k": 40
                }
            }
            risposta = requests.post(url, json=payload)
            dati = risposta.json()
            testo_ai = dati['response']
            
            
            scusa_generata = testo_ai.strip()
            
        except:
            scusa_generata = "⚠️ Errore: Ollama"

    return f"""
    <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; background-color: #f0f8ff; padding: 50px;">
            <div style="background: white; padding: 30px; border-radius: 20px; box-shadow: 0px 10px 20px rgba(0,0,0,0.1); display: inline-block;">
                <h1 style="color: #2c3e50;">Generatore di Scuse</h1>
                <p style="color: #7f8c8d;">Scrivi un argomento</p>
                
                <form method="POST">
                    <input type="text" name="argomento" placeholder="Un amongus che balla???" 
                           style="padding: 12px; width: 250px; border: 2px solid #ddd; border-radius: 10px; outline: none;">
                    <button type="submit" style="padding: 12px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold;">
                        Genera Scusa!
                    </button>
                </form>

                <div style="margin-top: 30px; padding: 20px; border-left: 5px solid #4CAF50; background-color: #f9f9f9; text-align: left; max-width: 400px;">
                    <h3 style="margin-top: 0;">La tua scusa:</h3>
                    <p style="font-size: 1.2em; color: #34495e;">
                        {scusa_generata if scusa_generata else "<i>Aspetto...</i>"}
                    </p>
                </div>

                
                
                <br><br>
                <img src="/static/img/sorry.jpg" alt="Scusa" style="width: 500px; border-radius: 10px;">
                <br>
                <a href="/" style="color: #3498db; text-decoration: none; font-weight: bold;">⬅ Torna alla Home</a>
            </div> </body>
    </html>
    """

@app.route('/invia', methods=['POST'])
def invia():
    nuovo_messaggio = request.form.get('messaggio')
    if nuovo_messaggio:

        with open("commenti.txt", "a", encoding="utf-8") as f:
            f.write(nuovo_messaggio + "\n")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=25565)
