import kivy
import RPi.GPIO as GPIO
import const
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty, ReferenceListProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
import wiringpi

"""
Initializing global parameters
"""
kivy.require('1.10.1') 
wiringpi.wiringPiSPISetup(const.selectPin,const.potSpeed)

class Controller(Widget):
  active = BooleanProperty(False)     
  mode = StringProperty(const.NULL)
  def __init__(self,GPIO):
    self.GPIO = GPIO
    self.mode = const.CONST
    self.active = False
    GPIO.setmode(GPIO.BCM)
    self.FPS = const.INITFPS
    self.enPin560State = GPIO.LOW
    self.enPin470State = GPIO.LOW
    self.enPin415State = GPIO.LOW
    self.potPin560State = const.MINPOT
    self.potPin470State = const.MINPOT
    self.potPin415State = const.MINPOT
    GPIO.setup(const.enPin560,GPIO.OUT,initial=self.enPin560State)
    GPIO.setup(const.enPin470,GPIO.OUT,initial=self.enPin470State)
    GPIO.setup(const.enPin415,GPIO.OUT,initial=self.enPin415State)
      
  def updateEnable(self):
    self.GPIO.output(const.enPin560,self.enPin560State)
    self.GPIO.output(const.enPin470,self.enPin470State)
    self.GPIO.output(const.enPin415,self.enPin415State)
  

  def initMode(self):
    assert self.active == True 
    if self.mode == const.CONST:
      self.enPin560State = self.GPIO.HIGH
      self.enPin470State = self.GPIO.HIGH
      self.enPin415State = self.GPIO.HIGH
    elif self.mode == const.TRIG1:
      self.enPin560State = self.GPIO.HIGH
      self.enPin470State = self.GPIO.LOW
      self.enPin415State = self.GPIO.HIGH
      Clock.schedule_once(self.blinkController,1.0 / self.FPS)
    elif self.mode == const.TRIG2:
      self.enPin560State = self.GPIO.LOW
      self.enPin470State = self.GPIO.HIGH
      self.enPin415State = self.GPIO.HIGH
      Clock.schedule_once(self.blinkController,1.0 / self.FPS)
    else:
      assert False
    self.updateEnable()

  def updateIntensity(self):
    buf = bytes([const.chanPot560]) 
    wiringpi.wiringPiSPIDataRW(const.selectPin,buf)
    buf = bytes([self.potPin560State])
    wiringpi.wiringPiSPIDataRW(const.selectPin,buf) 

    buf = bytes([const.chanPot470]) 
    wiringpi.wiringPiSPIDataRW(const.selectPin,buf)
    buf = bytes([self.potPin470State])
    wiringpi.wiringPiSPIDataRW(const.selectPin,buf) 

    buf = bytes([const.chanPot415]) 
    wiringpi.wiringPiSPIDataRW(const.selectPin,buf)
    buf = bytes([self.potPin415State])
    wiringpi.wiringPiSPIDataRW(const.selectPin,buf)

 
  def modeController(self,dt):
    if self.active == False:
      self.enPin560State = self.GPIO.LOW
      self.enPin470State = self.GPIO.LOW
      self.enPin415State = self.GPIO.LOW
      self.updateIntensity()
      self.updateEnable()
  

  def invertLED(self):
    self.enPin560State = not self.enPin560State 
    self.enPin470State = not self.enPin470State
    self.enPin415State = not self.enPin415State

  def blinkController(self,dt):
    if self.active == False:
      pass
    elif self.mode == const.TRIG1 or self.mode == const.TRIG2:
      self.invertLED() 
      self.updateEnable()
      Clock.schedule_once(self.blinkController,1.0 / self.FPS)
 


   

class OnButton(ToggleButton):
  def press_power(self):
    if self.state == const.DOWN:
      self.controller.active = True
      self.controller.initMode()
      print (self.controller.active)
    else:
      self.controller.active = False
      print (self.controller.active)

class ModeButton(ToggleButton):
  def press_mode(self):
    self.state = const.DOWN
    assert self.mode in const.validMode
    assert self.controller.active == False
    if self.controller.mode != self.mode:
      self.controller.mode = self.mode
      print("Entering",self.controller.mode,"mode") 
  def __init__(self,mode=const.NULL,**kwargs):
    self.mode = mode 
    super(ModeButton,self).__init__(**kwargs)  


class SliderFPS(Slider):
  pass  


class DriverLayout(Widget):
  controller = Controller(GPIO)
  onButton = ObjectProperty(None)
  constButton = ObjectProperty(None)
  trig1Button = ObjectProperty(None)
  trig2Button = ObjectProperty(None)
  trig3Button = ObjectProperty(None)
  fpsSlider = ObjectProperty(None)
  slider560 = ObjectProperty(None)
  slider470 = ObjectProperty(None)
  slider415 = ObjectProperty(None)
     

  logo = ObjectProperty(None)

  def setClocks(self):
    Clock.schedule_interval(self.controller.modeController,1.0/60.0)


class DriverApp(App):
  def build(self):
    driverLayout = DriverLayout()
    driverLayout.setClocks()
    return driverLayout
    






if __name__ == '__main__':
  DriverApp().run()
  print('Exiting and cleaning GPIO')
  GPIO.cleanup()




