import os


def create_folders_file(path,code):
  
  indexOfSlash = path.rfind("/")
  
  folder = path[:indexOfSlash].join("/")
  os.makedirs(folder, exist_ok=True)
  
  fileName = path[indexOfSlash+1:]  

  with open(path, 'w') as f:
    f.write(code)  


path=''
code='''
'''

create_folders_file(path,code)



