####################################
##作者：simon （彭洋明）
##起始时间：2020.4.15
##修改时间：2020.4.16
##版权所有：Copyright©2019-2020 小明之家 
####################################
#####################################
#本类用于计算图类最长路径和最短路径
#本类是一个通用类，可利用函数指针的概念来实现多态
#####################################


class a_star:
    ####################################
    #距离计算
    #@n_xy  :节点n的xy坐标
    #h(n) 是从状态n到目标状态的最佳路径的估计代价。
    #return :
    #返回估算路径 后面当优先级使用
    ####################################
    def h(self,n_xy):
        h_n=abs(n_xy[0]-self.end[0])+abs(n_xy[1]-self.end[1])
        return h_n


    ####################################
    #构造函数
    #@map   :地图对象
    #@start :开始坐标
    #@end   :寻找目标
    #@w_h   :map地图范围
    #@judge :函数指针参数为坐标，用于判断该坐标是否可通 如果返回Ture 说明是可以走通的 
    #@flag  :为真时启用最短路径查找，为假时启用最长路径查找
    ####################################
    def __init__(self,map,start,end,w_h,judge,flag):
        self.map    =map
        self.start  =start
        self.end    =end
        self.w_h    =w_h
        self.judge  =judge
        self.flag   =flag
        self.open   =[]    #保存所有已生成而未考察的节点
        self.closed =[]  #记录已访问过的节点

        #保存第一个节点  |坐标|h_n|g_n|父节点|
        one=[start,self.h(start),0,None]
        self.open.append(one)



    ####################################
    #返回open表中最合适的节点
    #return:
    #-1,None    该表已空
    # 0,inode   成功
    ####################################
    def _fit_inode(self):
        if not len(self.open):
            return -1,None
        return 0,self.open.pop(0)




    def inode_fn(self,site):
        return self.open[site][1]+self.open[site][2]
    ####################################
    #添加节点进open表
    #@xy        :节点坐标
    #@parent    :父节点
    ####################################
    def add_open(self,xy,parent):
        x=xy[0]
        y=xy[1]
        i = [(x,y),self.h((x,y)),parent[2]+1,parent]
        f_n=i[1]+i[2]
        #节点是否为终点
        if x==self.end[0] and y==self.end[1]:
            #直接加入open表
            #插入在合适的位置
            site=0
            for _site in  range(len(self.open)):
                site=_site
                if f_n <= self.inode_fn(site):
                    self.open.insert(site,i)
                    return
            #如果此时还没有插入 那么说明此时的fn是最大的
            self.open.append(i)
            return 
        #节点是否越界
        if x<0 or x>=self.w_h[0] or y<0 or y>=self.w_h[1] :
            return
        #节点处是否有障碍
        if not self.judge(self.map,x,y):
            return 
        #节点是否已经遍历
        for inode in self.closed :
            if x==inode[0][0] and y==inode[0][1]:
                return 
        for inode in self.open:
            if x==inode[0][0] and y==inode[0][1]:
                return 
        #正式加入open表
        
        #如果open表为空
        if not len(self.open) :
            self.open.append(i)
            return 
        #插入在合适的位置
        site=0
        for _site in  range(len(self.open)):
            site=_site
            if f_n <= self.inode_fn(site):
                self.open.insert(site,i)
                return
        #如果此时还没有插入 那么说明此时的fn是最大的
        self.open.append(i)
            




    






    ####################################
    #查找周围的可用的子节点，加入open表，且算出f(n)值设置父节点
    #parent |坐标|h_n|g_n|父节点|
    ####################################
    def find_neighbours(self,parent):
        #上
        up=(parent[0][0],parent[0][1]-1)
        #下
        down=(parent[0][0],parent[0][1]+1)
        #左
        left=(parent[0][0]-1,parent[0][1])
        #右
        right=(parent[0][0]+1,parent[0][1])
        #添加
        self.add_open(up,parent)
        self.add_open(down,parent)
        self.add_open(left,parent)
        self.add_open(right,parent)

        
        
    def __path_extension_judge(self,way_list,a,b):
        for inode in way_list:
            if inode==a or inode==b:
                return False
        if self.judge(self.map,a[0],a[1]) and self.judge(self.map,b[0],b[1]):
            return True

        return False
        


    def _path_extension(self,way_list):
        while True:
            for i in range(len(way_list)-1):
                a=way_list[i]
                b=way_list[i+1]
                if a[0]==b[0]:
                    #上下关系
                    #左右+1
                    #右
                    r1=(a[0]+1,a[1])
                    r2=(b[0]+1,b[1])
                    l1=(a[0]-1,a[1])
                    l2=(b[0]-1,b[1])
                    if self.__path_extension_judge(way_list,r1,r2):
                        way_list.insert(i+1,r2)
                        way_list.insert(i+1,r1)
                        break 
                    if self.__path_extension_judge(way_list,l1,l2):
                        way_list.insert(i+1,l2)
                        way_list.insert(i+1,l1)
                        break
                else:
                    #左右关系
                    #上下+1
                    u1=(a[0],a[1]-1)
                    u2=(b[0],b[1]-1)
                    d1=(a[0],a[1]+1)
                    d2=(b[0],b[1]+1)
                    if self.__path_extension_judge(way_list,u1,u2):
                        way_list.insert(i+1,u2)
                        way_list.insert(i+1,u1)
                        break 
                    if self.__path_extension_judge(way_list,d1,d2):
                        way_list.insert(i+1,d2)
                        way_list.insert(i+1,d1)
                        break
            if i == len(way_list)-2 :
                return 


    ####################################
    #一切准备就绪
    #开始进行A*算法计算
    #return : 两个返回值
    #0 ,    <llist>    1.返回0 表示寻找成功  2.<list>是路径
    #1 ，    None      1.寻路失败            2.空
    ####################################
    def start_run(self):
        while True:
            #从open表中取出最优节点
            fit_return,inode=self._fit_inode()
            if fit_return == -1 :
                break
            #如果该节点是终点，则寻路成功
            if inode[0] == self.end :
                break
            #将当前节点的的子节点更新在open表，设置好父节点，f(n) @@@注意避开close表中已经遍历的节点和路障
            self.find_neighbours(inode)
            #将当前节点放入close表
            self.closed.append(inode)
        #print("结束")
        #如果fit_return == -1 那就说明没找到
        if fit_return==-1 :
            return 1,None

        way_list=[]
        while not inode==None :
            way_list.append(inode[0])
            inode=inode[3]
        way_list.reverse()
        #此时已经算出了最短路径
        #如果外部需要最长路径，那么就用扩展法扩展为最长路径（但是 不是最优解）
        if self.flag == False:
            self._path_extension(way_list)
        return 0,way_list



