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

    if all(cell != 0 for ligne in grille for cell in ligne):  # Grille pleine
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

def main():
    n = 3
    grille = [[0 for _ in range(n)] for _ in range(n)]
    afficher_grille(grille)
    
    while True:
        print("C'est au tour du joueur X:")
        coup = meilleur_coup(grille, 1)  # Choisir le meilleur coup pour X
        if coup is None:  # Aucun coup valide trouvé
            print("Match nul !")
            break
        i, j = coup
        grille[i][j] = 1 
        afficher_grille(grille)
        if fonction_cout(grille) == 5:
            print("Le joueur X a gagné!")
            break

        print("C'est au tour du joueur O:")
        coup = meilleur_coup(grille, 2)  # Choisir le meilleur coup pour O
        if coup is None:  # Aucun coup valide trouvé
            print("Match nul !")
            break
        i, j = coup
        grille[i][j] = 2
        afficher_grille(grille)
        if fonction_cout(grille) == -5:
            print("Le joueur O a gagné!")
            break

if __name__ == "__main__":
    main()
