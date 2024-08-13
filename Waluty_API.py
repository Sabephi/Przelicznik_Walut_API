import requests
import time

#Kalkulator walut

#dekorator liczący czas funkcji
def dek_czasu(funkcja):
    def opakowanie(*args, **kwargs):
        start = time.time()
        wynik = funkcja(*args, **kwargs)
        koniec= time.time()
        print(f"{'>'*9} Czas wykonania {'<'*9} \n{koniec - start} sekund")
        return wynik
    return opakowanie
#klasa pobierająca aktualne dane ze strony
class main:
    def __init__(self, currency, toCurrency):
        self.currency = currency
        self.toCurrency = toCurrency
    @dek_czasu
    def getRate(self):
        request = requests.get(f"https://api.exchangerate-api.com/v4/latest/{self.currency}")
        json = request.json()
        return json['rates'][self.toCurrency]
#funkcja wyświetlająca waluty
@dek_czasu
def wyswietl_waluty():
    request_temp = requests.get(f"https://api.exchangerate-api.com/v4/latest/PLN")
    json_temp = request_temp.json()
    lista = []
    for i in json_temp['rates'].keys():
        lista.append(i)
    return(lista)

#Nieskończona pętla będąca menu
while True:
    print(f'''
{">"*14} MENU {"<"*14}          
1. Przelicz walutę na inną
2. Pokaż dostepne waluty
3. Wyjdź 
4. Test
''')
    wybor = input("Wybierz opcję: ")
#Przeliczanie walut
    if wybor == '1':
        waluta = input("Podaj walutę (ISO): ").upper()
        try:
            ilosc = float(input("Podaj ilość: "))
        except (ValueError, TypeError):
            print("Zła ilość")
#Wyświetlanie walut
        waluta2 = input("Podaj docelową walutę (ISO): ").upper()
        if waluta in wyswietl_waluty() and waluta2 in wyswietl_waluty():
            przelicznik = main(waluta, waluta2).getRate()
            print(f"\n{'>'*5} Twój przelicznik walut {'<'*5} \n{ilosc} {waluta} = {ilosc * przelicznik} {waluta2}\n")
        else:
            raise Exception("Niepoprawne dane")
    elif wybor == "2":
        print (f"{">"*8} Dostepne waluty {"<"*9}\n {wyswietl_waluty()}")
    elif wybor == "3":
        break
#Testowanie kodu
    elif wybor == "4":
        print(f'''
{">"*6} MENU TESTOWANIA {"<"*6}          
1. małe litery
2. nieprawidłowa waluta
3. zła ilość
''')
        wybor_testu = input("Wybierz opcję: ")
        if wybor_testu == "1":
            print("\nwaluta z małych liter")
            waluta = "pln".upper()
            waluta2 = "EUR".upper()
            ilosc = 3
            przelicznik = main(waluta, waluta2).getRate()
            print(f"\n{'>'*5} Twój przelicznik walut {'<'*5} \n{ilosc} {waluta} = {ilosc * przelicznik} {waluta2}\n")
        elif wybor_testu == "2":
            print("\nnieprawidłowa waluta")
            waluta = "pln".upper()
            waluta2 = "euro".upper()
            ilosc = 3
            if waluta in wyswietl_waluty() and waluta2 in wyswietl_waluty():
                przelicznik = main(waluta, waluta2).getRate()
                print(f"\n{'>'*5} test przeliczenia {'<'*5} \n{ilosc} {waluta} = {ilosc * przelicznik} {waluta2}\n")
            else:
                raise Exception("Niepoprawne dane")
        elif wybor_testu == "3":
            print("\nnieprawidłowa ilosc")
            try:
                waluta = "PLN".upper()
                waluta2 = "EUR".upper()
                ilosc = "abc"
                przelicznik = main(waluta, waluta2).getRate()
            except (ValueError, TypeError):
                print("Zła ilość")
        else:
            print("zły wybór")
    else:
        print("zły wybór")
