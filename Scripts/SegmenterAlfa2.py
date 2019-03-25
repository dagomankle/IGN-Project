# python 3 || obspy || windows2010
# Hecho por Daniel Ginez
# Asistente: Diana Mantilla

from obspy.core import read, UTCDateTime
from datetime import datetime, date, time, timedelta
from obspy.clients.arclink import Client# para generar la coneccion con la base de datos
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
from obspy.signal.util import smooth

class SignalDg:
	def __init__(self, *args):
		lArgs = []
		argNum = len(args)
		for arg in args:
			lArgs.append(arg)
		multiple = True

		if argNum == 8 :
			# ejemplo seg = Signal('EC','CAYR','','SHZ','2017-01-24 00:00:00', 24, 500, 320)
			try:
				print("Bienvenido a la primera clase de GeoDago")
				clienteArclink = Client('test', '192.168.1.7', 18001)# coneccion al stream
				self.__t = UTCDateTime(lArgs[4]) # +5 horas para utc y poner la fecha deseada. Hay que automatizar esto
				self.__tf = self.__t + 3600*lArgs[5]
				self.__oTrace = clienteArclink.get_waveforms(lArgs[0], lArgs[1], lArgs[2], lArgs[3],self.__t,self.__tf,route = False, compressed = False)
				self.__trace= clienteArclink.get_waveforms(lArgs[0], lArgs[1], lArgs[2], lArgs[3],self.__t,self.__tf,route = False, compressed = False)[0] # se obtiene el trazo principal
				self.__minimumPointEvent = lArgs[6]# amplitud minima
				self.__analisisTimeLapse = lArgs[7]
				print("\nconeccion exitosa")
			except ValueError:
				print("Error en la coneccion")

		elif argNum == 5:
			#ejemplo : main = Signal(trace.slice(timei,timef) ,timei ,timef, self.__minimumPointEvent,self.__analisisTimeLapse)
			self.__trace = lArgs[0]
			self.__t = lArgs[1] # +5 horas p^^ara utc y poner la fecha deseada. Hay que automatizar esto,
			self.__tf = lArgs[2]
			self.__minimumPointEvent = lArgs[3]
			self.__analisisTimeLapse = lArgs[4]

		elif argNum == 4:# se corre el script para un trazo unico
			#seg = SignalDg(self.__oTrace[x], self.__frecuencia, self.__analisisTimeLapse, "trace")
			multiple = False
			self.__oTrace = lArgs[0]
			self.__trace = lArgs[0]
			self.__t = self.__trace.stats.starttime
			self.__tf = self.__trace.stats.endtime
			self.__minimumPointEvent = lArgs[1]
			self.__analisisTimeLapse = lArgs[2]

		elif argNum == 3:# falta poner una excepcion de archivo mal leido
			#seg = Signal('volcan.mseed', 1000, 320)
			self.__oTrace = read(lArgs[0])
			self.__trace = read(lArgs[0])[0]
			self.__t = self.__trace.stats.starttime
			self.__tf = self.__trace.stats.endtime
			self.__minimumPointEvent = lArgs[1]
			self.__analisisTimeLapse = lArgs[2]
		else:
			print("Argumentos no aceptables")
			sys.exit()

		self.__trace.detrend()# funcion de la libreria stream que quita la media de un trazo para que este se encuentre encerado.
		self.__frecuencia = self.__trace.stats.sampling_rate
		self.__eventTraceList = []
		self.__subSearchTimeTraces = []# se usa para el control de la recursion durante la construccion del objeto, al final almcenara espacios de busqueda con un filtro
		self.__highestPoint = self.__trace.max()
		self.__noDataTimes = []

		if argNum != 5:
			if self.__eventObteiner(self.__trace, self.__t):
				self.__subTracesManager(self.__trace)
				self.__subSearchTimeTraces = self.__timesOrganizer()

				if multiple:
					self.__incomingTraces()
					self.__gapSetter()
					self.__subSegmenter()
					l=[]
					l.append(self.__eventTraceList  [6])
					#self.__timeSearcher(l)

	def __incomingTraces(self):# dado que si se interrumpe la señal un trazo se compone de varios puestos en el objeto trazo de forma bidimensional
		if len(self.__oTrace) != 1:
			#print ("\n Datos incompletos en relacion al tiempo")
			for x in range(1, len(self.__oTrace)):
				senial = SignalDg(self.__oTrace[x], self.__minimumPointEvent, self.__analisisTimeLapse, "trace")
				self.__eventTraceList.extend(senial.getEventLaps())
				self.__subSearchTimeTraces.extend(senial.getTimes("T"))
				if self.__highestPoint < senial.getMaxAmp():
					self.__highestPoint = senial.getMaxAmp()
				self.__tf = senial.getETime()
		else:
			print("Datos Completos")

	def __gapSetter(self):
		tiempos = []
		for x in range(0, len(self.__oTrace)-1):
			self.__noDataTimes.append([self.__oTrace[x].stats.endtime, self.__oTrace[x+1].stats.starttime])
		if self.__oTrace[-1].stats.endtime < self.__tf:
			self.__noDataTimes.append([self.__oTrace[-1].stats.endtime, self.__tf])
		self.__tf = self.__oTrace[-1].stats.endtime

	def __subTracesManager(self, trace):#funcion que gestiona la segmentacion del trazo para iniciar los analisis detallados

		aTime = self.__subSearchTimeTraces[-1][0]#fin a
		saTime = self.__timePicker(aTime, "a")#inicio a
		bTime = self.__subSearchTimeTraces[-1][1]#inicio b
		sbTime = self.__timePicker(bTime, "b")#fin b

		if(aTime != saTime):#entra en el if si el tiempo inicial y final de la rama a del árbol son diferentes,evita que se envíe un trazo nulo
			subTraceA = trace.slice( saTime,aTime)#Envía el trazo seleccionado para cortarlo
			if(subTraceA.stats.starttime!=subTraceA.stats.endtime):#evita que se envíe un trazo nulo si después de cortar el trazo el tiempo inicial y final son iguales
				if self.__eventObteiner(subTraceA, saTime):
					self.__subTracesManager(subTraceA)

		if(bTime != sbTime):#entra en el if si el tiempo inicial y final de la rama b del árbol son diferentes,evita que se envíe un trazo nulo
			subTraceB = trace.slice(bTime,sbTime)#Envía el trazo seleccionado para cortarlo
			if(subTraceB.stats.starttime!=subTraceB.stats.endtime):#evita que se envíe un trazo nulo si después de cortar el trazo el tiempo inicial y final son iguales
				if self.__eventObteiner(subTraceB, bTime):
					self.__subTracesManager(subTraceB)

	def __timePicker(self, time, type):#regresa el siguiente tiempo elegible para determinar  una traza
		control = True
		dateReturn = UTCDateTime('1000-01-10 05:00:00')
		if type == "a": # si se tiene la fecha de inicio buscara la fecha de finalizacion
			for x in range(0,len(self.__subSearchTimeTraces)):
				if(time > self.__subSearchTimeTraces[x][1]):
					control = False
					if dateReturn < self.__subSearchTimeTraces[x][1]:
						dateReturn = self.__subSearchTimeTraces[x][1]

			if control:
				dateReturn = self.__t
		else:# si se tiene la fecha de fin se buscara la de inicio
			for x in range(0,len(self.__subSearchTimeTraces)):
				if(time <= self.__subSearchTimeTraces[x][0]):
					control = False
					if dateReturn < self.__subSearchTimeTraces[x][0]:
						dateReturn = self.__subSearchTimeTraces[x][0]

			if control:
				dateReturn = self.__tf

		return dateReturn

	def __eventObteiner(self, trace, t):
		topPoint = trace.max()#obtiene el púnto maximo del trazo trace
		if abs(topPoint) >= self.__minimumPointEvent:#Ingresa si el puno maximo del trazo es mayor o igual que el punto mínimo para considerar que existe un evento
			puntoAlto = self.__highestPointPosition(trace,topPoint)
			timei = t+(1/self.__frecuencia)*puntoAlto - self.__analisisTimeLapse/2
			if timei < t:
				timei = t
			timef = t+(1/self.__frecuencia)*puntoAlto + self.__analisisTimeLapse/2
			sTrace = trace.slice(timei,timef)
			#sTrace.detrend()
			main = SignalDg(sTrace , sTrace.stats.starttime ,sTrace.stats.endtime, self.__minimumPointEvent,self.__analisisTimeLapse)# el segemento se toma como evento y se crea como nuevo Objeto signal !!!!!!!!!!!!!!1!!!!!
			self.__eventTraceList.append(main)
			tiempos = [timei, timei+(1/self.__frecuencia)*(main.__trace.count()-1), "E"]
			if tiempos not in self.__subSearchTimeTraces:
				self.__subSearchTimeTraces.append([timei, timei+(1/self.__frecuencia)*(main.__trace.count()-1), "E"])# veremos si se usa !!!!!!!!!!!!!!!!!
			return True
		else:#Ingresa aqui si el punto máximo del trazo es menor al punto mínimo para considerar evento, por lo cual no existe un evento
			timei = t
			timef = t+(1/self.__frecuencia)*(trace.count()-1)
			self.__subSearchTimeTraces.append([timei, timef, "N"])
			return False

	def __timesOrganizer(self):# organiza los tiempos usados guardados en base a la existencia de eventos
		internal = []
		internal2 = []
		i = 0
		for x in range(0,len(self.__subSearchTimeTraces)):
			control = True
			control2=True
			if self.__subSearchTimeTraces[x][2] == "E":#entra en este if en caso de que en este periodo de tiempo haya un evento
				for y in range(0,len(internal)):
					if x == 0:
						internal.append(self.__subSearchTimeTraces[0])
						internal2.append(self.__eventTraceList[0])
						control = False
						break
					else:
						if control and self.__subSearchTimeTraces[x][1] <= internal[y][0]:
							internal.insert(y,self.__subSearchTimeTraces[x])
							control = False
						if control2 and y<len(internal2) and (self.__eventTraceList[i].getTrace().stats.endtime<=internal2[y].getTrace().stats.starttime):
							internal2.insert(y,self.__eventTraceList[i])
							control2=False
						if(control==False and control2==False):
							break
				if control:
					internal.append(self.__subSearchTimeTraces[x])
				if control2:
					internal2.append(self.__eventTraceList[i])
				i = i+1
			else:#entra en este elif en caso de que en este periodo de tiempo no haya un evento
				for y in range(0,len(internal)):
					if x == 0:
						internal.append(self.__subSearchTimeTraces[0])
						control = False
						break
					elif self.__subSearchTimeTraces[x][1] <= internal[y][0]:
						internal.insert(y,self.__subSearchTimeTraces[x])
						control = False
						break
				if control:
					internal.append(self.__subSearchTimeTraces[x])

		self.__eventTraceList = internal2

		return internal

	def __highestPointPosition(self, trace, highestPoint):
		for x in range(0,trace.count()):
			if(trace[x] == highestPoint):
				return x# retorna la posicion de la diferencia mas alta que se puede encontrar

	def __subSegmenter(self):# se trabaja ocn tipo de datos SignalDg
		self.__eventTraceList[5].getTrace().plot()
		lista = [self.__eventTraceList[5]]
		#toBeReplaced = self.__pikeSearcher(lista, 5,False)
		#toBeReplaced = self.__pikeSearcher(self.__eventTraceList, -1, False)

		#toBeReplaced = self.__dataConverter(self.__eventTraceList, -1, False)
		#toBeReplaced = self.__dataConverter(lista, 5, False)
		#recuerda reconstruir  como se determina el punto inicial en el primer for  un for negativo
		'''d = 0
		print("\nEntramos")
		print("longitud:  ",len(toBeReplaced))
		for x in range(0,len(toBeReplaced)):
			pos = toBeReplaced[x][1]
			pos2 = toBeReplaced[x][2]
			print("\nD = ", d, "Largo de eventos", len(self.__eventTraceList))
			print( "Pos = " ,pos ,", pos+d = " ,pos+d , ", pos2 = ", pos2 , ", pos2+d = ", pos2+d)
			print()
			self.__eventTraceList.pop(pos + d)
			self.__subSearchTimeTraces. pop(pos2 +d)
			for y in range(0,  len(toBeReplaced[x][0])):
				self.__eventTraceList.insert(pos + d,toBeReplaced[x][0][y])
				self.__subSearchTimeTraces.insert(pos2 + d, [toBeReplaced[x][0][y].getTrace().stats.starttime, toBeReplaced[x][0][y].getTrace(), "E" ])
				d = d+1
			d = d-1'''

	def __dataConverter(self, lista, numero, value):
		toBeReplaced = []

		for x in lista:
			alma = x.getTrace().copy()
			testx = []
			testy = []

			for y in range(0, len(alma)):
				testy.append(abs(alma[y]))
				testx.append(y)
				alma.data[y] = (abs(alma[y]))
			alma2 = x.getTrace().copy()				
			#preuba de todos los datos

			f = interpolate.interp1d(testx, testy, kind="linear")
			ax_int = np.linspace(testx[0],testx[-1], 30)
			ay_int = f(ax_int)

			fig, ax = plt.subplots(figsize=(8, 6))
			ax.plot(testx, testy, color='red', label= 'Unsmoothed curve')
			ax.plot(ax_int, ay_int, color="blue", label= "Interpolated curve")
			fig.show()

			#a.append(ax_int, ay_int)

			alma2 = smooth(alma, 20)

			fig, ax = plt.subplots(figsize=(8, 6))
			ax.plot(testx, testy, color='red', label= 'Unsmoothed curve')
			ax.plot(testx, alma2, color="blue", label= "Interpolated curve")
			fig.show()

			#b = self.__pikeSearcher(testx, alma2)

			sera = []
			for y in range(0, len(alma2)):
				sera.append(alma2[y])

			f = interpolate.interp1d(testx, alma2, kind="linear")
			cx_int = np.linspace(testx[0],testx[-1], 81)
			cy_int = f(cx_int)

			fig, ax = plt.subplots(figsize=(8, 6))
			ax.plot(testx, testy, color='red', label= 'Unsmoothed curve')
			ax.plot(cx_int,cy_int, color="blue", label= "Interpolated curve")
			fig.show()

			#c = self.__pikeSearcher(cx_int, cy_int)
			print("b len. ", len(testx), " su media es: ", self.__localMean(alma2),  self.__localMean(x.getTrace()),"  c len. ", len (cx_int))

			print("ahora va el grafico 2 .....")
			print (len(self.__pikeSearcher( x ,testx, alma2, False, "b")) )

			print("ahora va el grafico 1 ..... lenx = ", len(ax_int), " leny =", len(ay_int) , " longitud real ", len(x.getTrace()))
			#print (len(self.__pikeSearcher( x ,ax_int, ay_int, False, "a")) )

			print("ahora va el grafico 3 .....")
			#print (len(self.__pikeSearcher( x ,cx_int,cy_int, False, "a")) )		

			#toBeReplaced.append(self.__pikeComparer(self.__pikeSearcher( x ,testx, alma2, False) , self.__pikeSearcher( x ,cx_int, cy_int, False)))

		return toBeReplaced

	def __pikeSearcher(self, sDG, xa, ya, aleluya, type):
		trace = sDG.getTrace()
		#media = self.__localMean(trace)
		media = self.__localMean(ya)
		control = True
		exist = []
		sss = []
		toBeReplaced = []

		d = 0
		u = 0

		if type == "a":
			#parameter = self.__umbralSetter(media, aleluya)
			parameter = [abs(media/4), 5]
			pos = 0
			for x in range(1, len(ya) - 1):
				if ya[pos] < ya[x]:
					pos = x		

		if type == "b":
			#parameter = self.__umbralSetter(media, aleluya)
			parameter = [abs(media/4), 15]
			pos = self.__highestPointPosition(trace, sDG.getMaxAmp()) #si se busca la posicion media se tiene el mismo int, Se plantea una venta de separacion entre los sismos de 20

		#print("\ndespues max es: ", len(trace) , "media es : = ", media ,":\n")
		print("whadahell:", pos)
		y = pos
		
		while y > 0:
			if control:
				if self.__lineDefiner(ya, y , parameter[1], parameter[0], media, "i"):
					#print("\n original y = ", y)
					control = False
					d = y
					y = d
					#print("evol y=", y, " el otro d = ", d)
					#print(trace.stats.starttime + (d/self.__frecuencia))
			elif ya[y] >= self.__minimumPointEvent:
				#print("wWHY afsadf valor =", trace[y])
				control = True
				#print("y=", y, " el otro d = ", d)
				z = 0
				while True:
					if y+z  == d :
						break
					if self.__lineDefiner(ya, y + z , parameter[1], parameter[0], media, "d"):
						u =  y + z
						break
					z = z + 5
				#print(" con  u = ", u, "y d =", d)
				if u < d:
					exist.append(((d-u) /2) + u)
			y = y - 5
			#print("\ndespues max es: ", len(trace) , "punto minimo es : = ", self.__minimumPointEvent ,":\n")
		control = True
		y = pos
		while y < len(ya):
			if control:
				if self.__lineDefiner(ya, y , parameter[1], parameter[0], media, "d"):
					control = False
					d = y
					y = d
			elif ya[y] >= self.__minimumPointEvent / 2:
				control = True
				z = 0
				while True:
					if y-z  == d :
						break
					if self.__lineDefiner(ya, y - z , parameter[1], parameter[0], media, "i"):
						u =  y - z
						break
					z = z + 5
				if u > d:
					exist.append(((u-d) /2) + d) 
			y = y + 5

		try:
			print("\n Arreglo Exist:\n")
			for y  in exist:
				print(trace.stats.starttime + y/self.__frecuencia )

			print("\n tiempos del SS:\n" )
			timei = trace.stats.starttime
			for y in range(0, len(exist)):# poner el  tiempo final
				timef = trace.stats.starttime + exist[y]/self.__frecuencia
				print("inicio: ", timei)
				print("final:  ", timef, "\n")
				sTrace = trace.slice(timei,timef)
				main = SignalDg(sTrace , sTrace.stats.starttime ,sTrace.stats.endtime, self.__minimumPointEvent,self.__analisisTimeLapse)
				sss.append(main)
				timei = timef

			#sTrace = trace.slice(sss[-1].getTrace().stats.endtime,trace.stats.endtime) # hay que comentar esto para probar en serio
			if len(sss) > 0:
				sTrace = trace.slice(sss[-1].getTrace().stats.endtime,trace.stats.endtime)
				sss.append(SignalDg(sTrace , sTrace.stats.starttime ,sTrace.stats.endtime, self.__minimumPointEvent,self.__analisisTimeLapse))
				#toBeReplaced.append([sss, x, positions[x]])
				#toBeReplaced.append([sss, positions[x], positions[x]])
				toBeReplaced.append(sss)
				aleluya = False
		except ValueError:
			aleluya = True
			print("acaso entra por aca")
			toBeReplaced =  self.__pikeSearcher(self, sDG, xa, ya, aleluya)

		return toBeReplaced

	def __umbralSetter(self, media, aleluya ):
		val = 0
		number = 15
		i = 1
		while i*abs(media) <= self.__minimumPointEvent/16:
			i = i + 1

		val = i*abs(media)
		if (i <= 2 and abs(media)  >= self.__minimumPointEvent/13) :
			val = val/3
			number = 50

		if aleluya:
			val = val/4
			number = 80
		val = [val, number]
		print("\b Umbral: a", val[0], " dois: ", val[1] )
		return val

	def __lineDefiner(self, trace, punto,cantidad, variacion, media, dir):
		resultado = True
		counter = 0
		if dir == "d":
			for x in reversed(range( punto - cantidad, punto)):
				if (abs(trace[x]) - variacion) >= media:
					counter = counter + 1
				if counter > 0 :
					resultado = False
					break
			#if resultado and abs(self.__localMean(trace, punto, punto + cantidad))  >  media :
			#	resultado = False
		elif dir == "i":
			#print("\n PUnto de Control con el tiempo inicial aprox : ", trace.stats.starttime + punto/self.__frecuencia, "punto init :", punto, "hasta : ", punto+cantidad)
			for x in range(punto, punto + cantidad):
				if (abs(trace[x]) - variacion )>= media:
					counter = counter + 1
				if counter > 0 :
					resultado = False
					break
			#if resultado and abs(self.__localMean(trace, punto, punto - cantidad))  >  media :
			#	resultado = False
				#print("punto de analisis :", x,  "el trace es : ", abs(trace[x])-variacion, " la media es ", media , "  contador ", counter)

		return resultado

	def __localMean(self, *args): # si solo se envio un argumento y es un trace se obtiene la media de todo el trazo; si son 3 argumentos devolvera la media de un trazo en los puntos dados 

		media = 0
		trace = args[0]
		if len(args) == 1:
			suma = 0
			for x in range(0, len(trace)):
				suma = suma + trace[x]
			media =  suma / len(trace)

		if len(args) == 3:
			suma = 0
			almacen1 = args[2]

			if almacen1 > len(trace):
				almacen1 = len(trace)

			for x in range(args[1], almacen1):
				suma = suma + trace[x]
			media =  suma / len(trace)

		return media

	#busca si algun evento fue cortado  e identifica donde quedó la otra parte
	#identifica en que posición deberá insertarse dicho trazo
	#recibe los trazos cortados y los inserta en la lista de eventos y en el de los tiempos
	def __timeSearcher(self, l):
		self.__eventTraceList[6].getTrace().plot()
		posicion=0#la posición donde debería agregarse el evento
		t=0#para almacenar los nuevos tiempos de la union de dos trazos
		aux=[]#trazo auxiliar a analizar
		trazo=[]#trazo cortado para buscar un evento
		analizar=[]#union de dos trazos que se envía para cortar
		Trazos=[]
		Tiempos=self.__subSearchTimeTraces#lista de tiempos de todos los trazos
		timei=0#guarda el tiempo inicial para cortar el trazo
		timef=0#guarda el tiempo final para cortar el trazo
		bandera=False
		#recorre toda la lista de eventos
		print ("La longitud de la lista ",len(l))
		for x in range(0,len(l)):
			print("Iteracion numero: ",x)
			aux=l[x].getTrace()
			bandera=False
			analizar=[]
			Trazos=[]
			timei=aux.stats.starttime#tiempo inicial del trazo
			timef=aux.stats.starttime+((aux.stats.endtime-aux.stats.starttime)*0.3)#al tiempo inicial del trazo le sumo el 10% del total
			trazo=aux.slice(timei,timef)#evalúa si hay un evento al inicio del trazo
			topPoint = trazo.max()#toma el punto maximo del inicio del trazo

			if abs(topPoint) >= self.__minimumPointEvent:#entra en el if en caso de que deba considerarse como evento
			#busco en la lista de tiempos el trazo que tiene como tiempo final el inicial del trazo
				for y in range(0,len(Tiempos)):
					p=str(Tiempos[y][1])#se amaena el tiempo inicial de la lista __subSearchTimeTraces
					a=p.split(".")
					p=str(timei)#se guarda el tiempo final del trazo a analizar
					b=p.split(".")
					print("\nTiempo final= ",a[0])
					print("Tiempos inicial= ",b[0])

					if(a[0]==b[0]):#si el inicial es igual al final
						t=Tiempos[y][0]#almaceno el nuevo tiempo inicial
						print("\n \n Nuevo tiempo inicial ",t, "trazo numero ",y)
						self.__subSearchTimeTraces.pop(y)
						bandera=True
						break
			if(bandera):#continúa si encuentra un evento
				posicion=x
				analizar[0]=t
				for z in range(0,len(self.__eventTraceList)):
					if(self.__eventTraceList[z].getTrace().stats.starttime==analizar[0]):
						break;
				self.__eventTraceList.pop(6)
				trazo=self.__traceSlicer(timei,t)
				Trazos.append(SignalDg(trazo,timei,t,self.__minimumPointEvent,self.__analisisTimeLapse))
				analizar=self.__pikeSearcher(Trazos,x,False)#envío a analizar el nuevo trazo
				aaa=SignalDg(trazo,timei,t,self.__minimumPointEvent,self.__analisisTimeLapse)
				self.__eventTraceList.insert(6,aaa)
				self.__subSearchTimeTraces.insert(y,[timei,t, "E"])
				self.__subSearchTimeTraces[y-1][1]=timei
				posicion=posicion+1
				x=posicion-1
				self.__eventTraceList.pop(x)
				for y in range(0,len(analizar)):
					self.__eventTraceList.insert(posicion,analizar[0][y])
					self.__subSearchTimeTraces.insert(posicion,[analizar[0][y].stats.starttime,analizar[y].stats.endtime, "E"])
					posicion=posicion+1
					x=posicion-1
				aux=l[x].getTrace()

			bandera=False
			analizar=[]
			timei=aux.stats.endtime-((aux.stats.endtime-aux.stats.starttime)*0.3)#tiempo inicial del trazo
			print ("Tiempo de inicio del nuevo trazo ",timei)
			timef=aux.stats.endtime#al tiempo final del trazo
			topPoint = aux.max()#toma el punto maximo del final del trazo
			if abs(topPoint) >= self.__minimumPointEvent:#entra en el if en caso de que deba considerarse como evento
				#busco en la lista de tiempos el trazo que tiene como tiempo final el inicial del trazo
				for y in range(1,len(Tiempos)):
					p=str(Tiempos[y][0])#se amaena el tiempo inicial de la lista __subSearchTimeTraces
					a=p.split(".")
					p=str(timef)#se guarda el tiempo final del trazo a analizar
					b=p.split(".")
					print("\nTiempo inicia= ",a[0])
					print("Tiempos iguales ",b[0])
					if(a[0]==b[0]):
						t=Tiempos[y][1]#almaceno el nuevo tiempo final
						print("\n \n Nuevo tiempo final ",t, "trazo numero ",y)
						analizar=self.__subSearchTimeTraces[y]
						self.__subSearchTimeTraces.pop(y)
						bandera=True
						break
			if(bandera):#continúa si encuentra un evento
				posicion=x
				analizar[1]=t
				for z in range(0,len(self.__eventTraceList)):
					if(self.__eventTraceList[z].getTrace().stats.starttime==analizar[0]):
						break;
				self.__eventTraceList.pop(6)
				trazo=self.__traceSlicer(timei,t)
				Trazos.append(SignalDg(trazo,timei,t,self.__minimumPointEvent,self.__analisisTimeLapse))
				analizar=self.__pikeSearcher(Trazos,x,False)#envío a analizar el nuevo trazo
				aaa=SignalDg(trazo,timei,t,self.__minimumPointEvent,self.__analisisTimeLapse)
				self.__eventTraceList.insert(6,aaa)
				self.__subSearchTimeTraces.insert(y,[timei,t, "E"])
				self.__subSearchTimeTraces[y-1][1]=timei
				posicion=posicion+1
				x=posicion-1
				'''#for y in range(0,len(analizar)):
						self.__eventTraceList.insert(12,trazo)
						self.__subSearchTimeTraces.insert(posicion,[analizar[0][y].stats.starttime,analizar[y].stats.endtime, "E"])
						posicion=posicion+1
						x=posicion-1'''
			self.__eventTraceList[6].getTrace().plot()

	def __traceSlicer(self,timei,timef):
		temp=self.__oTrace
		print("No Data len ",len(temp))

		aux=None
		for x in range(0,len(temp)):
			#print("Iteracion ",x)
			if(temp[x].stats.endtime>=timef):
				temp[x].detrend()
				aux=temp[x].slice(timei,timef)
				#print ("OTrace num ",x)
				break
		#aux.plot()
		#temp[x].plot()
		return aux
		lista=self.__subSearchTimeTraces
		print("Antes ",len(lista))
		x=0
		while x<len(lista)-1:
			if lista[x][2]=='N' and  lista[x+1][2]=='N':
				lista[x][1]=lista[x+1][1]
				lista.pop(x+1)
				x=x+1
			x=x+1
		self.__subSearchTimeTraces=lista
		print("Despues ",len(self.__subSearchTimeTraces))

	def __timeAranger(self):
		hola = 1

