#!/usr/bin/env python
# coding: utf-8

# In[124]:


import pyautogui
import time
import pyperclip
class mouse:

    def __init__(self):
        self.screenWidth, self.screenHeight = pyautogui.size()
    
    def __str__(self):
        return 'screen width: {}px screen height {}px '.format(self.screenWidth, self.screenHeight)
    
    def copy_clipboard(self):
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(.01)  # ctrl-c is usually very fast but your program may execute faster
        return pyperclip.paste()
    
    
    
    def click(self,x_axis,y_axis):
        pyperclip.copy('')
        time.sleep(2)
        pyautogui.click(x_axis, y_axis)
        pyautogui.click(x_axis, y_axis)
#         time.sleep(0.5)
#         pyautogui.click(x_axis, y_axis)
        
    def go_to_serach_bar(self,x_axis,y_axis):
        time.sleep(2)
        pyautogui.click(x_axis, y_axis)
        pyautogui.click(x_axis, y_axis)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pyperclip.copy('The text to be copied to the clipboard.')
        print(pyperclip.paste())

        

        
class automate:
    
    def __init__(self):
        self.mObj = mouse()
        
    def number_automate(self):
        
        ####################################################
        self.mObj.click(1250,750)
        number_text = self.mObj.copy_clipboard()

        
        if(number_text.isnumeric()):
            print(number_text)

            return (number_text)
        
        ###################################################
        self.mObj.click(1250,650)
        number_text = self.mObj.copy_clipboard()
        
        if(number_text.isnumeric()):
            print(number_text)

            return (number_text)
            
            
        
            
        ####################################################
        self.mObj.click(1250,580)
        number_text = self.mObj.copy_clipboard()
015152560965
        
        if(number_text.isnumeric()):
            
            print(number_text)
            return (number_text)
        
        
    def number_from_image(self):
        time.sleep(2)
        myScreenshot = pyautogui.screenshot(region=(1150,450, 300, 400))
        myScreenshot.save(r'file.png')
        time.sleep(2)
        
        self.text = (pytesseract.image_to_string(Image.open("file.png")))
        self.res = [(i) for i in self.text.split() if i.isdigit() and len(i)>10]
        return self.res
    


# In[125]:


mObj = automate()
# mObj.click(1250,650)
mObj.number_from_image()

# print(mObj.copy_clipboard())


# In[123]:


autoObj = automate()
autoObj.number_automate()


# In[1]:


get_ipython().system('pip install pytesseract')
get_ipython().system('pip install opencv-python')


# In[47]:


import cv2
import pytesseract
import re
from PIL import Image

class scraper:
    
    def number_from_image(self,image):
        time.sleep(2)
        myScreenshot = pyautogui.screenshot(region=(1200,400, 300, 500))
        myScreenshot.save(r'file name.png')

        
        self.text = (pytesseract.image_to_string(Image.open("file name.png")))
        self.res = [(i) for i in self.text.split() if i.isdigit() and len(i)>10]
        return self.res
    
    


# In[48]:


objScraper = scraper()

objScraper.number_from_image('test2.png')
# objScraper.take_image()


# In[99]:


pyautogui.screenshot(region=(0,0, 300, 400))


# In[ ]:




