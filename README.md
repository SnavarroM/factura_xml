# factura_xml


Script de Python para descargar archivos adjuntos de correo electrónico de Gmail y ejecutar scripts de Python
Este es un script de Python que utiliza la biblioteca Imbox para descargar archivos adjuntos de correo electrónico de una cuenta de Gmail y ejecutar un script de Python separado en cada archivo adjunto. El script utiliza la biblioteca schedule para ejecutar el trabajo cada minuto.

El script primero establece las variables de host, nombre de usuario, contraseña y carpeta de descarga. Luego verifica si la carpeta de descarga existe y la crea si no existe. Luego inicia sesión en la cuenta de Gmail utilizando la biblioteca Imbox y recupera todos los mensajes no leídos. Para cada mensaje, lo marca como leído e itera a través de cada archivo adjunto. Si el archivo adjunto tiene una extensión de archivo .xml, crea un nuevo nombre de archivo con una marca de tiempo y guarda el archivo adjunto en la carpeta de descarga. Luego ejecuta un script de Python separado en el archivo descargado utilizando la biblioteca subprocess.

El script utiliza un bloque try-except para manejar cualquier error que pueda ocurrir durante la descarga de archivos o la ejecución de scripts. Finalmente, el script cierra la sesión en la cuenta de Gmail y utiliza la biblioteca schedule para ejecutar el trabajo cada minuto. El script se ejecuta indefinidamente hasta que se detiene manualmente.
