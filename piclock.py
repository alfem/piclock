#!/usr/bin/python

import os, sys
import pygame
from time import sleep, gmtime, strftime
from pygame.locals import *
from configobj import ConfigObj

sys.path.append("./lib")

def console_display_init():
  drivers = ['fbcon', 'directfb', 'svgalib']
  detected = False
  for driver in drivers:
    print "Testing",driver,"...",
    if not os.getenv('SDL_VIDEODRIVER'):
      os.putenv('SDL_VIDEODRIVER', driver)
    try:
      pygame.display.init()
    except pygame.error:
      print "Error!"
      continue
    detected = True
    print "OK."
    break
    
  if not detected:
      raise Exception('Console video driver not available!')

# Main
def main():
    CONF = ConfigObj("piclock.conf")

    width = int(CONF["general"]["width"])
    height = int(CONF["general"]["height"])

    if os.getenv("DISPLAY"):
      pygame.display.init()
    else:
      console_display_init()

    pygame.init()
    pygame.mouse.set_visible(False)

    bgcolor=pygame.color.Color(CONF["clock"]["bgcolor"])
    fgcolor=pygame.color.Color(CONF["clock"]["fgcolor"])

    screen = pygame.display.set_mode((width, height), int(CONF["general"]["fullscreen"]))
    clock_big_font=pygame.font.Font(CONF["clock"]["font"], int(CONF["clock"]["bigsize"])) 
    clock_small_font=pygame.font.Font(CONF["clock"]["font"], int(CONF["clock"]["smallsize"])) 

    icon_alarm=pygame.image.load(os.path.join("icons","icon_alarm.png"))
    #sound_tick=pygame.mixer.Sound(os.path.join(".","sound_tick.wav"))

    running=True
    alarm=False


    time_x=int(CONF["clock"]["time_x"])
    time_y=int(CONF["clock"]["time_y"])
    seconds_x=int(CONF["clock"]["seconds_x"])
    seconds_y=int(CONF["clock"]["seconds_y"])

    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = 0
        elif event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            running = False
          if event.key == K_RETURN:
            alarm = True

      screen.fill(bgcolor)
      hhmm=strftime("%H:%M", gmtime())
      rtext=clock_big_font.render(hhmm, 1, fgcolor)
      screen.blit(rtext, (time_x, time_y))
      seconds=strftime(":%S", gmtime())
      rtext=clock_small_font.render(seconds, 1, fgcolor)
      screen.blit(rtext, (seconds_x,seconds_y))
      if alarm:
        screen.blit(icon_alarm, (15,350))
      pygame.display.flip()
      sleep(1)

    pygame.quit()


if __name__ == '__main__':
  main()

