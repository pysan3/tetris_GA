import random
import time
from time import sleep
import os
import copy
import numpy as np
from operator import itemgetter

BLOCKS_COORD_list = [
    [[1, 1], [2, 0], [2, 1], [2, 2]], #T
    [[1, 0], [1, 1], [2, 1], [2, 2]], #Z
    [[1, 1], [1, 2], [2, 0], [2, 1]], #S
    [[1, 0], [1, 1], [1, 2], [1, 3]], #I
    [[1, 1], [1, 2], [2, 1], [2, 2]], #O
    [[1, 1], [2, 1], [2, 2], [2, 3]], #J
    [[1, 2], [2, 0], [2, 1], [2, 2]]  #L
]

BLOCKS_COORD = tuple(tuple(tuple(x) for x in y) for y in BLOCKS_COORD_list)

#ディスプレイ消去
def displayClear():
    os.system('cls')

#フィールド作成
class Field:
    def __init__(self):
        self._height = 21
        self._width = 12
        self._delete_line = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        self._score = 0
        self._box = []
        for _ in range(4):
            self._box.append([])

    def _write(self):
        for _ in range(len(self._field)+1):
            print('\033[A\033[K', end = '')
        print(self._score)
        text = ''
        for line in self._field:
            for l in line:
                if l == 0:
                    text += '□'
                else:
                    text += '■'
            text += '\n'
        print(text, end = '')
        sleep(0.1)

    def field(self):
        return self._field

    def makeField(self):
        self._field = []
        for y in range(self._height):
            self._field.append([])
            for x in range(self._width):
                if x == 0 or x == self._width-1 or y == self._height-1:
                    self._field[y].append(2)
                else:
                    self._field[y].append(0)

    def updateField(self, b_shape, no_change):
        self._block = copy.deepcopy(b_shape[2])
        self._fieldCopy = copy.deepcopy(self._field)
        for i in range(len(self._block)):
            self._block[i] = [b_shape[0]+self._block[i][0], b_shape[1]+self._block[i][1]]
        for i in range(len(self._block)):
            self._field[self._block[i][0]][self._block[i][1]] = 1
        self._write()
        if no_change:
            self._field = copy.deepcopy(self._fieldCopy)

    def lineClear(self):
        counter = 0
        for y in range(len(self._field)):
            if self._field[y] == self._delete_line:
                counter += 1
        self._score += counter ** 2
        for y in range(len(self._field)):
            if self._field[y] == self._delete_line:
                self._field.pop(y)
                self._field.insert(0, [])
                for _ in range(self._width):
                    self._field[0].append(0)
                self._field[0][0], self._field[0][-1] = 2, 2
        if counter >= 1:
            self._write()

    def areBlock(self):
        for i in range(self._width):
            if self._field[3][i] == 1:
                return True
        return False

class Current:
    def __init__(self):
        pass

    def reset_vals(self):
        self._x = 0
        self._y = 0

    def blockType(self):
        self._blocknum = self._nextnum
        self._block = list(BLOCKS_COORD[self._blocknum])
        return self._blocknum
    def nextBlock(self):
        self._nextnum = random.randint(0, 6)
        self._block = list(BLOCKS_COORD[self._nextnum])
        return self._nextnum

    def rotate(self, moves):
        self._x += moves[0]
        num = moves[1]
        if num == 1:
            for i in range(len(self._block)):
                self._block[i] = [3 - self._block[i][1], self._block[i][0]]
        elif num == 2:
            for i in range(len(self._block)):
                self._block[i] = [3 - self._block[i][0], 3 - self._block[i][1]]
        elif num == 3:
            for i in range(len(self._block)):
                self._block[i] = [self._block[i][1], 3 - self._block[i][0]]

    def fit(self, f_shape):
        self._field = f_shape
        self._max = []
        list_x = []
        for x in range(12):
            for y in range(len(self._field)):
                if self._field[y][x] >= 1:
                    self._max.append(y)
                    break
        for i in range(len(self._block)):
            list_x.append(self._max[self._x + self._block[i][1]] - self._block[i][0] - 1)
        self._y = min(list_x)
        return [self._y, self._x, self._block]

    def print_field(self, generation):
        if generation != 0:
            generation = abs(generation) + 1
        for i in range(30):
            print('\033[K\033[A', end = '')
        print('第%d世代' % generation)
        text = ''
        for i in range(4):
            for j in range(4):
                if (i, j) in BLOCKS_COORD[self._nextnum]:
                    text += '■'
                else:
                    text += '□'
            text += '\n'
        print(text)
        for i in range(21):
            print('')

    def blockShape(self):
        return [self._y, self._x, self._block]

