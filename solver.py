# pylint: skip-file
from tetris import play_tetris
from tetris_write import play_tetris as tetris_write
import random
import copy
import glob
import math
import numpy
import threading
from msvcrt import getch
import os
from time import sleep

class GeneticAlgorithm:
    def __init__(self):
        self._gdata = [[[random.randint(1, 10) * ((-1) ** random.randint(1, 2)) for k in range(10)] for i in range(5)] for j in range(100)]
        for k in range(len(self._gdata)):
            for i in range(len(self._gdata[k])):
                for j in range(len(self._gdata[k][i])):
                    if self._gdata[k][i][j] > 0:
                        if random.randint(0, 1) == 0:
                            self._gdata[k][i][j] = self._gdata[k][i][j] * (-1)
        self._generation = 0
        self._gscore = []

    def genomData(self, i):
        return self._gdata[i]
    def genomScore(self, score, j):
        if j == 0:
            self._gscore.append(score**2)
        elif j == 1:
            self._gscore[-1] = int((self._gscore[-1] + score**2)/2)

    def crossOver(self):
        sum_gscore = sum(self._gscore)
        self._ndata = []
        for k in range(100):
            i, j = random.randint(0, sum_gscore), random.randint(0, sum_gscore)
            do = 0
            if j < i:
                i, j = j, i
            if i >= sum_gscore - self._gscore[-1]:
                i -= self._gscore[-2]
            for l in range(100):
                score = self._gscore[l]
                j -= score
                i -= score
                if j <= 0:
                    for y in range(5):
                        for x in range(10):
                            if random.randint(0, 1) == 0:
                                self._genom[y][x] = self._gdata[l][y][x]
                    break
                elif i <= 0:
                    if do == 0:
                        self._genom = copy.deepcopy(self._gdata[l])
                        do = 1
            self._ndata.append(self._genom)
        self._gdata = copy.deepcopy(self._ndata)
        for i in range(50):#突然変異
            self._gdata[random.randint(0, 99)][random.randint(0, 4)][random.randint(0, 9)] = random.randint(1, 10) * (-1)
        self._gscore = []

    def showBestGenom(self, i, file_name):
        genom_data = self._gdata[self._gscore.index(max(self._gscore))]
        with open(file_name, 'a') as f:
            f.write('第{}世代：'.format(i) + str(genom_data) + '\n')
        print('\007')
        #tetris_write(genom_data, i)

#インプットスレッド
class InputThread(threading.Thread):
    def __init__(self):
        super(InputThread, self).__init__()
        self._cmd = 110

    def run(self):
        while True:
            key = ord(getch())
            if key != 0:
                self._cmd = key
            elif key == 113:
                break

    def getCmd(self):
        return self._cmd

    def resetCmd(self):
        self._cmd = 110

def make_genomlog():
    file_list = glob.glob('.\\**', recursive = True)
    #.pyを検索
    python_file = []
    genom_log_list = 0
    for x in file_list:
        if 'genom_log' in x:
            for i in range(len(x)):
                try:
                    python_file.append(int(x[i]))
                except:
                    pass
    if python_file == []:
        python_file = [0]
    i = 0
    while True:
        i += 1
        if not i in python_file:
            genom_log_list = i
            break
    file_name = 'genom_log{}.txt'.format(genom_log_list)
    with open(file_name, 'w') as f:
        f.write('')
    return file_name

def main():
    file_name = make_genomlog()
    ga = GeneticAlgorithm()
    th = InputThread()
    th.start()#キーボード入力で中断をなくすにはこれをコメントアウト and 下の"inputThreading"を全部コメントアウト
    num = 0
    while True:
        num += 1
        print(num)
        for i in range(100):
            for j in range(2):
                ga.genomScore(play_tetris(ga.genomData(i)), j)
                #inputThreading
                if th.getCmd() != 110:
                    print('interruption')
                    while True:
                        sleep(1)
                        if th.getCmd() == 112:
                            os.system('cls')
                            print('restart')
                            print(num)
                            break
                th.resetCmd()
                #ここまで
        ga.showBestGenom(num, file_name)
        if num == 50:
            break
        ga.crossOver()

if __name__ == '__main__':
    main()

#lines in total : 907