#ALGORITMO GENETICO INVENTARIO OPTIMO DE ALMACEN DE CARNE
import random

class algoritmoGenetico:
    def __init__(self):  #creacion de variables
        self.poblacion = []
        self.genotipo = []
        self.bondad = []
        self.cc = []
        self.fprobabilidad = []
        self.eliteq = []
        self.elitecosto = []
        self.npoblacion = 50
        self.mayor = 0
        print ("Cálculo de cantidad óptima de pedido 'Q*' para el manejo de inventario de productos cárnicos\n")
        self.d = int(input("Introduzca la demanda constante\n"))
        self.tiempo = int(input("Introduzca la cantidad de tiempo en dias requerida para satisfacer la demanda\n"))
        self.almacen = int(input("Introduzca la capacidad de las neveras \n"))
        self.c0 = int(input("Introduzca el costo de cada pedido Co \n"))
        self.mantenimiento = int(input("Introduzca el costo de mantenimiento por kilo\n"))
        self.depreciacion = int(input("Introduzca el costo de depreciación de un kilo por día\n"))
        self.ntramos = int(input("Introduzca la cantidad de tramos\n"))
        self.tramoinferior = []
        self.tramosuperior = []
        self.tramopreciocompra = []

        print ("Introduzca el límite inferior del tramo 1")
        n = int(input())
        self.tramoinferior.append(n)
        
        print ("Introduzca el límite superior del tramo 1")
        n = int(input())
        self.tramosuperior.append(n)
        
        print ("Introduzca el costo de compra asociado al tramo 1")
        n = int(input())
        self.tramopreciocompra.append(n)

        for i in range(1,self.ntramos):
            n = self.tramosuperior[i-1] + 1
            self.tramoinferior.append(n)
            
            print ("Introduzca el límite superior del tramo ",i+1)
            n = int(input())
            self.tramosuperior.append(n)
            
            print ("Introduzca el costo de compra asociado al tramo ",i+1)
            n = int(input())
            self.tramopreciocompra.append(n)

        #Generación de población inicial
        if (self.almacen > self.tramosuperior[self.ntramos-1]):
            self.limitesuperior = self.tramosuperior[self.ntramos-1]
        else:
            self.limitesuperior = self.almacen

        self.limiteinferior = self.tramoinferior[0]

        a = bin(self.limitesuperior)
        self.posiciones = len(a)-2

        secuencia = []
        for i in range(self.limiteinferior, self.limitesuperior+1):
            secuencia.append(i)

        for i in range(self.npoblacion):
            a = random.choice(secuencia)
            self.poblacion.append(a)
            secuencia.remove(a)

        for i in range(self.npoblacion):
            a = bin(self.poblacion[i])
            a = a.lstrip("0b")
            self.genotipo.append(a)
            while len(self.genotipo[i]) < self.posiciones:
                self.genotipo[i] = "0"+self.genotipo[i]

        for i in range (self.npoblacion):
            for j in range (self.ntramos):
                if self.poblacion[i] >= self.tramoinferior[j] and self.poblacion[i] <= self.tramosuperior[j]:
                    self.cc.append(self.tramopreciocompra[j])               
        print ("Conjunto de Q* iniciales")
        print (self.poblacion,"\n")
        print ("Genotipo de la poblacion inicial")
        print (self.genotipo, "\n")
        print ("Costo de compra en kilos de cada pedido")
        print (self.cc,"\n")


    def evaluar(self):
        self.bondad = []
        for i in range(self.npoblacion):   #evaluar costo total de inventario 
            cp = self.d/self.poblacion[i]
            p = self.tiempo/cp
            cua = self.mantenimiento + (self.depreciacion*p)
            ct = (self.c0 * self.d/self.poblacion[i]) + (cua * self.poblacion[i]/2) + self.cc[i]*self.d
            ct = round(ct,2)
            if ct > self.mayor:
                self.mayor = ct
            self.bondad.append(ct)

    def ruleta(self):
        totalbondad = 0
        funcion = []
        suma = 0
        self.fprobabilidad = []
        posicionmejor = 0

        mejor = self.bondad[0]
        print ("Costo total para cada Q (bondad)")
        print (self.bondad,"\n")    #sacar complemento
        self.mayor = self.mayor * 1.1
        for i in range(self.npoblacion):
            n = self.mayor - self.bondad[i]
            totalbondad = totalbondad + n
            funcion.append(n)

        for i in range (self.npoblacion):  #crear funcion de probabilidad con complemento
            suma = suma + funcion[i]
            n = (suma / totalbondad) * 100
            n = round(n,2)
            self.fprobabilidad.append(n)

        print ("Función de probabilidad generada a partir de probabilidad de selección de cada Q")
        print (self.fprobabilidad)
            
        for i in range (self.npoblacion):
            if self.bondad[i] <= mejor:
                mejor = self.bondad[i]
                posicionmejor = i
                
        self.eliteq.append(self.poblacion[posicionmejor])
        self.elitecosto.append(self.bondad[posicionmejor])

        print("Q optimo de la generacion")
        print (self.eliteq)
        print ("Costo optimo de la generacion")
        print (self.elitecosto)

        aleatorio = []        
        for i in range (10000):  #seleccion por ruleta
            aleatorio.append(i)

        nuevageneracion= []
        
        s = ""
        while len(nuevageneracion) < self.npoblacion:
            esigual = True
            while esigual == True:
                a = random.choice(aleatorio)
                b = random.choice(aleatorio)
                if a!=b:
                    esigual = False
            a = a/100
            b = b/100

            posiciona = 0
            posicionb = 0
            for j in range(self.npoblacion):  #obtengo individuos a cruzar
                if j==0:
                    if a <= self.fprobabilidad[j]:
                        posiciona = j
                    if b <= self.fprobabilidad[j]:
                        posicionb = j
                else:
                    if a <= self.fprobabilidad[j] and a > self.fprobabilidad[j-1]:
                        posiciona = j
                        
                    if b <= self.fprobabilidad[j] and b > self.fprobabilidad[j-1]:
                        posicionb = j
                

            #cruzar
            descendencia = []
            padrea = self.genotipo[posiciona]
            padreb = self.genotipo[posicionb]
            for i in range(self.posiciones):
                descendencia.append(i)

            padrea = list(padrea)
            padreb = list(padreb)
            corte = random.randrange(self.posiciones)
            descendencia[:corte] = padrea[:corte]
            descendencia [corte:] = padreb[corte:]
            descendencia = s.join(descendencia)
            prueba = int(descendencia,2)
            if prueba <= self.limitesuperior and prueba >= self.limiteinferior:
                nuevageneracion.append(descendencia)

        self.genotipo = []
        self.genotipo = nuevageneracion

        self.poblacion = []
        for i in range (self.npoblacion):
            n = self.genotipo[i]
            n = int(n,2)
            self.poblacion.append(n)

        self.cc = []
        for i in range (self.npoblacion):
            for j in range (self.ntramos):
                if self.poblacion[i] >= self.tramoinferior[j] and self.poblacion[i] <= self.tramosuperior[j]:
                    self.cc.append(self.tramopreciocompra[j])  

                    
        print ("poblacion nueva")
        print (self.poblacion)
        print ("Genotipo")
        print (self.genotipo)
        print ("Costo de compra")
        print (self.cc)

    
    def mutacion(self):
        for i in range(self.npoblacion):
            for j in range(self.posiciones):
                n = random.randint(0,99)
                if n == 0:
                    aux = self.genotipo[i]
                    aux = list(aux)
                    if aux[j] == "0":
                        aux[j] = "1"
                    else:
                        aux[j] = "0"
                    s=""
                    aux = s.join(aux)
                    a = int(aux,2)
                    if a>=self.tramoinferior[0] and a<= self.tramosuperior[self.ntramos-1]:
                        print ("antes de mutacio ",self.genotipo[i])
                        self.genotipo[i] = aux
                        print ("mutacion exitosa ",self.genotipo[i])
                    else:
                         print("mutacion fallida")    
        
            
    
uno = algoritmoGenetico()
uno.evaluar()
for i in range (100):
    uno.ruleta()
    uno.mutacion()
    uno.evaluar()

mejorq = uno.eliteq[0]
mejorcosto = uno.elitecosto[0]
for i in range(len(uno.eliteq)):
    if uno.elitecosto[i] < mejorcosto:
        mejorcosto = uno.elitecosto[i]
        mejorq = uno.eliteq[i]

print ("El menor costo de inventario es ",mejorcosto," con una Q de ",mejorq)
    