class FieldMaker:
    def __init__(self, f_shape):
        self.f_shape = f_shape
        self._delete_line = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        self._best = [-10**9, [5, 5]]
        #self._best = [score, [self._movex, self._rotate]]

    def best(self, score, movex, rotate):
        if score >= self._best[0]:
            self._best = [score, [movex, rotate]]

    def returnbest(self):
        return self._best[1]

    def _rotate(self, movex, num):
        if num == 1:
            for i in range(len(self._block)):
                self._block[i] = [3 - self._block[i][1], self._block[i][0]]
        elif num == 2:
            for i in range(len(self._block)):
                self._block[i] = [3 - self._block[i][0], 3 - self._block[i][1]]
        elif num == 3:
            for i in range(len(self._block)):
                self._block[i] = [self._block[i][1], 3 - self._block[i][0]]
        l = []
        for i in range(len(self._block)):
            if (self._block[i][1] + movex) >= 11 or (self._block[i][1] + movex) == 0:
                l = [0]
                return l
        for i in range(4):
            for y in range(21):
                if self.f_block[y + self._block[i][0]][self._block[i][1] + movex] >= 1:
                    l.append(y)
                    break
        return l

    def resetBlock(self, b_type, movex, rotate):
        self.f_block = copy.deepcopy(self.f_shape)
        self._block = list(BLOCKS_COORD[b_type])
        l = self._rotate(movex, rotate)
        if len(l) != 4:
            return True
        elif b_type == 0:
            pass
        elif b_type <= 3:
            if rotate >= 2:
                return True
        elif b_type == 4:
            if rotate != 0:
                return True
        alpha = min(l)
        for i in range(4):
            self.f_block[alpha + self._block[i][0] - 1][movex + self._block[i][1]] = 1
        return False

    def resetNext(self, n_type, n_movex, n_rotate):
        self.f_next = copy.deepcopy(self.f_block)
        self._block = list(BLOCKS_COORD[n_type])
        l = self._rotate(n_movex, n_rotate)
        if len(l) != 4:
            return True
        elif n_type == 0:
            pass
        elif n_type <= 3:
            if n_rotate >= 2:
                return True
        elif n_type == 4:
            if n_rotate != 0:
                return True
        self._alpha = min(l)
        for i in range(4):
            self.f_next[self._alpha + self._block[i][0]-1][n_movex + self._block[i][1]] = 1
        return False

    def info(self):
        self._info = []
        self._LandingHeight()#直前のブロックの高さ
        self._ErodedPieceCells()#消えたライン数 * 直前のブロックの消えたライン数
        self._RowTransition()#隣の行と内容が違う行数
        self._ColTransition()#隣の列と内容が違う列数
        self._NumHoles()#穴の数、穴の深さの和、穴のある列数
        self._CulmulativeWells()#井戸の高さの和
        self._ExternalCols()#平均の高さとの差が4以上ある列数
        self._MaxHeight()#最大の高さ
        return self._info

    def _LandingHeight(self):
        self._block.sort(key=itemgetter(0))
        self._info.append(abs(self._block[0][0] - self._block[3][0]))#直前のブロックの高さ

    def _ErodedPieceCells(self):
        counter, block_counter = 0, 0
        for y in range(21):
            if self.f_next[y] == self._delete_line:
                counter += 1
                for i in range(4):
                    if self._alpha + self._block[i][0] == y + 1:
                        block_counter += 1
        self._info.append(counter * block_counter)

    def _RowTransition(self):
        counter = 0
        for y in range(20):
            for x in range(1, 10):
                if self.f_next[y][x] != self.f_next[y][x+1]:
                    counter += 1
        self._info.append(counter)
    def _ColTransition(self):
        counter = 0
        for x in range(1, 11):
            for y in range(19):
                if self.f_next[y][x] != self.f_next[y+1][x]:
                    counter += 1
        self._info.append(counter)

    def _NumHoles(self):
        counter = 0
        hole_depth = []
        row_with_holes = 0
        self._height = []
        for x in range(1, 11):
            current = 0
            for y in range(21):
                if self.f_next[y][x] == 1 and current == 0:
                    current = 1
                    height = y
                    self._height.append(y)
                elif self.f_next[y][x] == 0 and current == 1:
                    counter += 1
                    hole_depth.append(y - height)
                    row_with_holes += 1
                elif y == 20 and current == 0:
                    self._height.append(20)
        self._info.append(counter)#穴の数
        self._info.append(sum(hole_depth))#穴の深さの合計
        self._info.append(row_with_holes)#穴のある列数

    def _CulmulativeWells(self):
        self._info.append(0)
        for i in range(9):
            self._info[7] += abs(self._height[i] - self._height[i+1])#井戸の高さの和

    def _ExternalCols(self):
        self._info.append(0)
        for i in range(10):
            if abs(self._height[i] - (sum(self._height) / 10)) >= 3:
                self._info[8] += 1#平均の高さとの差が4以上ある列数

    def _MaxHeight(self):
        check = -1
        if self._height[0] - self._height[1] >= 4:
            check = 1
        if self._height[-1] - self._height[-2] >= 4:
            if check == 1:
                check = -1
            else:
                check = 1
        self._info.append(check)

