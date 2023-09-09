import re
import json

fw = open("roughCode/extractCommand", "w")
fwN = open("roughCode/newData", "w", encoding='utf-8')


with open('roughCode/newData', 'r', encoding='utf-8') as file:
    pattern = r'\$.*?(?:\n|\\)'
    
    previous = " "

    for line in file:
        extracted_text = re.search(pattern, line)

        if( len(previous) >=  1 and previous[-1] == "\\"):
            fw.write(line)

        elif( extracted_text != None ):
            fw.write(extracted_text.group())

        previous = line
        previous = previous.strip()

fileName=".vscode/tasks.json"

tasks = []
with open(fileName) as f:
  tasks = f.read()
  tasks = json.loads(tasks)

with open('roughCode/extractCommand', 'r', encoding='utf-8') as file:
    aCommand = ""
    listOfCommands = []
    
    
    for line in file:
        aCommand= aCommand + line
        
        if( line[-1] != "\\" ):
            # aCommand = aCommand + line    
            taskFormat = {
                    "label": "echo",
                    "type": "shell",
                    "command": "echo Hello",
                    "presentation": {
                        "panel": "new"
                    }
                }
            
            taskFormat["label"] = aCommand
            taskFormat["command"] = aCommand
            aCommand = ""
            
            listOfCommands.append(taskFormat)
    
    tasks["tasks"] = listOfCommands
    strTask = json.dumps(tasks)
    # fTask.write(strTask)    

with open(".vscode/tasks.json","w") as Optask:
    Optask.write(json.dumps(tasks))
