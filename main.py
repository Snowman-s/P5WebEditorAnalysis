from random import Random
import cv2
import numpy as np
from consts import *
from bs4 import BeautifulSoup
from PIL import ImageFont, ImageDraw, Image

# HTMLの解析
bsObj = BeautifulSoup(html,"html.parser")

# 要素の抽出
items = map(lambda k : str(k.th.a.contents[0]), bsObj.find_all("tr", {"class":"sketches-table__row"}))

import spacy
nlp = spacy.load('ja_ginza')
dict = {}

#https://universaldependencies.org/u/pos/index.html
ignoreUpos = [
  "ADP", # 接置詞 (～が、～で など)
  "NUM", # 数値記号
  "SCONJ", # 従属接続詞
  "PUNCT", # 句読点
  "SYM", # 記号
  "AUX", # 補助
]

for title in items:
  doc = nlp(title)
  for word in doc:
    if word.pos_ in ignoreUpos: continue
    wordStr = str(word.orth_)
    if dict.get(wordStr) == None :
      dict.update({wordStr:1})
    else:
      dict.update({wordStr:dict.get(wordStr) + 1})

canvas = np.zeros((1000, 1000), np.uint8)

r = Random()

fontpath ='C:\Windows\Fonts\HGRGE.TTC'

img_pil = Image.fromarray(canvas)

draw = ImageDraw.Draw(img_pil)

for k in dict.keys():
  font = ImageFont.truetype(fontpath, dict[k]*10)
  draw.text((r.randint(0,940),r.randint(0,940)), k,  255, font)

canvas = np.array(img_pil)

cv2.imwrite('out.jpg', canvas)
