""" Utilisateur JSON """

__author__ = "kaba_c"


import json
from pathlib import Path


DOSSIER_DATA = Path(__file__).resolve().parent / "data"
FICHIER_QUESTIONS = DOSSIER_DATA / "questions.json"


def charger_questions():
    """Charge les questions depuis le fichier JSON."""

    try:
        with FICHIER_QUESTIONS.open("r", encoding="utf-8") as fichier:
            questions = json.load(fichier)

        if not isinstance(questions, list):
            raise ValueError("Le fichier doit contenir une ls de questions.")

        for question in questions:
            if not isinstance(question, dict):
                raise ValueError("Une question est invalide.")

            champs = {"id", "theme", "question", "options", "reponse"}

            if not champs.issubset(question):
                raise ValueError("Il manque des informations dans une quests.")

            if question["reponse"] not in question["options"]:
                raise ValueError("La bonne réponse est dans les options.")

        return questions

    except FileNotFoundError:
        print("Erreur : le fichier questions.json est introuvable.")

    except (json.JSONDecodeError, OSError, ValueError) as erreur:
        print(f"Erreur lors du chargement des questions : {erreur}")

    return []


def choisir_theme(questions):
    """Affiche les thèmes disponibles et demande un choix."""

    themes = sorted(set(question["theme"] for question in questions))

    if not themes:
        print("Aucun thème disponible.")
        return None

    print("\n===== THÈMES DISPONIBLES =====")

    for numero, theme in enumerate(themes, start=1):
        print(f"{numero}. {theme}")

    while True:
        choix = input("Choisis un thème (numéro) : ").strip()

        if choix.isdigit():
            numero = int(choix)

            if 1 <= numero <= len(themes):
                return themes[numero - 1]

        print("Choix invalide. Essaie encore.")
