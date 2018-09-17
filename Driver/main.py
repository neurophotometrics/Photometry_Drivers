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


"""
Initializing global parameters
"""
kivy.require('1.10.1') 


class Controller(Widget):
  active = BooleanProperty(False)     
  mode = StringProperty(const.NULL)
  def __init__(self,GPIO):
    self.GPIO = GPIO
    self.mode = const.CONST
    self.active = False
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(const.enPin560,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(const.enPin470,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(const.enPin415,GPIO.OUT,initial=GPIO.LOW)
      
  def updateEnable(self,state1,state2,state3):
    self.GPIO.output(const.enPin560,state1)
    self.GPIO.output(const.enPin470,state2)
    self.GPIO.output(const.enPin415,state3)
  
  def updateIntensity(self):
    pass 
   
  def updateGPIO(self):
    if self.mode == const.CONST:
      self.updateEnable(self.GPIO.HIGH,self.GPIO.HIGH,self.GPIO.HIGH) 
      self.updateIntensity()
    elif self.mode == const.TRIG1:
      self.updateEnable(self.GPIO.LOW,self.GPIO.LOW,self.GPIO.LOW) 
      self.updateIntensity()
    elif self.mode == const.TRIG2:
      self.updateEnable(self.GPIO.HIGH,self.GPIO.LOW,self.GPIO.HIGH) 
      self.updateIntensity()
    else:
      # illegal state
      assert False


class OnButton(ToggleButton):
  def press_power(self):
    if self.state == const.DOWN:
      self.controller.active = True
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

class DriverLayout(Widget):
  controller = Controller(GPIO)
  onButton = OnButton()
  constButton = ModeButton()
  trig1Button = ModeButton()
  trig2Button = ModeButton()
  trig3Button = ModeButton()
  logo = ObjectProperty(None)

  def update(self,dt):
    self.controller.updateGPIO()


class DriverApp(App):
  def build(self):
    driverLayout = DriverLayout()
    Clock.schedule_interval(driverLayout.update,1.0/60.0)  
    return driverLayout
    






if __name__ == '__main__':
  DriverApp().run()
  print('Exiting and cleaning GPIO')
  GPIO.cleanup()