class Evaluation:
    def __init__(self, evafunc_list):
        self._npeva = np.array(evafunc_list)

    def func(self, f_info):
        self._result = []
        answer = 500
        for nord in range(len(self._npeva)):
            self._npinfo = self._npeva[nord] * np.array(f_info)
            for i in range(len(self._npinfo)):
                if abs(self._npinfo[i]) >= 20:
                    answer += self._npinfo[i]
        return answer

def play_tetris(evafunc_list, generation):
    displayClear()
    field = Field()
    eva = Evaluation(evafunc_list)
    current = Current()
    field.makeField()
    n_type = current.nextBlock()
    while True:
        current.reset_vals()
        f_shape = field.field()
        b_type = current.blockType()
        n_type = current.nextBlock()
        if (generation > 0 and field._score >= 200) or field.areBlock():
            field._write()
            print(field._score)
            break
        maker = FieldMaker(f_shape)
        for movex in range(0, 10):
            for rotate in range(4):
                if maker.resetBlock(b_type, movex, rotate):
                    continue
                for n_movex in range(0, 10):
                    for n_rotate in range(4):
                        if maker.resetNext(n_type, n_movex, n_rotate):
                            continue
                        maker.best(eva.func(maker.info()), movex, rotate)
        current.rotate(maker.returnbest())
        b_shape = current.blockShape()
        current.print_field(generation)
        field.updateField(b_shape, True) # self._write()
        b_shape = current.fit(field.field())
        field.updateField(b_shape, False) # self._write()
        field.lineClear() # self._write()

if __name__ == '__main__':
    print('genom list?')
    f = int(input())
    if f == 0:
        evafunc_list = [[random.randint(1, 10)  * ((-1) ** random.randint(0, 1)) for k in range(10)] for i in range(5)]
        number = 0
    else:
        with open('./genom_log{}.txt'.format(f), 'r', encoding="utf-8") as fi:
            file_row = fi.readlines()
        print('generation?')
        number = input()
        if number == '':
            number = -1
        else:
            number = int(number) - 1
        evafunc_str = file_row[number]
        evafunc_str = evafunc_str[evafunc_str.find('：')+1:-1]
        evafunc_list = []
        for i in range(5):
            evafunc_list.append([])
            remember = 0
            for j in range(evafunc_str.find(']')):
                if j <= remember:
                    continue
                for k in range(4):
                    num = 3 - k
                    try:
                        evafunc_list[i].append(int(evafunc_str[j:j+num]))
                        remember = j + num
                        break
                    except:
                        pass
            evafunc_str = evafunc_str[evafunc_str.find(']')+1:]
        if number == -1:
            number = 49
    play_tetris(evafunc_list, number * -1)