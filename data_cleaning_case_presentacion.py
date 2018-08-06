﻿## This scrpit was developed based on a project developed by the author
## for Udacity's Introduction to Machine Learning.
## It 
## Input: A pkl file containing with raw data about an enron employee 
## Output: A pandas  data frame containing the clean data repository

## LIBRARY NEEDED TO MANIPULATE PICKLE FILE
import pickle
## LIBRARY FOR PLOTTING DATA
import matplotlib.pyplot as plt
## LIBRARY NEEDED 
import numpy
## LIBRARY THAT CONTAINS THE PANDAS DATAFRAME
import pandas as pd


## STEP 1 - READ THE BINARY DATA FROM A PKL FILE AND STORE IT IN A DICTIONARY
## open the file of serialized data, unpack it and save it in a dictinary


with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
import csv
 
w = csv.writer(open("output.csv", "w"))
for key, val in data_dict.items():
    w.writerow([key, val])

## STEP 2 - VISUALIZE THE STRUCTURE OF THE DATA
## A) WE VISUALIZE A SUMMARY OF THE FIRST THREE ROWS OF DATA 
## we can see that it consists of a key (the name of an employee) and
## a dictionary of features that describe that employee
print('-------------------------VISUALIZING THE STRUCTURE OF THE ORIGINAL DATA-------------------')

iterator = iter(data_dict.items())
for i in range(3):
    print(next(iterator))

print('--------------------------------------------------------------------------')
## B) LETS SEE HOW LARGE IS THE DATA SET 
print ("Number of records: "), (len(data_dict))

## C) GET A COUNT OF HOW MANY FEATURES WE HAVE
print ("How many features: "), (len(data_dict['METTS MARK']))
## D) PRINT THE LIST OF FEATURES PER RECORD
lista_de_features = data_dict['METTS MARK']
for f in lista_de_features:
    
    print ("feature: "), (f)
## E) IF YOU THINK ABOUT IT, THE FEATURE email_address IS NOT VERY USEFUL
## F) LETS BUILD TWO LISTS WITH THE NAME OF THE FEATURES IN THE DATA
## THAT ARE USEFUL

datos_finanzas = ['salary',
                'bonus',
                'long_term_incentive',
                'deferred_income',
                'deferral_payments',
                'loan_advances',
                'other',
                'expenses',                
                'director_fees', 
                'total_payments',
              'exercised_stock_options',
              'restricted_stock',
              'restricted_stock_deferred',
              'total_stock_value']
datos_email = ['to_messages',
              'from_messages',
              'from_poi_to_this_person',
              'from_this_person_to_poi',
              'shared_receipt_with_poi']


## STEP 3 - GET RID OF OBVIOUS OUTLIERS

print('------------------------------OBVIOUS OUTLIER----------------------------------------')
## FOR THIS EXAMPLE I WILL CONSIDE AN OUTLIER ANY EMPLOYEE WITH A SALARY > 10 MILLION
for key, value in data_dict.items():
        if data_dict[key]['salary'] != 'NaN' and data_dict[key]['salary'] >10000000:
            print (key, value)
            break
        ## test

## ELIMINAMOS EL OUTLIER
data_dict.pop("TOTAL", 0)

## PASO 4 - ORDENAMOS LA DATA
## CREAMOS UN DATAFRAME
df = pd.DataFrame.from_dict(data_dict, orient='index')
## LLENAMOS LOS 'NAN' CON EL TIPO DE DATO numpy.nan
df = df.replace('NaN', numpy.nan)

## ORDENAMOS LAS FEATURES PARA COMPARAR CON DCTO ORIGINAL Y FACILITAR RASTREO DE ERRORES
## LA PRIMERA FEATURE O CARACTERISTICA ES LA ETIQUETA QUE INDICA SI EL EMPLEADO
## ES SOSPECHOSO O NO. ESTA ETIQUETA ES LA UNICA QUE ES FIJA Y VERIFICADA PARA CADA
## REGISTRO (EMPLEADO) ASI QUE NO NECESITAMOS 'LIMPIARLA' O CORREGIRLA
features = ['poi'] + datos_finanzas + datos_email
# USAMOS NUETRA LISTA DE FEATURES PARA PONERLE NOMBRE A LAS COLUMNAS DEL DATAFRAME 
df = df[features]

## LLENAMOS CON CEROS LA DATA QUE TIENE COMO VALOR  EL TIPO numpy.nan
df[datos_finanzas] = df[datos_finanzas].fillna(value = 0)
df[datos_email] = df[datos_email].fillna(value = 0)
## COMPROBAMOS QUE LOS 0'S HAN SIDO INSERTADOS EN VEZ DE 'NAN'
print(df.head(12))

## PASO 5 - ANALISIS ESTADISTICO DE LOS DATOS QUE TENEMOS
print(df.describe())


## PASO 6 - CORRECCIONES
counter = 0
for person_name, row in df.iterrows():
    ## SUMAMOS LA DATA DE PAGOS Y VEMOS SI CUADRA CON total_payments
    total_payment_data = row[datos_finanzas[:9]].sum()
    
    if total_payment_data != row['total_payments']:
        print("Totales para esta persona no cuadran: "), (person_name)
        counter += 1
