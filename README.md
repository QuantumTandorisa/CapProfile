# CapProfile
 ______            ____             _____ __   
  / ____/___ _____  / __ \_________  / __(_) /__ 
 / /   / __ `/ __ \/ /_/ / ___/ __ \/ /_/ / / _ \
/ /___/ /_/ / /_/ / ____/ /  / /_/ / __/ / /  __/
\____/\__,_/ .___/_/   /_/   \____/_/ /_/_/\___/ 
          /_/                                    

## Descripción
CapProfile es una aplicación que te permite obtener, enviar y analizar tendencias de búsqueda en tiempo real en la plataforma de Facebook. Con esta herramienta, puedes establecer temas prioritarios y recibir notificaciones cuando esos temas se encuentren entre las tendencias populares. Además, la aplicación almacena tendencias en una base de datos y muestra gráficos para visualizar tendencias a lo largo del tiempo.

## Requisitos
- Python 3.x
- Bibliotecas requeridas, que puedes instalar ejecutando `pip install -r requirements.txt`.
- instalar PyTorch y sus componentes en tu entorno virtual. Asegúrate de ejecutar el siguiente comando.
`(myenv) $ pip install torch==1.9.1+cpu torchvision==0.10.1+cpu torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html`


## Funcionalidades

- **Búsqueda en Facebook:** CapProfile realiza búsquedas en Facebook utilizando consultas y muestra resultados con nombres de perfil y URL de perfiles de usuario relevantes.

- **Análisis de Sentimientos:** La aplicación utiliza el análisis de sentimientos para evaluar el contenido de los perfiles y proporciona información sobre el sentimiento general de las publicaciones.

- **Extracción de Entidades:** CapProfile también puede extraer entidades de texto, como nombres, lugares y otros elementos relevantes en las publicaciones.

- **Análisis de Aspectos:** La herramienta realiza un análisis de aspectos para identificar temas específicos dentro de las publicaciones.

- **Almacenamiento de Resultados:** Los resultados de las búsquedas y los análisis se pueden guardar en un archivo de texto llamado `results.txt`.

## Uso

1. Configura las consultas que deseas buscar en la lista `queries` en el script `CapProfile.py`.

2. Ejecuta el script con Python 3.x usando el comando:
   ```bash
   python3 CapProfile.py

## Personalización

Puedes personalizar la aplicación ajustando las siguientes variables en el script:

queries: Agrega o modifica las consultas que deseas buscar.

num_results: Establece el número de resultados que deseas obtener por consulta.

save_results: Cambia a True si deseas guardar los resultados en el archivo results.txt.

Puedes ajustar los agentes de usuario (USER_AGENTS) y las configuraciones de proxy (PROXIES) según tus necesidades
