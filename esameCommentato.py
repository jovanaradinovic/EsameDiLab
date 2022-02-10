
import datetime #aggiungo la libreria per verificare date 

class ExamException(Exception): #creo la classe per le eccezioni

    pass
 
class CSVTimeSeriesFile: #creo una classe in grado di leggere una serie temporale che può calcolare la varianza media per ogni mese
    def __init__ (self,name): #Costruttore che prende il nome del file
        self.name = name #imposta il nome
        if not isinstance(name, str): 
            raise ExamException(f"Error: parametro 'name' deve essere una stringa e non '{type(name)}'") #Se name non è una stringa, genera un errore e torna a main
        pass   #f modo per formattare le stringhe che permette l’inserimento attraverso le graffe di valori al interno 

    def is_date(self,string): #creo la classe per verificare se è una stringa
        format="%Y-%m" #definire format
        try:
            datetime.datetime.strptime(string,format) #Restituisce true se la stringa può essere interpretata come una data.
            return True

        except ValueError: 
            return False

    def get_data(self): #Creo una lista che restituisce liste con liste di data
        
        complete_list = [] #Inizializzare un elenco vuoto per salvare tutti i valori
 
        try:
            my_file = open(self.name, 'r')
        except Exception as e: 
           raise ExamException(f"Error successso leggendo file '{e}'") #Provo ad aprire il file e ottenere i dati se non riesce a sollevare, eccezione e aborto.

        for line in my_file: #Se riesco ad aprire il file comincio a leggere riga per riga

            elements = line.split(",") #Divisione separata da virgola

            if elements[0] != 'date': #Salto il primo elemento che è heading

                try: #Ho impostato la data e il valore
                    date = str(elements[0])
                    #Controlla se la data non ha senso come data
                    # Utilizzando la funzione di supporto che ho aggiunto alla classe
                    if not self.is_date(date): 
                    # Esegui se l'output di is_date è False
                    # E vai al ciclo successivo
                        continue

                    value = int(elements[1]) # Rendi il valore un intero se non lo è non accettarlo

                    if value < 0:
                        continue # Se il valore è un numero negativo non accettarlo e continuare
                except:
                    continue

                if len(complete_list) > 0: # Controlla se il timestamp è un duplicato di uno qualsiasi dei timestamp di anteprima salvati
                    for item in complete_list: # Scorri i timestamp dell'anteprima
                        prev_date = item[0] # Salva il valore dei dati sul timestamp delle anteprime

                        if date == prev_date:
                            raise ExamException("Timestamp è un duplicato")

                    prev_date = complete_list[-1][0] # Controlla se il timestamp segue quello precedente
                    if date < prev_date:
                        raise ExamException("Timestamp non è in ordine")

                complete_list.append([date,value]) # Aggiungo la data e gli elenchi di valori all'elenco principale per ogni passaggio

        my_file.close() #Chiudo il file

        if not complete_list:
            raise ExamException("File è vuoto") 

        return complete_list

def compute_avg_monthly_difference(time_series,first_year,last_year): # Funzione per calcolare la media
    if(last_year > time_series[-1][0][:4]):
        raise ExamException("Error: last_year non è presente in data.csv file")

    if(first_year < time_series[0][0][:4]): 
        raise ExamException("Error: first_year non è presente in the data.csv file")    

    if first_year == last_year: # Se i due anni indicati sono gli stessi
        raise ExamException("Primo e secondo anno sono uguali")    

    if not isinstance(time_series, list):
        raise ExamException(f"Error: parameter 'time_series' deve essere una lista e non '{type(time_series)}'") 
    
    # Controlla se first e last_year sono stringhe
    if type(first_year) is not str:
        raise ExamException(f"First_year non è un valore computabile. Tipo di dato inserito: {type(first_year)}")  

    if type(last_year) is not str:
        raise ExamException(f"Last_year non è un valore computabile. Tipo di dato inserito: {type(last_year)}")         
    
    data = [int(i[1]) for i in time_series if int(i[0][:4]) >= int(first_year) and int(i[0][:4]) <= int(last_year)] #riempie data se l'anno è compreso nell'intervallo tra il primo e l'ultimo anno
    years = int(last_year)-int(first_year)+1 #numeri di anni che si considerano
    result = [[]for i in range(0,years)] #riempie con liste vuote tante quanti sono gli anni

    conta = 0

    for i in range(0,len(data)):
        if i != 0 and i % 12 == 0: 
                conta+=1
        result[conta].append(data[i]) # riempie le 3 liste di prima con i mesi di ciascun anno

    avg = [] #inizzializare un elenco vuoto per average 
    somma = 0
    conta = 0
    for i in range(0,12): # i scorre gli elemementi delle sottoliste
        for j in range(1,years): # j scorre gli anni
            if (result[j][i] == 0 or result[j-1][i] == 0) and years == 2: #due casi dove ignoro quelli mesi 
                somma = 0 
            else: 
                if (result[j][i] == 0 or result[j-1][i] == 0) and years > 2:
                    conta += 1
                    if(conta - years < 2): #servirebbe years - conta
                        somma = 0
                        j = years
                    else:
                        somma += 0
                else:
                    somma += result[j][i] - result[j-1][i]
        avg.append(somma/(years-1))
        somma = 0
    
    return avg  #ritorna average 


def main():
    pass



