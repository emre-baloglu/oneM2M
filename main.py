from oneM2M_parser import Onem2m
from time import sleep

if __name__ == '__main__':
    m2m = Onem2m()
    m2m.get_all_entity()
    entity_name = input('Enter entity name: ')

    try:
        result = m2m.get_entity_data(entity_name)
        count = result["m2m:cin"]["st"]
        # print(f'{count}. {entity_name} Temperature: {result["m2m:cin"]["con"]}\n')

        while True:
            choice = input('1- Get all entities\n2- Get entity last value\n3- Follow last values\n4- Change Entity'
                           '\n5- Exit\nChoice: ')
            if choice == '5':
                break

            elif choice == '1':
                m2m.get_all_entity()

            elif choice == '2':
                m2m.get_last_value(entity_name, count)

            elif choice == '3':
                m2m.follow_value(entity_name, count)

            elif choice == '4':
                entity_name = m2m.change_entity_name()

            else:
                print(f'{m2m.CFAIL}Wrong choice value !!!\n{m2m.CENDC}')

    except KeyError as ke:
        print(f'{m2m.CWARNING}The container represented is full for entity {entity_name} !!\n{m2m.CENDC}')
        print(f'{m2m.CFAIL}Rebuild {entity_name} entity !!\n{m2m.CENDC}')
        # print(ke)
    finally:
        print(f'{m2m.CWARNING}The program has been closed !!\n{m2m.CENDC}')