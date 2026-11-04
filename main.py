""" Projet final """

__author__ = "kaba_c"


from quiz import Question, Quiz
from utils import charger_questions, choisir_theme
from user import (
    charger_utilisateurs,
    obtenir_utilisateur,
    enregistrer_resultat,
    afficher_historique
)


def lancer_quiz(nom, utilisateurs, donnees_questions):
    """Prépare et lance un quiz."""

    theme = choisir_theme(donnees_questions)

    if theme is None:
        return

    questions_theme = [
        Question(
            question["id"],
            question["theme"],
            question["question"],
            question["options"],
            question["reponse"]
        )
        for question in donnees_questions
        if question["theme"] == theme
    ]

    if not questions_theme:
        print("Aucune question disponible pour ce thème.")
        return

    quiz = Quiz(theme, questions_theme)

    termine = quiz.jouer()

    if not termine:
        return

    quiz.afficher_resultats()

    if enregistrer_resultat(nom, quiz, utilisateurs):
        print("\nRésultat sauvegardé avec succès !")
    else:
        print("\nErreur : le résultat n'a pas pu être sauvegardé.")


def main():
    """Fonction principale du programme."""
    temp()


def temp():
    print("=" * 40)
    print("       BIENVENUE AU QUIZ PYTHON")
    print("=" * 40)

    nom = input(" Ibrahim : ").strip()

    if not nom:
        nom = "Ibrahim"

    questions = charger_questions()

    print("Contenu chargé :", questions)
    print("Nombre de questions :", len(questions))

    if not questions:
        print("Impossible de démarrer sans questions valides.")
        return

    try:
        utilisateurs = charger_utilisateurs()
    except RuntimeError as erreur:
        print(erreur)
        print("Vérifie le fichier utilisateurs.json.")
        return

    obtenir_utilisateur(nom, utilisateurs)

    while True:
        print("\n========== MENU PRINCIPAL ==========")
        print("1. Jouer à un quiz")
        print("2. Voir mes résultats")
        print("3. Quitter")
        print("====================================")

        choix = input("Ton choix (1-3) : ").strip()

        if choix == "1":
            lancer_quiz(nom, utilisateurs, donnees_questions=questions)

        elif choix == "2":
            afficher_historique(nom, utilisateurs)

        elif choix == "3":
            print("Merci d'avoir joué. À bientôt !")
            break

        else:
            print("Choix invalide. Saisis 1, 2 ou 3.")


if __name__ == "__main__":
    main()
