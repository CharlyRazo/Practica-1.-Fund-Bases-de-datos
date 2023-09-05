import pandas as pd

"""
Funciones y variables auxiliares
"""

"""
Esta función toma un mensaje que se le dara al usuario para solicitar un indice y buscara si esta en  
el dataframe drugs.
Args:
    message (Str): Mensaje para el usuario.
    drugs (DataFrame): Dataframe de medicamentos.
Returns:
    response (int): Indice valido.
"""
def get_id(message,drugs):
    while True:
        try:
            response = int(input(message))
            if response in drugs.index.values:
                return response
            else:
                print("Error: El ID no se encuentra en el inventario.")
                print("Favor de intentar nuevamente")
        except ValueError:
            print("Error: Debes ingresar un número válido.")
            print("Favor de intentar nuevamente.")

"""
Esta función le permite al usuario escoger la Categoria del medicamento.

Returns:
    response (int): Categoria de medicamento.
"""
dict_categories = {1:"Antibioticos", 2:"Desinflamantes", 3:"Analgesicos", 4:"Alimentos", 5:"Bebidas", 6:"Otros"}
def get_category():
    while True:
        try:
            print("Favor de escoger la categoria. Ingresar solo el numero:")
            response = int(input("1. Antibioticos\n2. Desinflamantes\n3. Analgesicos\n4. Alimentos\n5. Bebidas\n6. Otros\n"))
            return dict_categories[response]
        except ValueError:
            print("Error: Debes ingresar un número válido.")
            print("Favor de intentar nuevamente.")

"""
Esta función le pregunta al usuario sobre el Precio del medicamento y lo regresa en formato moneda.

Returns:
    response (str): Precio en formato moneda
"""            
def get_price():
    while True:
        try:
            response = float(input("Favor de escribir el precio del medicamento. Ingresar solo el numero:\n"))
            response = "$" + str(response)
            return response
        except ValueError:
            print("Error: Debes ingresar un número válido.")
            print("Favor de intentar nuevamente.")

"""
Esta función le pregunta la Cantidad de medicamento.

Returns:
    response (int): Cantidad
"""      
def get_quantity():
    while True:
        try:
            response = int(input("Favor de escribir la cantidad en existencia. Ingresar solo el numero:\n"))
            return response
        except ValueError:
            print("Error: Debes ingresar un número válido.")
            print("Favor de intentar nuevamente.")


"""
Funcion que muestra la tabla de medicamentos y permite agregar, eliminar o actualizar un registro.

Args:
    drugs (DataFrame): Recibe el dataframe de medicamentos donde hara estas consultas y actualizaciones
Return:
    drugs (Dataframe): Regresa el dataframe actualizado
"""

def hoja_medicamentos(drugs):
    print("\n")
    print(drugs)
    print("\n\n")
    print("Indique la opcion a realizar")

    # bucle para solicitar una opcion valida
    while True:
        user_input = input("1. Agregar registro \n2. Eliminar registro  \n3. Actualizar registro \n4. Volver al menu anterior\n")

        # Agregar registro
        if user_input == "1":
            drug_name = input("Ingresa el nombre del medicamento:\n")

            # Caso en el que el medicamento no ha sido registrado, te permite registrarlo
            if drug_name not in drugs["Nombre"].values:
                category = get_category()
                price = get_price()
                quantity = get_quantity()
                id = drugs.index.values[-1] + 1  # se le suma +1 al ultimo indice y se asigna como ID al nuevo medicamento
                new_record = {"Nombre": drug_name, "Categoria": category, "Precio": price, "Cantidad en Existencia": quantity}
                drugs.loc[id] = new_record
                drugs = drugs.sort_index()
                print(drugs)
                print("\nSe agrego tu registro de forma exitosa.")
                print("¿Desea seleccionar otra opcion?")
                
            # Caso en el que el medicamento ya esta registrado
            else:
                print("El medicamento ya se encuentra en el inventario.")
                print('En caso de querer modificarlo, favor de elegir "Actualizar registro".\n')
                
        # Eliminar registro
        elif user_input == "2":
            id = get_id("Ingresa el ID del registro a eliminar:\n", drugs)
            drugs = drugs.drop(index=id)
            print(drugs)
            print("\nSe elimino tu registro de forma exitosa.")
            print("¿Desea seleccionar otra opcion?")
        
        # Actualizar registro
        elif user_input == "3":
            id = get_id("Ingresa el ID del registro a actualizar:\n", drugs)
            drugs = drugs.drop(index=id) # Borramos para luego agregarlo con el mismo ID
            drug_name = input("Ingresa el nombre del medicamento\n")
            category = get_category()
            price = get_price()
            quantity = get_quantity()
            new_record = {"Nombre": drug_name, "Categoria": category, "Precio": price, "Cantidad en Existencia": quantity}
            drugs.loc[id] = new_record
            drugs = drugs.sort_index()
            print(drugs)
            print("\nSe actualizo tu registro de forma exitosa.")
            print("¿Desea seleccionar otra opcion?")
        
        elif user_input == "4":
            print("Volviendo al menu anterior.")
            break

        else:
            print("Opcion no valida, favor de intentarlo nuevamente.")

    return drugs