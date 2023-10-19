# -*- coding: utf-8 -*-
'''
   ______            ____             _____ __   
  / ____/___ _____  / __ \_________  / __(_) /__ 
 / /   / __ `/ __ \/ /_/ / ___/ __ \/ /_/ / / _ \
/ /___/ /_/ / /_/ / ____/ /  / /_/ / __/ / /  __/
\____/\__,_/ .___/_/   /_/   \____/_/ /_/_/\___/ 
          /_/                                    
'''
#########################################################
#   CapProfile.py
#
# It is an application that allows you to obtain, send 
# and analyze search trends in real time on the Facebook 
# platform. With this tool, you can set priority topics 
# and receive notifications when those topics are among 
# the popular trends. In addition, the application stores
# trends in a database and displays graphs to visualize 
# trends over time.
#
#
# 10/18/23 - Changed to Python3 (finally)
#
# Author: Facundo Fernandez 
#
#
#########################################################

import requests
from bs4 import BeautifulSoup
import time
import random
import concurrent.futures
from requests.exceptions import RequestException, Timeout
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import logging
import urllib3
import re

# registry settings / Configuración de registro
logging.basicConfig(level=logging.INFO, filename='facebook_search.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
]

PROXIES = [
    "http://proxy1.example.com:8000",
    "http://proxy2.example.com:8000",
    "http://proxy3.example.com:8000",
]

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def search_on_facebook(queries, num_results=5, save_results=False):
    # List to store the results / Lista para almacenar los resultados
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for query in queries:
            # Sending each query to the search_facebook_profile function in a separate thread / Envío de cada consulta a la función search_facebook_profile en un hilo separado
            future = executor.submit(search_facebook_profile, query, num_results)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            # Compilation of the results of each thread / Recopilación de los resultados de cada hilo
            results.extend(future.result())

    if save_results:
        save_to_file(results)

    return results


def search_facebook_profile(query, num_results):
    # List to store the results of a profile / Lista para almacenar los resultados de un perfil
    results = []

    for _ in range(3):
        try:
            url = f"https://www.facebook.com/search/top/?q={query}"
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            proxies = {"http": random.choice(PROXIES)}
            response = requests.get(url, timeout=5, headers=headers, proxies=proxies, verify=False)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Getting the page title and recording it in the log file / Obtención del título de la página y registro en el archivo de registro
            title = soup.title.string
            logging.info("Title: %s", title)

            # Selection of user profiles found on the page / Selección de los perfiles de usuario encontrados en la página
            profiles = soup.select("a[data-hovercard^='/ajax/hovercard/user']")[:num_results]
            for profile in profiles:
                # Extraction of the URL, profile name and email name / Extracción de la URL, nombre de perfil y nombre de correo electrónico
                profile_url = "https://www.facebook.com" + profile['href']
                profile_name = profile.text.strip()
                email_name = extract_email_name(profile_url)
                results.append({"name": profile_name, "url": profile_url, "email": email_name})

            break

        except Timeout:
            logging.warning("Timeout error. Retrying...")
            time.sleep(3)

        except (RequestException, Exception) as e:
            logging.error("Error making request: %s", str(e))
            break

    return results


def extract_email_name(profile_url):
    try:
        response = requests.get(profile_url, timeout=5)
        response.raise_for_status()

        email_pattern = re.compile(r"[\w\.-]+@[\w\.-]+")
        emails = email_pattern.findall(response.text)
        if emails:
            return emails[0].split("@")[0]  # Returns the name before the '@' symbol of the first found email / Devuelve el nombre antes del símbolo '@' del primer correo electrónico encontrado

    except (RequestException, Exception) as e:
        logging.error("Error extracting email name: %s", str(e))

    return None


def save_to_file(results):
    try:
        with open("results.txt", "w") as file:
            for result in results:
                file.write(f"Name: {result['name']}\n")
                file.write(f"URL: {result['url']}\n")
                file.write(f"Email: {result['email']}\n")
                file.write("---\n")

        logging.info("Results saved to 'results.txt' file")

    except Exception as e:
        logging.error("Error saving results to file: %s", str(e))


def get_profile_text(profile_url):
    try:
        response = requests.get(profile_url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        post_elements = soup.select("div.user-post")
        texts = [element.get_text() for element in post_elements]

        return "\n".join(texts)

    except (RequestException, Exception) as e:
        logging.error("Error getting profile text: %s", str(e))

    return ""


def analyze_sentiments(results):
    # Utiliza AutoModelForSequenceClassification para cargar el modelo sin depender de PyTorch o TensorFlow
    model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


    # Creating text processing pipelines for sentiment analysis, entity extraction, and aspect analysis / Creación de tuberías de procesamiento de texto para análisis de sentimientos, extracción de entidades y análisis de aspectos
#    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
#    entity_extractor = pipeline("ner")
#    aspect_analyzer = TextClassificationPipeline("aspect-based-sentiment-analysis")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for result in results:
            # Sending each profile to the analyze_profile function in a separate thread / Envío de cada perfil a la función analyze_profile en un hilo separado
            future = executor.submit(analyze_profile, result, sentiment_analyzer, entity_extractor, aspect_analyzer)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            # Recording the results in the log file / Registro de los resultados en el archivo de registro
            result = future.result()
            logging.info("Profile: %s", result["name"])
            logging.info("URL: %s", result["url"])
            logging.info("Email: %s", result["email"])
            logging.info("Sentiment: %s", result["sentiment"])
            logging.info("Entities: %s", result["entities"])
            logging.info("Aspects: %s", result["aspects"])
            logging.info("---")

def analyze_profile(result, sentiment_analyzer, entity_extractor, aspect_analyzer):
    text = get_profile_text(result["url"])

    try:
        sentiment_results = sentiment_analyzer(text)
        sentiment = sentiment_results[0]["label"]
        result["sentiment"] = sentiment
    except Exception as e:
        logging.error("Error in sentiment analysis: %s", str(e))
        result["sentiment"] = None

    try:
        entities = entity_extractor(text)
        result["entities"] = entities
    except Exception as e:
        logging.error("Error in entity extraction: %s", str(e))
        result["entities"] = None

    try:
        aspect_results = aspect_analyzer(text)
        aspects = [aspect["aspect"] for aspect in aspect_results]
        result["aspects"] = aspects
    except Exception as e:
        logging.error("Error in aspect analysis: %s", str(e))
        result["aspects"] = None

    return result


if __name__ == "__main__":
    queries = ["Family", "Address", "Friends"]
    num_results = 3

    results = search_on_facebook(queries, num_results=num_results, save_results=True)
    analyze_sentiments(results)
