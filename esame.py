
import datetime

class ExamException(Exception): #classe per le eccezioni

    pass
 
class CSVTimeSeriesFile: 
    def __init__ (self,name):
        self.name=name
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
    pass




def main():
    pass



