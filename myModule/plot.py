import matplotlib.pyplot as plt
import imageio
from myModule import io

def savePlotMat(mat, outDir,fileName):
    plt.matshow(mat)
    plt.savefig(f'{outDir}\\{fileName}')
    plt.clf()
    plt.close()


def pngs2Gif():
    gif_images = []

    fileNameList= io.getFileNameList('out\\pic')
    fileNameList.sort(key=lambda x: int(x[0:x.index('.')])) # 按照数字大小排序，否则按照文字排序会错序
    for fileNameExt in fileNameList:

        gif_images.append(imageio.imread('out\\pic\\'+fileNameExt))  # 读取多张图片
    imageio.mimsave("out\\autocell.gif", gif_images, fps=5)  # 转化为gif动画
    print('gif done')