import pandas as pd
import numpy as np
import re


"""
Esta función le pregunta al usuario la fecha en que se realiza la compra y verifica que la escriba
en el formato valido

Returns:
    date (str): Fecha en formado dd/mm/aaaa.
"""
def date_valid():
    while True:
        pattern = r"^\d{2}/\d{2}/\d{4}$"
        date = input("Indique la fecha de venta en formato dd/mm/aaaa.:\n")
        if re.match(pattern, date) is not None: 
            return date
            break
        else:
            print("Error: Formato no válido.")
            print("Favor de intentar nuevamente.")


"""
Esta función le pregunta al usuario el ID del medicamento que pondrá en venta y verifica que
realmente se encuentre en el dataframe drugs
Args:
    drugs (DataFrame): df de medicamentos
Returns:
    id (int): Id valido dado por el usuario.
"""
def drug_id_valid(drugs):
    while True:
        try:
            id = int(input("Indique el ID de un medicamento valido:"))
            if id in drugs.index.values:
                return id
                break
            else:
                print("Error: El ID no se encuentra en el inventario.")
                print("Favor de intentar nuevamente")
        except ValueError:
            print("Error: Debes ingresar un número válido.")
            print("Favor de intentar nuevamente.")


"""
Esta función le pregunta al usuario la cantidad de medicamento a vender, verifica en la tabla
drugs que en efecto haya suficiente medicamento, de lo contrario arroja error
Args:
    id_drug (int): Id del medicamento a vender
    drugs (DataFrame): df de medicamentos
Returns:
    quantity (int): Cantidad valida dada por el usuario
"""
def quantity_valid(id_drug, drugs):
    while True:
        try:
            quantity = int(input("Indique la cantidad: "))
            if quantity <= drugs.loc[id_drug]["Cantidad en Existencia"]:
                return quantity
                break
            else:
                print("Error: El numero es mayor a la cantidad disponible.")
                print("Favor de intentar nuevamente")
        except ValueError:
            print("Error: Debes ingresar un número válido.")
            print("Favor de intentar nuevamente.")


"""
Esta función le permite buscar el ID correspondiente de la tabla de ventas dependiendo
de la fecha escrita. En caso de que la fecha no este registrada en la tabla entoces se le
agrega un ID nuevo
Args:
    date (str): Id del medicamento a vender
    dates_list (List): Lista de fechas registradas en el df sales
    sales (Dataframe): df de ventas
Returns:
    id_date (int): Id correspondiente a la fecha
"""
def get_id_date(date, dates_list, sales):
    if date in dates_list:
        position_in_dates_list = dates_list.index(date)
        id_date = position_in_dates_list + 1 # dates_list inicia en 0, entonces le sumamos 1
        return id_date
    else:
        id_date = sales.index.values[-1] + 1  # se le suma +1 al ultimo indice
        return id_date
    

"""
Esta función le permite obtener la lista de fechas registradas en del df sales en formato dd/mm/aaaa
Args:
    sales (DataFrame): df de ventas
Returns:
    dates_list (List): Lista de fechas registradas
"""
def get_dates_list(sales):
    df_dates = sales[['Año', 'Mes', 'Dia']]
    df_dates.columns = ["year", "month", "day"]
    dates_list = pd.to_datetime(df_dates).dt.strftime('%d/%m/%Y').tolist()
    return dates_list  
    

"""
Funcion que muestra la tabla de medicamentos y permite generar una interfaz de venta.
Le pedira al usaurio escoger el ID de medicamento a vender, la cantidad y dependiendo de la disponibilidad 
del producto, le permitirá realizar la compra y actualizar los df de drugs y sales.

Args:
    drugs (DataFrame): df de medicamentos
    sales (DataFrame): df de ventas
Return:
    drugs (DataFrame): df de medicamentos actualizado
    sales (DataFrame): df de ventas actualizado
"""
def interfaz_ventas(drugs, sales):
    print("\n")
    print(drugs)
    print("\n\n")
    print("Indique la opcion a realizar")

    while True:
        user_input = input("1. Realizar venta\n2. Volver al menu anterior\n")
    
        if user_input == "1":
            dates_list = get_dates_list(sales)
            date = date_valid()
            id_drug = drug_id_valid(drugs)
            quantity = quantity_valid(id_drug, drugs)
            total = quantity * float(drugs.loc[id_drug]["Precio"][1:])   #eliminamos el signo de '$' y lo multiplicamos por la cantidad

            # obteniendo el id de la fecha
            id_date = get_id_date(date, dates_list, sales)
            
            # actualizando la tabla de medicamentos
            drugs.loc[id_drug, "Cantidad en Existencia"] = drugs.loc[id_drug, "Cantidad en Existencia"] - quantity

            # actualizando la tabla de ventas
            if id_date <= len(sales):
                total_sold_before_update =  float(sales.loc[id_date]["Total vendido"][1:])  # es un string de la forma "$ddd.dd", le quitamos el primer caracter y nos quedamos con el numero
                total_sold = total_sold_before_update + total
            else:
                total_sold = total
            new_record = {"Dia": date[0:2], "Mes" : date[3:5], "Año" : date[6:10], "Total vendido": "$" + str(total_sold)}
            sales.loc[id_date] = new_record
            
            print(drugs)
            print("**********************************************\n")
            print("               RESUMEN DE COMPRA              \n\n")
            print("Medicamento: " + drugs.loc[id_drug]["Nombre"])
            print("Cantidad: " + str(quantity))
            print("Importe a total: $" + str(total)+"\n")
            print("**********************************************")
            print("\nSe realizo tu venta de forma exitosa.")
            print("Los registros ya fueron actualizados.\n")
            print("¿Desea seleccionar otra opcion?")
            
        elif user_input == "2":
            print("Volviendo al menu anterior.")
            break
        else:
            print("Opcion no valida, favor de intentarlo nuevamente.")

    return drugs, sales
            
        
        