# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 11:39:12 2019

@author: Protik
"""

from selenium import webdriver
#from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
#from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import shutil
import time
from time import time as sec
import numpy as np
from selenium.webdriver.chrome.options import Options
chrome_options = Options()

prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
chrome_options.add_experimental_option("prefs", prefs)
"""from selenium.webdriver.common.desired_capabilities import DesiredCapabilities    
capabilities = DesiredCapabilities.CHROME
capabilities['loggingPrefs'] = {'browser': 'ALL'}
"""
#(executable_path='C:\\Users\\Protik\\Desktop\\WebScrap\\driverdriver.exe')
#(executable_path=os.path.abspath("driverdriver.exe"))

def log_in(driver, id_, pass_, url):
       driver.get(url = url)
       
       id_bt = driver.find_element_by_id("username")
       id_bt.send_keys(id_)
       
       pass_bt = driver.find_element_by_id("password")
       pass_bt.send_keys(pass_)
       
       sub_bt = driver.find_element_by_id("Login_btn")
       sub_bt.click()
       
       return driver

#time.sleep(2)

def ClientMaster(driver):
       client_bt = driver.find_element_by_id("ClientMasterHead")
       client_bt.click()

       driver_New_Win = driver.window_handles[1]
       driver.switch_to.window(driver_New_Win)
       
       return driver

#Loop
#dnd = []
def Download_PDF(driver, data):
       skipped = []
       #file_list = []
       time.sleep(1)
       for CodeTxt_ in tqdm(data):
              if str(CodeTxt_) == "NAN":
                     continue
              try:
                     ex = True
                     check = sec()
                     time_es = sec()-check
                     while ex and time_es < 5:
                            try:
                                   CodeTxt = driver.find_element_by_id("clientCodeTxt")
                                   CodeTxt.clear()
                                   CodeTxt.send_keys(str(CodeTxt_))
                                   ex = False
                            except:
                                   time_es = sec()-check
                                   time.sleep(.2)
                     if time_es >= 5:
                            u = 1/0
                            
              except:
                     skipped.append((CodeTxt_, "code"))
                     driver.quit()
                     driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"), options=chrome_options)#, desired_capabilities=capabilities)
              
                     driver = log_in(driver, id_, pass_, url)
              
                     time.sleep(2)
              
                     driver = ClientMaster(driver)
                     print(CodeTxt_, "code")
                     continue
              
              try:
                     ex = True
                     check = sec()
                     time_es = sec()-check
                     while ex and time_es < 5:
                            try:
                                   viewClient = driver.find_element_by_id("viewClientDetails")
                                   viewClient.click()
                                   ex = False
                            except:
                                   time_es = sec()-check
                                   time.sleep(.2)
                     if time_es >= 5:
                            u = 1/0
              except:
                     driver.refresh()
                     skipped.append((CodeTxt_, "view"))
                     print(CodeTxt_, "view")
                     continue
                     
              
              

              try:
                     ex = True
                     check = sec()
                     time_es = sec()-check
                     while ex and time_es < 5:
                            try:
                                   download_pdf = driver.find_element_by_id("pdfLink")
                                   download_pdf.click()
                                   ex = False
                            except:
                                   time_es = sec()-check
                                   time.sleep(.2)
                     if time_es >= 5:
                            u = 1/0
              except:
                     try:
                            confirm_bt = driver.find_element_by_class_name("confirm")
                            confirm_bt.click()
                            
                            time.sleep(2)
                            
                            download_pdf = driver.find_element_by_id("pdfLink")
                            download_pdf.click()
                            
                     except:
                            driver.refresh()
                            skipped.append((CodeTxt_, "down"))
                            print(CodeTxt_, "down")
                            continue
              
              time.sleep(1)
              """ext = cr_ext
              while ext != ".pdf":
                     f_name, ext = os.path.splitext(max([dn_loc + "\\" + f for f in os.listdir(dn_loc)],key=os.path.getctime))
                     filename = f_name + ext
                     time.sleep(.2)
                     
              try:
                     new_pdf = CodeTxt_ + ".pdf"
                     shutil.move(filename,os.path.join(dn_loc, new_pdf))
              except:       
                     skipped.append((CodeTxt_, "rename"))"""
                     
              
       return driver, skipped
              
def chunks(data, c_size):
    for i in range(0, len(data), c_size):
        yield np.array(data[i:i + c_size])


"""      
for i in range(len(itr)):
       new_pdf = itr[i] + ".pdf"
       shutil.move(file_list[i],os.path.join(dn_loc, new_pdf))
    """   
       #page.append(chrome.page_source)
#chrome.close()
#sweet-alert showSweetAlert visible
       
if __name__ == "__main__":
              
       dn_loc = "C:/Users/Protik/Downloads"
       f_loc = "C:/Users/Protik/Desktop/WebScrap/"
       
       test = "****"
       Sheet = "****"
       
       cr_ext = ".crdownload"
       
       data = pd.read_csv(f_loc + Sheet)
       
       final = list(data[data.columns[0]])
       
       final = list(set(final))
       
       url = "****"
       id_ = "****"
       pass_ = "****"
       
       fn_len = int(len(final)/50)
       fn_curr = 1
       #chrome = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"), desired_capabilities=capabilities)
       
       skipped = []
       
       for chunk in chunks(final, 50):
              
              check = sec()
              chrome = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"), options=chrome_options)#, desired_capabilities=capabilities)
              
              chrome = log_in(chrome, id_, pass_, url)
              
              time.sleep(2)
              
              chrome = ClientMaster(chrome)
              
              chrome, t_skip = Download_PDF(chrome, chunk)
              
              print(len(t_skip), "/ 50 Skipped.....")
              time_es = sec()-check
              print("Chunk No : ", fn_curr, "/", fn_len)
              print("Time : ", int(time_es*fn_curr), "/", int(time_es*fn_len))
              fn_curr += 1
              
              time.sleep(3)
              
              skipped.extend(t_skip)

              chrome.quit()
              
       print("Download - Done")
       time.sleep(1)
       print("Saving Files.....")
       save = open("****", "w")
       for i in tqdm(final):
              save.write(i + "\n")
       save.close()
       time.sleep(1)
       print("Saving Skipped Files.....")
       skip = open("****", "w")
       for i in tqdm(skipped):
              skip.write(i[0]+","+ i[1]+ "\n")
       skip.close()
              
              
