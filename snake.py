import pygame
import time
import random

pygame.init()

# Define color, 255, 255)
white = (255, 255, 255)
red = (250, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

black = (0,0,0)
purple = (100,10,254)
orange = (255,165,0)
pink = (255,255,254)# Set display dimensions
dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("le super jeu du serpent")

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 9

font_style = pygame.font.SysFont(None, 30)


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
    
def message2(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 12, dis_height / 6])


def game_loop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    score = 0

    while not game_over:

        while game_close:
            dis.fill(purple)
            message(" Vous avez perdu au super jeu de serpent", black)
            message2("votre score :"+str(score),orange)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(purple)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for i in snake_list:
            pygame.draw.rect(dis, black, [i[0], i[1], snake_block, snake_block])

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 7
            score += 10
            print('score:',score)

        pygame.draw.rect(dis, white, [0, 0, 100, 40])
        score_font = pygame.font.SysFont("comicsansms", 35)
        value = score_font.render("Your Score: " + str(score), True, black)
        # print('score:',score)
        dis.blit(value, [0, 0])

        clock.tick(snake_speed+score)

    pygame.quit()
    quit()


game_loop()
