def afficher_grille(grille):
    emojis = {0: "⬜", 1: "❌", 2: "⭕"} 
    for ligne in grille:
        print(" ".join([emojis[cell] for cell in ligne]))

def fonction_cout(grille):
    # On récupére d'abord les lignes, les colonnes et les diagonales
    lignes = grille
    colonnes = [list(col) for col in zip(*grille)]
    diagonales = [[grille[i][i] for i in range(len(grille))], [grille[i][len(grille)-1-i] for i in range(len(grille))]]
    directions = lignes + colonnes + diagonales

    # Vérification des gagnants
    for x in directions:
        if x == [1, 1, 1]:
            return 1 # Le joueur X a gagné
        elif x == [2, 2, 2]:
            return -1 # Le joueur O a gagné

    # Vérification du match nul
    if all(cell != 0 for ligne in grille for cell in ligne):
        return 0

    return 0

def main():
    n = 3
    grille = [[0 for _ in range(n)] for _ in range(n)]
    afficher_grille(grille)

if __name__ == "__main__":
    main()
