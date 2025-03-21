greeting = ''
with open('greeting.txt', 'rt') as text:
    alfa = [st for st in text.readlines()]
    greeting = ''.join(alfa)
    print(greeting)