import pygame, random

pygame.init()  # 파이게임 초기화

넓 = 1500
높 = 1000
screen = pygame.display.set_mode((넓, 높))  # 화면 크기 설정
clock = pygame.time.Clock()  # 시간 조절을 위한 시계 객체 생성

# 색깔 설정
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (183, 183, 183)

# 폰트 설정
large_font = pygame.font.SysFont('malgungothic', 72)  # 대형 폰트 설정
small_font = pygame.font.SysFont('malgungothic', 36)  # 작은 폰트 설정

# 게임 초기 점수 설정
score = 0

# 셀 크기 및 열, 행 개수 설정
CELL_SIZE = 30
COLUMN_COUNT = 넓 // CELL_SIZE  # 열 개수
ROW_COUNT = 높 // CELL_SIZE  # 행 개수

# 방향 설정
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
direction = UP  # 초기 방향 설정

# 게임 오버 플래그
game_over = False

# 뱀의 몸통 초기 위치 설정
bodies = [(COLUMN_COUNT // 2, ROW_COUNT // 2)]  # 뱀의 초기 위치

# 빨간색 셀 위치 생성
red_cells = []  # 빨간색 셀을 저장할 리스트
for _ in range(5):  # 5개의 빨간색 셀 생성
    red_cell = (random.randint(0, COLUMN_COUNT - 1), random.randint(0, ROW_COUNT - 1))
    red_cells.append(red_cell)  # 생성된 셀을 리스트에 추가
1
# 음식 위치 생성
foods = []
for _ in range(10):
    while True:
        column_index, row_index = (random.randint(0, COLUMN_COUNT - 1), random.randint(0, ROW_COUNT - 1))
        if (column_index, row_index) not in foods and (column_index, row_index) not in bodies and (column_index, row_index) not in red_cells:
            foods.append((column_index, row_index))  # 먹이의 위치를 랜덤으로 설정
            break

pygame.mixer.init()  # 오디오 초기화

while True:  # 게임 루프
    screen.fill(BLACK)  # 화면 초기화

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
        first_body = bodies[0]  # 뱀의 머리 위치
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
           column_index < 0 or \
           column_index >= COLUMN_COUNT or \
           row_index < 0 or \
           row_index >= ROW_COUNT or \
           (column_index, row_index) in red_cells:
            game_over = True  # 게임 오버 조건

        bodies.insert(0, (column_index, row_index))  # 새로운 머리 위치 삽입
        eat = False
        if (column_index, row_index) in foods:
            foods.remove((column_index, row_index))  # 먹은 음식 제거
            while True:
                new_pos = (random.randint(0, COLUMN_COUNT - 1), random.randint(0, ROW_COUNT - 1))
                if new_pos not in foods and new_pos not in bodies and new_pos not in red_cells:
                    foods.append(new_pos)  # 새로운 음식 위치 추가
                    break
            eat = True
            score += 1  # 점수 증가

        if not eat:
            bodies.pop()  # 먹지 않았다면 꼬리 제거

    # 뱀의 무지개색 반짝임 효과
    snake_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # 무지개색 랜덤 생성

    # 화면 그리기
    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT):
            pygame.draw.rect(screen, GRAY, pygame.Rect(CELL_SIZE * column_index, CELL_SIZE * row_index, CELL_SIZE, CELL_SIZE), 1)  # 그리드 그리기

    for column_index, row_index in foods:
        pygame.draw.circle(screen, GREEN, (CELL_SIZE * column_index + CELL_SIZE // 2, CELL_SIZE * row_index + CELL_SIZE // 2), CELL_SIZE // 2)  # 음식 그리기

    for column_index, row_index in bodies:
        pygame.draw.rect(screen, snake_color, pygame.Rect(CELL_SIZE * column_index, CELL_SIZE * row_index, CELL_SIZE, CELL_SIZE))  # 뱀 그리기

    # 빨간색 셀 그리기
    for red_cell in red_cells:
        pygame.draw.rect(screen, RED, pygame.Rect(CELL_SIZE * red_cell[0], CELL_SIZE * red_cell[1], CELL_SIZE, CELL_SIZE))  # 빨간색 셀 그리기

    # 점수 표시
    score_image = small_font.render(f'점수 {score}', True, GREEN)  # 점수 텍스트 생성
    screen.blit(score_image, (10, 10))  # 점수 표시 위치 지정

    if game_over:
        game_over_image = large_font.render('게임 종료', True, RED)  # 게임 오버 텍스트 생성
        screen.blit(game_over_image, game_over_image.get_rect(centerx=넓 // 2, centery=높 // 2))  # 게임 오버 텍스트 표시 위치 지정

    pygame.display.update()  # 화면 업데이트
    clock.tick(10)  # 게임 속도 조절

pygame.quit()  # 게임 종료
