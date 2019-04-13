# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 10:48:40 2019

@author: jiefeng
"""

from numpy import *

def distance(a,b):
    #计算两个坐标间的距离
    dist=abs(a[0]-b[0])+abs(a[1]-b[1])
    return dist

class point:
    def __init__(self):
        self.position = [0,0]     # 名称
        self.F = 0     # 尺寸
        self.G = 0     # 列表
        self.H = 0
        self.father = [-1,-1]

#先定义MAP
#1表示不可走 0表示可以走
map=zeros([10,10],int16)
map[2,4]=1
map[3,4]=1
map[4,4]=1
map[5,4]=1
map[6,4]=1
map[2,5]=1
map[3,5]=1
map[4,5]=1
map[5,5]=1
map[6,5]=1


print(map)

#输入起点和终点
start_loc=[0,0]
end_loc=[0,0]

#起点
ok=1
while (ok==1):
    start_loc[1]=int(input("请输入起点的纵坐标:\n"))
    start_loc[0]=int(input("请输入起点的横坐标:\n"))
    if ((start_loc[0]<0)or(start_loc[0]>9)or(start_loc[1]<0)or(start_loc[1]>9)):
        #坐标越界
        print("该位置不能作为起点 请重新输入\n")
    else:
        if (map[start_loc[0],start_loc[1]]==1):
            #坐标定在了障碍物的位置
            print("该位置不能作为起点 请重新输入\n")
        else:
            ok=0

#终点
ok=1
while (ok==1):
    end_loc[1]=int(input("请输入终点的纵坐标:\n"))
    end_loc[0]=int(input("请输入终点的横坐标:\n"))
    if ((end_loc[0]<0)or(end_loc[0]>9)or(end_loc[1]<0)or(end_loc[1]>9)):
        #坐标越界
        print("该位置不能作为终点 请重新输入\n")
    else:
        if (map[end_loc[0],end_loc[1]]==1):
            #坐标定在了障碍物的位置
            print("该位置不能作为终点 请重新输入\n")
        else:
            ok=0


#创建开放列表和封闭列表
#并且设置两个矩阵记录该点有没有在封闭列表或者开放列表
isinopen=zeros([10,10],int16)
isinclose=zeros([10,10],int16)
#列表的每一个单位包括：该点的坐标 F值 G值 H值 父节点的坐标
start=point()
start.position[0]=start_loc[0]
start.position[1]=start_loc[1]

#将起点放入开放列表
openlist=[start]

isinopen[start.position[0],start.position[1]]=1

closelist=[]


while openlist!=[]:
    
    #首先 寻找当前节点 也就是开放列表中F最小的节点
    minF=10000
    index_min=0
    current=point()
    for i in range(len(openlist)):
        if (openlist[i].F<minF):
            minF=openlist[i].F
            index_min=i
            current=openlist[i]
        
    #至此成功得到当前节点
    #下面就要把当前节点从开放列表中删除，把它放进封闭列表
    #先删除
    del openlist[index_min]
    isinopen[current.position[0],current.position[1]]=0
    #再添加
    closelist.append(current)
    isinclose[current.position[0],current.position[1]]=1
    
    
    if isinclose[end_loc[0],end_loc[1]]==1:
        #终点节点被加入到封闭列表中
        break;
    
    
    #接下来对相邻的节点进行分析
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            
            #现在在处理的节点的坐标位置：
            temp_loc=[current.position[0]+i,current.position[1]+j]
            
            if (temp_loc[0]<0)or(temp_loc[0]>9)or(temp_loc[1]<0)or(temp_loc[1]>9):
                continue
            
            if ((i==0)and(j==0)):
                #碰到当前节点本身
                continue
            
            if map[temp_loc[0],temp_loc[1]]==1:
                #该节点不能通行
                continue
            
            if isinclose[temp_loc[0],temp_loc[1]]==1:
                #已经在封闭列表中
                continue
            
            if isinopen[temp_loc[0],temp_loc[1]]==1:
                #已经在开放列表当中了
                #计算当前节点到这个点的距离tempG
                if (i==0)or(j==0):
                    tempG=1+current.G
                else:
                    tempG=1.4+current.G
                #找到该节点在开放列表中的位置
                for ii in range(len(openlist)):
                    if openlist[ii].position==temp_loc:
                        break
                
                #更新G值和F值
                openlist[ii].G=tempG
                openlist[ii].F=openlist[ii].G+openlist[ii].H
                openlist[ii].father=current.position
            
            else:
                #还没在开放列表中
                temp=point()
                
                #设置坐标
                temp.position=[temp_loc[0],temp_loc[1]]
                #计算F G H
                if (i==0)or(j==0):
                    temp.G=1+current.G
                else:
                    temp.G=1.4+current.G
                
                temp.H=distance(end_loc,temp_loc)
                temp.F=temp.G+temp.H
                #把它的父节点设置为当前节点
                temp.father=current.position
                
                #添加至开放列表
                openlist.append(temp)
                isinopen[temp_loc[0],temp_loc[1]]=1
                continue
            



if isinclose[end_loc[0],end_loc[1]]==1:
    #说明找到了路径
    print("ok")
else:
    print("cannot reach")
        

#用result显示结果    
result=map
for i in range(len(map)):
    for j in range(len(map[0])):
        #起点
        if (i==start_loc[0])and(j==start_loc[1]):
            result[i,j]=1
            continue
        
        #终点
        if (i==end_loc[0])and(j==end_loc[1]):
            result[i,j]=3
            continue
        
        #障碍物
        if map[i,j]==1:
            result[i,j]=4
            continue
        
        #通路
        if isinclose[i,j]==1:
            result[i,j]=2
            continue
        
print(result)
            
        
                
            
    





































