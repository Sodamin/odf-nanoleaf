try:
  import usocket as socket
except:
  import socket
import time
import gc

gc.collect() # Garbage Collector

# Settings
import config # Relevant Configs outsourced in config.py file
pinOutValue = config.pinOutValue
numOfLEDPacks = config.numOfLEDPacks
tileArray = config.tileArray

# Script Routing
connectNetwork = True
initializeLights = True
ledTest = False
displayTest = False

# Other Settings
standardPixelBrightness = 1.0

###############################################################
################### Light Functions ###########################
###############################################################

def allToColor(R, G, B, brightness):
  pixels[0] = (255,255,255)
  R = int(R*brightness)
  G = int(G*brightness)
  B = int(B*brightness)
  pixels.fill((R, G, B))
  pixels.write()     
  status = "Set all Colors to" + " R: " + str(R) + " G: " + str(G) + " B: " + str(B)
 # print("colors Set")
  #rainbow_cycle(10)
  return status

def tilesToColor(tileNums, R, G, B, brightness):
  for tileNum in tileNums:
    for pixel in tileArray[tileNum]:
      pixels[pixel] = (R, G, B)
  pixels.brightness(brightness)

def commandFromRequest(request):
  try:
    mode = request[request.find('?mode=')+6:request.find('&')]
  except:
    mode = 'none'
  try:
    R = int(request[request.find('&R=')+3:request.find('&R=')+6])
  except:
    R = 0
  try:
    G = int(request[request.find('&G=')+3:request.find('&G=')+6])
  except:
    G = 0
  try:
    B = int(request[request.find('&B=')+3:request.find('&B=')+6])
  except:
    B = 0
  try:
    brightness = float(request[request.find('&brightness=')+12:request.find('&brightness=')+15])
  except:
    brightness = 1.0
  try:
    speed = float(request[request.find('&speed=')+7:request.find('&speed=')+10])
  except:
    speed = 0
  command = {'mode': mode, 'R': R, 'G': G, 'B': B, 'brightness': brightness, 'speed': speed}
  return(command)

if initializeLights:
  from neopixel import NeoPixel
  from machine import Pin

  pin = Pin(pinOutValue, Pin.OUT)
  pixels = NeoPixel(pin, numOfLEDPacks)
  if ledTest:
    for i in range(numOfLEDPacks):   
      pixels[i] = (255,255,255)
    pixels.write()

  print("Lights Initialized")

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def color_chase(color, wait):
    for i in range(numOfLEDPacks):
        pixels[i] = color
        time.sleep(wait)
        pixels.write()


def rainbow_cycle(wait):
  for rounds in range(50):
    for j in range(int(255/10)):
        for i in range(89,numOfLEDPacks):
            rc_index = (i * 256 // numOfLEDPacks) + j*10
            pixels[i] = wheel(rc_index & 255)
        time.sleep(wait)
        pixels.write()


RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

if ledTest:
  while True:
    allToColor(255,255,255,1)
    time.sleep(0.015)
    allToColor(0,0,0,1)
    time.sleep(0.015)
    print("next cycle")
    #rainbow_cycle(0)  # Increase the number to slow down the rainbow

if displayTest:
  import display
  display.test()
if not connectNetwork:
  import network
  import esp
  
  esp.osdebug(None)
  
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(config.credentials[0]["ssid"], config.credentials[0]["password"])
  while station.isconnected() == False:
    pass
  print('Connection successful')
  print(station.ifconfig())

if connectNetwork:
  import web
  web.connect(config)

def web_page_old():
  html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
  <p>GPIO state: <strong></strong></p><p><a href="/?mode=setAll&R=203&G=122&B=002&brightness=0.3"><button class="button">Test 1</button></a></p> </body></html>"""
  return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)



while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  command = commandFromRequest(request)
  if command['mode'] == 'setAll':
    status = allToColor(command['R'], command['G'], command['B'], float(command['brightness']))
  if command['mode'] == 'rainbow':
    rainbow_cycle(1)#command['speed'])
    status = 'rainbow'
  else:
    print('Command not recognized. Please try commands like http://192.168.0.88/?mode=setAll&R=203&G=122&B=002&brightness=0.3')
    status = 'no status'
  conn.send(b'HTTP/1.1 200 OK\n')
  conn.send(b'Content-Type: text/html\n')
  conn.send(b'Status: ')
  conn.send(status)
  conn.close()
