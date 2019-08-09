class Coordenada:
    def __init__(self, x, y, esquerda, direita, baixo, cima):
        self._x = x
        self._y = y
        self._esquerda = esquerda
        self._direita = direita
        self._baixo = baixo
        self._cima = cima
     
    def setX(self, x):
        self._x = x
     
    def setY(self, y):
        self._y = y

    def getX(self, x):
        self._x = x
     
    def getY(self, y):
        self._y = y

    def setEsquerda(self, esquerda):
        self._esquerda = esquerda
     
    def setDireita(self, direita):
        self._direita = direita
     
    def getEsquerda(self):
        return self._esquerda
         
    def getDireita(self):
        return self._direita
     
    def setBaixo(self, baixo):
        self._baixo = baixo
     
    def setCima(self, cima):
        self._cima = cima
     
    def getBaixo(self):
        return self._baixo
         
    def getCima(self):
        return self._cima

    def constructor(self):
        return {
            "x": self._x,
            "y": self._y,
            "esquerda": self._esquerda,
            "direita": self._direita,
            "cima ": self._cima,
            "baixo": self._baixo
        }