import pygame
from abc import ABCMeta, abstractmethod
from Common_Variables import *
class UI():
    # オブジェクト生成時自動格納するリストを設定する関数
    @classmethod
    def set_dict(cls, dict):
        cls.dict = dict

    def __init__(self, name, rect):
        self.name = name
        self.rect = rect
    
    # 状態の更新
    @abstractmethod
    def update(self):
        pass

    # 描画
    @abstractmethod
    def draw(self, screen):
        pass
    

class Button(UI):
    def __init__(self, group: int, name: str, rect: Rect, image_name: str = None, drawFlag:bool = True, frame:bool = False):
        super().__init__(name, rect)
        self.swi = 0 # スイッチの状態
        self.group = group # グループ番号
        if(image_name is not None):
            self.image = load_image(image_name, rect.width, rect.height) # ボタンの画像
        else:
            self.image = None
        self.drawFlag = drawFlag # ボタンを知覚できるか
        self.frame = frame

        # 親クラスに定義されているUIをすべて保存するリストに自分も追加
        self.dict["%s"%(self.name)] = self
    
    def change_image(self, image_name: str):
        self.image = load_image(image_name, self.rect.width, self.rect.height) # ボタンの画像
    
    def change_frame(self):
        self.frame = not self.frame

    def update(self):
        pass

    def draw(self, screen):
        if(self.drawFlag):
            if(self.image is not None):
                # 画像を描画
                screen.blit(self.image, self.rect)
            else:
                pygame.draw.rect(screen, (255,255,255) ,self.rect)
                
        if(self.frame):# 枠を描画
            rect = pygame.Rect(0, 0, self.rect.width + 10, self.rect.height + 10)
            rect.center = self.rect.center
            pygame.draw.rect(screen, (0,255,255), rect, 5)

#テキストの表示
class Text(UI):
    def __init__(self, name:str, pos:tuple, text:str, size:int, color, drawFlag = True,
                 backcolor = None):
        self.pos = pos 
        self.text = text
        self.size = size
        self.color = color
        self.drawFlag = drawFlag
        if(backcolor is None): # テキストの背後の色の設定
            self.backcolorFlag = False
        else:
            self.backcolorFlag = True
            self.backcolor = backcolor
        
        self.font = pygame.font.SysFont("yumincho",int(self.size))

        blitwh = self.measure_text_size()# テキストのサイズを測定
        blitw = blitwh[0]
        blith = blitwh[1]

        # name と　Rectを設定
        super().__init__(name, pygame.Rect(pos[0], pos[1], blitw, blith))
        # 親クラスを継承したUIをすべて保存するリストに自分も追加
        self.dict["%s"%(self.name)] = self
    
    # テキストのサイズを測定
    def measure_text_size(self) -> tuple:
        blitw = 0
        maxblitw = 0 # 最大の横幅を記録
        blith = 0
        for c in self.text:
            # 「/」を発見したら改行
            jtext = self.font.render( c, True, self.color)# 描画する文字列の設定
            if c == "/":#ボタンの横幅を考慮 
                if(blitw > maxblitw):
                    maxblitw = blitw
                blitw = 0
                blith += jtext.get_rect().h
                continue
            blitw += jtext.get_rect().w
        
        return (blitw, blith + jtext.get_rect().h)


    # テキスト内容を変更する関数
    def change_text(self, text:str):
        self.text = text
        # テキストのサイズを測定
        blitwh = self.measure_text_size()
        blitw = blitwh[0]
        blith = blitwh[1]
        self.rect.width = blitw
        self.rect.height = blith
        print(self.rect.height, self.rect.width)
    
    def change_drawFlag(self):
        self.drawFlag = not self.drawFlag

    def update(self):
        pass

    def draw(self, screen):
        if(self.drawFlag):
            if(self.backcolorFlag):
                pygame.draw.rect(screen, self.backcolor, self.rect, 0)
            blitw = 0
            blith = 0
            #テキストを一文字づつ表示することで改行を可能にしている
            for c in self.text:
                # 「/」を発見したら改行
                jtext = self.font.render( c, True, self.color)# 描画する文字列の設定
                if c == "/":#ボタンの横幅を考慮 
                    blitw = 0
                    blith += jtext.get_rect().h
                    continue
                screen.blit(jtext, (self.rect.left + blitw ,self.rect.top + blith))
                blitw += jtext.get_rect().w

