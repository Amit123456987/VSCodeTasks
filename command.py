import json

commands=""
with open("comandtext", "r") as f:
  commands = f.read().replace("\\","").replace("\n\n","#").replace("\n","").replace("$","\n")
  commands = commands.strip("\n")

fileName=".vscode/tasks.json"

with open(fileName) as f:
  tasks = f.read()

  tasks = json.loads(tasks)
  listOfTasks = tasks["tasks"]
  newListOfTasks = []

  groupdOfCommandIndex = 1
  for command in commands.split("#"):
    
    namesOfGroupOfCommands = []

    for singleCommand in command.split("\n"):
      singleCommand = singleCommand.strip("\n").strip()

      taskFormat = {
              "label": "echo",
              "type": "shell",
              "command": "echo Hello",
              "presentation": {
                  "panel": "new"
              }
          }
      
      taskFormat["label"] = singleCommand[:30]
      taskFormat["command"] = singleCommand
      taskFormat["hide"] = True

      namesOfGroupOfCommands.append(singleCommand[:30])

      newListOfTasks.append(taskFormat)
    
    groupofCommands = {
      "label": str(groupdOfCommandIndex),
      "dependsOn": namesOfGroupOfCommands
    }
    newListOfTasks.append(groupofCommands)

    groupdOfCommandIndex = groupdOfCommandIndex + 1

  tasks["tasks"] = newListOfTasks

  tasks = json.dumps(tasks)

  with open(fileName, 'w') as f:
    f.write(tasks)

