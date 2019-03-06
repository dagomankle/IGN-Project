# se asume a esta funcion llegan dos arreglos en el cual cada elemento es una tupla de fecha inicial y final; el primer arreglo debe comprender al segundo 
import SegmenterAlfa.py

def dataComparator(*args):
	resultados = ""
	incluidos = 0
	# asdf
	if len(args) == 2:
		setA = args[0]
		setB = args[1]
		i = 0

		for x in range(0, len(setA)):
			if setA[x][0] > setB[i][1]:
				i = i +1
			if setA[x][0] <= setB[i][0] and setA[x][1] >= setB[i][1]:
				incluidos = incluidos  + 1
		resultados = [incluidos,len(setB), (incluidos*100)/len(setB)]

	return resultados

#seg = SignalDg('EC','CAYR','','SHZ','2017-01-24  00:00:00', 24, 1000, 320)
def bigTimesManager(nombre1, nombre2, nombre3, nombre4, fechainit, dias, amp, ventana):
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
		superSignal.addETime(dgSignals[x].getETime())
		superSignal.addNoDataTimes(dgSignals[x].getNoDataTimes())

	return superSignal

#sera = bigTimesManager('EC','CAYR','','SHZ','2017-01-24  00:00:00', 2, 1000, 320)
    
