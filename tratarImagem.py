# -*- coding: utf-8 -*-
# ----------------------------------------------------------  Bibliotecas --------------------------------------------------------------
import numpy as np
from coordenada import Coordenada
import cv2
import csv
import os
# import sys
# sys.setrecursionlimit(100000)
# ----------------------------------------------------------  Variaveis Globais ---------------------------------------------------------
valor = 255
max = 255
min = 0
pontosDeConcentracao = []
caminhoOrigem = './mama/recursos/'
caminhoDestino = './mama/imgs/'

# ----------------------------------------------------------  Funcoes -------------------------------------------------------------------
def verificarPopulacao(img, x, y, dist, percent):
    contador = 0
    xIni = x-dist
    xFim = x+dist
    yIni = y-dist
    yFim = y+dist
    for i in range(xIni, xFim):
        for j in range(yIni, yFim):
            if(img[i, j] == 0):
                contador = contador + 1

    if(contador > int((xFim-xIni)*(yFim-yIni)*(percent))):
        img[xIni:xFim, yIni:yFim] = 0
    else:
        img[xIni:xFim, yIni:yFim] = 140

def excluirGruposIsolados(dist, img, x, y, percent):
    # Excluir grupos isolador
    if(x+dist < int(img.shape[0]) and x-dist >= 0 and y+dist < int(img.shape[1]) and y-dist >= 0):
        if(img[x, y] == img[x+1, y] == img[x-1, y] == img[x, y-1] == img[x, y+1] == 
            img[x+1, y+1] == img[x-1, y+1] == img[x+1, y-1] == img[x-1, y-1] == 0):
            verificarPopulacao(img, x, y, dist, percent) 

def verificarVizinhos(tamanho, img, raio, x, y, percent): 
    distVizinhos = 1
    contador = 0
    if(raio > 0):
        if(x+distVizinhos < int(img.shape[0]) and x-distVizinhos >= 0 and y+distVizinhos < int(img.shape[1]) and y-distVizinhos >= 0):
            excluirGruposIsolados(tamanho, img, x, y, percent)
            if (img[x+distVizinhos, y] >= (img[x, y]-raio) and img[x+distVizinhos, y] <= (img[x, y]+raio)):
                contador = contador + 1
            if (img[x-distVizinhos, y] >= (img[x, y]-raio) and img[x-distVizinhos, y] <= (img[x, y]+raio)):
                contador = contador + 1
            if (img[x, y+distVizinhos] >= (img[x, y]-raio) and img[x, y+distVizinhos] <= (img[x, y]+raio)):
                contador = contador + 1
            if (img[x, y-distVizinhos] >= (img[x, y]-raio) and img[x, y-distVizinhos] <= (img[x, y]+raio)):
                contador = contador + 1
            if (img[x-distVizinhos, y-distVizinhos] >= (img[x, y]-raio) and img[x-distVizinhos, y-distVizinhos] <= (img[x, y]+raio)):
                contador = contador + 1
            if (img[x+distVizinhos, y+distVizinhos] >= (img[x, y]-raio) and img[x+distVizinhos, y+distVizinhos] <= (img[x, y]+raio)):
                contador = contador + 1
            if (img[x+distVizinhos, y-distVizinhos] >= (img[x, y]-raio) and img[x+distVizinhos, y-distVizinhos] <= (img[x, y]+raio)):
                contador = contador + 1
            if (img[x-distVizinhos, y+distVizinhos] >= (img[x, y]-raio) and img[x-distVizinhos, y+distVizinhos] <= (img[x, y]+raio)):
                contador = contador + 1
            if(contador > 3):
                img[x, y] = img[x-distVizinhos, y] = img[x+distVizinhos, y] = img[x, y-distVizinhos] = img[x, y+distVizinhos] = 0
            else:
                img[x, y] = img[x-distVizinhos, y] = img[x+distVizinhos, y] = img[x, y-distVizinhos] = img[x, y+distVizinhos] = 140



