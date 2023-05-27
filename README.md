
   README

   Este proyecto consiste en un script en Python que realiza búsquedas en Facebook y analiza los sentimientos, las entidades y los aspectos de los perfiles encontrados.

   Requisitos previos

        - Python 3.7 o superior
        - Paquetes de Python: requests, BeautifulSoup, concurrent.futures, transformers

   Configuración

   Antes de ejecutar el script, asegúrate de configurar correctamente las siguientes variables en el archivo `script.py`:

        - `USER_AGENTS`: Una lista de User Agents que simulan diferentes navegadores.
        - `PROXIES`: Una lista de proxies para realizar las solicitudes.
        - `logging.basicConfig()`: Configura el nivel de registro y el archivo de registro.

   Uso

   1. Asegúrate de tener instalados todos los paquetes de Python necesarios. Puedes instalarlos ejecutando el siguiente comando:

     pip install -r requirements.txt


   El script buscará perfiles de Facebook basados en las consultas proporcionadas y analizará los sentimientos, las entidades y los aspectos de los perfiles encontrados.
   Los resultados se guardarán en un archivo `results.txt` y se registrarán en el archivo `facebook_search.log`.

   Personalización

   Puedes personalizar el comportamiento del script modificando los siguientes parámetros:

        - `queries`: Una lista de consultas para buscar perfiles en Facebook.
        - `num_results`: El número máximo de resultados por consulta.

   Contribución

   Si deseas contribuir a este proyecto, siéntete libre de enviar pull requests o abrir issues en el repositorio.

   Notas

   Este script se proporciona con fines educativos y de demostración. Úsalo con responsabilidad.
