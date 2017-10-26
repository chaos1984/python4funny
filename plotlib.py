# -*- coding: utf-8 -*-
# 载入模块
import matplotlib.pyplot as plt
import pandas as pd


def plotfigure(bdffile):
	# 初始化
	node_loc = {}#节点位置
	node_dis = {}#节点位移

	# 读入网格信息
	for line in open(bdffile):
	    if 'GRID ' in line:
	        data = line.split()#分割数据
	        
	        node_loc[data[1]]=[float(line[(24+8*i):(32+8*i)]) for i in range(3)] #获得节点位置

	# 读入结果信息
	fo6file = bdffile.replace("bdf","f06")
	for line in open('ori.f06'):
	    if ' G ' in line:
	        data = line.split()#分割数据
	        node_dis[data[0]]=[float(i) for i in data[2:]]

	# 整理数据
	node_info =pd.concat([pd.DataFrame(node_loc,index=['X','Y','Z']).T,    \
		pd.DataFrame(node_dis,index=['T1','T2','T3','R1','R2','R3']).T],axis=1)

	# 绘图
	plt.figure()
	plt.gca().set_aspect('equal')
	plt.tricontourf(node_info.X,node_info.Y,node_info.T3,15)#绘图
	plt.colorbar()#显示色标
	plt.grid()#显示栅格
	plt.title('Z_DISP')#抬头
	plt.xlabel('X_LOC')#X坐标标签
	plt.ylabel('Y_LOC')#Y坐标标签
	plt.savefig("pic.jpg")
	#X = node_info.sort(columns='T3').X[0]#最小值的X坐标值
	#Y = node_info.sort(columns='T3').Y[0]#最小值的Y坐标值
	#plt.scatter(X,Y,color="black",marker = 'H')#绘制最小值的位置
	#string = 'Min=%7.5f' %(node_info.sort(columns='T3').T3[0])#显示内容
	#plt.text(X,Y,string)#图中输出最小值数值
	# plt.show()

if __name__ == '__main__':
	plotfigure("c:\Temp\NASTRAN\exa\ori.bdf")