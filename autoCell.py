# 元胞状态：买入 持有 卖出 ，需要考虑量的问题，就是元胞属性多一个持有量
"""
元胞自动机 Python 实现
"""
import numpy as np
import random
import matplotlib.pyplot as plt
import imageio
from myModule import io


class Cell:
    # 元胞
    def __init__(self,state,x,y):
        # S=0=易感者 I=1=感染者 R=2=康复人群
        self.state=state
        self.x=x
        self.y=y

config={
    'Beta':0.75,
    'gamma':0.25
}

class CellularAutomation:
    HEIGHT=30
    WIDTH=30
    def __init__(self,height=HEIGHT,width=WIDTH):
        self.height=height
        self.width=width
        self.timer=0
        self.cellSpace =[]
        self.historySpace=[]

        # 当前元胞空间和历史元胞空间分别初始化，以保证地址不同。
        # python类里面默认拷贝对象，引用传递了
        for i in range(0,height):
            row=[]
            for j in range(0,width):
                row.append(Cell(np.random.choice([0, 1, 2], p = [0.95,0.05,0]),i,j))# 初始时三种状态随机
            self.cellSpace.append(row)

        for i in range(0, height):
            row = []
            for j in range(0, width):
                row.append(Cell(np.random.choice([0, 1, 2], p = [0.95,0.05,0]),i,j))
            self.historySpace.append(row)

    def mat2np(self):
        # cell矩阵转为numpy矩阵
        self.stateData = []
        for i in range(0, self.height):
            row=[]
            for j in range(0, self.width):
                row.append(self.cellSpace[i][j].state)
            self.stateData.append(row)

        self.stateData=np.array(self.stateData)
        # print(self.stateData)
        return self.stateData


    def countNeighbourState(self, currentCell:Cell, state):
        # 3x3摩尔型邻居
        # 计算当前元胞,邻居元胞状态为state状态的个数
        x=currentCell.x
        y=currentCell.y
        count=0
        for i in range(x-1, x+2):
            for j in range(y-1,y+2):
                if i<0 or i>=self.width or j<0 or j>=self.height:
                    continue
                if not (i==x and j==y) :
                    if self.historySpace[i][j].state==state:
                        count+=1
        return count

    def countStateCell(self,state):
        # 查询整个元胞空间，state元胞的数量
        ...

    def valueCopy(self,src,target):
        for i in range(0,self.height):
            for j in range(0,self.width):
                target[i][j].x=src[i][j].x
                target[i][j].y = src[i][j].y
                target[i][j].state = src[i][j].state


    def stateUpdate(self):
        # 判断当前元胞的状态，并根据规则更新状态
        # 演化规则
        self.valueCopy(src=self.cellSpace, target=self.historySpace)
        for i in range(0, self.height):
            for j in range(0, self.width):
                currenCell=self.cellSpace[i][j]
                historyCell=self.historySpace[i][j]

                # 当前元胞是0易感者，周围存在感染者1，以β概率对它进行感染，变成1
                if currenCell.state==0:
                    if self.countNeighbourState(historyCell,state=1)>0 and\
                            random.random()<config.get('Beta'):
                        currenCell.state=1
                # 1感染者每个时刻以概率γ痊愈，变成康复人群2
                if currenCell.state==1 and random.random()<config.get('gamma'):
                    currenCell.state=2
                # 康复人群2不会再被感染

        self.valueCopy(src=self.cellSpace, target=self.historySpace)
        self.timer+=1
        self.mat2np()


    def plot(self):
        # 画出当前状态
        plt.title("time {}".format(self.timer))

        plt.imshow(self.stateData)
        plt.show()


    def updateAndPlot(self,nIter):
        # self.mat2np()  # 0时刻
        # print()
        outPicDirPath = 'out\\pic'
        io.mkDir(outPicDirPath)
        io.delFileByDir(outPicDirPath)  # 先删除旧的文件
        pics=[]

        for i in range(nIter):
            self.stateUpdate()
            # print()
            pic=plt.imshow(self.stateData, cmap=plt.cm.hot,
                         vmin=0, vmax=1)
            plt.colorbar()
            plt.grid(True)
            # plt.show()
             # 画完一张重置图
            pics.append(pic)

            plt.savefig('{}\\{}.png'.format(outPicDirPath,i))
            plt.clf()

    def pngs2Gif(self):
        gif_images = []

        fileNameList= io.getFileNameList('out\\pic')
        fileNameList.sort(key=lambda x: int(x[0:x.index('.')])) # 按照数字大小排序，否则按照文字排序会错序
        for fileNameExt in fileNameList:

            gif_images.append(imageio.imread('out\\pic\\'+fileNameExt))  # 读取多张图片
        imageio.mimsave("out\\autocell.gif", gif_images, fps=5)  # 转化为gif动画
        print('gif done')

if __name__=='__main__':
    ca=CellularAutomation( 10,10)
    # ca.plot()
    ca.updateAndPlot(50)
    ca.pngs2Gif()