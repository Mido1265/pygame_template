import pygame
import math
from typing import Union
from abc import ABCMeta, abstractmethod
from Common_Variables import *

# マップ(親クラス)
class Coin(metaclass=ABCMeta):

    # オブジェクト生成時自動格納するリストを設定する関数
    @classmethod
    def set_list(cls, list):
        cls.list = list

    # オブジェクトを映すカメラを設定する関数
    @classmethod
    def set_camera(cls, camera):
        cls.camera = camera

    def __init__(self, x, y, r):
        self.x = x * self.camera.size#x座標
        self.y = y * self.camera.size#y座標
        self.r = r * self.camera.size#半径
        


    # 座標を移動させる関数
    def move_coin(self, x, y):
        self.x += x
        self.y += y
    
    # 座標を変更する関数
    def warp_coin(self, x, y):
        self.x = x
        self.y = y

    # 状態の更新
    @abstractmethod
    def update(self, time):
        pass

    # 描画
    @abstractmethod
    def draw(self, screen):
        pass

################################################################

# 普通のコイン
class Normal_coin(Coin):
    def __init__(self, x, y, r):
        # self.str = ""
        self.list.append(self)
        super().__init__(x, y, r)
        self.color = (255, 255, 0)

    def update(self, time):
        pass

    def draw(self, screen, x, y):
        # コンクリート地面
        pygame.draw.circle(screen, self.color, (self.x + x, self.y + y), self.r)

        
    