print("Nro de totales que no cuadran"), (counter)
## LOS TOTALES DE 2 PERSONAS NO CUADRAN BHATNAGAR SANJAY and BELFER ROBERT
## SI OBSERVAMOS LA DATA VEMOS QUE LOS DATOS DE BELFER SE HAN CORRIDO UNO A
## LA IZAQUIRDA, Y DEL OTRO A LA DERECHA
## A. CORREGIMOS LA DATA DE ROBERT BELFER
## QUEREMOS LAS COLUMNAS DE DATOS FINANCIEROS (LA COLUMNA 0 NO ES DATO FINANCIERO)
belfer_errores = df.ix['BELFER ROBERT', 1:15].tolist()
##  CORRER LA DATA A LA IZQUIERDA
belfer_errores.pop(0) ## BORAMOS LA COLUMNA 1
belfer_errores.append(0) ## ANEXAMOS UNA COLUMNA AL FINAL PARA TOTAL_STOCK_VALUE (=0)
## REINSERTAMOS LA DATA CORREGIDA
df.ix['BELFER ROBERT', 1:15] = belfer_errores
## B.  CORREGIMOS LA DATA DE BHANTNAGER SANJAY CORRIENDOLA A LA DERECHA
## BORRAMOS LA COLUMNA 15, Y ANADIMOS UNA NUEVA COLUMNA QUE SERA LA COLUMNA UNO (=0)
sanjay_errores = df.ix['BHATNAGAR SANJAY', 1:15].tolist()
sanjay_errores.pop(-1) ## BORRAMOS LA ULTIMA COLUMNA (15)
sanjay_errores = [0] + sanjay_errores
df.ix['BHATNAGAR SANJAY', 1:15] = sanjay_errores
## VERIFICAMOS SI LOS DATOS CORREGIDOS CUADRAN
counter = 0
for person_name, row in df.iterrows():
    
    ## CONFIRMAMOS QUE LOS ERRORES EN SUMATORIA DE TOTAL_PAYMENTS HAN SIDO CORREGIDOS
    total_payment_data = row[datos_finanzas[:9]].sum()
    
    if total_payment_data != row['total_payments']:
        print ("Totales para esta persona no cuadran: "), (person_name)
        counter += 1
print("Nro de totales que no cuadran"), (counter)

## HACEMOS EL MISMO CHEQUEO DE SUMATORIA PARA DATOS DE STOCK
counter = 0
for person_name, row in df.iterrows():
    
    ## SUMAMOS LA DATA DE PAGOS Y VEMOS SI CUADRA CON total_stock_value
    total_stock_data = row[datos_finanzas[10:-1]].sum()
    
    if total_stock_data != row['total_stock_value']:
        print("Totales para esta persona no cuadran: "), (person_name)
        counter += 1
print("Nro de totales de que no cuadran"), (counter)
## EL OUPUT NOS DICE QUE NO HAY ERRORES DE SUMTORIA DE total_stock_value


## PASO 7 - ELIMINAR OTROS OUTLIERS NO TAN OBVIOS
## VISUALIZAMOS UN SCATTERPLOT QUE MUESTRA OUTLIERS
## LOS POIS (SOSPECHOSOS) LOS MARCAREMOS CON ASTERISCOS ROJOS
## LOS NO POIS LOS MARCAREMIS CON ASTERISCOS AZULES
for person_name, row in df.iterrows():
    ## SI LA PERSONA ES UN POI MARCAMOS CON * COLOR ROJO
    ## DE LO CONTRARIO MARCAMOS CON + COLOR AZUL
    if row['poi'] == 1:
        plt.scatter(row['total_stock_value'], row['total_payments'], color="r", marker="*")
    else:
        plt.scatter(row['total_stock_value'], row['total_payments'], color="b", marker="+")
           
plt.xlabel('total_stock_value')
plt.ylabel('total_payments')
plt.savefig("image.png")
plt.show()
## COMO VEMOS EN EL SCATTERPLOT HAY UNAS PERSONAS CON TOTAL_STOCK_VALUE
## DESPROPORCINADAMENTE ALTOS EN COMPARACION CON TOTAL_PAYMENTS
## VEMOS QUE LA MAYORIA DE ESTOS SON OUTLIERS
## CONFIRMAMOS ESTOS OUTLIERS VIENDO LAS ESTADISTICAS
print(df.describe())

## EFECTIVAMENTE HAY OUTLIERS EN TOTAL PAYMENTS VIENDO LOS QUANTILES 

## UTILIZAREMOS LA REGLA DE OUTLIERS USANDO EL IQR
## ULTIMO first_quartile+1.5 * IQR < OUTLIER < PRIMER third_quartile−1.5 * IQR
IQR = df.quantile(q = 0.75) - df.quantile(q = 0.25)
first_quartile = df.quantile(q = 0.25)
third_quartile = df.quantile(q = 0.75)
## ENCONTRAMOS LOS OUTLIERS EN CADA FEATURE DE CADA EMPLEADO
outliers = df[(df>(third_quartile + 1.5*IQR) ) | (df<(first_quartile - 1.5*IQR) )]##.count(axis=1)
outliers[datos_finanzas] = outliers[datos_finanzas].fillna(value = 0)
outliers[datos_email] = outliers[datos_email].fillna(value = 0)
outliers = outliers.sort_values(datos_finanzas + ['from_poi_to_this_person','from_this_person_to_poi'] , axis=0,ascending=False)
print ("Lista de outliers")
print (outliers.head(12))

## ELIMINAMOS LOS OUTLIERS
df.drop(axis=0, labels=['FREVERT MARK A', 'LAVORATO JOHN J',
                        'WHALLEY LAWRENCE G', 'ALLEN PHILLIP K','KITCHEN LOUISE','MCMAHON JEFFREY',
                        'FALLON JAMES B','MARTIN AMANDA K'], inplace=True)           
## COMPROBAMOS LA ELIMINACION DE LOS OUTLIERS DEL DATAFRAME QUE IRA AL ALGORITMO
print('--------------------------------------------------------------------------------------------------')
print('ENTIDADES EN LA DATA FINAL QUE SE UTILIZARA EN EL ALGORITMO')
print('--------------------------------------------------------------------------------------------------')
for person_name, row in df.iterrows():
    print(person_name)




        