# LAS FUNCIONES SIGUIENTES NO SON PARTE FUNCIONAL DE LA CREACION DEL OBJETO; SON FUNCIONES DE MUESTREO U OBTENCION DE DATOS

# falta lograr encapsulacion :S a pesar del get se pasa la informacion; la solucion seria crear una nueva lista y copiar de uno en uno los datos o algo asi

	def getTimes(self, letra ):# imprime todos los tiempos analisados si se pone T de arugmento, con E solo tiempos de eventos si se pone N los trazos sin eventos
		times = []
		if letra == "T":#si se quiere imprimir todos los tiempos, haya evento(E) o no(N)
			for x in range(0,len(self.__subSearchTimeTraces)):
				times.append(self.__subSearchTimeTraces[x])
		elif letra == "E" or "N":#En caso de que se quiera imprimir únicamente los tiempos que tengan eventos(E) o los que no(N)
			for x in range(0,len(self.__subSearchTimeTraces)):
				if(self.__subSearchTimeTraces[x][2] == letra):
					times.append(self.__subSearchTimeTraces[x])
		else:
			print("Fracaso")

		return times

	def addTimes(self, Ttimes):
		self.__subSearchTimeTraces.extend(Ttimes)

	def getStats(self):
		status = self.__trace.stats()
		return status

	def getMinPoint(self):
		min = self.__minimumPointEvent
		return min

	def getTrace(self):
		trace = self.__trace
		return trace

	def getOTrace(self):
		trace = self.__oTrace
		return trace

	def addOTrace(self, moreTraces):
		self.__oTrace.extend(moreTraces)

	def getFrecuencia(self):
		frecuencia = self.__frecuencia
		return frecuencia

	def getSTime(self):
		sTime = self.__t
		return sTime

	def getETime(self):
		eTime = self.__tf
		return eTime

	def setETime(self, newTime):
		self.__tf = newTime

	def getMaxAmp(self):
		hp = self.__highestPoint
		return hp

	def setMaxAmp(self, newAmp):
		self.__highestPoint = newAmp

	def getEventLaps(self): # se debe hacer sobre carga con args para obtener solo uno de los laps
		eLaps = self.__eventTraceList
		return eLaps

	def addEventLaps(self, moreEventLaps): # se debe hacer sobre carga con args para obtener solo uno de los laps
		self.__eventTraceList.extend(moreEventLaps)

	def plotEventLaps(self):# se debe hacer sobre carga con args para plotear solo uno
		num = 0
		for x in self.__eventTraceList:
			print(num)
			num =num + 1
			x.getTrace().plot()

	def getNumberELaps(self):
		return len(self.__eventTraceList)

	def plotNoEvents(self):
		for x in range(0,len(self.__subSearchTimeTraces)):
			if(self.__subSearchTimeTraces[x][2] == "N"):
				self.__trace.slice( self.__subSearchTimeTraces[x][0],self.__subSearchTimeTraces[x][1]).plot()

	def getNoDataTimes(self): # se debe hacer sobre carga con args para obtener solo uno de los laps
		nodata = self.__noDataTimes
		return nodata

	def addNoDataTimes(self, data): # se debe hacer sobre carga con args para obtener solo uno de los laps
		self.__noDataTimes.extend(data)

