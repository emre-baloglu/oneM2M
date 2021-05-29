import requests
from time import sleep
import re

class Onem2m:
    def __init__(self):
        self.api_url = 'http://127.0.0.1:7579/Mobius/'
        self.api_filter = 'http://127.0.0.1:7579/Mobius?fu=1&ty=2'
        self.api_headers = {
            'Accept': 'applications/json',
            'X-M2M-RI': '123456',
            'X-M2M-Origin': 'TestRequest'
        }
        self.entity_list = []
        self.CFAIL = '\033[91m'
        self.CWARNING = '\033[93m'
        self.COKGREEN = '\033[92m'
        self.CENDC = '\033[0m'

    def get_all_entity(self):
        response = requests.get(self.api_filter, headers=self.api_headers)
        json_data = response.json()

        if len(json_data["m2m:uril"]) == 0:
            print(f'{self.CFAIL}Any entity not found ! Please build entity/entities\n{self.CENDC}')
            print(f'{self.CFAIL}The program has been closed !!\n{self.CENDC}')
            exit()
        else:
            print('Existing entity/entities')
            for r in json_data["m2m:uril"]:
                list = re.split("/", r)
                if not (list[1] in self.entity_list):
                    self.entity_list.append(list[1])
                entity_index = self.entity_list.index(list[1]) + 1
                print(f'{self.COKGREEN}{str(entity_index)} - {list[1]}{self.CENDC}', end="    ")
            print("\n")

    def get_entity_data(self, entity_name):
        try:
            response = requests.get(self.api_url+entity_name+'/data/la', headers=self.api_headers)
            return response.json()
        except Exception as e:
            print(e)
            print(f'{self.CFAIL}\nLast data not found{self.CENDC}')

    def get_last_value(self, entity_name, count):
        data = self.get_entity_data(entity_name)
        if count != data["m2m:cin"]["st"]:
            count = data["m2m:cin"]["st"]
            print(f'{self.COKGREEN}{count}. {entity_name} Value: {data["m2m:cin"]["con"]}\n{self.CENDC}')
        else:
            sleep(3)

    def follow_value(self, entity_name, count):
        try:
            print(f'{self.CWARNING}Press "Ctrl+C" for back to the menu{self.CENDC}')
            while True:
                data = self.get_entity_data(entity_name)
                if count != data["m2m:cin"]["st"]:
                    count = data["m2m:cin"]["st"]
                    print(f'{self.COKGREEN}{count}. {entity_name} Value: {data["m2m:cin"]["con"]}{self.CENDC}')
                    sleep(3)
        except KeyboardInterrupt:
            print(f'{self.CWARNING}\nReturning to the menu !\n{self.CENDC}')

    def change_entity_name(self):
        chosen_entity = input('Enter the new entity name: ')
        while not (chosen_entity in self.entity_list):
            print(f'{self.CFAIL}The entered entity does not exist !!{self.CENDC}')
            chosen_entity = input('Please enter an existing entity: ')

        print(f'{self.CWARNING}\nEntity exchange succesful. New entity : {chosen_entity}\n{self.CENDC}')
        return chosen_entity
