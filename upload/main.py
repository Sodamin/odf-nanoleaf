try:
  import usocket as socket
except:
  import socket

import time

import gc
gc.collect()

# Script Routing
connectNetwork = False
initializeLights = True
ledTest = True
displayTest = False

# Settings
ssid = ''
password = ''
pinOutValue = 25
numOfLEDPacks = 10
standardPixelBrightness = 1.0
tileArray = [[0,1,2],[3,4,5],[6,7,8],[9,10,11]]

  
# Light Functions

def allToColor(R, G, B, brightness):
  pixels[0] = (255,255,255)
  #pixels.fill((R, G, B))
  pixels.write()     
  status = "Set all Colors to" + " R: " + str(R) + " G: " + str(G) + " B: " + str(B)

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
  command = {'mode': mode, 'R': R, 'G': G, 'B': B, 'brightness': brightness}
  return(command)

if initializeLights:
  from neopixel import NeoPixel
  from machine import Pin

  led = Pin(2, Pin.OUT)
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
        time.sleep(0.5)


def rainbow_cycle(wait):
  for rounds in range(50):
    for j in range(255):
        for i in range(numOfLEDPacks):
            rc_index = (i * 256 // numOfLEDPacks) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.write()

if displayTest:
  import machine, display, time, math, network, utime
  print("Testing Display")
  tft = display.TFT() 
  tft.init(tft.ST7789,bgr=True,rot=tft.LANDSCAPE, miso=17,backl_pin=4,backl_on=1, mosi=19, clk=18, cs=5, dc=16)
  tft.setwin(40,52,320,240)
  tft.set_bg(tft.WHITE)
  tft.clear()
  text="Welcome to ODF-Nanoleaf"
  tft.text(120-int(tft.textWidth(text)/2),10,text,tft.BLACK)
  from machine import TouchPad, Pin
  tIn2 = TouchPad(Pin(2))
  tIn2.config(1000)
  while True:
    tIn2Touch = tIn2.read()
    if (tIn2Touch < 1007):
      tIn2TouchYN = True
    else:
      tIn2TouchYN = False
    print(tIn2TouchYN)
    if tIn2TouchYN:
      text="Touch Detected - Start LEDs"
      tft.text(120-int(tft.textWidth(text)/2),67-int(tft.fontSize()[1]/2+tft.fontSize()[1]+10),text,tft.BLACK)
      break
    time.sleep(1)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

if ledTest:
  while True:
    pixels.fill(RED)
    pixels.write()
    # Increase or decrease to change the speed of the solid color change.
    time.sleep(1)
    pixels.fill(GREEN)
    pixels.write()
    time.sleep(1)
    pixels.fill(BLUE)
    pixels.write()
    time.sleep(1)

    color_chase(RED, 0.1)  # Increase the number to slow down the color chase
    color_chase(YELLOW, 0.1)
    color_chase(GREEN, 0.1)
    color_chase(CYAN, 0.1)
    color_chase(BLUE, 0.1)
    color_chase(PURPLE, 0.1)

    rainbow_cycle(0)  # Increase the number to slow down the rainbow


if connectNetwork:
  import network
  import esp
  
  esp.osdebug(None)
  
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid, password)
  while station.isconnected() == False:
    pass
  print('Connection successful')
  print(station.ifconfig())


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
    status = allToColor(command['R'], command['G'], command['B'], command['brightness'])
  else:
    print('Command not recognized. Please try commands like http://host/?mode=setAll&R=203&G=122&B=002&brightness=0.3')
    conn.send(b'HTTP/1.1 200 OK\n')
  conn.send(b'Content-Type: text/html\n')
  conn.send(b'Status: ')
  conn.send(status)
  conn.close()
