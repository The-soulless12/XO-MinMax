def afficher_grille(grille):
    emojis = {0: "⬜", 1: "❌", 2: "⭕"} 
    for ligne in grille:
        print(" ".join([emojis[cell] for cell in ligne]))

def fonction_cout(grille):
    # On récupère les lignes, colonnes et diagonales
    lignes = grille
    colonnes = [list(col) for col in zip(*grille)]
    diagonales = [[grille[i][i] for i in range(len(grille))], [grille[i][len(grille)-1-i] for i in range(len(grille))]]
    directions = lignes + colonnes + diagonales

    for x in directions:
        if x == [1, 1, 1]:  # Le joueur X a gagné
            return 5
        elif x == [2, 2, 2]:  # Le joueur O a gagné
            return -5

    if all(cell != 0 for ligne in grille for cell in ligne):
        return 0

    return 0 
 
def minmax(grille, profondeur, alpha, beta, joueur):
    score_actuel = fonction_cout(grille)
    
    # Si le jeu est terminé, retourne le score
    if score_actuel == 5 or score_actuel == -5 or all(cell != 0 for ligne in grille for cell in ligne):
        return score_actuel

    # Si c'est au tour du joueur 'X' (maximiser le score)
    if joueur == 1:
        meilleur_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if grille[i][j] == 0: 
                    grille[i][j] = 1 
                    score = minmax(grille, profondeur + 1, alpha, beta, 2)  # Tour de 'O'
                    grille[i][j] = 0  # On annule le coup
                    
                    meilleur_score = max(meilleur_score, score)
                    alpha = max(alpha, meilleur_score)
                    if beta <= alpha:
                        break  # Élagage Beta
        return meilleur_score

    # Si c'est au tour du joueur 'O' (minimiser le score)
    else:
        meilleur_score = float('inf')
        for i in range(3):
            for j in range(3):
                if grille[i][j] == 0: 
                    grille[i][j] = 2 
                    score = minmax(grille, profondeur + 1, alpha, beta, 1)  # Tour de 'X'
                    grille[i][j] = 0  # On annule le coup
                    
                    meilleur_score = min(meilleur_score, score)
                    beta = min(beta, meilleur_score)
                    if beta <= alpha:
                        break  # Élagage Alpha
        return meilleur_score

def meilleur_coup(grille, joueur):
    meilleur_score = -float('inf') if joueur == 1 else float('inf')
    coup = None

    for i in range(3):
        for j in range(3):
            if grille[i][j] == 0: 
                grille[i][j] = joueur
                score = minmax(grille, 0, -float('inf'), float('inf'), 2 if joueur == 1 else 1)
                grille[i][j] = 0  # On annule le coup

                if (joueur == 1 and score > meilleur_score) or (joueur == 2 and score < meilleur_score):
                    meilleur_score = score
                    coup = (i, j)

    return coup

def demander_coordonnees(grille, n):
    while True:
        try:
            i, j = map(int, input("Entrez les coordonnées de votre coup (format : ligne colonne) : ").split())
            if 0 <= i < n and 0 <= j < n:  # Vérifie si les coordonnées sont dans la grille
                if grille[i][j] == 0:  
                    return i, j 
                else:
                    print("Cette case est déjà occupée. Veuillez en choisir une autre.")
            else:
                print("Coordonnées invalides. Assurez-vous d'entrer deux chiffres entre 0 et 2 séparés par un espace.")
        except (ValueError, IndexError):
            print("Coordonnées invalides. Assurez-vous d'entrer deux chiffres entre 0 et 2 séparés par un espace.")

def tour_jeu(grille, joueur, n, conseils, est_humain):
    coup = meilleur_coup(grille, joueur)  # Choisir le meilleur coup
    if coup is None:  # Aucun coup valide trouvé
        print("Match nul !")
        return True
    
    if joueur == 1:  # Tour du joueur X
        if est_humain:
            print("C'est à votre tour, cher joueur X:")
            if conseils == "Y": 
                print(f"💡 Conseil : Nous vous suggérons de jouer en ({coup[0]} {coup[1]}).")
            i, j = demander_coordonnees(grille, n)
        else:
            print("C'est au tour du joueur X:")
            i, j = coup

        grille[i][j] = 1
        afficher_grille(grille)
        if fonction_cout(grille) == 5:  # X a gagné
            print("Le joueur X a gagné!")
            return True
    else:  # Tour du joueur O
        if est_humain:
            print("C'est à votre tour, cher joueur O:")
            if conseils == "Y":  
                print(f"💡 Conseil : Nous vous suggérons de jouer en ({coup[0]} {coup[1]}).")
            i, j = demander_coordonnees(grille, n) 
        else:
            print("C'est au tour du joueur O:") 
            i, j = coup

        grille[i][j] = 2
        afficher_grille(grille)
        if fonction_cout(grille) == -5:  # O a gagné
            print("Le joueur O a gagné!")
            return True

    return False

def pc_contre_pc(grille, n):
    while True:
        # Tour de X (PC)
        if tour_jeu(grille, 1, n, conseils=None, est_humain=False):
            break

        # Tour de O (PC)
        if tour_jeu(grille, 2, n, conseils=None, est_humain=False):
            break

def humain_contre_pc(grille, conseils, n):
    while True:
        # Tour de X (humain)
        if tour_jeu(grille, 1, n, conseils, est_humain=True):
            break

        # Tour de O (PC)
        if tour_jeu(grille, 2, n, conseils, est_humain=False):
            break

def pc_contre_humain(grille, conseils, n):
    while True:
        # Tour de X (PC)
        if tour_jeu(grille, 1, n, conseils, est_humain=False):
            break

        # Tour de O (humain)
        if tour_jeu(grille, 2, n, conseils, est_humain=True):
            break

def menu():
        print("\nMenu principal :")
        print("1. PC [X] contre PC [O]")
        print("2. Humain [X] contre PC [O]")
        print("3. PC [X] contre Humain [O]")
        print("4. Quitter")
        choix = input("Choisissez une option (1/2/3/4) : ")
        return choix

def activer_conseils():
        while True:
            choix_conseils = input("💡 Voulez-vous activer les conseils ? (Y/N) : ").strip().upper()
            if choix_conseils in {"Y", "N"}:
                return choix_conseils
            else:
                print("Entrée invalide. Veuillez répondre par 'Y' ou 'N'.")

def main():
    n = 3

    while True:
        choix = menu()
        if choix == "1":
            pc_contre_pc([[0 for _ in range(n)] for _ in range(n)], n)
        elif choix == "2":
            conseils = activer_conseils()
            humain_contre_pc([[0 for _ in range(n)] for _ in range(n)], conseils, n)
        elif choix == "3":
            conseils = activer_conseils()
            pc_contre_humain([[0 for _ in range(n)] for _ in range(n)], conseils, n)
        elif choix == "4":
            print("Merci d'avoir joué. À bientôt !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()