def encontrarPontosDeConcentracao(img, x, y, raio):
    global pontosDeConcentracao
    distVizinhos = 1
    if(raio > 0):
        if(x+distVizinhos < int(img.shape[0]) and x-distVizinhos >= 0 and y+distVizinhos < int(img.shape[1]) and y-distVizinhos >= 0):
            if(img[x,y] >= 0 and img[x,y] <=160):
                print(img[x,y])
                img[x,y] = 140
            if (img[x+distVizinhos, y] >= (img[x, y]-raio) and img[x+distVizinhos, y] <= (img[x, y]+raio)
            and  img[x-distVizinhos, y] >= (img[x, y]-raio) and img[x-distVizinhos, y] <= (img[x, y]+raio)
            and  img[x, y+distVizinhos] >= (img[x, y]-raio) and img[x, y+distVizinhos] <= (img[x, y]+raio)
            and  img[x, y-distVizinhos] >= (img[x, y]-raio) and img[x, y-distVizinhos] <= (img[x, y]+raio)):
                img[x, y] = img[x-distVizinhos, y] = img[x+distVizinhos, y] = img[x, y-distVizinhos] = img[x, y+distVizinhos] = 0
                img[x-1, y-1] = img[x-1, y+1] = img[x+1, y+1] = img[x+1, y-1] = 0
                pontosDeConcentracao.append(Coordenada(x, y, x-1, x+1, y-1, y+1))

        
def percorrerImagem(img, raio): 
    for x in range(0, int(img.shape[0])-1):
        for y in range(0, int(img.shape[1])-1):
            # Gerar Bordas
            if(img[x, y] < min + raio and img[x, y] >=  min):
                img[x, y] = 0

            # # Mapear 
            if(img[x, y] >= 150 and img[x, y] < max):
                encontrarPontosDeConcentracao(img, x, y, raio)

def iniciarVarredura(img, raio, tamanho, percent):
    global pontosDeConcentracao
    tamanho = pixelToMillimiter(tamanho)
    percent = percent / 100
    percorrerImagem(img, raio) 
    for coord in pontosDeConcentracao:
        verificarVizinhos(tamanho, img, raio, coord._esquerda, coord._y, percent)
        verificarVizinhos(tamanho, img, raio, coord._direita, coord._y, percent)
        verificarVizinhos(tamanho, img, raio, coord._x, coord._cima, percent)
        verificarVizinhos(tamanho, img, raio, coord._x, coord._baixo, percent)
        verificarVizinhos(tamanho, img, raio, coord._esquerda, coord._baixo, percent)
        verificarVizinhos(tamanho, img, raio, coord._esquerda, coord._cima, percent)
        verificarVizinhos(tamanho, img, raio, coord._direita, coord._baixo, percent)
        verificarVizinhos(tamanho, img, raio, coord._direita, coord._cima, percent)

def pixelToMillimiter(tamanho):
    # 1 milimitro equivale a 3.78 pixels
    pixels = 3.78 
    return int(tamanho * pixels)

def verificarArquivo(caminho):
    listaDeImgs = []
    if os.path.exists(caminho):
        for arq in os.listdir(caminho):
            if(not os.path.isfile(arq)):
                if (arq.lower().endswith(".jpg") or arq.lower().endswith(".png")):
                    listaDeImgs.append(arq.lower())

    return listaDeImgs
# ----------------------------------------------------------  Executavel ----------------------------------------------------------------
imgs = verificarArquivo(caminhoOrigem)
if(len(imgs) > 0):
    for arqName in imgs:
        # # Transformar em PB
        cv2.startWindowThread()
        img = cv2.imread(caminhoOrigem + arqName, 0)
        cv2.imwrite(caminhoDestino + 'original' + arqName, img)

        imgAlter = img
        iniciarVarredura(imgAlter, 5, 1, 50)
        cv2.imwrite(caminhoDestino + 'alterada' + arqName, imgAlter)

# # cv2.namedWindow("preview" )
# cv2.namedWindow("preview", cv2.WINDOW_NORMAL)
# cv2.imshow("preview", img)
# cv2.waitKey(0)
# cv2.waitKey(30000)
# cv2.destroyAllWindows()