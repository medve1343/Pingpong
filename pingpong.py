import pygame
import sys


pygame.init()


WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
BALL_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")


clock = pygame.time.Clock()


player1 = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed = [5, 5]  


score_player1 = 0
score_player2 = 0


font = pygame.font.Font(None, 36)

paused = False


collision_sound = pygame.mixer.Sound("collision_sound.wav")
score_sound = pygame.mixer.Sound("score_sound.wav")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                score_player1 = 0
                score_player2 = 0
                ball.x = WIDTH // 2 - BALL_SIZE // 2
                ball.y = HEIGHT // 2 - BALL_SIZE // 2
                paused = False

    if not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= 5
        if keys[pygame.K_s] and player1.bottom < HEIGHT:
            player1.y += 5
        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= 5
        if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
            player2.y += 5

        
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]
            collision_sound.play()  

       
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed[0] = -ball_speed[0]
            collision_sound.play()  

        
        if ball.left <= 0:
            score_player2 += 1
            ball_speed[0] = -ball_speed[0]
            ball.x = WIDTH // 2 - BALL_SIZE // 2
            ball.y = HEIGHT // 2 - BALL_SIZE // 2
            paused = True
            score_sound.play()  
        elif ball.right >= WIDTH:
            score_player1 += 1
            ball_speed[0] = -ball_speed[0]
            ball.x = WIDTH // 2 - BALL_SIZE // 2
            ball.y = HEIGHT // 2 - BALL_SIZE // 2
            paused = True
            score_sound.play()  

    
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)

    
    score_text = font.render(f"{score_player1} - {score_player2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    
    if paused:
        paused_text = font.render("Paused", True, WHITE)
        screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2 - paused_text.get_height() // 2))

    
    pygame.display.flip()

    clock.tick(FPS)