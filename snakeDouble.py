# -*- coding: utf-8 -*
import pygame
import sys
import random

# 全局定义
SCREEN_X = 600
SCREEN_Y = 600


# 蛇类
# 点以5为单位
class Snake(object):
    # 初始化各种需要的属性 [开始时默认向右/身体块x5]
    def __init__(self, listen):
        self.keyType = listen
        dir = random.choice([0, 1, 2, 3])
        if dir == 0:
            if listen == "dir":
                self.dirction = pygame.K_RIGHT
            else:
                self.dirction = pygame.K_d
        if dir == 1:
            if listen == "dir":
                self.dirction = pygame.K_LEFT
            else:
                self.dirction = pygame.K_a
        if dir == 2:
            if listen == "dir":
                self.dirction = pygame.K_UP
            else:
                self.dirction = pygame.K_w
        if dir == 3:
            if listen == "dir":
                self.dirction = pygame.K_DOWN
            else:
                self.dirction = pygame.K_s
        self.body = []
        for x in range(5):
            self.addnode()

    # 无论何时 都在前端增加蛇块
    def addnode(self):
        allpos = []
        # 不靠墙太近 200 ~ SCREEN_X-200 之间
        for pos in range(200, SCREEN_X - 200, 10):
            allpos.append(pos)
        left, top = (random.choice(allpos), random.choice(allpos))
        if self.body:
            left, top = (self.body[0].left, self.body[0].top)
        node = pygame.Rect(left, top, 10, 10)
        if self.dirction == pygame.K_LEFT or self.dirction == pygame.K_a:
            node.left -= 10
        elif self.dirction == pygame.K_RIGHT or self.dirction == pygame.K_d:
            node.left += 10
        elif self.dirction == pygame.K_UP or self.dirction == pygame.K_w:
            node.top -= 10
        elif self.dirction == pygame.K_DOWN or self.dirction == pygame.K_s:
            node.top += 10
        self.body.insert(0, node)

    # 删除最后一个块
    def delnode(self):
        self.body.pop()

    # 死亡判断
    def isdead(self):
        # 撞墙
        if self.body[0].x not in range(SCREEN_X):
            return True
        if self.body[0].y not in range(SCREEN_Y):
            return True
        # 撞自己
        if self.body[0] in self.body[1:]:
            return True
        return False

    # 移动！
    def move(self):
        self.addnode()
        self.delnode()

    # 改变方向 但是左右、上下不能被逆向改变
    def changedirection(self, curkey):
        if self.keyType == "dir":
            LR = [pygame.K_LEFT, pygame.K_RIGHT]
            UD = [pygame.K_UP, pygame.K_DOWN]
            if curkey in LR + UD:
                if (curkey in LR) and (self.dirction in LR):
                    return
                if (curkey in UD) and (self.dirction in UD):
                    return
                self.dirction = curkey
        else:
            LR = [pygame.K_a, pygame.K_d]
            UD = [pygame.K_w, pygame.K_s]
            if curkey in LR + UD:
                if (curkey in LR) and (self.dirction in LR):
                    return
                if (curkey in UD) and (self.dirction in UD):
                    return
                self.dirction = curkey


# 食物类
# 方法： 放置/移除
# 点以5为单位
class Food:
    def __init__(self):
        self.rect = pygame.Rect(-10, 0, 10, 10)

    def remove(self):
        self.rect.x = -10

    def set(self):
        if self.rect.x == -10:
            allpos = []
            # 不靠墙太近 5 ~ SCREEN_X-5 之间
            for pos in range(10, SCREEN_X - 10, 10):
                allpos.append(pos)
            self.rect.left = random.choice(allpos)
            self.rect.top = random.choice(allpos)
            print(self.rect)


def show_text(screen, pos, text, color, font_bold=False, font_size=60, font_italic=False):
    # 获取系统字体，并设置文字大小
    cur_font = pygame.font.SysFont("宋体", font_size)
    # 设置是否加粗属性
    cur_font.set_bold(font_bold)
    # 设置是否斜体属性
    cur_font.set_italic(font_italic)
    # 设置文字内容
    text_fmt = cur_font.render(text, 1, color)
    # 绘制文字
    screen.blit(text_fmt, pos)


def main():
    pygame.init()
    screen_size = (SCREEN_X, SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    scoresA = 0
    scoresB = 0
    isdead = False

    # 蛇/食物
    snakeA = Snake('char')
    snakeB = Snake('dir')
    food = Food()
    clock.tick(1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snakeA.changedirection(event.key)
                snakeB.changedirection(event.key)
                # 死后按space重新
                if event.key == pygame.K_SPACE and isdead:
                    return main()

        screen.fill((255, 255, 255))

        # 画蛇身 / 每一步+1分
        if not isdead:
            scoresA += 1
            scoresB += 1
            snakeA.move()
            snakeB.move()
        for rect in snakeA.body:
            pygame.draw.rect(screen, (20, 220, 39), rect, 0)
        for rect in snakeB.body:
            pygame.draw.rect(screen, (220, 20, 39), rect, 0)
        # 显示死亡文字
        isdead = snakeA.isdead() | snakeB.isdead()
        if isdead:
            show_text(screen, (100, 200), 'GAME OVER!', (227, 29, 18), False, 50)
            show_text(screen, (150, 260), 'press space to try again...', (0, 0, 22), False, 15)
            if scoresA > scoresB:
                show_text(screen, (200, 290), 'LEFT WIN!', (0, 0, 22), False, 15)
            elif scoresA < scoresB:
                show_text(screen, (200, 290), 'RIGHT WIN!', (0, 0, 22), False, 15)
            else:
                show_text(screen, (200, 290), 'WIN WIN!', (0, 0, 22), False, 15)

        # 食物处理 / 吃到+50分
        # 当食物rect与蛇头重合,吃掉 -> Snake增加一个Node
        if food.rect == snakeA.body[0]:
            scoresA += 50
            food.remove()
            snakeA.addnode()
        if food.rect == snakeB.body[0]:
            scoresB += 50
            food.remove()
            snakeB.addnode()

        # 食物投递
        food.set()
        pygame.draw.rect(screen, (136, 0, 21), food.rect, 0)

        # 显示分数文字
        show_text(screen, (50, 500), 'Scores: ' + str(scoresA), (223, 223, 223))
        show_text(screen, (350, 500), 'Scores: ' + str(scoresB), (223, 223, 223))

        pygame.display.update()
        clock.tick(3)


if __name__ == '__main__':
    main()
