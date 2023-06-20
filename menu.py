import pygame
import sys  # ゲーム終了時に必要

import platform # このパソコンのOSがwindowsかどうか調べる
import os # ファイル関連
# subprocess.call('explorer.exe "%s"' % dir_name)
# モジュールのインポート
import tkinter, tkinter.filedialog, tkinter.messagebox
from tkinter import filedialog # 名前を付けて保存を行えるようになる
import ast # テキストに辞書形式で保存されたオブジェクトを、文字列ではなく辞書として扱えるようにするために必要
import json# テキストに辞書形式で保存されたオブジェクトを、文字列ではなく辞書として扱えるようにするために必要


from UI import *
from Common_Variables import *
from coin import *
from pusher import *

class Menu():
    def __init__(self, screen, Field):
        self.screen = screen
        self.Field = Field

        self.cameramode = "通常"# "カメラ移動"
        self.mouse_pos = (0, 0)

        
        
        # オブジェクト生成時に自動格納される辞書を設定
        self.UIs = {} # 削除や追加されることがほとんどないため、辞書の方が便利
        UI.set_dict(self.UIs)
        self.set_UI()

    def set_UI(self):
        Button(1, "サンプルボタン", pygame.Rect(CANVAS_WIDTH * (17/20) - 10,
                 CANVAS_HEIGHT * (1 / 10), CANVAS_WIDTH / 20, CANVAS_WIDTH / 20),
                "サンプルボタン.png",  drawFlag = True, frame = False)
        Text("サンプル文", (CANVAS_WIDTH * (15/20) - 10, CANVAS_HEIGHT * (3 / 10)),
              "これは/サンプルです", 40, (100, 0, 0), drawFlag = True,
              backcolor = (0, 255, 0))
        
        textRule= TextRule()  # テキスト処理のロジックInputTextクラスをインスタンス化
        Textbox("サンプル", pygame.Rect(100, 100, 50, 50),"ここに入力", textRule, drawFlag = True)
        

    def draw(self):
        for UI in self.UIs.values():
            UI.draw(self.screen)

    def event(self, event):
        # カメラの移動
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3):
            self.cameramode = "カメラ移動"
            self.mouse_pos = event.pos
            
        elif(self.cameramode == "カメラ移動"
           and event.type == pygame.MOUSEMOTION):
            x, y = event.pos
            self.Field.camera.move_pos(x - self.mouse_pos[0], y - self.mouse_pos[1])
            self.mouse_pos = (x, y)

        elif(self.cameramode == "カメラ移動" 
            and event.type == pygame.MOUSEBUTTONUP):
            self.cameramode = "通常"
        
        # カメラの拡大
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 4):
            size = self.Field.camera.size / 0.8
            pass

        # カメラの縮小
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 5):
            size = self.Field.camera.size * 0.8
            pass


        if event.type == pygame.KEYDOWN:  # キーを押したとき
            # pキーを押したとき
            if event.key == pygame.K_p:
                print("カメラのサイズ：%s"%(self.Field.camera.size))
                print("カメラの座標(%s, %s)"%(self.Field.camera.x, self.Field.camera.y))

        # テキストボックス処理
        
        # ボタンを左クリック
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
            # メニューボタンを押したなら  
            # メニューボタンを押したなら  
            for n in self.UIs.values():  
                if (n.__class__.__name__ == "Button"
                    and n.drawFlag 
                    and n.group == 1
                    and n.rect.collidepoint(event.pos)):
                    if(n.name == "サンプルボタン"):
                        if(n.swi == 0):
                            n.swi = 1
                            print("ボタンon！")
                            self.UIs["サンプル文"].change_text("ボタンon!")
                            self.UIs["サンプルボタン"].change_frame()
                        else:
                            n.swi = 0
                            print("ボタンoff！!")
                            self.UIs["サンプル文"].change_text("ボタンoff!!")
                            self.UIs["サンプルボタン"].change_frame()
                if(n.__class__.__name__ == "Textbox") :
                    if(n.writeFlag):
                        pass
                    else:
                        n.change_writeFlag()
                    