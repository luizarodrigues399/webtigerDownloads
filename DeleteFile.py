from datetime import datetime, date, timedelta
import os, time, Config, shutil


def Delete(path):
        for filename in os.listdir(path):
                hoje = datetime.now()
                info = os.stat(path+filename)
                dataAntiga = datetime.strptime(time.ctime(info.st_mtime), "%a %b %d %H:%M:%S %Y") #info.st_mtime-> ultima modificacao
                time.sleep(1)

                diferenca =(hoje - dataAntiga)
                diferencaSeconds =  diferenca.seconds
                diferencaDays = diferenca.days 
                if (diferencaSeconds >= 18000) or (diferencaDays >= 1): # 5 horas ou mais de 1 dia    
                        print "DELETANDO:",filename," ",diferenca
                        shutil.rmtree(path+filename)
                        time.sleep(1)

if __name__ == "__main__":        
        tempo = datetime.now() #anterior
        time.sleep(2)

	path = Config.ProjectDir	
        while (True):
                tempo2=datetime.now() #atual
                diferenca = (tempo2 - tempo)
                if (diferenca >= timedelta(seconds=10)): #(minutes=1)):
                        try:
                                Delete(path)
                        except Exception as e:
                                print e 
                        tempo =  tempo2 #anterior
                





