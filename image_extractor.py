
import fitz
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def extract_from_image_line(data):
    line = []
    for i in range(data.shape[1]):
        P = data[:, i].argmax()
        if P > 0:
            line.append(P)

    return line

pdffile = "ecg_2020-07-09_12.17.pdf"

doc = fitz.open(pdffile)
page = doc.loadPage(0) #number of page
pix = page.getPixmap()
output = "outfile.png"
pix.writePNG(output)



im = Image.open('outfile.png')

size = im.size


r, g, b = im.split()

r = np.asarray(r)
g = np.asarray(g)
b = np.asarray(b)

b = (b - r)
r = b
g = b

r = Image.fromarray(r)
g = Image.fromarray(g)
b = Image.fromarray(b)

im = Image.merge("RGB", (r, g, b)).convert('L')

A1 = np.asarray(im.crop((0, 138, im.width, 308)).transpose(Image.FLIP_TOP_BOTTOM) )
A2 = np.asarray(im.crop((0, 308, im.width, 478)).transpose(Image.FLIP_TOP_BOTTOM))
A3 = np.asarray(im.crop((0, 478, im.width, 648)).transpose(Image.FLIP_TOP_BOTTOM))
A4 = np.asarray(im.crop((0, 648, im.width, 818)).transpose(Image.FLIP_TOP_BOTTOM))

line = []
line += extract_from_image_line(A1)
line += extract_from_image_line(A2)
line += extract_from_image_line(A3)
line += extract_from_image_line(A4)

a, b = len(line) // 10, 8 * len(line) // 10





G = np.asarray(line[a:b])
spread = G.max() - G.min()
peaks, _ = find_peaks((G - G.mean()) * -1 + G.mean(), height=1.07 * G.mean())

plt.rcParams["figure.figsize"] = (60,8)
plt.plot(range(len(G)), G)
plt.plot(peaks, G[peaks], "x")

print((peaks[1:] - peaks[:-1]).std())



plt.show()


