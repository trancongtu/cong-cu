import base64, io, json, os, sys
from PIL import Image

S = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(S, 'media', 'bai10')
OUT_DIR = os.path.dirname(S)
QR = sys.argv[1] if len(sys.argv) > 1 else None

PHOTOS = {'hero': 's01_1.jpg', 'dad': 's02_1.jpg', 'mom': 's02_6.jpg', 'didi': 's03_1.jpg',
          'meimei': 's03_3.jpg', 'gege': 's04_3.jpg', 'jiejie': 's04_5.jpg', 'jia': 's05_2.jpg',
          'photo': 's05_6.jpg', 'lawyer': 's07_1.jpg', 'year': 's09_1.jpg', 'friends': 's11_1.jpg',
          'cute': 's12_1.jpg', 'dog': 's13_4.jpg', 'doctor': 's13_5.jpg'}
STROKES = {'爸': 's02_2', '妈': 's02_4', '妹': 's03_2', '弟': 's03_5', '哥': 's04_1', '姐': 's04_4',
           '家': 's05_1', '人': 's05_3', '照': 's05_4', '片': 's05_5', '口': 's06_1', '和': 's06_2',
           '律': 's07_2', '师': 's07_3', '多': 's08_1', '大': 's08_2', '岁': 's08_3', '今': 's09_2',
           '年': 's09_3', '谁': 's10_1', '他': 's11_2', '们': 's11_3', '可': 's12_2', '爱': 's12_3',
           '只': 's12_4', '医': 's13_1', '生': 's13_2', '狗': 's13_3'}


def jpg_uri(path, size):
    im = Image.open(path).convert('RGB')
    im.thumbnail((size, size))
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=74, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def file_uri(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


imgs = {}
for k, f in PHOTOS.items():
    imgs[k] = jpg_uri(os.path.join(MEDIA, f), 900 if k == 'hero' else 240)
for c, f in STROKES.items():
    imgs['st_' + c] = file_uri(os.path.join(MEDIA, f + '.gif'), 'image/gif')

hero = imgs['hero']
tpl = open(os.path.join(S, 'template.html'), encoding='utf-8').read()
html = tpl.replace('__IMG_hero__', hero).replace('__IMG_JSON__', json.dumps({k: v for k, v in imgs.items() if k != 'hero'}, ensure_ascii=False))

if QR:
    qr_uri = file_uri(QR, 'image/png')
    block = f'<img class="qr" src="{qr_uri}" alt="Mã QR mở bài học trên điện thoại">'
else:
    block = ''
html = html.replace('__QR_BLOCK__', block)

standalone = ('<!doctype html>\n<html lang="vi">\n<head>\n<meta charset="utf-8">\n'
              '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
              '</head>\n<body>\n' + html.replace('__BACK__', '<a class="back" href="../">← Tất cả bài</a>') + '\n</body>\n</html>\n')
open(os.path.join(OUT_DIR, 'web', 'bai10', 'index.html'), 'w', encoding='utf-8').write(standalone)
print('size MB', round(len(html.encode()) / 1e6, 2))
