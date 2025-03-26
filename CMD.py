import datetime
import screen_brightness_control as sc
import webbrowser
from subprocess import Popen
import Voice.Main_voice as voice
import os

import Settings.Data 


def Main(cmd: str, data: list = []):
    match cmd:
        case "ctime":  # Получение времени в формате int и str. Вход: (format - "int" или "str")
            time = str(datetime.datetime.now().time())[:5]
            try:
                format = data[0]
            except:
                format = "str"
            output = ""
            if "int" in format:
                output = time
            elif "str" in format:
                str_time = ""
                if int(time[0]) != 0:
                    if int(time[0]) == 1:
                        str_time = f'{Settings.Data.VA_time_to_words[int(f"{time[0]}{time[1]}")]}'
                    else:
                        str_time = f'{str_time}{Settings.Data.VA_time_to_words[int(f"{time[0]}0")]} '
                        if int(time[1]) != 0:
                            str_time = f'{str_time}{Settings.Data.VA_time_to_words[int(time[1])]}'
                else:
                    str_time = f'{str_time}{Settings.Data.VA_time_to_words[int(time[1])]}'
                str_time = f'{str_time}... '

                if int(time[3]) != 0:
                    if int(time[3]) == 1:
                        str_time = f'{str_time}{Settings.Data.VA_time_to_words[int(f"{time[3]}{time[4]}")]}'
                    else:
                        str_time = f'{str_time}{Settings.Data.VA_time_to_words[int(f"{time[3]}0")]} '
                        if int(time[4]) != 0:
                            str_time = f'{str_time}{Settings.Data.VA_time_to_words2[int(time[4])]}'
                else:
                    str_time = f'{str_time}{Settings.Data.VA_time_to_words2[int(time[4])]}'
                output = str_time
                print(str_time)
            return output

        case "screen_br":  # Изменение яркости монитора. Вход: (bright - int(0, 100))
            try:
                bright = data[0]
                sc.set_brightness(bright)
                return "OK"
            except:
                return "ERROR"

        case "open_browser":  # Открытие браузера
            try:
                os.startfile('"Labels\\Yandex"')
                return "OK"
            except:
                return "ERROR"

        case "close_browser":
            try:
                Popen('taskkill /im browser.exe /f', shell=True)
                return "OK"
            except:
                return "ERROR"

        case "request":
            voice.tts("Ожидаю запроса")
            req = voice.stt(mod=True).replace(" ", "+")
            try:
                webbrowser.open(f"https://yandex.ru/search/?text={req}")
                return "OK"
            except:
                return "ERROR"
        case "question":
            req = data[0].replace(" ", "+")
            try:
                webbrowser.open(f"https://yandex.ru/search/?text={req}")
                return "OK"
            except:
                return "ERROR"

