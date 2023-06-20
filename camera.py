import pygame
from Common_Variables import *
class Camera():
    def __init__(self):
        self.x = 0 # カメラのx座標
        self.y = 0 # カメラのy座標
        self.size = 1# カメラの倍率
        
        # 描画したいオブジェクトのリストを保存するリスト
        self.OBJlist = [] 

    def set_OBJlist(self, list):
        # 2重リストを作成
        self.OBJlist.append(list)

    def clear_OBJlist(self):
        self.OBJlist.clear()

    def move_pos(self, x: int, y: int):
        
        self.x += x
        self.y += y

    def draw(self, screen):
        # 登録されているオブジェクトを描画
        for mapobjs in self.OBJlist:
            for mapobj in mapobjs:
                mapobj.draw(screen, self.x, self.y)

        
