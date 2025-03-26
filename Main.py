from threading import Thread
import Background_Function.BG_Fun as BG_fun
import Voice.Main_voice as voice
import local.number.word_to_number as word_to_number
import CMD
import importlib
import time
import json
import os


def sleep_fun(skip: bool = False):
    if skip == True:
        Main()
    print("sleep")
    with open("Settings/Main_settings.json", "r", encoding="utf-8") as MS_file:
        Name = json.load(MS_file)["Name"]
    while True:
        input_data = voice.stt(mod=True)
        if input_data == Name:
            print("sleep_off")
            Main()
        elif Name in input_data:
            print("sleep_off")
            Main(input_from_sleep=input_data)

def Main(input_from_sleep: str = ""):
    while True:
        with open("Settings/CMD_data.json", "r", encoding="utf-8") as cmd_file:
            CMD_data = json.load(cmd_file)
        with open("Settings/Main_settings.json", "r", encoding="utf-8") as MS_file:
            Main_settings = json.load(MS_file)
        with open("Settings/Status.json", "r", encoding="utf-8") as St_file:
            Status = json.load(St_file)
        
        #input_text = input().lower()
        if input_from_sleep != "":
            input_text = input_from_sleep
            input_from_sleep = ""
        else:
            input_text = voice.stt()
            if input_text == "sleep":
                sleep_fun()
        print(input_text)

        command = Filter_text(input_text=input_text, CMD_data=CMD_data)

        print(command)
        if command[0] != "":
            back_data = CMD.Main(command[0], command[1])
            if back_data == "OK":
                print("OK")
                voice.tts("Хорошо")
            elif back_data == "ERROR":
                print("ERROR")
                voice.tts("Ошибка")
            elif back_data != None:
                print(back_data)
                voice.tts(back_data)










def Filter_text(input_text: str, CMD_data: dict):
    output_com = ""
    data = []
    for k, v in CMD_data["com"].items():
        for c in v["trig"]:
            if c in input_text:
                if v["tbr"] != []:
                    for t in v["tbr"]:
                        if t in input_text:
                            output_com = k
                else:
                    output_com = k
    if output_com != "":
        if CMD_data["com"][output_com]["need_data"] != []:
            need_data_list = CMD_data["com"][output_com]["need_data"]
            for c in need_data_list:
                match c:
                    case "int":
                        num = word_to_number.word_to_num(input_text)
                        if num != None:
                            data.append(int(num))
                        else:
                            while True:
                                print("Выберите значение")
                                voice.tts("Выберите значение")
                                num2 = word_to_number.word_to_num(voice.stt(mod=True))
                                try:
                                    data.append(int(num2))
                                    break
                                except:
                                    print("ERROR")
                                    voice.tts("Ошибка")
                    case "text":
                        for c in CMD_data["com"][output_com]["trig"]:
                            id = input_text.find(c)
                            if id != -1:
                                data.append(input_text[id+len(c):])
                        if data == []:
                            data.append(voice.stt(mod=True))


    output = [output_com, data]
    return output




















# def Main():
#     while True:
#         with open("Settings/Commands.json", "r", encoding="utf-8") as cmd_file:
#             cmd = json.load(cmd_file)
#         with open("Settings/Main_settings.json", "r", encoding="utf-8") as MS_file:
#             Main_settings = json.load(MS_file)
#         with open("Settings/Status.json", "r", encoding="utf-8") as St_file:
#             Status = json.load(St_file)
        
#         input_data = input()
#         command = Filter(input_data, cmd)
#         print(command)
#         CMD.Main(command)

# def Filter(input_data: str, cmd: dict):
#     output = []
#     Verb = ""
#     for k, v in cmd["Verbs"].items():
#         for c in v:
#             if c in input_data:
#                 Verb = k
#     for k, v in cmd["cmd"].items():
#         if Verb == k:
#             for kk, vv in v.items():
#                 for c in vv:
#                     if c in input_data:
#                         output.append(f"{Verb}_{kk}")
#     for k, v in cmd["Dop_info"].items():
#         if k in str(output[0]):
#             for kk, vv in v.items():
#                 for c in vv:
#                     if c in input_data:
#                         output[0] = f"{output[0]}_{kk}"
#     output.append(input_data)
#     return output




# def Main():
#     with open("Settings/Main_settings.json", "r", encoding="utf-8") as MS_file:
#         Main_settings = json.load(MS_file)
#     with open("Settings/Status.json", "r", encoding="utf-8") as St_file:
#         Status = json.load(St_file)

#     Mode = Status["Mode"]
    
    # try:
    #     Module = importlib.import_module(f"Modes.{Mode}.{Mode}_mode")
    #     t1 = Thread(target=Module.Main, daemon=True)
    # except ModuleNotFoundError:
    #     print(f"Режим с названием: \"{Mode}\" не найден.")
    # t2 = Thread(target=BG_fun.Main, daemon=True)
    # t1.start()
    # t2.start()

    # t1.join()

if __name__ == "__main__":
    print("Start")
    sleep_fun(skip=True)
