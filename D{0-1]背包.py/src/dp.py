import numpy as np
import matplotlib.pyplot as plt
import time
import openpyxl

global profit
profit = []

global weight
weight = []
global prowei
prowei = []

global profitData
profitData = []

global weightData
weightData = []
global endMax
endMax = []
global pathList
pathList = []
global endPath
endPath = []

def getData():
    
    fileName = str(input('请输入文件名'))
    file = open('../' + fileName, 'r')
    line = file.readline()
    while (line):
      
        line = file.readline()
        if line.__contains__("profit"):
            line = file.readline().strip('\n').strip('.').strip(',')
            profitData.append(line)
        elif line.__contains__("weight"):
            line = file.readline().strip('\n').strip('.').strip(',')
            weightData.append(line)

    for group in range(len(profitData)):
        three_P_List = []
        three_W_List = []
        three_PW_List = []
        group_P_List = []
        group_W_List = []
        group_PW_List = []
        n = 0

        # 将每一组价值/重量数据按照逗号分组,两个列表分别用于存放每一组价值/重量数据分组后的结果
        proList = str(profitData[group]).split(',')
        weiList = str(weightData[group]).split(',')

        # 内层循环遍历上述分组后的每一组数据，将每组数据按照三元组/九元组进行存储
        for p in range(len(proList)):
            three_P_List.append(int(proList[p]))
            three_W_List.append(int(weiList[p]))
            three_PW_List.append(int(proList[p]) / int(weiList[p]))
            n = n + 1
            if n == 3:
                group_P_List.append(three_P_List)
                group_W_List.append(three_W_List)
                group_PW_List.append(three_P_List + three_W_List + three_PW_List)
                three_P_List = []
                three_W_List = []
                three_PW_List = []
                n = 0
        profit.append(group_P_List)
        weight.append(group_W_List)
        prowei.append(group_PW_List)
        global flagList
        flagList = profit
    return fileName


def show(n):
    pointXList = str(weightData[n]).split(',')
    pointYList = str(profitData[n]).split(',')
    plt.xlabel = ('weight')
    plt.ylabel = ('profit')
    plt.xlim(0, 3000)
    plt.ylim(0, 3000)
    color = '#6c3466'
    area = np.pi * 1 ** 1
    for point in range(len(pointXList)):
        plt.scatter(int(pointXList[point]), int(pointYList[point]), s=area, color=color)
    plt.show()

def sort(n):
    prowei[n].sort(key=lambda x: x[8], reverse=True)
    print(prowei[n])


# ============================回溯求解模块=================================
def huisu(num, maxWeight, x, y, totalP, totalW):  # 访问一个节点   x,y 计算当前价值
    if y != 3:
        totalP = totalP + profit[num][x][y]
        totalW = totalW + weight[num][x][y]
    if x == len(profit[num]) - 1:
        # 总价值和总重量
        if totalW > maxWeight:
            # print(totalP)
            pathList.append(totalP)
            return 0
        else:
            endMax.append(totalP)
            pathList.append(totalP)
        return 0
    else:
        for i in range(4):
            huisu(num, maxWeight, x + 1, i, totalP, totalW)
    return 0


# =============================打印路径模块====================================
def path(position, num):
    endMidPath = []
    str1 = ''
    for i in range(len(profit[num])):
        endMidPath.append(position % 4)
        # print(position%4)
        position = int(position / 4)
    endMidPath.reverse()
    for i in range(len(endMidPath)):
        if i == 0:
            str1 = str1 + '开始选择--->'
            # print('从根节点开始')
        elif endMidPath[i] != 3:
            str1 = str1 + str(profit[num][i][endMidPath[i]]) + '--->'
            # print('第' + str(i) + '个背包选择' + str(profit[num][i][endMidPath[i]]))
        else:
            str1 = str1 + '不做选择--->'
            # print('第' + str(i) + '个背包不选任何元素')
    print(str1.strip('--->'))
    endPath.append(str1.strip('--->'))


# ===============================动态规划求解模块=================================
def dp(num, maxWeight):
    l = []
    profitArr = []
    profitArr = profit[num]
    weightArr = []
    weightArr = weight[num]
    for i in range(maxWeight + 1):
        l.append(0)
    for i in range(len(profit[num])):
        for j in range(maxWeight, -1, -1):
            for k in range(3):
                if j >= weightArr[i][k]:
                    l[j] = max(l[j], l[j - weightArr[i][k]] + profitArr[i][k])
    print(l[maxWeight])


# =========================保存为txt=======================
def saveTxt(fileName, num, maxWeight, maxValue, sunTime):
    file = open('../查询结果.txt', 'a')
    file.write('文件名:\n' + fileName + '\n')
    file.write('第几组数据:\n' + str(num) + '\n')
    file.write('背包容量:\n' + str(maxWeight) + '\n')
    file.write('求解的最大价值:\n' + str(maxValue) + '\n')
    file.write('运行时间:\n' + str(sunTime) + 's\n')
    file.write('解向量:\n')
    for item in endPath:
        file.write(item + '\n')
    file.close()


# ========================主函数=======================
if __name__ == '__main__':
    fileName = getData()
    # 列表中包含若干个子列表，每个子列表包含一组数据的价值信息，每个子列表又包含若干个三元组列表，三元组列表记录了记录了该组数据每个项集
    print('数据读入完成！')
    print('价值信息：')
    for i in profit[0]:
        print(i)
    # 同价值信息，用于记录重量信息
    print('重量信息：')
    print(weight)
    # 列表包含若干子列表，一个子列表表示一组数据的价值-重量-价值重量比信息，子列表分为若干九元组。九元组记录了改组数据的价值-重量-价值重量比九条信息
    print('价值-重量-价值重量比信息：')
    print(prowei)
    while (True):
        x = int(input('请选择：\n1、画散点图\n2、非递增排序\n3、求解\n'))
        if x == 1:
            n = int(input('请选择对第几条数据做散点图'))
            show(n - 1)
            continue
        elif x == 2:
            n = int(input('请选择要对第几条数据进行排序'))
            sort(n - 1)
            continue
        elif x == 3:
            n = int(input('请选择算法\n1、回溯法\n2、动态规划算法\n'))
            num = int(input('请输入要求解第几组数据'))
            maxWeight = int(input('请输入背包容纳的最大重量'))
            if n == 1:
                profit[num - 1] = [[0, 0, 0]] + profit[num - 1]
                weight[num - 1] = [[0, 0, 0]] + weight[num - 1]
                for i in profit[0]:
                    print(i)
                time1 = time.time()
                huisu(num - 1, maxWeight, 0, 0, 0, 0)
                time2 = time.time()
                endMax.sort(reverse=True)
                print('最大价值：' + str(endMax[0]))
                print('运行时间：' + str(time2 - time1) + 's')
                for item in range(len(pathList)):
                    if pathList[item] == endMax[0]:
                        path(item, num - 1)
            elif n == 2:
                time1 = time.time()
                dp(num - 1, maxWeight)
                time2 = time.time()
                print(time2 - time1)
            x = int(input('请选择：\n1.保存为txt\n2.不保存'))
            if x == 1:
                saveTxt(fileName, num, maxWeight, endMax[0], time2 - time1)
            else:
                pass
        else:
            print('输入有误，请重新输入！')
            continue
