from random import randrange

def individuoChecker(individuo, ciudades):
	control = True
	for x in range(0, len(ciudades)):
		try:
			index = individuo.index(ciudades[x])
		except ValueError:
			control = False
			break
	return control

def funcAptitud(individuo, ciudades, distancias):
	aptitud = 0
	for x in range(0, len(individuo)-1):
		aptitud =  aptitud + distancias[ ciudades.index(individuo[x]) ][ ciudades.index(individuo[x+1]) ]
	aptitud = aptitud + distancias[ ciudades.index(individuo[-1]) ][ ciudades.index(individuo[0]) ]
	return aptitud

def randomGenerator(size, numLimit, repeat):
	arreglo = []
	repeat = size
	if  repeat:
		for x in range(0, size):
			arreglo.append(randrange(numLimit))
	else:
		while repeat != size:
			for x in range(0, repeat):
				index = -1
				num = randrange(numLimit)
				try:
					index = arreglo.index(num)
				except ValueError:
					arreglo.append(num)
				if index == -1:
					repeat  = + 1

	return arreglo

def randomIndividuos(size, number, ciudades):
	poblacion = []
	for x in range(0, number):
		individuo = ""
		repetido = True
		while repetido:
			individuo = ""
			arreglo = randomGenerator(size, len(ciudades), True )
			repetido = False
			for y in arreglo:
				individuo = individuo +ciudades[y]
			if individuoChecker(individuo, ciudades) == False:
				repetido = True
			else:
				for y in poblacion:
					if y == individuo:
						repetido = True
						break
		poblacion.append(individuo)

	return poblacion

def mutagenos(individuo, mutacion, ciudades):
	numero = int(len(individuo) * mutacion) 
	posiciones = randomGenerator(numero, len(individuo), False)
	for x in range(0, len(posiciones)):
		individuo =  individuo[:posiciones[x]]+ ciudades[randrange(len(ciudades))]+ individuo[posiciones[x]+1:]

	return individuo

def reproduccion(genomas,resto, parents, mutacion, ciudades):
	poblacion = parents

	for x in range(0, resto):
		control = True
		indiviuo = ""
		while True:
			p1 = randrange(len(parents))
			p2 = randrange(len(parents))
			if p1 != p2:
				break
		while control:
			mascara = randomGenerator(genomas, 2, ciudades)
			individuo = ""
			control = False
			for y in range(0, genomas):
				if mascara[y] == 1:
					individuo = individuo + parents[p1][y]
				else:
					individuo = individuo + parents[p2][y]	
			individuo = mutagenos(individuo, mutacion, ciudades)
			if individuoChecker(individuo, ciudades) == False:
				control = True
			else:
				for y in range(0,len(poblacion)):
					if individuo == poblacion[y]:
						control = True
						print(individuo)
						break
		poblacion.append(individuo)

	return poblacion

def poblacionMaker(genomas,poblacion, padresNumero, ciudades, distancias, tipo, aptitudes, mutacion, estado):
	parents = []
	indices = []
	resto = len(poblacion)-padresNumero 
	size = len(aptitudes)

	if tipo == "minimo":
		for y in range(0,4):
			value = -1 
			apti = 10000
			control = True
			for x in range(0,len(aptitudes)):
				for z in range(0, len(indices)):
					if x == indices[z]:
						control = False
				if apti > aptitudes[x] and control:
					 apti = aptitudes[x]
					 value = x
				control = True
			indices.append(value)
			parents.append(poblacion[value])
	else:
		print("no esta todavia ")

	print("\nPadres Elegidos:")
	paptitudes = []
	for x in range(0, len(parents)):
		apt = aptitudes[indices[x]]
		paptitudes.append(apt)
		print( str(indices[x]+1)+"  " + parents[x]+ "  su aptitud es :  "+ str(apt)) 

	if estado == "m":
		poblacion = reproduccion(genomas,resto, parents, mutacion, ciudades )
	else:
		poblacion = [parents, paptitudes]

	return poblacion

def main (genomas,poblacionTamano,ciudades, distancias, padresNumero, tipo, mutacion, generaciones ):
	poblacion= randomIndividuos(genomas,poblacionTamano,ciudades)
	aptitudes = []

	print("-------- -------- Simulacion --------------------------\n\nPoblacion Inicial:")
	for x in range(0, poblacionTamano):
		apt = funcAptitud(poblacion[x], ciudades, distancias)
		aptitudes.append(apt)
		print(str(x+1) + "  " + poblacion[x] + "  su aptitud es :  "+ str(apt))
	i = 0
	while i < generaciones:
		poblacion = poblacionMaker(genomas,poblacion, padresNumero,ciudades, distancias, tipo, aptitudes, mutacion, "m")

		i = i+1
		aptitudes = []
		print("\n\nGeneracion "+ str(i) +":")
		for x in range(0, poblacionTamano):
			apt = funcAptitud(poblacion[x], ciudades, distancias)
			aptitudes.append(apt)
			print(str(x+1) + "  " + poblacion[x] + "  su aptitud es :  "+ str(apt))

	return poblacionMaker(genomas,poblacion, padresNumero,ciudades, distancias, tipo, aptitudes, mutacion, "f")


def simulaciones (genomas,poblacionTamano,ciudades, distancias, padresNumero, tipo, mutacion, generaciones , simulaciones):
	psoluciones = []
	paptitudes = []


	for x in range(0, simulaciones):
		psoluciones.append(main(genomas,poblacionTamano,ciudades, distancias, padresNumero, tipo, mutacion, generaciones))
		paptitudes.append(sum(psoluciones[x][1]) / float(len(psoluciones[x][1])))

	gSolucion = psoluciones[paptitudes.index(min(paptitudes))]
	solucion = gSolucion[0][ gSolucion[1].index(min(gSolucion[1]))]

	print("\n\n\n La solucion es : " + solucion +"  con un  recorrido de "+str(min(gSolucion[1])) + "Km")



distancias = [
[0,1,2,3,4,5,6,7,8],
[1,0,9,8,7,6,5,4,3],
[2,9,0,1,2,3,4,5,6],
[3,8,1,0,9,8,7,6,5],
[4,7,2,9,0,1,2,3,4],
[5,6,3,8,1,0,9,8,7],
[6,5,4,7,2,9,0,1,2],
[7,4,5,6,3,8,1,0,9],
[8,3,6,5,4,7,2,9,0]
]

ciudades = "abcdefghi"

simulaciones(20,8,ciudades, distancias, 4, "minimo", 0.3, 90, 40)
#main(20,8,ciudades, distancias, 4, "minimo", 0.3, 90)