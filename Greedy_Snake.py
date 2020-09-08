####################################
##作者：simon （彭洋明）
##起始时间：2020.4.14
##修改时间：2020.4.15
##版权所有：Copyright©2019-2020 小明之家 
####################################
import copy
import a_star
import snake
import pygame
from pygame.locals import *


############################################
#判断是否可走，该函数不直接调用，作为参数给a_start模块使用
############################################
def judge(map,x,y):
    if map[y][x]==snake.WAY or map[y][x]==snake.FOOD:
        return True
    return False





############################################
#以下函数都是绘制函数，不直接调用，作为参数给snake模块使用
############################################
def draw_wall(x,y):
    global rect,wall_image
    rect.top=y
    rect.left=x
    screen.blit(wall_image,rect)
def draw_way(x,y):
    pass
def draw_head(x,y):
    global rect,head_image
    rect.top=y
    rect.left=x
    screen.blit(head_image,rect)
def draw_body(x,y):
    global rect,body_image
    rect.top=y
    rect.left=x
    screen.blit(body_image,rect)
def draw_tail(x,y):
    global rect,tail_image
    rect.top=y
    rect.left=x
    screen.blit(tail_image,rect)
def draw_food(x,y):
    global rect,food_image
    rect.top=y
    rect.left=x
    screen.blit(food_image,rect)




############################################
#输入方向，要snake模块作出反应
#@snake ：snake对象
#@operation ：移动队列
#return:
#返回移动后的结果（胜利，撞墙，死亡，吃到食物）
############################################
def dispose(snake,operation):

    #pygame在作祟 不加下面两行会卡死
    event = pygame.event.get()
    pygame.event.clear()
    '''
    if event.type == KEYDOWN:
        if event.key==K_w and new_snake.direction !=snake.H_DOWN:
            new_snake.direction=snake.H_UP
        elif event.key==K_s and new_snake.direction !=snake.H_UP:
            new_snake.direction=snake.H_DOWN
        elif event.key==K_a and new_snake.direction !=snake.H_RIGHT:
            new_snake.direction=snake.H_LEFT
        elif event.key==K_d and new_snake.direction !=snake.H_LEFT:
            new_snake.direction=snake.H_RIGHT
    '''
    
    snake.set_direction(operation.pop(0))
    ret=snake.move()
    #print(ret)
    return ret







############################################
#进行移动，且显示出来
#@snake ：snake对象
#@operation ：移动队列
############################################
def rungame(new_snake,operation):
    screen.fill((230, 230, 230))
    #进行键盘事件的处理等
    dispose(new_snake,operation)
    #绘制整个图像
    new_snake.fill()
    #  让最近绘制的屏幕可见
    pygame.display.flip()






############################################
#该函数给Start_pathfinding函数调用
#将两个相邻的坐标转化为方向
#@a 起始坐标
#@b 结束坐标
############################################
def transform(a,b):
    if a[0] == b[0]:
        if a[1]>b[1]:
            return snake.H_UP
        else:
            return snake.H_DOWN
    else:
        if a[0]>b[0]:
            return snake.H_LEFT
        else:
            return snake.H_RIGHT


#寻路路径
operation = [] 
#追尾模式开关
rear_end=0
#追尾路径
rear_end_path=[]

