import pygame
from pygame.locals import *
from Common_Variables import *
from menu import *
from camera import *

# ----------------------------------#
# Field(ゲーム領域)の定義
class Field:
    def __init__(self, screen):
        self.screen = screen
        # カメラを定義
        self.camera = Camera()
        
        self.set_game()# ゲームを初期設定(初期化はinit_game関数)

        self.menu = Menu(self.screen, self)

        # メインループ開始
        clock = pygame.time.Clock()
        while True:
            clock.tick(FPS)
            self.update()
            pygame.draw.rect(self.screen, (0,0,0),
                             (0, 0, CANVAS_WIDTH, CANVAS_HEIGHT))
            self.camera.draw(self.screen)
            self.menu.draw()
            pygame.display.update()
            self.event()
            
    
    # 一度だけ行う最初の準備
    def set_game(self):
        ##        # 素材のロード
        # self.load_images()
        # self.load_sounds()

        # オブジェクト生成時に自動格納されるリストを設定
        self.Coins = []
        Coin.set_list(self.Coins)

        self.Pushers = []
        Pusher.set_list(self.Pushers)

        # オブジェクトを映すカメラを設定
        Coin.set_camera(self.camera)
        Pusher.set_camera(self.camera)

        self.init_game()

    # ゲームを初期化(初期設定)する関数
    def init_game(self):

        # 時間を初期化
        self.time = 0
        # 更新をストップ(一時停止)
        self.mode = "stop"

        # コインオブジェクトをリセットする。
        self.Coins.clear()
        self.Pushers.clear()
        
        # ボードを生成
        Pusher_1(400,200,700, 400)
        # コインオブジェクトを初期位置に生成
        Normal_coin(700, 500, 50)
        

        self.camera.clear_OBJlist()
        self.camera.set_OBJlist(self.Pushers)
        self.camera.set_OBJlist(self.Coins)
        
    
    #イメージのロード
    def load_images(self):
        # スプライトの画像を登録
        # 片方だけサイズ変更する場合は、もう片方を0とかくex):load_image("SubSpot.png",0,40)
        # 左上を透過色に設定する場合は、4つ目の引数に-1を、
        # 任意の色を透過色に設定する場合は(0,0,0)など直接指定をする
        # Spear.image = load_image("beam.png", SPEAR_WIDTH, SPEAR_HEIGHT,-1)
##        self.Map1 = load_image("最初の部屋.png", CANVAS_WIDTH, CANVAS_HEIGHT)
##        Girl.liveimage = load_image("少女_生きてる.png", CELL_WIDTH, CELL_HEIGHT*1.5, -1)
        #Car.images["%s:%s"%(CAR_W, CAR_H)] = load_image("車.png", CAR_W, CAR_H, -1)
        pass
        
    #サウンドのロード
    def load_sounds(self):
        #Block.bomb_sound = load_sound("bomb.wav")
        pass

    def update(self):
        # UIの更新
        for UI in self.menu.UIs.values():
            UI.update()
            
        """ゲーム状態の更新"""
        if(self.mode == "play"):
            #時間を進める
            self.time += 1
            #状態を更新する(時間に依存)
            for mapobj in self.Coins:
                mapobj.update(self.time)

            for vehicle in self.Pushers:
                vehicle.update(self.time)
    
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:  # キーを押した瞬間
                # ESCキーならスクリプトを終了
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                # # Ctrl + zキーで最新のマップオブジェクトを一つ削除
                # key = pygame.key.get_pressed()
                # if (key[pygame.K_LCTRL] == 1
                #     and key[pygame.K_z] == 1):
                #     del self.MapOBJs[-1]

            self.menu.event(event)# Menuクラスのevent関数でUIへの入力を受け付ける

screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT)) # screen を準備する
pygame.init()
pygame.display.set_caption("Game")
Field(screen)
