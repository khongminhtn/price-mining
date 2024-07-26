from datetime import datetime   

def tprint(message):
  now = datetime.now()
  print(f'{now.day}/{now.month}/{now.year}T{now.hour}:{now.minute}:{now.second} - {message}')
