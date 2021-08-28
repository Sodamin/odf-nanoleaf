def test():
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
