# Test-Habi

## 1) Primer requerimiento
Para realizar el primer requerimiento se esta planteando que exige:
● Los usuarios pueden consultar los inmuebles con los estados: “pre_venta”, “en_venta” y “vendido” (los inmuebles con estados distintos nunca deben ser visibles por el usuario). 
● Los usuarios pueden filtrar estos inmuebles por: Año de construcción, Ciudad, Estado. 
● Los usuarios pueden aplicar varios filtros en la misma consulta. 
● Los usuarios pueden ver la siguiente información del inmueble: Dirección, Ciudad, Estado, Precio de venta y Descripción.
Para resolver este requerimiento, se utilizara serverless framework para facilitar el uso de aws
Creare una funcion lamdba con un projecto que maneje serverless y nodejs(solo para manejo de comandos)
el microservicio maneja un handler que es el archivo que permite la ejecución en un microservicio que sera interpretado en python. Todo con el proposito de consultar a un servidor SQL y poder retoenar una respuesta con lo solicitado.
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



