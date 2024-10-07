import cv2
import os
import numpy as np
from PIL import Image
import pyautogui

当前工作目录 = os.path.dirname(os.path.abspath(__file__))

def 读入文件夹下的第一张图片(当前文件夹='.'):
    # 获取当前路径下的一张图片
    图片目录 = os.path.join(当前工作目录, 当前文件夹)
    for 文件 in os.listdir(图片目录):
        if 文件.endswith('.png') or 文件.endswith('.jpg'):
            图片路径 = os.path.join(当前工作目录, 文件)
            print(f"尝试读取图片: {图片路径}")
            try:
                pil_image = Image.open(图片路径)
                image = np.array(pil_image)
                if image.shape[2] == 3:
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                print(f"成功读取图片，尺寸: {image.shape}")
                return image
            except Exception as e:
                print(f"无法读取图片: {图片路径}")
                print(f"错误: {e}")
                continue
    print("没有找到图片文件")
    return None

# 返回的是从左到右，从上到下的按键坐标列表 高音1中音1低音1 然后高音2中音2低音2 这样
def 检测所有音符按键(游戏截图=None,是否显示=False):
    if 游戏截图 is None:
        try:
            游戏截图 = 读入文件夹下的第一张图片()
        except Exception as e:
            print(f"无法读取图片: {e}")
            return None
    # 保存原始图片用于绘制
    原始图片 = 游戏截图.copy()
    # 二值化 阈值254
    游戏截图 = cv2.cvtColor(游戏截图, cv2.COLOR_BGR2GRAY)
    _, 游戏截图 = cv2.threshold(游戏截图, 250, 255, cv2.THRESH_BINARY)
    # 开运算内核15
    游戏截图 = cv2.morphologyEx(游戏截图, cv2.MORPH_OPEN, (15,15))
    # 闭运算内核15
    游戏截图 = cv2.morphologyEx(游戏截图, cv2.MORPH_CLOSE, (15,15))
    # print('显示cv2处理结果')
    # cv2.imshow('cv2处理结果', cv2.resize(游戏截图, (游戏截图.shape[1]//2, 游戏截图.shape[0]//2)))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # 轮廓检测
    轮廓, _ = cv2.findContours(游戏截图, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 存储所有符合条件的按键坐标
    按键坐标列表 = []
    # 遍历轮廓
    # print(f"检测到 {len(轮廓)} 个轮廓")
    for 轮廓 in 轮廓:
        # 获取轮廓的边界矩形
        x, y, w, h = cv2.boundingRect(轮廓)
        # 如果接近正方形，并且在图片下半部分
        if 0.8 < w/h < 1.2 and y > 游戏截图.shape[0]//2 and w*h > 1000:
            # 在原始图片上绘制红色矩形 
            cv2.rectangle(原始图片, (x, y), (x+w, y+h), (0, 0, 255), 2)
            # 将红色矩形中心坐标放进按键坐标列表
            按键坐标列表.append((x+w//2, y+h//2))
    print("一共读取到",len(按键坐标列表),"个按键")
    # 按照从左到右，从上到下的顺序排序坐标
    按键坐标列表.sort(key=lambda coord: (coord[0], coord[1]))
    
    # 获取屏幕尺寸
    屏幕宽度, 屏幕高度 = pyautogui.size()
    
    # 计算缩放比例
    宽度比例 = 屏幕宽度 / 原始图片.shape[1]
    高度比例 = 屏幕高度 / 原始图片.shape[0]
    缩放比例 = min(宽度比例, 高度比例) * 0.8  # 使用80%的屏幕空间
    
    # 计算新的尺寸
    新宽度 = int(原始图片.shape[1] * 缩放比例)
    新高度 = int(原始图片.shape[0] * 缩放比例)
    
    # 缩放图片
    显示图片 = cv2.resize(原始图片, (新宽度, 新高度))
    
    if 是否显示==True:
        # 显示结果
        cv2.imshow('检测结果', 显示图片)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return 按键坐标列表  # 返回绘制了矩形的原始大小图片和排序后的坐标列表

def 测试():
    游戏截图 = 读入文件夹下的第一张图片('.')  # 明确指定当前目录
    if 游戏截图 is not None:
        print(检测所有音符按键(游戏截图,是否显示=True))
    else:
        print("无法进行音符按键检测，因为没有有效的游戏截图")
    print('cv2检测所有音符按键测试完成，返回出了按键坐标列表')
if __name__ == '__main__':
    测试()
