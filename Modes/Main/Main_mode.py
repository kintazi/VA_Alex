import sys
import os
sys.path.append(f"{os.getcwd()}")

import json

def Main():
    while True:
        with open("Settings/Commands.json", "r", encoding="utf-8") as cmd_file:
            cmd = json.load(cmd_file)
        
        input_data = input()
        command = Filter(input_data, cmd)
        print(command)

def Filter(input_data: str, cmd: dict):
    output = []
    Verb = ""
    for k, v in cmd["Verbs"].items():
        for c in v:
            if c in input_data:
                Verb = k
    for k, v in cmd["cmd"].items():
        if Verb == k:
            for kk, vv in v.items():
                for c in vv:
                    if c in input_data:
                        output.append(f"{Verb}_{kk}")
    for k, v in cmd["Dop_info"].items():
        if k in str(output[0]):
            for kk, vv in v.items():
                for c in vv:
                    if c in input_data:
                        output[0] = f"{output[0]}_{kk}"
    output.append(input_data)
    return output

if __name__ == "__main__":
    Main()
