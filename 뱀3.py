import pygame, random

pygame.init()  # 파이 게임 초기화
넓 = 600
높 = 800
screen = pygame.display.set_mode((넓, 높))  # 화면 크기 설정
clock = pygame.time.Clock() 

# 색깔
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (183,183,183)
large_font = pygame.font.SysFont('malgungothic', 72)
small_font = pygame.font.SysFont('malgungothic', 36)
score = 0
CELL_SIZE = 30
COLUMN_COUNT = 넓 // CELL_SIZE
ROW_COUNT = 높 // CELL_SIZE
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
direction = UP
game_over = False

bodies = [(COLUMN_COUNT // 2, ROW_COUNT // 2)]

# 빨간색 셀 위치 생성
red_cell = (random.randint(0, COLUMN_COUNT - 1), random.randint(0, ROW_COUNT - 1))

foods = []
for _ in range(10):    
    while True:
        column_index, row_index = (random.randint(0, COLUMN_COUNT - 1), random.randint(0, ROW_COUNT - 1))
        if (column_index, row_index) not in foods and (column_index, row_index) not in bodies:
            foods.append((column_index, row_index))
            break

pygame.mixer.init()

while True:  # 게임 루프
    screen.fill(BLACK)  # 화면 지우기

    # 이벤트 처리
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN and not game_over:
        if event.key == pygame.K_LEFT:
            direction = LEFT
        elif event.key == pygame.K_RIGHT:
            direction = RIGHT
        elif event.key == pygame.K_UP:
            direction = UP
        elif event.key == pygame.K_DOWN:
            direction = DOWN

    if not game_over:
        first_body = bodies[0]
        if direction == LEFT:
            column_index = first_body[0] - 1
            row_index = first_body[1]
        elif direction == RIGHT:
            column_index = first_body[0] + 1
            row_index = first_body[1]
        elif direction == UP:
            column_index = first_body[0]
            row_index = first_body[1] - 1
        elif direction == DOWN:
            column_index = first_body[0]
            row_index = first_body[1] + 1

        # 벽이나 자신의 몸 또는 빨간 셀에 부딪혔는지 확인
        if (column_index, row_index) in bodies or \
           column_index < 0 or column_index >= COLUMN_COUNT or \
           row_index < 0 or row_index >= ROW_COUNT or \
           (column_index, row_index) == red_cell:
            game_over = True
            pygame.mixer.music.stop()

        bodies.insert(0, (column_index, row_index))
        eat = False
        if (column_index, row_index) in foods:
            foods.remove((column_index, row_index))
            while True:
                new_pos = (random.randint(0, COLUMN_COUNT - 1), random.randint(0, ROW_COUNT - 1))
                if new_pos not in foods and new_pos not in bodies:
                    foods.append(new_pos)
                    break
            eat = True
            score += 1

        if not eat:
            bodies.pop()

    # 화면 그리기
    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT):
            pygame.draw.rect(screen, GRAY, pygame.Rect(CELL_SIZE * column_index, CELL_SIZE * row_index, CELL_SIZE, CELL_SIZE), 1)

    for column_index, row_index in foods:
        pygame.draw.circle(screen, GREEN, (CELL_SIZE * column_index + CELL_SIZE // 2, CELL_SIZE * row_index + CELL_SIZE // 2), CELL_SIZE // 2)

    for column_index, row_index in bodies:
        pygame.draw.rect(screen, GREEN, pygame.Rect(CELL_SIZE * column_index, CELL_SIZE * row_index, CELL_SIZE, CELL_SIZE))

    # 빨간색 셀 그리기
    pygame.draw.rect(screen, RED, pygame.Rect(CELL_SIZE * red_cell[0], CELL_SIZE * red_cell[1], CELL_SIZE, CELL_SIZE))

    score_image = small_font.render(f'점수 {score}', True, GREEN)
    
    screen.blit(score_image, (10, 10))

    if game_over:
        game_over_image = large_font.render('게임 종료', True, RED)
        screen.blit(game_over_image, game_over_image.get_rect(centerx=넓 // 2, centery=높 // 2))

    pygame.display.update()  # 화면 업데이트
    clock.tick(10)  # 게임 속도 조절

pygame.quit()