segLocal = SignalDg('ovolcan.mseed', 1000, 320)

#segLocal = SignalDg('EC.BVC2..BHZ.D.2018.002', 1000, 320)

'''def bigTimesManager(nombre1, nombre2, nombre3, nombre4, fechainit, dias, amp, ventana):
	dgSignals = []
	added = 0 
	tiempox = UTCDateTime(fechainit)

	for x in range(0, dias):
		dgSignals.append(SignalDg(nombre1,nombre2,nombre3,nombre4,str(tiempox + added), 24, amp, ventana))
		added = added + 86400

	superSignal = dgSignals[0]
	for x in range(1, len(dgSignals)):
		superSignal.addTimes(dgSignals[x].getTimes("T"))
		superSignal.addOTrace(dgSignals[x].getOTrace())
		superSignal.setETime(dgSignals[x].getETime())
		if superSignal.getMaxAmp() < dgSignals[x].getMaxAmp():
			superSignal.setMaxAmp(dgSignals[x].getMaxAmp())
		superSignal.setETime(dgSignals[x].getETime())
		superSignal.addNoDataTimes(dgSignals[x].getNoDataTimes())

	return superSignal

sera = bigTimesManager('EC','CAYR','','SHZ','2017-01-24  00:00:00', 2, 1000, 320)'''


