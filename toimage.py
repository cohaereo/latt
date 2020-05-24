from PIL import Image
import math
from sys import argv
import os

if(len(argv) < 2):
    print(f"No file specified. Usage: {argv[0]} <raw latt binary (.rlatt)>")
    exit(1)

f = open(argv[1], 'rb')
code = f.read()
# code = [1, 1, 1, 1, 1, 1, 1, 1, 1, 12, 5, 1, 1, 1, 1, 1, 1, 1, 1, 6, 3, 11, 23, 5, 17, 7, 5, 8, 3, 3, 3, 5, 8, 1, 1, 1, 1, 18, 7, 5, 8, 5, 8, 1, 1, 1, 19, 7, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 12, 6, 1, 1, 1, 1, 5, 3, 11, 23, 6, 5, 8, 1, 1, 1, 1, 1, 1, 1, 1, 5, 8, 5, 8, 1, 1, 1, 5, 18, 8, 5, 17, 8, 3, 3, 3, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 12, 21, 5, 11, 23, 2]
widthheight = int(math.ceil(math.sqrt(len(code))))
pad = int(math.pow(widthheight, 2)) - len(code)
code += bytes([22]) * pad

arrow = Image.open('latt_arrow_small.png')
finished = Image.new('1', (widthheight * 128, widthheight * 128))

for y in range(widthheight):
    for x in range(widthheight):
        c = code[y*widthheight+x]
        finished.paste(arrow.copy().rotate(360 - c * 15), (x * 128, y * 128))

finished.save(os.path.splitext(argv[1])[0] + ".png")