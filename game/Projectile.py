import pygame

# definir la classe qui va gerer le projectile
class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.velocity = 12
        self.player = player
        self.image = pygame.image.load('static/assets/projectile.png')
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 85
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        # tourner le projectile
        self.angle += 8
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        self.rect.x += self.velocity
        self.rotate()
        
        # verifie si le projectile rentre en colision avec un monstre
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            # on va supprimer le projectile
            self.remove()
            # infliger des degats
            monster.damage(self.player.attack)
            

        # verifie si notre projetile n'est plus a l'ecran
        if self.rect.x > 1080:
            # supprimer le projectile en dehors de l'ecran
            self.remove()
            print("destruction du projectile")

