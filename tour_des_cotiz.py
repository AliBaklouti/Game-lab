import pygame
import sys
import random

pygame.init()

largeur_fenetre = 800
hauteur_fenetre = 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption('Jeu des points')

noir = (0, 0, 0)
blanc = (255, 255, 255)
rouge = (255, 0, 0)

rayon_points = 20
score = 0
font = pygame.font.Font(None, 36)

# Ajout d'un timer de 30 secondes
temps_de_jeu = 30  # 30 secondes
temps_depart = pygame.time.get_ticks()

def nouveau_point():
    x = random.randint(rayon_points, largeur_fenetre - rayon_points)
    y = random.randint(rayon_points, hauteur_fenetre - rayon_points)
    return (x, y)

point_x, point_y = nouveau_point()

running = True
encerclement = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    distance = ((point_x - mouse_x) ** 2 + (point_y - mouse_y) ** 2) ** 0.5
    encerclement = distance < rayon_points

    if encerclement and pygame.mouse.get_pressed()[0]:
        score += 1
        point_x, point_y = nouveau_point()

    # Calcul du temps restant
    temps_actuel = pygame.time.get_ticks()
    temps_restant = max(temps_de_jeu - (temps_actuel - temps_depart) // 1000, 0)

    fenetre.fill(noir)
    pygame.draw.circle(fenetre, rouge, (point_x, point_y), rayon_points)

    score_text = font.render(f"Score: {score}", True, blanc)
    fenetre.blit(score_text, (10, 10))

    # Affichage du temps restant
    temps_text = font.render(f"Temps restant: {temps_restant} s", True, blanc)
    fenetre.blit(temps_text, (largeur_fenetre - 200, 10))

    pygame.display.flip()

    # Vérification de la fin du jeu
    if temps_restant == 0:
        running = False

# À la fin du jeu, affichage du score
fenetre.fill(noir)
score_text = font.render(f"Score final: {score}", True, blanc)
fenetre.blit(score_text, (largeur_fenetre // 2 - 100, hauteur_fenetre // 2 - 18))
pygame.display.flip()

# Attente pendant quelques secondes avant de fermer la fenêtre
pygame.time.delay(3000)

pygame.quit()
sys.exit()
