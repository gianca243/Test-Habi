# Test-Habi
Para poder invokar el servicio localmente primero se debe tener nodejs y pip3, con virtualenv:
```
pip3 install virtualenv
```
Adicionalmente se debe instalar pipenv
Linux

```bash
pip install pipenv
```

MacOS

```bash
brew install pipenv
```
Seguido a este paso se debe crear el entorno virtual:
```bash
virtualenv venv
```
y activar:
```bash
source ./venv/bin/activate
```
se instalan las dependencias de node:
```
npm i
```
y por ultimo las dependencias necesarias para python
```
pipenv install --dev
```
## Invoke-local

Se debe realizar un:

```
npm run invoke
```
## Unit-Test

Se debe realizar un:

```
npm run test
```

## Uso del endpoint
En postman se configura un request con el siguiente metodo y endpoint
POST - https://dsdhkjagu9.execute-api.us-east-2.amazonaws.com/dev/get_properties
Que tenga un body:
```
{
    "year": 2000,
    "city": "bogota",
    "status": "pre_venta" 
}
```
Se adjunta prueba al repositorio

## 1) Primer requerimiento
Para realizar el primer requerimiento se esta planteando que exige:
● Los usuarios pueden consultar los inmuebles con los estados: “pre_venta”, “en_venta” y “vendido” (los inmuebles con estados distintos nunca deben ser visibles por el usuario). 
● Los usuarios pueden filtrar estos inmuebles por: Año de construcción, Ciudad, Estado. 
● Los usuarios pueden aplicar varios filtros en la misma consulta. 
● Los usuarios pueden ver la siguiente información del inmueble: Dirección, Ciudad, Estado, Precio de venta y Descripción.
Para resolver este requerimiento, se utilizara serverless framework para facilitar el uso de aws
Creare una funcion lamdba con un projecto que maneje serverless y nodejs(solo para manejo de comandos)
el microservicio maneja un handler que es el archivo que permite la ejecución en un microservicio que sera interpretado en python. Todo con el proposito de consultar a un servidor SQL y poder retornar una respuesta con lo solicitado.
Entonces al momento de utilizar serverless se configura en AWS un IAM que me permitira crear un perfil
local en serverless para poder coordinar el despliegue. Seguido de esto se procedera con los siguientes pasos.

### conexión a la base de datos
Antes de todo es importante comprobar que se pueda realizar una conexción a la base de datos utilizo
MySQL workbench para poder probar la conexión y poder probar querys en un entorno esteril.

En amazon Hay un servicio que es el system mangement que tiene un store parameters que permite guardar 
variables de entorno que se pueden utilizar dentro del handler, siempre y cuando este manifestado en
el YML del serverless, con el proposito de guardar los datos de la base de datos ya que es información 
sensible. 

Se realiza un utils para agregar una función que se encargue de la conexión a la BD

### Planteamiento del handler
El handler se podria invocar a través de una funcion GET por el cual se podria pasar los filtros por medio de queryParameters pero un POST abre la posibilidad de en un futuro poder tener más parametros de busqueda sin el inconveniente de tener un endpoint con la url tan enorme. Se define en el serverles el tipo de función y la ruta que utilizara.

### Inicio del Handler
Para poder realizar los filtros de manera adecuada se hace una revisión del cuerpo que parametriza la query a través de un esquema que se maneja con un paquete llamado cerberus. Después de comprobar que el cuerpo cumple con la forma esperada y de no ser así retornar una respuesta insatisfactoria ya que de todas formas si los filtros no son aplicables la query tendra un resultado negativo.

En caso de que el cuerpo de la consulta sea el adecuado se utiliza la utilidad para conectarse a la BD y poder realizar una query.

### Consulta a SQL
**Primera duda:** Como se obtiene los ultimos datos de una tabla, solo buscando la ultimá modificación
**Solución:** Se debe primero de obtener solo los ultimos resultados de la tabla status_history agrupados por porpiedad, haciendo un JOIN con la misma tabla pero con la proyección condicionada por la fecha maxima, para luego poder hacer un JOIN con la tabla status, para al final hacer otro JOIN con la tabla property.
**hipotesis** En algun momento como las tablas de sql tienen un id autoincremental plante hacer un count de las propiedades a consultar y hacer un order by fecha en la tabla de status_history, para luego hacer un join a esa tabla. Pero si una propiedad fue actualizada varias veces seguidas no iba a traer los datos solicitados. Así que se descarto la idea

### Respuesta
Se creo una utilidad que permita dar formato a la respuesta de la query ya que sql retorna una lista de tuplas, lo que significa que no hay un cabecero o nombre de columna, a la que asociar cada posición de la tupla entonces se crea una utilidad para crear un diccionario que permita desde el front entender mejor cual es la información que se esta recibiendo. Por ultimo se envia el resultado de la consulta con su respectivo status code, y se realiza un try en toda la función para que cualquier error al momento de programar se cachee y se pueda revisar o en caso de existir un error en el servidor de SQL se pueda ver el detalle.

