import os   # 画像の読み込み時に必要
from pygame.locals import *
import pygame

# 画面の大きさ
CANVAS_WIDTH  = 1500
CANVAS_HEIGHT = 900

# 1秒間のフレーム数
FPS = 60
# 1フレームで何time進むか
TIME = 1

# 画像, 音の読み込み
def load_image(filename,w = 0,h = 0, colorkey = None):
    """画像をロードして画像と矩形を返す"""
    newfilename = os.path.join("./images/", filename)
    try:
        image = pygame.image.load(newfilename).convert_alpha()
    except FileNotFoundError:
        print("探索したファイルpath : ", os.getcwd())
        raise SystemExit("Error : ", filename, "が見つかりません")
        
        
    image = image.convert()
    
    # サイズ変更する場合
    if not (w==0 and h==0):
        if(w == 0):
            image=pygame.transform.smoothscale(image, (image.rect.width,int(h)))
        elif(h == 0):
            image=pygame.transform.smoothscale(image, (int(w),image.get_rect().height))            
        else:
            image=pygame.transform.smoothscale(image, (int(w),int(h)))
    
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
        
    return image
    

def split_image(image, n):
    """横に長いイメージを同じ大きさのn枚のイメージに分割
    分割したイメージを格納したリストを返す"""
    image_list = []
    w = image.get_width()
    h = image.get_height()
    w1 = w // n
    for i in range(0, w, w1):
        surface = pygame.Surface((w1,h))
        surface.blit(image, (0,0), (i,0,w1,h))
        surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
        surface.convert()
        image_list.append(surface)
    return image_list

def load_sound(filename):
    """サウンドをロード"""
    filename = os.path.join("./sounds", filename)
    return pygame.mixer.Sound(filename)

