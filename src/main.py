"""

SISTEMA DE INVENTARIADO

"""

import pandas as pd
import funcionesMedicamentos
import funcionesVentas
import funcionesInterfazVentas as funcionesInterfazVentas

# inicio del programa
print('*******************************************')
print('*                                         *')
print('* Bienvenidos al sistema de inventariado. *')
print('*                                         *')
print('*******************************************\n')

# leyendo los archivos archivo
drugs = pd.read_excel("../data/inventario.xlsx", sheet_name="Medicamentos", skiprows=3, index_col=0)
dtype = {"Dia": str, "Mes": str, "Año": str, "Total vendido": str}
sales = pd.read_excel("../data/inventario.xlsx", sheet_name="Ventas", skiprows=3, index_col = 0, dtype=dtype)
 
# bucle para solicitar una opcion valida
while True:
    print("Favor de escribir el numero de la acción que desea realizar\n")
    user_input = input("1. Visualizar la hoja de medicamentos \n2. Visualizar la hoja de ventas  \n3. Realizar venta \n4. Finalizar el programa\n")

    if user_input == "1":
        print('*******************************************')
        print('*                                         *')
        print('*  Visualizando la hoja de medicamentos.  *')
        print('*                                         *')
        print('*******************************************\n')
        drugs = funcionesMedicamentos.hoja_medicamentos(drugs)
    
    elif user_input == "2":
        print('*************************************')
        print('*                                   *')
        print('*  Visualizando la hoja de ventas.  *')
        print('*                                   *')
        print('*************************************\n')
        sales = funcionesVentas.hoja_ventas(sales)
        
    
    elif user_input == "3":
        print('********************************')
        print('*                              *')
        print('*      Interfaz de ventas      *')
        print('*                              *')
        print('********************************\n')
        drugs, sales = funcionesInterfazVentas.interfaz_ventas(drugs, sales)

    elif user_input == "4":
        print("Finalizando el programa") 
        break
    
    else:
        print("Opcion no valida. Favor de escribir uno de los numeros indicados\n") 

# almacenando la informacion en el excel
writer = pd.ExcelWriter("../data/inventario.xlsx", engine="openpyxl", mode = "a", if_sheet_exists="overlay")
drugs.to_excel(writer, sheet_name="Medicamentos", index=True, startrow=3)
sales.to_excel(writer, sheet_name="Ventas", index=True, startrow=3)
writer.close()




