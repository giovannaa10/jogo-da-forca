from flask import Flask, render_template, request, redirect, url_for, session
import random
import webbrowser
from threading import Timer

app = Flask(__name__)
app.secret_key = "chave_forca_simples"

PALAVRAS = ["PYTHON", "FLASK", "CODIGO", "BANANA", "INTERNET"]

def novo_jogo():
    palavra = random.choice(PALAVRAS)
    session['palavra'] = palavra
    session['letras_descobertas'] = ["_"] * len(palavra)
    session['letras_erradas'] = []
    session['erros'] = 0

@app.route("/")
def index():
    if 'palavra' not in session:
        novo_jogo()

    venceu = "_" not in session['letras_descobertas']
    perdeu = session['erros'] >= 6

    return render_template(
        "index.html",
        palavra=session['palavra'],
        letras_descobertas=session['letras_descobertas'],
        letras_erradas=session['letras_erradas'],
        erros=session['erros'],
        max_erros=6,
        venceu=venceu,
        perdeu=perdeu
    )

@app.route("/jogar", methods=["POST"])
def jogar():
    letra = request.form.get("letra", "").upper().strip()
    
    if letra and len(letra) == 1 and letra.isalpha():
        palavra = session['palavra']
        descobertas = session['letras_descobertas']
        erradas = session['letras_erradas']

        if letra not in descobertas and letra not in erradas:
            if letra in palavra:
                for i in range(len(palavra)):
                    if palavra[i] == letra:
                        descobertas[i] = letra
                session['letras_descobertas'] = descobertas
            else:
                erradas.append(letra)
                session['letras_erradas'] = erradas
                session['erros'] += 1

    return redirect(url_for("index"))

@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    novo_jogo()
    return redirect(url_for("index"))

def abrir_navegador():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
    Timer(1, abrir_navegador).start()
    app.run(debug=False) 