class Textbox(UI):
    def __init__(self, name, rect, text, textRule, drawFlag = True):
        super().__init__(name, rect)
        self.text=Text(self.name + "※", (self.rect.left, self.rect.top),
                        text, self.rect.height, (100, 100, 0), drawFlag)#実際に表示する文字列
        self.framecolor=(255,255,0)
        self.textRule=textRule
        self.drawFlag=drawFlag
        
        # self.font = pygame.font.SysFont("yumincho", self.rect.height)
        # self.mouseX=0
        # self.mouseY=0

        self.writeFlag=False#テキストボックスに文字を入力できるかどうか
        self.frameFlag=False#テキストボックスの枠を描画するかどうか
        self.swi=0
        
        
        # テキスト入力時のキーとそれに対応するイベント
        self.event_trigger = {
            K_BACKSPACE: textRule.delete_left_of_cursor,
            K_DELETE: textRule.delete_right_of_cursor,
            K_LEFT: textRule.move_cursor_left,
            K_RIGHT: textRule.move_cursor_right,
            K_RETURN: textRule.enter,
        }
        
    def change_drawFlag(self):
        self.drawFlag = not self.drawFlag
        self.text.change_drawFlag()
    
    def change_writeFlag(self):
        self.writeFlag = not self.writeFlag

    def change_frameFlag(self):
        self.frameFlag = not self.frameFlag

    def change_framecolor(self,color):
        self.framecolor = color
    
    #テキストボックスを操作できる関数
    def Click_textbox(self,n,event):
    
        if(n.DrawFlag):
            if event.type == MOUSEMOTION:
                #マウスの現在位置(見せかけの座標)を取得
                n.mouseX, n.mouseY = event.pos
                #全体拡大率を考慮する
                n.mouseX/=self.Z
                n.mouseY/=self.Z

            #テキストボックスにマウスが重なり、FrameFlagがFalseだったら
            if(n.mouseX>n.x and n.mouseX<n.x+n.w and n.mouseY>n.y and n.mouseY<n.y+n.h):
                if(n.frameFlag==False):#上記の条件と別で既述しないと下記のelifがうまく機能しない
                    n.changeFrameFlag(True)

            #テキストボックスにマウスが重なっておらず、FrameFlagがTrueかつ、選択状態でないなら
            elif(n.frameFlag and n.swi==0):
                n.changeFrameFlag(False)
                    
            #テキストボックスをクリックしたとき
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(int(self.Z*n.x),int(self.Z*n.y),
                                   int(self.Z*n.w),int(self.Z*n.h)).collidepoint(event.pos):
                    
                    if(n.swi==0):
                        if(n.text==""):
                            n.text="|"
                        else:
                            n.textRule.input(n.text)
                        n.writeFlag=True
                        n.changeFrameColor((0,200,0))#フレームを緑に変更
                        n.changeFrameFlag(True)
                        n.swi=1
                        
                else:
                    #テキストボックス選択中に範囲外をクリックしたときEnterと同じ働きをする
                    if(n.swi==1):
                        n.writeFlag=False
                        n.changeFrameFlag(False)
                        n.changeFrameColor((255,255,0))#フレームを黄色に変更
                        n.swi=0
                        n.text = n.event_trigger[K_RETURN]()
                        return n.text  #確定した文字列を返す       

            if(n.writeFlag):
                # キーダウンかつ、全角のテキスト編集中でない
                if (event.type == KEYDOWN and not n.textRule.is_editing):
                    if event.key in n.event_trigger.keys():
                        n.ChangeFlag=True
                        n.text = n.event_trigger[event.key]()
                    # 入力の確定
                    if (event.unicode in ("\r", "") and event.key == K_RETURN):
                        
                        n.writeFlag=False
                        n.changeFrameFlag(False)
                        n.changeFrameColor((255,255,0))#フレームを黄色に変更
                        n.swi=0
                        return n.text  #確定した文字列を返す
                        
                elif event.type == TEXTEDITING:  # 全角入力
                    n.text = n.textRule.edit(event.text, event.start)
                elif event.type == TEXTINPUT:  # 半角入力、もしくは全角入力時にenterを押したとき
                    n.ChangeFlag=True
                    n.text = n.textRule.input(event.text)
    
    def update(self):
        pass

    # テキストボックスの表示
    def draw(self, screen):
        if(self.drawFlag):
            # 枠を描画
            if(self.frameFlag):
                pygame.draw.line(screen, self.framecolor, (self.rect.left, self.rect.top), ((self.rect.left+self.rect.width),self.rect.top), 2)
                pygame.draw.line(screen, self.framecolor, ((self.rect.left+self.rect.width), self.rect.top), ((self.rect.left+self.rect.width),(self.rect.top+self.rect.height)), 2)
                pygame.draw.line(screen, self.framecolor, ((self.rect.left+self.rect.width),(self.rect.top+self.rect.height)), (self.rect.left,(self.rect.top+self.rect.height)), 2)
                pygame.draw.line(screen, self.framecolor, (self.rect.left,(self.rect.top+self.rect.height)), (self.rect.left,self.rect.top*self.Z), 2)

