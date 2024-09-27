## Documentación Modelo de ML 

**Modelo de predicción de emisiones de co2 en vehículos**

+ **Objetivo del Modelo**: Predecir las emisiones de CO2 de vehículos de diferentes tipos (eléctricos, híbridos, y de combustible) con base en sus características técnicas.

Usaremos la informacion de los datasets: 

 1)Electric cars
 
 2)Fuel vehicles 
 
 3)Hybrid vehicle 

Tienen información técnica y de rendimiento de distintos modelos de carros ,en el mercado, así como las emisiones que cada uno de ellos producen.

Luego de analizar los datasets, optamos por un Modelo de **regresión lineal multiple** ya que observamos que nuestra variable a predecir, *Emisiones de co2*, estaba directamente relacionada con distintas variables del dataset (el tipo de combustible que usamos, su eficiencia, etc) De igual forma al estar tratando de predecir una variable continua *Emisiones de co2* la regresión lineal se ajusta perfecto.

Para realizar este modelo seguimos los siguientes pasos:

+ **ETL**: Una vez decididos los datos nos aseguramos que siguieran limpios y si eran necesaria una normalización o escalado, en nuestro caso el tamaño de los registros eran similares en cada data set por lo que no había un sesgo significativo hacia ningún tipo de carro. 

+ **EDA**: Analizamos la distribución de las emisiones y otros variables para poder seleccionar las que usaríamos para la predicción, ver la correlación entre las columnas fue fundamental para decidir nuestras variables independientes.

Con esta información volvimos a realizar una nueva transformación concatenando los data sets en uno solo y con solo las columnas de las variables que íbamos a usar 'identifier', 'manufacturer', 'make', 'fuel_type','emissions_co2_g_per_km', 'energy_consumption_wh_per_km','engine_power_kw', 'electric_range_km', 'registration year','fuel consumption'

+ **Realizamos el modelo** creando dfs sobre las variables dependientes y la independiente

Usamos una división de 80/20 con los datos para entrenar y testear el modelo

Después de correrlo, obtenemos buenas métricas un MSE de 570 aprox. que al sacarle raíz nos deja una variación en la predicción de +- 23.8 en un rango que va de los 0 a 350. Una R² de 85% aprox. que nos dice que la variabilidad en las emisiones de CO2 puede ser explicada por las características del vehículo que usamos como variables independientes 

+ **Se graficó la distribución de las predicciones vs valores reales** con el conjunto de test y observamos que los puntos se concentran principlamnete en la diagonal m=1 con ordenada al origen = 0. Lo que indica que las predicciones están o son muy cercanas a los valores reales lo que nos confirma que no hay una sobres o sub estimación significativa 

+ **Se realiza un diccionario** para probar futuras predicciones con nuevos valores y también vemos una predicción del conjunto de testeo y lo comparamos vs los datos reales y vemos que varia en 2 unidades de emisión de co2,

Después de todo lo observado concluimos que el modelo es bastante aceptable y las predicciones que realiza de emisiones de co2 son bastante certeras y muy cercanas a la realidad por lo que se podrían usar estos datos como una fuente confiable a la hora de decidir si un vehículo se ajusta a los parámetros de contaminación que la empresa quiere usar para su flota de taxis a la hora de adquirir nuevos vehículos para esta. 

Al final se crearon funciones para mejor interacción con el usuario
