from display import DisplayDriver


d = DisplayDriver()

d.start()

while True:
    d.update()
