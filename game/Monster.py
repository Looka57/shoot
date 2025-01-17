import pygame
import random
import Animation

# definir la class du monstre
class Monster(Animation.AnimateSprite):
    def __init__(self, game, name, size, offset=0):
        super().__init__(name, size)
        self.game = game
        self.health = 100
        self.max_health = 100
        self.atk = 1
        # self.image = pygame.image.load('assets/mummy.png')
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 540 - offset
        self.loot_amount = 10
        self.start_animation ()
        
    def set_speed(self, speed):
        self.default_speed = speed
        self.velocity = random.randint(1, speed)
        
        # le changement de score
    def set_loot_amount(self, amount):
        self.loot_amount = amount
        
        
        
    # degat subit
    def damage(self, amount):
        # infliger les degats
        self.health -= amount
        
        # verifier si son nouveau point de vie est inferieur ou egal a 0
        if self.health <= 0:
            # Reapparaitre comme un nouveau monstre (le tuer visuellement pour le joueur)
            self.rect.x = 1000 + random.randint(0, 300)
            self.velocity = random.randint(1, self.default_speed)
            self.health= self.max_health
            # ajouer le nombre de point de score
            self.game.add_score(self.loot_amount)
            
            # si la barre d'event est chargé a son maximum
            if self.game.comet_event.is_full_loaded():
                # retirer du jeu
                self.game.all_monsters.remove(self)
                # appel de la methode pour essayer de declencher la pluie de comete
                self.game.comet_event.attempt_fall()
                
                
    def update_animation(self):
        self.animate(loop=True)
        
        
    def update_health_bar(self, surface):
        # # definir une couleur pour notre jauge de vie
        # bar_color = (81, 168, 112)
        # definir la couleur de base de la jaune
        # back_color_base = (87, 100, 92)
        
        # # definir la position de la jauge ainsi que sa largeur et son epaisseur
        # bar_position = [self.rect.x +10, self.rect.y -20, self.health, 5]
        # # definir la position de la jauge ainsi que sa largeur et son epaisseur
        # back_bar_position = [self.rect.x +10, self.rect.y -20, self.max_health, 5]
        
        # barre de vie en base
        pygame.draw.rect(surface, (87, 100, 92), [self.rect.x +10, self.rect.y -20, self.max_health, 5])
        # dessine la barre de vie
        pygame.draw.rect(surface, (81, 168, 112), [self.rect.x +10, self.rect.y -20, self.health, 5])
        
    def forward(self): 
        # le deplacement ne se fait que si il n'y a pas de collision avec le groupe de joueur
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        else:
            # si il y a collision, le monstre subit des degats
            self.game.player.damage(self.atk)

# definir une classe pour la momie
class Mummy(Monster):
    def __init__(self, game):
        super().__init__(game, "mummy", (130, 130))
        self.set_speed(5)
        self.set_loot_amount(20)
        
# definir une classe pour l'alien
class Alien(Monster):
    def __init__(self, game):
        super().__init__(game, "alien", (300, 300), 130)
        self.health = 250
        self.max_health = 250
        self.atk = 2
        self.set_speed(2)
        self.set_loot_amount(100)