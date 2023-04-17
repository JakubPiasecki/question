from flask import Flask, render_template, request, redirect, url_for
import csv
import os
import random

nazwa_pliku = 'pytania.csv'

app = Flask(__name__)

def wczytaj_pytania():
    pytania = []
    with open(nazwa_pliku, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pytania.append(row)
    return pytania

def zapisz_pytania(pytania):
    with open(nazwa_pliku, mode='w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['ID', 'Pytanie', 'Odpowiedź']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for pytanie in pytania:
            writer.writerow(pytanie)

@app.route('/')
def index():
    pytania = wczytaj_pytania()
    return render_template('index.html', pytania=pytania)

@app.route('/dodaj', methods=['POST'])
def dodaj_pytanie():
    pytania = wczytaj_pytania()
    nowe_pytanie = request.form['nowe_pytanie']
    odpowiedz = request.form['odpowiedz']
    id = len(pytania) + 1
    pytania.append({'ID': id, 'Pytanie': nowe_pytanie, 'Odpowiedź': odpowiedz})
    zapisz_pytania(pytania)
    return redirect(url_for('index'))

@app.route('/flashcards')
def flashcards():
    pytania = wczytaj_pytania()
    random.shuffle(pytania)
    return render_template('flashcards.html', pytania=pytania)

if __name__ == '__main__':
    app.run(debug=True)
