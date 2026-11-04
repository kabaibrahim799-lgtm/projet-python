""" Quiz """

__author__ = "kaba_c"


import random
import json


class Question:
    """Représente une question du quiz."""

    def __init__(self, identifiant, theme, question, options, reponse):
        self.identifiant = identifiant  # int pour l'identitifiant
        self.theme = theme  # str pour le theme
        self.question = question  # strpour la question
        self.options = options  # list pour avoir la liste des options pour la question
        self.reponse = reponse  # str pour la bonne réponse

    def afficher(self):
        """Affiche la question et les réponses possibles."""

        print(self.question)

        for numero, option in enumerate(self.options, start=1):
            print(f"{numero}. {option}")

    def verifier(self, choix):
        """Vérifie si la réponse choisie est correcte."""

        if not choix.isdigit():
            return False

        numero = int(choix)

        if 1 <= numero <= len(self.options):
            return self.options[numero - 1] == self.reponse

        return False


class Quiz:
    """Gère le déroulement du quiz."""

    def __init__(self, theme, questions):
        self.theme = theme
        self.questions = questions
        self.score = 0
        self.details = []

    def jouer(self):
        """Pose les questions et calcule le score."""

        questions = self.questions.copy()
        random.shuffle(questions)

        for numero, question in enumerate(questions, start=1):
            print(f"\n===== QUESTION {numero}/{len(questions)} =====")

            question.afficher()

            while True:
                choix = input(
                    "Ta réponse (numéro ou q pour quitter) : "
                ).strip()

                if choix.lower() == "q":
                    print("Quiz interrompu. Aucun résultat enregistré.")
                    return False

                if choix.isdigit() and 1 <= int(choix) <= \
                        len(question.options):
                    break

                print("Choix invalide. Réessaie.")

            correcte = question.verifier(choix)
            reponse_donnee = question.options[int(choix) - 1]

            self.details.append({
                "question": question.question,
                "reponse_donnee": reponse_donnee,
                "reponse_correcte": question.reponse,
                "correcte": correcte
            })

            if correcte:
                self.score += 1
                print("Bonne réponse !")
            else:
                print(f"Oups. La bonne réponse était : {question.reponse}")

        return True

    @property
    def score_pourcentage(self):
        """Calcule le score en pourcentage."""

        if not self.questions:
            return 0

        return round(self.score / len(self.questions) * 100)

    def afficher_resultats(self):
        """Affiche le résumé des résultats."""

        total = len(self.questions)
        mauvaises_reponses = total - self.score

        print("\n========== RÉSULTATS ==========")
        print(f"Thème : {self.theme}")
        print(f"Score : {self.score}/{total}")
        print(f"Pourcentage : {self.score_pourcentage}%")
        print(f"Bonnes réponses : {self.score}")
        print(f"Mauvaises réponses : {mauvaises_reponses}")
        print("================================")

        print("\nDétail des réponses :")

        for detail in self.details:
            statut = "Correcte" if detail["correcte"] else "Incorrecte"

            print(f"\nQuestion : {detail['question']}")
            print(f"Ta réponse : {detail['reponse_donnee']}")
            print(f"Bonne réponse : {detail['reponse_correcte']}")
            print(f"Résultat : {statut}")


def lire_json() -> list[Question]:
    """Lire un fichier JSON et recréer l'objet correspondant."""
    try:
        with open("data/questions.json", "r", encoding="utf-8") as f:
            donnees = json.load(f)

        list_questions: list[Question] = []
        total_point = 0
        for elem in donnees:
            question = Question(elem["id"], elem["theme"], elem["question"],
                                elem["options"], elem["reponse"])
            list_questions.append(question)

        for question in list_questions:
            print(question.question)
            for index, elem in enumerate(question.options):
                print(f"{index + 1}. {elem}")
            reponse = input("quelle est la bonne réponse ?")
            if question.options[int(reponse) - 1] == question.reponse:
                print("bonne repones")
                total_point += 1
            else:
                print("mauvaise reponse")

    except (FileNotFoundError):
        return None

    return []
