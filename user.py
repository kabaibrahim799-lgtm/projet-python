""" Enregistrement """

__author__ = "kaba_c"


import json
from datetime import datetime
from pathlib import Path


DOSSIER_DATA = Path(__file__).parent / "data"
FICHIER_UTILISATEURS = DOSSIER_DATA / "utilisateurs.json"


def charger_utilisateurs():
    """Charge les utilisateurs depuis le fichier JSON."""

    DOSSIER_DATA.mkdir(parents=True, exist_ok=True)

    if not FICHIER_UTILISATEURS.exists():
        return {}

    try:
        with FICHIER_UTILISATEURS.open("r", encoding="utf-8") as fichier:
            utilisateurs = json.load(fichier)

        if not isinstance(utilisateurs, dict):
            raise ValueError("Le fichier doit contenir un objet JSON.")

        for profil in utilisateurs.values():
            if (
                not isinstance(profil, dict)
                or not isinstance(profil.get("scores"), list)
            ):
                raise ValueError("Un profil utilisateur est invalide.")

        return utilisateurs

    except (json.JSONDecodeError, OSError, ValueError) as erreur:
        raise RuntimeError(
            f"Impossible de charger les utilisateurs : {erreur}"
        ) from erreur


def sauvegarder_utilisateurs(utilisateurs):
    """Enregistre les utilisateurs dans le fichier JSON."""

    DOSSIER_DATA.mkdir(parents=True, exist_ok=True)

    try:
        with FICHIER_UTILISATEURS.open("w", encoding="utf-8") as fichier:
            json.dump(
                utilisateurs,
                fichier,
                indent=4,
                ensure_ascii=False
            )

        return True

    except OSError as erreur:
        print(f"Erreur lors de la sauvegarde : {erreur}")
        return False


def obtenir_utilisateur(nom, utilisateurs):
    """Récupère un joueur ou crée son profil."""

    if nom not in utilisateurs:
        utilisateurs[nom] = {"scores": []}

    return utilisateurs[nom]


def enregistrer_resultat(nom, quiz, utilisateurs):
    """Enregistre le résultat d'un quiz terminé."""

    profil = obtenir_utilisateur(nom, utilisateurs)

    resultat = {
        "theme": quiz.theme,
        "score": quiz.score_pourcentage,
        "bonnes_reponses": quiz.score,
        "total_questions": len(quiz.questions),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    profil["scores"].append(resultat)

    if sauvegarder_utilisateurs(utilisateurs):
        return True

    profil["scores"].pop()
    return False


def afficher_historique(nom, utilisateurs):
    """Affiche les résultats précédents du joueur."""

    profil = obtenir_utilisateur(nom, utilisateurs)
    scores = profil["scores"]

    print(f"\n===== HISTORIQUE DE {nom} =====")

    if not scores:
        print("Aucun résultat enregistré pour le moment.")
        return

    for numero, resultat in enumerate(scores, start=1):
        print(
            f"{numero}. Date : {resultat['date']} | "
            f"Thème : {resultat['theme']} | "
            f"Score : {resultat['score']}% "
            f"({resultat['bonnes_reponses']}/"
            f"{resultat['total_questions']})"
        )

    moyenne = sum(resultat["score"] for resultat in scores) / len(scores)

    print("\n===== PROGRESSION =====")
    print(f"Nombre de quiz terminés : {len(scores)}")
    print(f"Moyenne des scores : {moyenne:.1f}%")
