import os
import requests
from pydub import AudioSegment


# ------------------ Custom Classes -------------------------

PWD = os.path.dirname(__file__)

class Scripture:
    def __init__(self, address):
        self.address = address
        self.bible_book = self.get_bible_book()
        self.chapter = self.get_chapter()
        self.verses_string = self.get_verses_string()
        self.verses_list = self.get_verses_list()

    def get_bible_book(self):
        # find out for each scripture the bible book, chapter and verse
        bible_book = self.address.split(" ")[0]

        # Se for um livro bíblico SEM número na frente
        if len(bible_book) <= 1:
            scripture_sliced = self.address.split(" ")
            bible_book = " ".join((scripture_sliced[0], scripture_sliced[1]))

        return bible_book

    def get_chapter(self):
        first_part_address = self.address.split(":")[0]
        try:
            chapter = int(first_part_address.split(" ")[-1])
        except ValueError:
            return 0

        return chapter

    def get_verses_string(self):
        try:
            second_part_address = self.address.split(":")[1].replace(" ", "")
        except IndexError:
            return "0"
        return second_part_address

    def get_verses_list(self):
        if "," in self.verses_string:
            verses = self.verses_string.split(",")
        else:
            verses = [self.verses_string]
        return verses


class DownloadManager:
    def __init__(self, endpoint, parameters, scripture_object):
        self.endpoint = endpoint
        self.params = parameters
        self.scripture_object = scripture_object
        self.json = self.get_json()

    def get_json(self):
        # Getting the json from the API
        try:
            response = requests.get(self.endpoint, params=self.params)
        except requests.exceptions.RequestException:
            return 1

        try:
            json = response.json()["files"]["T"]["MP3"][0]
        except TypeError:
            return 2

        return json

    def get_milliseconds(self, time):
        dividido = time.split(":")
        hour = int(dividido[0])
        minute = int(dividido[1])
        sec = float(dividido[2])

        sec_total = (hour * 3600) + (minute * 60) + sec
        milliseconds = sec_total * 1000

        return milliseconds

    def download_audio(self):
        response_audio = requests.get(self.json["file"]["url"])

        with open(f"{PWD}/static/dashboard/audio/input/in_audio.mp3", "wb") as f_in_audio:
            f_in_audio.write(response_audio.content)

        # cut audio based on the json file
        try:
            audio_complete = AudioSegment.from_file(f"{PWD}/static/dashboard/audio/input/in_audio.mp3", format="mp3")
        except FileNotFoundError:
            return 1

        output_audio_list = []

        for verse in self.scripture_object.verses_list:
            if "-" in verse:
                verses_list = [int(verse.split("-")[0]), int(verse.split("-")[1])]
            else:
                verses_list = [int(verse), int(verse)]

            try:
                start_milliseconds = self.get_milliseconds(self.json["markers"]["markers"][verses_list[0] - 1]["startTime"])
                end_milliseconds = (self.get_milliseconds(self.json["markers"]["markers"][verses_list[1] - 1]["startTime"]) +
                                    self.get_milliseconds(self.json["markers"]["markers"][verses_list[1] - 1]["duration"]))
            except IndexError:
                return 2

            extract = audio_complete[start_milliseconds:end_milliseconds]
            output_audio_list.append(extract)

        output_audio = output_audio_list[0]
        for audio in output_audio_list[1:]:
            output_audio = output_audio + audio

        output_audio.export(f"{PWD}/static/dashboard/audio/output/{self.scripture_object.bible_book}_{self.scripture_object.chapter}.{self.scripture_object.verses_string}.wav", format="wav")

        return 0


