import o3d3xx
import cv2 as cv
from PIL import Image
import numpy as np

class Imagem:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.image = None

    def CreateBlank(self):
        # Create black blank image
        self.image = np.zeros((self.altura, self.largura, 3), np.uint8)

    def PreencherFundo(self, cor):
        # Since OpenCV uses BGR, convert the color first
        color = tuple(reversed(cor))
        # Fill image with color
        self.image[:] = color

    def Show(self):
        cv.imshow('image',self.image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def Show(self, imagem):
        cv.imshow('image', imagem)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def SetPixel(self, x, y, cor):
        self.image[x][y] = cor

    def GetPixel(self, x, y):
        return self.image[x][y]

    def PreencherImagemIFM(self, dist):
        index = 0

        for x in range(self.altura):
            for y in range(self.largura):
                if (dist[index] != 0):
                    self.SetPixel(x, y, (255,0,0))
                index = index + 1


class Camera:
    cam = None
    captura = None

    def __init__(self, ip):
        self.cam = o3d3xx.ImageClient(ip, 2000)

    def CapturarImagem(self):
        self.captura = self.cam.readNextFrame()

    def BuscarDistancias(self):
        return self.captura['distance']
    
class Operacoes:
    def ConverterUmCanal(Self, imagem):
        return cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

    def Threshold(self, imagem):
        r, mask = cv.threshold(imagem,127,255,cv.THRESH_BINARY)
        return mask

    def BuscarContornos(self, img, x, y):
        thres = self.Threshold(img)
        contours,h = cv.findContours(thres,cv.RETR_CCOMP ,cv.CHAIN_APPROX_NONE)
        return contours

    def DrawContours(self, imagem, contornos, cor):
        for contorno in contornos:
            cv.drawContours(imagem, contorno, -1, cor, cv.FILLED)
        return imagem

    def ShowContours(self, x, y, contornos):
        imag = Imagem(x, y)
        imag.CreateBlank()
        for contorno in contornos:
            cv.drawContours(imag.image, contorno, -1, (0,0,0), cv.FILLED)
        imag.Show(imag.image)

    def BuscarCirculos(self, contornos):
        formas = []
        for contorno in contornos:
            peri = cv.arcLength(contorno, True)
            approx = cv.approxPolyDP(contorno, 0.04 * peri, True)
            
            #Circulos
            if len(approx) > 6:
                formas.append(contorno)

        return formas

    def CarregarImagem(self, path):
        return cv.imread(path, 0)
