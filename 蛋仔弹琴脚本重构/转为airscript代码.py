import 坐标
import os
import midi文件处理
class 转airscript代码类:
    def __init__(self):
        self.坐标类=坐标.坐标类()
    def 处理弹琴代码(self,音乐时间轴=midi文件处理.midi文件处理类().遍历mid文件(),时间加速=1,八度映射=4,自动适配八度=True,手动适配元组=((4, 1), (4 + 1, 2),(4 + 2, 3))):
        头文件=self.头文件()
        总代码=头文件 
        if 自动适配八度==True:
            映射 = self.坐标类.设置第几个八度对应的低音1中音2高音3元组((八度映射,1),(八度映射+1, 2), (八度映射+2, 3) )#, (6, 3), (7, 3)
        else:
            映射 = self.坐标类.设置第几个八度对应的低音1中音2高音3元组(*手动适配元组)  # , (6, 3), (7, 3) 可以加多个参数
        # 坐标处理.找到note号对应的坐标(61, f)
        所有的任务=''
        for 第几个轨道,轨道 in enumerate(音乐时间轴,start=1):
            第几个线程任务=f'''def task{第几个轨道}():
    with concurrent.futures.ThreadPoolExecutor() as executor{第几个轨道}:
        pass
'''
            for 第几个音符,音符 in enumerate(轨道):
                调,时间=音符
                try:
                    坐标=self.坐标类.找到midi编号对应的坐标(调,映射)
                except:continue
                第几个线程任务+=f'        time.sleep({时间*时间加速})\n'
                第几个线程任务+=f'        executor{第几个轨道}.submit(click, {坐标[0]}, {坐标[1]})\n'
            所有的任务+=第几个线程任务
        总代码+=所有的任务
        总代码+=self.处理结尾()
        return 总代码
    def 处理结尾(self,结尾前字符串='',任务个数=1):
        总字符串=结尾前字符串
        for i in range(1, 任务个数 + 1):
            总字符串+=f'''thread{i} = threading.Thread(target=task{i})
thread{i}.start()
thread{i}.join()
'''
        return 总字符串
    def 测试点击某些坐标(self,时间=0.5):
        开头 = f'''def task1():
    with concurrent.futures.ThreadPoolExecutor() as executor1:
        pass
'''
        总代码 = self.头文件()+开头
        所有坐标 = self.坐标类.高音12坐标
        # 将数据处理成一个字典，方便后续处理
        for line in 所有坐标:
            总代码 += f'        time.sleep({时间})\n'
            总代码 += f'        executor1.submit(click, {line[0]}, {line[1]})\n'
        总代码+=self.处理结尾()
        return 总代码
    def 测试点击所有坐标(self,时间=0.5) :
        开头 = f'''def task1():
    with concurrent.futures.ThreadPoolExecutor() as executor1:
        pass
'''
        总代码 = self.头文件()+开头
        所有坐标 = self.坐标类.返回36键坐标从低音到高音()
        # 将数据处理成一个字典，方便后续处理
        for line in 所有坐标:
            总代码 += f'        time.sleep({时间})\n'
            总代码 += f'        executor1.submit(click, {line[0]}, {line[1]})\n'
        总代码+=self.处理结尾()
        return 总代码
    def 头文件(self):
        str='''import time
import threading
import concurrent.futures
from airscript.system import R
from airscript.action import click
from airscript.node import Selector
from airscript.screen import FindColors
from airscript.screen import CompareColors
from airscript.screen import FindImages
from airscript.screen import Ocr
'''
        return str
    def 输出到记事本(self,代码):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'转airscript代码.txt'), 'w', encoding='utf-8') as f:
            f.write(代码)
def 测试():
    转airscript代码测试类=转airscript代码类()
    # print(转airscript代码测试类.处理结尾(''))
    # 转airscript代码测试类.输出到记事本(转airscript代码测试类.测试点击所有坐标())
    # print('测试点击所有坐标测试完成')
    转airscript代码测试类.输出到记事本(转airscript代码测试类.处理弹琴代码())
    print('测试处理弹琴代码完成')
    # print('转airscript代码测试完成')
if __name__ == '__main__':
    测试()
    

