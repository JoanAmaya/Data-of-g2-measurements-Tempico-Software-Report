import numpy as np
import matplotlib.pyplot as plt
import pyTempico as tempico
import bisect
import time

class default_settingsg2():
    def __init__(self):
        self.device=tempico.TempicoDevice('COM9')
        self.device.open()
        self.device.reset()
        
        self.device.ch1.enableChannel()
        self.device.ch2.enableChannel()
        self.device.ch3.enableChannel()
        self.device.ch4.enableChannel()
        self.device.close()
    


class generate_g2():
    def __init__(self):
        #Init parameters
        #Open the connection with the device
        self.device=tempico.TempicoDevice('COM9')
        self.device.open()
        print(self.device.getSettings())
        
        try:
        # self.device.reset()
        # self.device.ch3.disableChannel()
        # self.device.ch4.disableChannel()
            self.totalTime=0
            self.device.setNumberOfRuns(100)
            self.device.setThresholdVoltage(1.6)
            self.data_coincidente=[]
            #Set up the parameters of the channels to get the measurements
            self.chA=self.device.ch1
            self.chB=self.device.ch3
            self.device.ch1.enableChannel()
            self.device.ch2.disableChannel()
            self.device.ch3.enableChannel()
            self.device.ch4.disableChannel()
            self.chA.setMode(2)
            self.chB.setMode(2)
            self.chA.setNumberOfStops(2)
            self.chB.setNumberOfStops(2)
            self.chA.setStopMask(0)
            self.chB.setStopMask(0)
            #Average values for take the g2 with only a start
            self.get_measurement()
            self.average_timeA=0
            self.average_timeB=0
            self.average_timeA=self.get_average_counts(self.measStStchA)
            self.average_timeB=self.get_average_counts(self.measStStchB)
            print("El promedio de tiempo de llegada para el canalA es de "+str(self.average_timeA))
            print("El promedio de tiempo de llegada para el canalB es de "+str(self.average_timeB))
            
            # self.all_g2_measurements()
            # self.calculate_total_time()
            # self.create_g2_data()
            # self.create_g2_graphic()
            # self.create_histogram_g2()
            self.device.close()
        except:
            self.device.close()
            
    #Funcion para generar una medicion en el tempico
    #La funcion devuelve un array con números en microsegundos
    #La g2 a realizar sera en un intervalo de microsegundos
    def all_g2_measurements(self):
        for i in range(20):
                print("Intento de medición número: "+str(i+1)+" de 200")
                self.get_g2_measurement()
        if len(self.data_coincidente)==0:
            exit_or_not=input("Escriba 1 si quiere volver a intentar o cualquier otra cosa si quiere salir")
            if exit_or_not=="1":
                print("Intentando nuevamente realizar las mediciones")
                time.sleep(2)
                self.all_g2_measurements()
                
    def calculate_total_time(self):
        for i in self.data_coincidente:
            temp_value=abs(i)
            self.totalTime+=temp_value
           
    
    def get_measurement(self):
        self.measStStchA=[]
        self.measStStchB=[]
        for i in range(10):
            try:
                medicion=self.device.measure()
                print(medicion)
                print("Medicion intento número "+str(i)+" de 10")
                print(medicion)
                for i in medicion:
                    if len(i)==5:
                        chnumber=i[0]
                        stop_1=i[3]
                        stop_2=i[4]
                        if stop_1!=-1 and stop_2!=-1:
                            stop_diference=abs(stop_2-stop_1)
                            stop_diference=stop_diference/(10**6)
                            if chnumber==1:
                                self.measStStchA.append(stop_diference)
                            else:
                                self.measStStchB.append(stop_diference)
            except:
                print("No se pudo realizar la medicion número de intento fallido: "+str(i)+"/10")                    
            
        if len(self.measStStchA)==0 or len(self.measStStchB)==0:
            exit_or_not=input("Escriba 1 si quiere volver a intentar o cualquier otra cosa si quiere salir")
            if exit_or_not=="1":
                print("Las 10 mediciones no pudieron ser realizadas intentando nuevamente")
                time.sleep(2)
                self.get_measurement()
        
            
    #Get the average of the stops to get the measure of pulses time arrive
    def get_average_counts(self,channel_Array):
        total_values=len(channel_Array)
        total_sum=sum(channel_Array)
        total_average=total_sum/total_values
        return total_average
    
    
    def get_g2_measurement(self):
        self.chA.setNumberOfStops(1)
        self.chB.setNumberOfStops(1)
        old_time=self.totalTime
        old_data_coincidence=self.data_coincidente
        medicion=self.device.measure()
        data_tuple=[]
        try:
            for i in range(100):
                dataA=medicion[i]
                dataB=medicion[i+100]
                tupla=(dataA,dataB)
                data_tuple.append(tupla)
            for i in data_tuple:
                if len(i[0])>0 and len(i[1])>0:
                    if i[0][3]!=-1 and i[1][3]!=-1:
                        #cambiar el nombre de coincidencia
                        stop_diference= i[1][3]-i[0][3]    
                        stop_diference=stop_diference/(10**6)
                        self.data_coincidente.append(stop_diference)
        except:
            self.data_coincidente=old_data_coincidence
            self.totalTime=old_time
    
    #Count the elements in the array between lower and upper
    def count_elements_in_range(self,arr, lower, upper):
        left_index = bisect.bisect_left(arr, lower)
        right_index = bisect.bisect_right(arr, upper)
        return right_index - left_index
                      
    def create_g2_data(self):
        #Tomaremos unicamente los valores iniciales de los puntos encontrados para hacer la gráfica 
        min_value=round(min(self.data_coincidente))
        max_value=round(max(self.data_coincidente))
        binwidth=5
        self.domain_values=np.arange(min_value,max_value,binwidth)
        self.g2_values=[]
        self.data_coincidente.sort()
        N_1=1/self.average_timeA
        N_2=1/self.average_timeB
        inverse_ct=N_1*N_2*self.totalTime*binwidth
        cte=1/inverse_ct
        self.cnst=cte
        for i in self.domain_values:
            range_lower=i-(binwidth/2)
            range_upper=i+(binwidth/2)
            N_12=self.count_elements_in_range(self.data_coincidente,range_lower,range_upper)
            g2_point=N_12*cte
            self.g2_values.append(g2_point)
        
    
    def create_g2_graphic(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.domain_values, self.g2_values, label='$g^{(2)}(\\tau)$', color='blue')
        plt.axhline(y=1, color='black', linestyle='--', linewidth=0.7)  # Línea base g2=1
        plt.xlabel('$\\tau$ (Tiempo)')
        plt.ylabel('$g^{(2)}(\\tau)$')
        plt.title('Función de correlación de segundo orden $g^{(2)}(\\tau)$')
        plt.legend()
        plt.grid(True)
        plt.savefig("Funciong2.png")
        plt.show()
        
    #valor teorico de acuerdo a los datos del arduino
    #g2 calculada con la formula original
    def create_histogram_g2(self):
        hist,bin_edges=np.histogram(self.data_coincidente,self.domain_values)
        new_hist=hist*self.cnst
        print("Histograma normalizado")
        print(new_hist)
        print("Longitud de datos de histograma")
        print(len(new_hist))
        print("Valores de g2 creados")
        print(self.g2_values)
        print("Longitud de datos de g2")
        print(len(self.g2_values))
        plt.figure(figsize=(10, 6))
        plt.hist(bin_edges[:-1], bins=bin_edges, weights=new_hist, alpha=0.7, color='blue', edgecolor='black')
        # Título y grid
        plt.title('Función de correlación de segundo orden $g^{(2)}(\\tau)$')
        plt.xlabel('$\\tau$ (Tiempo)')
        plt.ylabel('Frecuencia')
        plt.grid(True)
        
        # Guarda y muestra la figura
        plt.savefig("Histogramag2.png")
        plt.show()

        
        
        
        
objeto_prueba=generate_g2()
#defaul_values=default_settingsg2()

        











    

# #Prueba histograma
# data_counts=[0]
# max_data_amount=1000
# datos_aleatorios=(np.random.poisson(lam=4.0, size=max_data_amount))*10
# count, bins, ignored = plt.hist(datos_aleatorios, 14, density=True)
# plt.show()
# def promedio_datos_obtenidos(datos_obtenidos):
#     total_datos=len(datos_obtenidos)
#     suma_total=sum(datos_obtenidos)
#     promedio=suma_total/total_datos
#     return promedio

# print(promedio_datos_obtenidos(datos_aleatorios))

    


#File concept to create the g2 measurement for TempicoSoftware


#Codigo tempico software para obtener mediciones del tempico



#datos ficticios


