'''
Name: Alex Valickis
Date: June 20th 2013
Purpose: Side scrolling video game
'''
    
import pygame, random
pygame.init()

screen = pygame.display.set_mode((640, 480))

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Ship.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        if not pygame.mixer:
            print("problem with sound")
        else:
            pygame.mixer.init()
            self.sndPickUp = pygame.mixer.Sound("PickUp.ogg")
            self.sndCrash = pygame.mixer.Sound("Crash.ogg")
            self.sndMusic = pygame.mixer.Sound("SpaceGameMusic.ogg")
            self.sndMusic.play(-1)
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        if mousey < 30:
            mousey = 30
        
        if mousey > 450:
            mousey = 450
            
        self.rect.center = (60, mousey)
                
class Perl(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Perl.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dx = 5
    
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.bottom >= screen.get_width():
            self.reset()
        if self.rect.top <= screen.get_height() - screen.get_height() - self.rect.height:
            self.reset()
        if self.rect.left <= screen.get_width() - screen.get_width() - self.rect.width:
            self.reset() 
            
    def reset(self):
        self.rect.left = 640
        self.rect.centery = random.randrange(0, screen.get_height())
      
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Asteroid.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.right <= 0:
            self.reset()
        if self.rect.top <= screen.get_height() - screen.get_height() - self.rect.height:
            self.reset()
        if self.rect.bottom >= screen.get_height() + self.rect.height:
            self.reset()
    
    def reset(self):
        self.rect.left = 640
        self.rect.centery = random.randrange(0, screen.get_height())
        self.dy = random.randrange(-2, 2)
        self.dx = random.randrange(-4, -2)
    
class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Background.gif")
        self.rect = self.image.get_rect()
        self.dx = -5
        self.reset()
        
    def update(self):
        self.rect.left += self.dx
        if self.rect.left <= -600:
            self.reset() 
    
    def reset(self):
        self.rect.right = 1440

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 100
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        self.text = "Hull Strength: %" + "%d, Score: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
    
def game():
    pygame.display.set_caption("G-ALEX-Y!")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    ship = Ship()
    perl = Perl()
    asteroid1 = Asteroid()
    asteroid2 = Asteroid()
    asteroid3 = Asteroid()
    background = Background()
    scoreboard = Scoreboard()

    friendSprites = pygame.sprite.OrderedUpdates(background, perl, ship)
    AsteroidSprites = pygame.sprite.Group(asteroid1, asteroid2, asteroid3)
    scoreSprite = pygame.sprite.Group(scoreboard)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        
        #check collisions
        
        if ship.rect.colliderect(perl.rect):
            ship.sndPickUp.play()
            perl.reset()
            scoreboard.score += 100

        hitAsteroids = pygame.sprite.spritecollide(ship, AsteroidSprites, False)
        if hitAsteroids:
            ship.sndCrash.play()
            scoreboard.lives -= 200
            if scoreboard.lives <= 0:
                keepGoing = False
                GameOver(scoreboard.score)
            for theAsteroid in hitAsteroids:
                theAsteroid.reset()
                
        friendSprites.update()
        AsteroidSprites.update()
        scoreSprite.update()
        
        friendSprites.draw(screen)
        AsteroidSprites.draw(screen)
        scoreSprite.draw(screen)
        
        pygame.display.flip()
    
    ship.sndMusic.stop()
    #return mouse cursor
    pygame.mouse.set_visible(True) 
    return scoreboard.score
    
def instructions(score):
    pygame.display.set_caption("G-ALEX-Y!")

    ship = Ship()
    background = Background()
    
    allSprites = pygame.sprite.Group(background, ship)
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    instructions = (
    "G-ALEX-Y     Last score: %d" % score ,
    "",
    "              Instructions",  
    '',
    "You are a space exploration ship",
    "traveling to undescovered Shipts.",
    "",
    "Fly into artifacts to collect points,",
    "but be careful not to fly too close",    
    "to the asteroids. Your ship will ",
    "explode if it is hit by them too",
    "many times! Steer with your",
    "mouse to controll the ship.",
    "",
    "click to start, escape to quit..."
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 0))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
        
    ship.sndMusic.stop()    
    pygame.mouse.set_visible(True)
    return donePlaying
        
def GameOver(score):
    pygame.display.set_caption("G-ALEX-Y!")

    ship = Ship()
    background = Background()
    
    allSprites = pygame.sprite.Group(background, ship)
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    GameOverMessage = (
    "                   GAME OVER",
    "",
    "",
    "               Your Score: %d" % score ,
    "",
    "",
    "",
    "               Play Again? (Y/N)"
    )
    
    for line in GameOverMessage:
        tempLabel = insFont.render(line, 1, (255, 255, 0))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    Scoreboard.score = 0
                    keepGoing = False
                    donePlaying = True
                    Scoreboard.score = game()
                elif  event.key == pygame.K_n:
                    keepGoing = False
                    donePlaying = True
                    
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
        
    ship.sndMusic.stop()    
    pygame.mouse.set_visible(True)
    return donePlaying

def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = instructions(score)
        if not donePlaying:
            score = game()


if __name__ == "__main__":
    main()
    
    
