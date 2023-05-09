import openai
import requests
import json
import datetime
from translate import Translator
from API_KEYS import OPENAI_KEY

BOOK_NAME = 'El guardian entre el centeno (Unknown)\n'
CLIPPINGS_ROUETE = "F:/documents/My Clippings.txt"

openai.api_key = OPENAI_KEY


def generate_text_gpt(prompt):
    # porfavor crea una anki flash card para cada una de las palabras que te voy a pasar, el formato desado es el siguiente, amor;love next line muerte;deth...love,deth,moon
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=512,
        n=1,
        stop=None,
        temperature=0,
    )

    message = completions.choices[0].text
    return message.strip()


def generate_text_libre_translate(world):
    url = "https://libretranslate.com/translate"
    payload = {"q": world, "source": "auto", "target": "es", "format": "text", "api_key": ""}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url=url, data=payload, headers=headers)
    print(response.json())


def retrieve_words_from_boook():
    with open(CLIPPINGS_ROUETE, 'r', encoding='utf-8-sig') as archivo:
        line = archivo.readline()
        while line != '':
            if line == BOOK_NAME:
                for _ in range(3):
                    line = archivo.readline()
                yield line.rstrip().lower().replace(",", "").replace(".", "")

            line = archivo.readline()


def file_name():
    fecha_actual = datetime.datetime.now()
    fecha_actual_str = fecha_actual.strftime('%d_%m_%Y')

    return fecha_actual_str


if __name__ == '__main__':
    file_name = file_name()
    print("INICIANDO proceso de traduccion...")

    # Recuperar palabras ya traducidas
    with open('words.json', 'r') as archivo:
        datos = json.load(archivo)

    # Generar nuevas traducciones
    with open(f"./AnkiFlashCards/{file_name}.txt", 'w') as AnkiCadsFile:
        for word in retrieve_words_from_boook():
            if word not in datos[word[:1]]["words"]:
                translator = Translator(to_lang="es")
                translation = translator.translate(word)

                AnkiCadsFile.write(f"{word}:{translation}\n")
                datos[word[:1]]["words"].append(word)

    # Actualizar fichero de palabras ya traducidas
    with open('words.json', 'w') as archivo:
        json.dump(datos, archivo)

# JSON vacio
# {"a": {"id": 1, "words": []}, "b": {"id": 2, "words": []}, "c": {"id": 3, "words": []}, "d": {"id": 4, "words": []},
#  "e": {"id": 5, "words": []}, "f": {"id": 6, "words": []}, "g": {"id": 7, "words": []}, "h": {"id": 8, "words": []},
#  "i": {"id": 9, "words": []}, "j": {"id": 10, "words": []}, "k": {"id": 11, "words": []},
#  "l": {"id": 12, "words": []}, "m": {"id": 13, "words": []}, "n": {"id": 14, "words": []},
#  "o": {"id": 15, "words": []}, "p": {"id": 16, "words": []}, "q": {"id": 17, "words": []},
#  "r": {"id": 18, "words": []}, "s": {"id": 19, "words": []}, "t": {"id": 20, "words": []},
#  "u": {"id": 21, "words": []}, "v": {"id": 22, "words": []}, "w": {"id": 23, "words": []},
#  "x": {"id": 24, "words": []}, "y": {"id": 25, "words": []}, "z": {"id": 26, "words": []}}

