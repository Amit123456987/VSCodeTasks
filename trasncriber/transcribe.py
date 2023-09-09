
with open('pyCode.py', 'wr', encoding='utf-8') as file:
    code = file.read()
    code  = code.replace("fish","(").replace("dish",")").replace("square","[]")
    file.write(code)
