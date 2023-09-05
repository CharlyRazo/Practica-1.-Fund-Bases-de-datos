import re
import pandas as pd

"""
Funciones y variables auxiliares
"""

"""
Esta función toma un mensaje que se le dara al usuario para solicitar un indice y buscara si esta en  
el dataframe sales.
Args:
    message (Str): Mensaje para el usuario.
    drugs (DataFrame): Dataframe de ventas.
Returns:
    response (int): Indice valido.
"""
def get_id(message1,sales):
    while True:
        try:
            response = int(input(message1))
            if response in sales.index.values:
                return response
            else:
                print("Error: El ID no se encuentra en el inventario.")
                print("Favor de intentar nuevamente")
        except ValueError:
            print("Error: Debes ingresar un número válido.")
            print("Favor de intentar nuevamente.")


"""
Esta función le pregunta al usuario por la fecha y lo obliga a colocarlo en formato dd/mm/aaaa
Recibe la lista de fechas que hay registradas en la tabla de ventas y verifica que no se encuentre
ya registrada para no repetir informacion y regresa un diccionario para poder agregarlo como nuevo
registro en el dataframe
Args:
    dates_list (List): Fechas registradas en el dataframe ventas.
Returns:
    dictionary (dict): Diccionario que sera nuevo registro.
"""
def get_date(dates_list):
    while True:
        pattern = r"^\d{2}/\d{2}/\d{4}$"
        date = input("Indique la fecha de venta en formato dd/mm/aaaa.:\n")
        if re.match(pattern, date) is not None: 
            if date not in dates_list:
                dictionary = {"Dia": date[0:2], "Mes" : date[3:5], "Año" : date[6:10]}
                return dictionary
                break
            
            else:
                print("Error: La fecha que usted indica ya se encuentra en la lista")
                print("Favor de intentarlo nuevamente\n")
        else:
            print("Error: Formato no válido.")
            print("Favor de intentar nuevamente.")


"""
Esta función le pregunta al usuario el total vendido en el dia.

Returns:
     (str): Total vendido en formato moneda
"""
def get_total_sold():
    while True:
        try:
            response = int(input("Favor de escribir el total vendido. Ingresar solo el numero:\n"))
            return "$" + str(response)
        except ValueError:
            print("Error: Debes ingresar un número válido.")
            print("Favor de intentar nuevamente.")


"""
Esta función genera la lista de fechas registradas en formato dd/mm/aaaa.
Args:
    sales (DataFrame): df de ventas
Returns:
    dates_list (str): Lista de fechas
"""
def get_dates_list(sales):
    df_dates = sales[['Año', 'Mes', 'Dia']]
    df_dates.columns = ["year", "month", "day"]
    dates_list = pd.to_datetime(df_dates).dt.strftime('%d/%m/%Y').tolist()
    return dates_list


"""
Funcion que muestra la tabla de ventas y permite agregar, eliminar o actualizar un registro
Args:
    sales (DataFrame): df a actualizar
Return:
    sales (DataFrame): df actualizado
"""
def hoja_ventas(sales):
    print("\n")
    print(sales)
    print("\n\n")
    print("Indique la opcion a realizar")
    
    # bucle para solicitar una opcion valida
    while True:
        dates_list = get_dates_list(sales)
        user_input = input("1. Agregar registro \n2. Eliminar registro  \n3. Actualizar registro \n4. Volver al menu anterior\n")

        # Agregar registro
        if user_input == "1":
            id = sales.index.values[-1] + 1  # se le suma +1 al ultimo indice
            new_record = get_date(dates_list)
            new_record["Total vendido"] = get_total_sold()
            new_record["ID"] = id
            sales.loc[id] = new_record
            print(sales)
            print("\nSe agrego tu registro de forma exitosa.")
            print("¿Desea seleccionar otra opcion?")

        # Eliminar registro
        elif user_input == "2":
            id = get_id("Ingresa el ID del registro a eliminar:\n", sales)
            sales = sales.drop(index=id)
            print(sales)
            print("\nSe elimino tu registro de forma exitosa.")
            print("¿Desea seleccionar otra opcion?")
        
        # Actualizar registro
        elif user_input == "3":
            id = get_id("Ingresa el ID del registro a actualizar:\n", sales)
            date_to_eliminate = sales["Dia"][id] + "/" + sales["Mes"][id] + "/" +sales["Año"][id]
            dates_list = dates_list[dates_list != date_to_eliminate]
            sales = sales.drop(index=id)
            new_record = get_date(dates_list)
            new_record["Total vendido"] = get_total_sold()
            new_record["ID"] = id
            sales.loc[id] = new_record
            print(sales)
            print("\nSe actualizo tu registro de forma exitosa.")
            print("¿Desea seleccionar otra opcion?")
            
        elif user_input == "4":
            print("Volviendo al menu anterior.")
            break
        else:
            print("Opcion no valida, favor de intentarlo nuevamente.")

    return sales