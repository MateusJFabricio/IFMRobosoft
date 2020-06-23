import o3d3xx
import cv2 as cv
from PIL import Image
import numpy as np
import RobosoftIfm as rbs

imageWidth = 352
imageHeight = 264
branco = (255, 255, 255)

#Criar uma imagem vazia
imagem = rbs.Imagem(imageWidth, imageHeight)
imagem.CreateBlank()
imagem.PreencherFundo(branco)

# Obtencao de imagem ____________________________________________
camera = rbs.Camera('192.168.0.101')
while(True):
    camera.CapturarImagem()
    
    distancias = camera.BuscarDistancias()

    imagem.PreencherImagemIFM(distancias)

    operacoes = rbs.Operacoes()
    thres = operacoes.ConverterUmCanal(imagem.image)
    #imagem.Show(thres)
    contornos = operacoes.BuscarContornos(thres,imageWidth, imageHeight)
    circulos = operacoes.BuscarCirculos(contornos)

    imag = rbs.Imagem(imageWidth, imageHeight)
    imag.CreateBlank()
    imag.image = operacoes.DrawContours(imag.image, contornos, (255, 0, 0))
    imag.image = operacoes.DrawContours(imag.image, circulos, (0, 0, 0))
    imag.Show(imag.image)

    operacoes.ShowContours(imageWidth, imageHeight, circulos)

#imagem.Show()