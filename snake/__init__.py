####################################
##作者：simon （彭洋明）
##起始时间：2020.4.14
##修改时间：2020.4.17
##版权所有：Copyright©2019-2020 小明之家 
####################################
import numpy as np
import random


######
WAY             = 0     #道路
BARRIER         = 1     #障碍
HEAD            = 2     #蛇头
BODY            = 3     #蛇身
TAIL            = 4     #蛇尾
FOOD            = 5     #食物


H_UP            = 0     #向上
H_DOWN          = 1     #向下
H_LEFT          = 2     #向左
H_RIGHT         = 3     #向右


CRD_WAY         = 0     #碰撞道路
CRD_BAB         = 1     #会死（碰到蛇身和障碍)
CRD_FOOD        = 2     #碰到食物
CRD_FLOODING    = 3     #满屏
######




################################################
#描述窗口的一些属性信息，比如窗口大小，方格大小
################################################
class properties_window:
    def __init__(self,grid_size=5,width=20,length=20):
        self.__grid_size=grid_size
        self.__width=width
        self.__length=length
    def get_properties(self):
        return self.__grid_size,self.__width,self.__length






################################################
#贪吃蛇的类
################################################
class snake:
    
    ############################################
    #返回方块像素多少、虚拟宽度、虚拟长度
    ############################################
    def get_rect_swh(self):
        return self.__properties_window.get_properties()



    ############################################
    #设置绘制函数 图形接口
    ############################################
    def set_draw_function(self,draw_wall,draw_way,draw_head,draw_body,draw_tail,draw_food):
        self.draw_wall=draw_wall
        self.draw_way=draw_way
        self.draw_head=draw_head
        self.draw_body=draw_body
        self.draw_tail=draw_tail
        self.draw_food=draw_food



    ############################################
    #调用外部函数来画方块
    #道路 围墙 蛇 食物
    ############################################
    def fill(self):
        size,w,h=self.__properties_window.get_properties()
        for x in range(w):
            x1=x*size
            for y in range(h):
                attribute=self.get_attribute(x,y)
                y1=y*size
                if   attribute == WAY:
                    self.draw_way(x1,y1)
                elif attribute == BODY:
                    self.draw_body(x1,y1)
                elif attribute== BARRIER:
                    self.draw_wall(x1,y1)
                elif attribute== HEAD:
                    self.draw_head(x1,y1)
                elif attribute== TAIL:
                    self.draw_tail(x1,y1)
                elif attribute== FOOD:
                    self.draw_food(x1,y1)

    def set_attribute(self,x,y,attribute):
        self.map[y][x] = attribute




    ############################################
    #获得地图方块属性
    #@x :要获得方块的x坐标
    #@y :要获得方块的y坐标
    ############################################
    def get_attribute(self,x,y):
        return self.map[y][x]




    ############################################
    #碰撞检测
    #@x :要检测方块的x坐标
    #@y :要检测方块的y坐标
    #return:
    #CRD_WAY        :一切正常
    #CRD_BAB = 1    :吃到围墙或者自己
    #CRD_FOOD= 2    :吃到食物
    ############################################
    def crd(self,x,y):
        a=self.get_attribute(x,y)
        if a==WAY or a==TAIL:
        #道路
            return CRD_WAY
        elif a==BARRIER or HEAD==a or a==BODY  :
        #吃到自己或者撞到障碍
            return CRD_BAB
        else:
        #吃到食物 
            return CRD_FOOD




    ############################################
    #获取尾的坐标
    ############################################
    def get_tail(self):
        tail_inde=0
        tail_x=self.snake[tail_inde][0]
        tail_y=self.snake[tail_inde][1]
        return  tail_x,tail_y




    ############################################
    #获取头的坐标
    ############################################
    def get_head(self):
        head_inde=self.len-1
        head_x=self.snake[head_inde][0]
        head_y=self.snake[head_inde][1]
        return head_x,head_y


    ############################################
    #移动时删尾操作
    ############################################
    def del_tail(self):
        #获取当前的尾巴
        del_x,del_y=self.get_tail()
        self.set_attribute(del_x,del_y,WAY)
        #删除当前的尾巴
        self.snake.pop(0)
        #形成新的尾巴
        new_x,new_y=self.get_tail()
        self.set_attribute(new_x,new_y,TAIL)
        self.len-=1




    ############################################
    #移动时加头操作
    ############################################
    def add_head(self,x,y):
        #旧头变身子
        worn_head_x,worn_head_y=self.get_head()
        self.set_attribute(worn_head_x,worn_head_y,BODY)
        #形成新头
        self.snake.append([x,y])        #加头
        self.set_attribute(x,y,HEAD)
        self.len+=1





    ############################################
    #依附于移动函数的子函数
    ############################################
    def child_move(self,crd_return,x,y):
        head_x,head_y=self.get_head()

        if crd_return == CRD_WAY:
            #未吃到食物
            self.del_tail()
            self.add_head(x,y)
        else:
            #吃到食物的情况
            self.add_head(x,y)
            return self.rand_food()

    #获取方向 
    def set_direction(self):
        return self.direction

    #设置方向
    def set_direction(self,direction):
        self.direction=direction

    ############################################
    #移动函数
    #根据方向信息进行移动
    #且返回移动结果
    #return:
    #CRD_WAY        :一切正常
    #CRD_BAB = 1    :吃到围墙或者自己
    #CRD_FOOD= 2    :吃到食物 （已经自动生成食物，返回可以做成绩处理）
    ############################################
    def move(self):
        head_x,head_y=self.get_head()
        if self.direction==H_UP:
            #向上
            new_head_x=head_x
            new_head_y=head_y-1
        elif self.direction==H_DOWN:
            #向下
            new_head_x=head_x
            new_head_y=head_y+1
        elif self.direction==H_LEFT:
            #向左
            new_head_x=head_x-1
            new_head_y=head_y
        elif self.direction==H_RIGHT:
            #向右
            new_head_x=head_x+1
            new_head_y=head_y
           
        crd_return=self.crd(new_head_x,new_head_y)
        if crd_return==CRD_BAB:
            #死亡直接返回
            return CRD_BAB
        if self.child_move(crd_return,new_head_x,new_head_y)== CRD_FLOODING:
            return CRD_FLOODING
        return crd_return


    #满屏判断
    def pathless(self):
        flag=1
        s,w,h=self.__properties_window.get_properties()
        for x in range(w):
            for y in range(h):
                if self.get_attribute(x,y) ==WAY :
                    flag=0
        if flag :
            return CRD_FLOODING



    ############################################
    #自动生成食物函数
    #跳过障碍物生成
    #return:
    #CRD_FLOODING   满屏
    ############################################
    def rand_food(self):
        #先查看是否还有道路
        if self.pathless() == CRD_FLOODING:
            return CRD_FLOODING
        grid_size,width,length=self.__properties_window.get_properties()
        while True:
            a=random.randint(1,width-2)
            b=random.randint(1,length-2)
            if  self.get_attribute(a,b)==WAY:
                break
        self.food=[a,b]
        self.set_attribute(a,b,FOOD)
     



    ############################################
    #进行地图的初始化
    #1.围墙的生成
    #2.随机食物的生成
    #3.小蛇的生成
    ############################################
    #初始地图生成器
    def _map_generation(self,width,length):
        #生成一个这么大的地图
        self.map=np.zeros((length,width),dtype=np.int)
        #设置围墙
        for i in range(width):
            self.set_attribute(i,0,BARRIER)
            self.set_attribute(i,length-1,BARRIER)
        for i in range(length):
            self.set_attribute(0,i,BARRIER)
            self.set_attribute(width-1,i,BARRIER)
        #设置小蛇 蛇头在后面可以提高效率
        self.snake=[]
        self.snake.append([width//2,length//2+2])   #蛇尾  
        self.snake.append([width//2,length//2+1])  #生成蛇身
        self.snake.append([width//2,length//2])  #生成蛇头
        #在地图中标记小蛇
        x1=self.snake[2][0]
        y1=self.snake[2][1]
        x2=self.snake[1][0]
        y2=self.snake[1][1]
        x3=self.snake[0][0]
        y3=self.snake[0][1]
        self.set_attribute(x1,y1,HEAD)
        self.set_attribute(x2,y2,BODY)
        self.set_attribute(x3,y3,TAIL)
        self.len=3
        #随机生成食物
        self.rand_food()
             



    ############################################
    #返回真实的窗口大小
    ############################################
    def get_window_WH(self):
        size,W_n,H_n=self.__properties_window.get_properties()
        return W_n*size,H_n*size
         



    ############################################
    #初始化函数
    #@grid_size :每个方格的边长占用方格数
    #@width     ：x方向的方格数    
    #@length    ：y方向的方格数
    ############################################
    def __init__(self,grid_size,width,length):
        #参数检查
        if width<5 or length<5:
            width   =5
            length  =5
        #初始化像素占用信息等信息
        self.__properties_window=properties_window(grid_size,width,length)
        self.direction=H_UP   #默认向上
        #生成二维地图（蛇的生成，围墙的生成，食物的生成）
        self._map_generation(width,length)