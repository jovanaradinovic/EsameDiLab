
import datetime

class ExamException(Exception): #classe per le eccezioni

    pass
 
class CSVTimeSeriesFile:
    def __init__ (self,name):
        self.name = name
        if not isinstance(name, str):
            raise ExamException(f"Error: parametro 'name' deve essere una stringa e non '{type(name)}'")
        pass

    def is_date(self,string):
        format="%Y-%m"
        try:
            datetime.datetime.strptime(string,format)
            return True

        except ValueError:
            return False

    def get_data(self):
        
        complete_list = []
 
        try:
            my_file = open(self.name, 'r')
        except Exception as e: 
           raise ExamException(f"Error successso leggendo file '{e}'")

        for line in my_file:

            elements = line.split(",")

            if elements[0] != 'date':

                try:
                    date = str(elements[0])

                    if not self.is_date(date):
                        continue

                    value = int(elements[1])

                    if value < 0:
                        continue
                except:
                    continue

                if len(complete_list) > 0:
                    for item in complete_list:
                        prev_date = item[0]

                        if date == prev_date:
                            raise ExamException("Timestamp è un duplicato")

                    prev_date = complete_list[-1][0]
                    if date < prev_date:
                        raise ExamException("Timestamp non è in ordine")

                complete_list.append([date,value])

        my_file.close()

        if not complete_list:
            raise ExamException("File è vuoto")

        return complete_list

def compute_avg_monthly_difference(time_series,first_year,last_year):
    if(last_year > time_series[-1][0][:4]):
        raise ExamException("Error: last_year non è presente in data.csv file")
    if(first_year < time_series[0][0][:4]):
        raise ExamException("Error: first_year non è presente in the data.csv file")    
    if first_year == last_year:
        raise ExamException("Primo e secondo anno sono uguali")    
    if not isinstance(time_series, list):
        raise ExamException(f"Error: parameter 'time_series' deve essere una lista e non '{type(time_series)}'") 
    if type(first_year) is not str:
        raise ExamException(f"First_year non è un valore computabile. Tipo di dato inserito: {type(first_year)}")  
    if type(last_year) is not str:
        raise ExamException(f"Last_year non è un valore computabile. Tipo di dato inserito: {type(last_year)}")         
    
    data = [int(i[1]) for i in time_series if int(i[0][:4]) >= int(first_year) and int(i[0][:4]) <= int(last_year)]
    years = int(last_year)-int(first_year)+1
    result = [[]for i in range(0,years)]    

    conta = 0

    for i in range(0,len(data)):
        if i != 0 and i % 12 == 0: 
                conta+=1
        result[conta].append(data[i])

    avg = []
    somma = 0
    conta = 0
    for i in range(0,12):
        for j in range(1,years):
            if (result[j][i] == 0 or result[j-1][i] == 0) and years == 2:
                somma = 0
            else: 
                if (result[j][i] == 0 or result[j-1][i] == 0) and years > 2:
                    conta += 1
                    if(conta - years < 2):
                        somma = 0
                        j = years
                    else:
                        somma += 0
                else:
                    somma += result[j][i] - result[j-1][i]
        avg.append(somma/(years-1))
        somma = 0
    
    return avg


def main():
    pass



