import os, pyautogui, time, random, sys, pyglet


start_time = time.time()
schetchik = 0
pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
searched_return = 'screen\\searched_return.png'
searched_sell = 'screen\\searched_sell.png'

time.sleep(2)
looking_for_return = pyautogui.locateOnScreen(searched_return, confidence= 0.95)
try:
    while schetchik <= 100: #int(input(f'Введите количество лотов:\n')):
        looking_for_return = pyautogui.locateOnScreen(searched_return)
        if looking_for_return != None:
            pyautogui.moveTo(searched_return, duration=0.05)
            time.sleep(0.05)
            pyautogui.click()
            time.sleep(0.05)
            looking_for_sell = pyautogui.locateOnScreen(searched_sell, confidence= 0.95)
            if looking_for_sell != None:
                pyautogui.moveTo(searched_sell, duration=0.05)
                time.sleep(0.05)
                pyautogui.click()
                time.sleep(0.05)
            else:
                time.sleep(0.1)
            schetchik += 1
        else:
            time.sleep(0.3)
except ValueError:
    print(f'Произошла ошибка через {finish_time-start_time} работы')
finally:
    finish_time = time.time()
    print(f'Скрипт работал {(finish_time - start_time)//60} минут {(finish_time - start_time)%60//1} секунд')
    print(f'Количество выставленных лотов: {schetchik}')
