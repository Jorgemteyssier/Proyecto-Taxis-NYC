#se puede remplazar desde el anio 2014 hasta el 2024
def year():
    return 2023

year = year()  

#Ruta para almacenar los datos particionados temporalmente
def ruta():
    return f'data_particionada_temporal/{year}_particion'

#lista trimestral a remplazar ene_march, april_june, 
#july_september, october_december
def trimestre():
    return 'october_december'

#Para modificar el mes de extraccion de la data a trabajar

#"January", "February", "March", "April", "May", 
#"June", "July", "August", "September", "October", 
# "November", "December"


def control_mes_uno():
    return 'October'
def control_mes_dos():
    return 'November'
def control_mes_tres():
    return 'December'


