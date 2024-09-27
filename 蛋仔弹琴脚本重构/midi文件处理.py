import os
import json
class midi文件处理类():
    def __init__(self):
        self.midi所在文件夹=os.path.dirname(os.path.abspath(__file__)) #当前文件的目录
        self.mid数据 = self.读文件夹下的一个midi文件(self.midi所在文件夹)
        self.time=0
    def 检查最多的连续的3个八度的键占所有键的百分比(self,百分比=0.9):
        '''
        检查连续的3个八度占全体的键的百分比
        '''
        使用所有的调的统计, 最小的调, 最大的调,最小音量,最大音量=self.预处理出调的情况()
        # 将调的数量存储在一个列表中，按调的顺序排列
        调列表 = [使用所有的调的统计[i] for i in sorted(使用所有的调的统计.keys())]
        # 计算总音符数量
        总音符数量 = sum(调列表)
        # 检查是否存在连续3个调，其音符数量占总音符数量的90%以上
        for i in range(len(调列表) - 2):
            # 取连续3个调的音符数量
            连续音符数量 = 调列表[i] + 调列表[i + 1] + 调列表[i + 2]
            # 检查比例是否超过阈值
            if 连续音符数量 / 总音符数量 >= 百分比:
                print(f"连续三个八度的键占比为：{连续音符数量 / 总音符数量:.2f}，从第{i+1}个八度开始")
                return True, i+1  # 返回True和连续3个调的编号（从1开始）

        return False, None  # 没有找到满足条件的连续3个调
    def 读文件夹下的一个midi文件(self,文件夹路径="."):
        '''
        返回一个同级目录下的mid文件
        '''
        import os
        import mido
        try:
            mid=None
            文件路径 = None
            for 文件名 in os.listdir(文件夹路径):
                if 文件名.endswith(".mid"):
                    文件路径 = os.path.join(文件夹路径, 文件名)
                    mid = mido.MidiFile(文件路径)
                    break
            if 文件路径:
                print(f"读取{文件夹路径}下的一个midi文件：{文件路径}")
            else:
                print(f"在{文件夹路径}中没有找到.mid文件")
            return mid
        except Exception as e:print("读取midi文件时发生错误",e)
        return None
    def 遍历mid文件(self,打印每行=False,策略='策略1'):
        '''
        遍历mid文件，默认遍历文件夹目录的一个midi文件，把对应的音符和时间返回到音乐时间轴，并转换为JSON格式
        '''
        音乐时间轴=[]
        if 策略=='策略1':
            # 策略1 每on算上当前on的时间，然后加上次off积累的时间，然后按这个键然后sleep这么久
            音乐时间轴 = self.策略1(打印每行)
            # 不转json
            return 音乐时间轴
        elif 策略=='策略2':
            # 策略2 音乐时间轴只有on的时间 sleepon的时间再调   off的时间直接sleep上
            音乐时间轴 = self.策略2(打印每行)
        # 将音乐时间轴转换为JSON格式
        json音乐时间轴str = json.dumps(音乐时间轴, ensure_ascii=False)
        return json音乐时间轴str
    def 预处理出调的情况(self):
        对应八度的字典 = {i: 0 for i in range(1, 10)}
        最小的调=9999
        最小音量=9999
        最大的调=0
        最大音量=0
        for 第几个轨道, 轨道 in enumerate(self.mid数据.tracks, start=0):
            for 第几个指令, 轨道内的指令 in enumerate(轨道):  # 每个音轨的消息遍历
                if hasattr(轨道内的指令, 'note'):
                    调 = 轨道内的指令.note
                    音量 = 轨道内的指令.velocity
                    对应八度的字典[int(调/12)]+=1 #从1开始
                    最大的调=max(最大的调,调)
                    最小的调=min(最小的调,调)
                    最大音量=max(最大音量,音量)
                    最小音量=min(最小音量,音量)
        return 对应八度的字典,最小的调,最大的调,最小音量,最大音量
    def 策略1(self,打印每行=False):
        '''
        策略：每on算上当前on的时间，然后加上次off积累的时间，然后按这个键然后sleep这么久
        '''
        音乐时间轴 = []
        ticks_per_beat = self.mid数据.ticks_per_beat
        tempo_microseconds = 500000  # 默认初始速度为500000微秒
        # 音乐时间轴 : 每个轨道 都有对应的调 和 弹的时间
        for 第几个轨道, 轨道 in enumerate(self.mid数据.tracks, start=0):
            睡时间=0
            音乐时间轴.append([])
            for 第几个指令, 轨道内的指令 in enumerate(轨道):  # 每个音轨的消息遍历
                # if 第几个指令 >= 500: break
                if 打印每行 == True: print(轨道内的指令)
                if hasattr(轨道内的指令, 'note'):
                    转换后的时间 = 轨道内的指令.time / ticks_per_beat * tempo_microseconds / 1000000
                    调是开还是关=轨道内的指令.type
                    调=轨道内的指令.note 
                    # 如果调是on并且有音量 则加入到音乐时间轴(要按的音符和时间)
                    if 调是开还是关 == 'note_on' and 轨道内的指令.velocity!=0:
                        音乐时间轴[第几个轨道].append((调,睡时间+转换后的时间))
                        睡时间 = 0
                    else:睡时间+=转换后的时间
        return [[(int(调), float(时间)) for 调, 时间 in 轨道] for 轨道 in 音乐时间轴]
    def 策略2(self,打印每行=False):
        # 策略：音乐时间轴只有on的时间 sleepon的时间再调   off的时间直接sleep上
        音乐时间轴 = []
        ticks_per_beat = self.mid数据.ticks_per_beat
        tempo_microseconds = 500000  # 默认初始速度为500000微秒
        # 音乐时间轴 : 每个轨道 都有对应的调 和 弹的时间
        for 第几个轨道, 轨道 in enumerate(self.mid数据.tracks, start=0):
            睡时间=0
            音乐时间轴.append([])

            for 第几个指令, 轨道内的指令 in enumerate(轨道):  # 每个音轨的消息遍历
                if 打印每行 == True: print(轨道内的指令)
                转换后的时间 = 轨道内的指令.time / ticks_per_beat * tempo_microseconds / 1000000
                if hasattr(轨道内的指令, 'note'):
                    调是开还是关=轨道内的指令.type
                    调=轨道内的指令.note
                    if 调是开还是关 == 'note_on' and 轨道内的指令.velocity!=0:
                        音乐时间轴[第几个轨道].append((调,睡时间+转换后的时间))
                        睡时间 = 0
                    else:睡时间+=转换后的时间
        return [[(int(调), float(时间)) for 调, 时间 in 轨道] for 轨道 in 音乐时间轴]
def 测试():
    # midi文件处理类 = midi文件处理类()
    # 使用所有的调的统计,最小的调,最大的调,最小音量,最大音量=midi文件处理类.预处理出调的情况()
    # 音乐时间轴=midi文件处理类.遍历mid文件(打印每行=True)
    # print('使用所有调的情况', 使用所有的调的统计,'\n最小的调', 最小的调,'\n最大的调', 最大的调,'\n最小音量', 最小音量,'\n最大音量', 最大音量)
    # print(音乐时间轴)
    print(midi文件处理类().检查最多的连续的3个八度的键占所有键的百分比())
    # midi处理 = midi文件处理类()
    # jsonstr音乐时间轴 = midi处理.遍历mid文件(打印每行=False)
    # print(jsonstr音乐时间轴)
    
if __name__=="__main__":
    测试()

