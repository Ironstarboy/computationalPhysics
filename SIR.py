import numpy as np
import random
import matplotlib.pyplot as plt
import imageio
from myModule import io,plot
from tqdm import tqdm
plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题

def initSpace():
    space=[]
    for i in range(0, height):
        row = []
        for j in range(0, width):
            row.append(np.random.choice(
                [0, 1, 2],# S=0=易感者 I=1=感染者 R=2=康复人群
                p=[0.95, 0.05, 0]))  # 初始时三种状态随机
        space.append(row)
    return space

def countNeighbourState(x,y,mat,state):
    # 3*3摩尔型邻居
    # 计算当前元胞，它的邻居元胞状态为state状态的个数
    count=0
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if i<0 or i>=width or j <0 or j>=height:
                continue
            if not(i==x and j==y):
                if mat[i][j]==state:
                    count+=1
    return count

# 当前时刻元胞空间，按照规则,迭代出下一个时刻的元胞空间
def update(t0mat):
    height=len(t0mat)
    width=len(t0mat[0])
    t1mat=np.ones((height,width))

    for i in range(height):
        for j in range(width):
            # 当前元胞是0易感者，周围存在感染者1，以β概率对它进行感染，变成1
            t1mat[i][j]=t0mat[i][j]
            if \
                    t0mat[i][j]==0 and \
                    countNeighbourState(i,j,t0mat,state=1)>1 and \
                    random.random()<Beta:
                t1mat[i][j]=1
            # 1感染者每个时刻以概率γ痊愈，变成康复人群2
            if t0mat[i][j]==1 and random.random()<gamma:
                t1mat[i][j]=2
            # TODO 死亡概率呢
            # 康复人群2不会再被感染
    return t1mat

def iterTS(stateTS,T):
    stateTS[0]=initSpace()
    for t in range(1,T):
        t0mat=stateTS[t-1]
        t1mat=stateTS[t]
        stateTS[t]=update(t0mat)
    return stateTS

def plotCellSpace(stateTS):
    outPicDir='out\pic'
    io.mkDir(outPicDir)
    io.delFileByDir(outPicDir)

    for i in tqdm(range(len(stateTS))):
        stateSpace=stateTS[i]
        plot.savePlotMat(stateSpace,outPicDir,f'{i}.png')


def countNum(mat):
    # 计算单个元胞空间，各个状态元胞的数量
    height = len(mat)
    width = len(mat[0])
    num={
        '0':0,
        '1':0,
        '2':0
    }
    for i in range(height):
        for j in range(width):
            state=mat[i][j]
            if state==0:
                num['0']+=1
            elif state==1:
                num['1']+=1
            else:
                num['2']+=1
    return num

def getNumTS(matTS,T):
    num0TS=[]
    num1TS=[]
    num2TS=[]
    for t in range(T):
        mat=matTS[t]
        num=countNum(mat)
        num0TS.append(num['0'])
        num1TS.append(num['1'])
        num2TS.append(num['2'])
    return num0TS,num1TS,num2TS

def plotNum(matTS,T):
    num0TS, num1TS, num2TS=getNumTS(matTS,T)
    plt.plot(num0TS,label='易感者')
    plt.plot(num1TS, label='感染者')
    plt.plot(num2TS, label='康复人群')

    plt.legend()
    plt.title('SIR')
    plt.xlabel('time')
    plt.ylabel('人数')
    plt.show()

if __name__=='__main__':
    height=50
    width=50
    T=50
    stateTS=[0]*T
    Beta=0.75 # 感染指数
    gamma=0.35 # 痊愈指数


    stateTS=iterTS(stateTS,T)

    plotCellSpace(stateTS)
    plot.pngs2Gif()
    plotNum(stateTS,T)