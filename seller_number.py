import pyautogui
import time
import pyperclip
import cv2
import pytesseract
import re
import logging
from PIL import Image

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
        
        #############################,######################
        self.mObj.click(1250,650)
        number_text = self.mObj.copy_clipboard()
        
        if(number_text.isnumeric()):
            print(number_text)

            return (number_text)
            
            
        
            
        ####################################################
        self.mObj.click(1250,580)
        number_text = self.mObj.copy_clipboard()

        
        if(number_text.isnumeric()):
            
            print(number_text)
            return (number_text)
        
        
    def number_from_image(self):
        time.sleep(1)
        myScreenshot = pyautogui.screenshot(region=(1200,450, 300, 400))
        myScreenshot.save(r'file.png')
        
        
        #rgb to gray scale
        time.sleep(1)
        print('screenshot done!')
        img = Image.open('file.png').convert('LA')
        img.save('file.png')
#         img.show('file.png')
        time.sleep(1)
        
        self.text = (pytesseract.image_to_string(Image.open("file.png")))
        
        with open('text.txt', 'a') as filehandle:                        
            filehandle.write('%s\n' % self.text)
         
        temp = re.findall("\+?\d.*\d", self.text)
        
        for i in  temp:
            if '.' in i or len(i) < 6:
                temp.remove(i)
            
            
        return str(temp[0])
    


    def broswer_open(self,url=' '):
        import webbrowser

        chrome_path = '/usr/bin/google-chrome %s'

        webbrowser.get(chrome_path).open(url)

        
    def next_tab(self,url=''):
        webbrowser.open(url)
      

        
class main:
    def __init__(self):
        self.seller_list = []
        
    def run(self):
        mObj = automate()
        
        with open('list_product_link.txt', 'r') as filehandle:
            for line in filehandle:
                # remove linebreak which is the last character of the string

                line = line.split('\n')[0]
                
                mObj.broswer_open(line)
                time.sleep(2)
                number = mObj.number_from_image()
                
                pyautogui.hotkey('ctrl', 'w')
                
                if number != []:
                
                    temp = []
                    temp.append(line)
                    temp.append(number)

                    with open('url_number.txt', 'a') as filehandle:                        
                        temp = line + ',' + number
                        filehandle.write('%s\n' % temp)
                        
                

            
obj = main()
obj.run()