############################################
#整个项目的核心算法
#计算正确有效的路径
#@operation :输出参数 进行路径的输出
############################################
def Start_pathfinding(operation):
    global rear_end,rear_end_path,new_snake
    s,w,h = new_snake.get_rect_swh()
    head_x,head_y=new_snake.get_head()
    food_x=new_snake.food[0]
    food_y=new_snake.food[1]
    tail_x,tail_y=new_snake.get_tail()
    a_snake=a_star.a_star(new_snake.map,(head_x,head_y),(food_x,food_y),(w,h),judge,True)
    a_return,way_list = a_snake.start_run()
    if a_return :
        #暂时吃不到食物
        #使用最长路径算法开始追尾
                    #############最长路径#############
        if rear_end == 0 or len(rear_end_path)==0:
            #得用最长路径算法来追尾
            a_snake=a_star.a_star(new_snake.map,(head_x,head_y),(tail_x,tail_y),(w,h),judge,False)
            a_return,way_list = a_snake.start_run()
            rear_end_path.clear()
            operation.clear()
            for i in range(len(way_list)-1):
                #计算出具体操作
                rear_end_path.append(transform(way_list[i],way_list[i+1]))
            for i in range(len(rear_end_path)//2):
                operation.append(rear_end_path.pop(0))
            rear_end=1
        else:
            operation.clear()
            operation.append(rear_end_path.pop(0))
    else:
        #能吃到食物
        #计算路径 叫敢死队去吃,看看吃了还能不能看见尾巴
        operation.clear()
        for i in range(len(way_list)-1):
            #计算出具体操作
            operation.append(transform(way_list[i],way_list[i+1]))
        #如果是最后一个食物，可以直接去吃，不用派出虚拟蛇
        if not new_snake.pathless() == snake.CRD_FLOODING :

            #敢死队上阵
            #先拷贝拷贝
            operation_bak = copy.deepcopy(operation)
            new_snake_bak = copy.deepcopy(new_snake)
            for i in range(len(operation_bak)):
                dispose(new_snake_bak,operation_bak)
            #不出意外蛇已经跑完了 而且成功吃到了食物 查看是否找到尾巴
            bak_head_x,bak_head_y = new_snake_bak.get_head()
            bak_tail_x,bak_tail_y = new_snake_bak.get_tail()
            a_snake=a_star.a_star(new_snake_bak.map,(bak_head_x,bak_head_y),(bak_tail_x,bak_tail_y),(w,h),judge,True)
            a_return,way_list = a_snake.start_run()
            if a_return :
                #############最长路径#############
                if rear_end == 0 or len(rear_end_path)==0:
                    #不能找到尾巴 那就说明 这步走不得
                    #得用最长路径算法来追尾
                    a_snake=a_star.a_star(new_snake.map,(head_x,head_y),(tail_x,tail_y),(w,h),judge,False)
                    a_return,way_list = a_snake.start_run()
                    rear_end_path.clear()
                    operation.clear()
                    for i in range(len(way_list)-1):
                        #计算出具体操作
                        rear_end_path.append(transform(way_list[i],way_list[i+1]))
                    for i in range(len(rear_end_path)//2):
                        operation.append(rear_end_path.pop(0))
                    rear_end=1
                    #operation.clear()
                    #operation.append(transform(way_list[0],way_list[1]))
                        
                else:
                    operation.clear()
                    operation.append(rear_end_path.pop(0))
            else:
                #关掉追尾模式
                rear_end=0
                rear_end_path.clear()
        else:
            return 1





#main:
#进行一系列的初始化，且对snake模块设置好打印函数
new_snake=snake.snake(20,20,20)
new_snake.set_draw_function(draw_wall,draw_way,draw_head,draw_body,draw_tail,draw_food)
w,h=new_snake.get_window_WH()
rect_size,rect_w,rect_h=new_snake.get_rect_swh()
pygame.init()
screen = pygame.display.set_mode((w,h))
wall_image = pygame.image.load("./res/wall.png")
head_image = pygame.image.load("./res/head.png")
tail_image = pygame.image.load("./res/tail.png")
body_image = pygame.image.load("./res/body.png")
food_image = pygame.image.load("./res/food.png")
rect = pygame.Rect(0,0,rect_w,rect_h)
#开始寻路
while True:
    flag=0
    #如果没有指定路径那么就去寻找路径
    if len(operation) == 0:
        flag=Start_pathfinding(operation)

    for i in range(len(operation)):
        rungame(new_snake,operation)
        pygame.time.delay(5)
    if flag:
        break

print("恭喜满屏了")
exit(0)