# ------------------- Dictionary Bible Books in Portuguese ---------------------------
BIBLE_BOOKS_NUMBER_T = {
    "gênesis": 1,
    "êxodo": 2,
    "levítico": 3,
    "números": 4,
    "deuteronômio": 5,
    "josué": 6,
    "juízes": 7,
    "rute": 8,
    "1 samuel": 9,
    "2 samuel": 10,
    "1 reis": 11,
    "2 reis": 12,
    "1 crônicas": 13,
    "2 crônicas": 14,
    "esdras": 15,
    "neemias": 16,
    "ester": 17,
    "jó": 18,
    "salmos": 19,
    "salmo": 19,
    "provérbios": 20,
    "eclesiastes": 21,
    "cântico de salomão": 22,
    "isaías": 23,
    "jeremias": 24,
    "lamentações": 25,
    "ezequiel": 26,
    "daniel": 27,
    "oseias": 28,
    "joel": 29,
    "amós": 30,
    "obadias": 31,
    "jonas": 32,
    "miqueias": 33,
    "naum": 34,
    "habacuque": 35,
    "sofonias": 36,
    "ageu": 37,
    "zacarias": 38,
    "malaquias": 39,
    "mateus": 40,
    "marcos": 41,
    "lucas": 42,
    "joão": 43,
    "atos": 44,
    "romanos": 45,
    "1 coríntios": 46,
    "2 coríntios": 47,
    "gálatas": 48,
    "efésios": 49,
    "filipenses": 50,
    "colossenses": 51,
    "1 tessalonicenses": 52,
    "2 tessalonicenses": 53,
    "1 timóteo": 54,
    "2 timóteo": 55,
    "tito": 56,
    "filêmon": 57,
    "hebreus": 58,
    "tiago": 59,
    "1 pedro": 60,
    "2 pedro": 61,
    "1 joão": 62,
    "2 joão": 63,
    "3 joão": 64,
    "judas": 65,
    "apocalipse": 66,
    "gên": 1,
    "êx": 2,
    "le": 3,
    "núm": 4,
    "de": 5,
    "jos": 6,
    "jz": 7,
    "ru": 8,
    "1sa": 9,
    "2sa": 10,
    "1rs": 11,
    "2rs": 12,
    "1cr": 13,
    "2cr": 14,
    "esd": 15,
    "ne": 16,
    "est": 17,
    "sal": 19,
    "pr": 20,
    "ec": 21,
    "cân": 22,
    "is": 23,
    "je": 24,
    "la": 25,
    "ez": 26,
    "da": 27,
    "os": 28,
    "jl": 29,
    "am": 30,
    "ob": 31,
    "jon": 32,
    "miq": 33,
    "na": 34,
    "hab": 35,
    "sof": 36,
    "ag": 37,
    "za": 38,
    "mal": 39,
    "mt": 40,
    "mr": 41,
    "lu": 42,
    "jo": 43,
    "at": 44,
    "ro": 45,
    "1co": 46,
    "2co": 47,
    "gál": 48,
    "ef": 49,
    "fil": 50,
    "col": 51,
    "1te": 52,
    "2te": 53,
    "1ti": 54,
    "2ti": 55,
    "tit": 56,
    "flm": 57,
    "he": 58,
    "tg": 59,
    "1pe": 60,
    "2pe": 61,
    "1jo": 62,
    "2jo": 63,
    "3jo": 64,
    "ju": 65,
    "ap": 66,
    "gên.": 1,
    "êxo.": 2,
    "lev.": 3,
    "núm.": 4,
    "deu.": 5,
    "jos.": 6,
    "juí.": 7,
    "1 sam.": 9,
    "2 sam.": 10,
    "1 crô.": 13,
    "2 crô.": 14,
    "esd.": 15,
    "nee.": 16,
    "sal.": 19,
    "pro.": 20,
    "ecl.": 21,
    "cân.": 22,
    "isa.": 23,
    "jer.": 24,
    "lam.": 25,
    "eze.": 26,
    "dan.": 27,
    "ose.": 28,
    "obd.": 31,
    "miq.": 33,
    "hab.": 35,
    "sof.": 36,
    "zac.": 38,
    "mal.": 39,
    "mat.": 40,
    "mar.": 41,
    "luc.": 42,
    "jo.": 43,
    "at.": 44,
    "rom.": 45,
    "1 cor.": 46,
    "2 cor.": 47,
    "gál.": 48,
    "efé.": 49,
    "fil.": 50,
    "col.": 51,
    "1 tes.": 52,
    "2 tes.": 53,
    "1 tim.": 54,
    "2 tim.": 55,
    "filêm.": 57,
    "heb.": 58,
    "tia.": 59,
    "1 ped.": 60,
    "2 ped.": 61,
    "apo.": 66,
}




# ------------------ Custom Functions -----------------------


# ------------------------ CONSTANTS ---------------------------------
ENDPOINT = "https://b.jw-cdn.org/apis/pub-media/GETPUBMEDIALINKS"
BIBLE_BOOKS_NUMBER = BIBLE_BOOKS_NUMBER_T

# ------------------------ MAIN ---------------------------------


def download_query(lines):

    scriptures = [line.strip().lower() for line in lines]

    print("All scriptures entered. Please wait while we process the downloads.")

    downloaded_files = []

    # Process each input line
    for address in scriptures:

        texto = Scripture(address=address)

        # Getting the json from the API
        try:
            params = {
                "booknum": BIBLE_BOOKS_NUMBER[f"{texto.bible_book}"],
                "output": "json",
                "pub": "nwt",
                "fileformat": "MP3",
                "alllangs": 0,
                "track": texto.chapter,
                "langwritten": "T",
                "txtCMSLang": "T",
            }

        except KeyError:
            continue

        downloader = DownloadManager(endpoint=ENDPOINT, parameters=params, scripture_object=texto)

        if downloader.json == 1:
            print("Couldn't connect to server. Please check to see if your computer is connected to the internet.")
            exit()
        elif downloader.json == 2:
            print(f"Error [{texto.address}]: Invalid scripture.")
            continue

        result = downloader.download_audio()

        if result == 0:
            print(f"{texto.address} (status): in")
            file_name = (f"{downloader.scripture_object.bible_book}_{downloader.scripture_object.chapter}."
                         f"{downloader.scripture_object.verses_string}.wav")
            downloaded_files.append(file_name)

        elif result == 1:
            print("Could open the buffer file on folder 'input'. Make sure the folder and the file within it exist.")
            exit()

        elif result == 2:
            print(f"{texto.address} (status): error; the audio for that scripture doesn't exist.")
            continue

    return downloaded_files