class TextRule:
    """
    PygameのINPUT、EDITINGイベントで使うクラス
    カーソル操作や文字列処理に使う
    """

    def __init__(self) -> None:
        self.text = ["|"]  # 入力されたテキストを格納していく変数
        self.editing: List[str] = []  # 全角の文字編集中(変換前)の文字を格納するための変数
        self.is_editing = False  # 編集中文字列の有無(全角入力時に使用)
        self.cursor_pos = 0  # 文字入力のカーソル(パイプ|)の位置

    def __str__(self) -> str:
        """self.textリストを文字列にして返す"""
        return "".join(self.text)

    def edit(self, text: str, editing_cursor_pos: int) -> str:
        """
        edit(編集中)であるときに呼ばれるメソッド
        全角かつ漢字変換前の確定していないときに呼ばれる
        """
        if text:  # テキストがあるなら
            self.is_editing = True
            for x in text:
                self.editing.append(x)  # 編集中の文字列をリストに格納していく
            self.editing.insert(editing_cursor_pos, "|")  # カーソル位置にカーソルを追加
            disp = "[" + "".join(self.editing) + "]"
        else:
            self.is_editing = False  # テキストが空の時はFalse
            disp = "|"
        self.editing = []  # 次のeditで使うために空にする
        # self.cursorを読み飛ばして結合する
        return (
            format(self)[0 : self.cursor_pos]
            + disp
            + format(self)[self.cursor_pos + 1 :]
        )

    def input(self, text: str) -> str:
        """半角文字が打たれたとき、もしくは全角で変換が確定したときに呼ばれるメソッド"""
        self.is_editing = False  # 編集中ではなくなったのでFalseにする
        for x in text:
            self.text.insert(self.cursor_pos, x)  # カーソル位置にテキストを追加
            # 現在のカーソル位置にテキストを追加したので、カーソル位置を後ろにずらす
            self.cursor_pos += 1
        return format(self)

    def delete_left_of_cursor(self) -> str:
        """カーソルの左の文字を削除するためのメソッド"""
        # カーソル位置が0であるとき
        if self.cursor_pos == 0:
            return format(self)
        self.text.pop(self.cursor_pos - 1)  # カーソル位置の一個前(左)を消す
        self.cursor_pos -= 1  # カーソル位置を前にずらす
        return format(self)

    def delete_right_of_cursor(self) -> str:
        """カーソルの右の文字を削除するためのメソッド"""
        # カーソル位置より後ろに文字がないとき
        if len(self.text[self.cursor_pos+1:]) == 0:
            return format(self)
        self.text.pop(self.cursor_pos + 1)  # カーソル位置の一個後(右)を消す
        return format(self)

    def delete_cursor(self):
        self.text.pop(self.cursor_pos)  # カーソルを消す
        return format(self)

    def enter(self) -> str:
        """入力文字が確定したときに呼ばれるメソッド"""
        # カーソルを読み飛ばす
        entered = (
            format(self)[0 : self.cursor_pos] + format(self)[self.cursor_pos + 1 :]
        )
        self.text = ["|"]  # 次回の入力で使うためにself.textを空にする
        self.cursor_pos = 0  # self.text[0] == "|"となる
        return entered

    def move_cursor_left(self) -> str:
        """inputされた文字のカーソル(パイプ|)の位置を左に動かすメソッド"""
        if self.cursor_pos > 0:
            # カーソル位置をカーソル位置の前の文字と交換する
            self.text[self.cursor_pos], self.text[self.cursor_pos - 1] = (
                self.text[self.cursor_pos - 1],
                self.text[self.cursor_pos],
            )
            self.cursor_pos -= 1  # カーソルが1つ前に行ったのでデクリメント
        return format(self)

    def move_cursor_right(self) -> str:
        """inputされた文字のカーソル(パイプ|)の位置を右に動かすメソッド"""
        if len(self.text) - 1 > self.cursor_pos:
            # カーソル位置をカーソル位置の後ろの文字と交換する
            self.text[self.cursor_pos], self.text[self.cursor_pos + 1] = (
                self.text[self.cursor_pos + 1],
                self.text[self.cursor_pos],
            )
            self.cursor_pos += 1  # カーソルが1つ後ろに行ったのでインクリメント
        return format(self)




        
    

    

        