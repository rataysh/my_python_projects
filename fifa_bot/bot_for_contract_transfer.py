import os, pyautogui, time, random, pyglet


start_time = time.time()
schetchik = 0
pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = True
searched_to_trade = r'screen\to_trade.png'
searched_sell = r'screen\searched_sell.png'
searched_buy_now = r'screen\player_price.PNG'
searched_start_price = r'screen\start_price.png'

time.sleep(2)
# looking_for_return = pyautogui.locateOnScreen(searched_return, confidence= 0.95)
try:
    while schetchik <= 80: #int(input(f'Введите количество лотов:\n')):
        looking_for_return = pyautogui.locateOnScreen(searched_to_trade, confidence= 0.90)
        if looking_for_return != None:
            pyautogui.moveTo(looking_for_return, duration=0.1)
            time.sleep(0.15)
            pyautogui.click()
            time.sleep(0.4)
            looking_for_buy_now = pyautogui.locateOnScreen(searched_buy_now, confidence= 0.90)
            if looking_for_buy_now != None:
                pyautogui.moveTo(searched_buy_now, duration=0.1)
                time.sleep(0.15)
                pyautogui.click()
                time.sleep(0.1)
                pyautogui.write('1400')
                time.sleep(0.1)
                looking_for_start_price = pyautogui.locateOnScreen(searched_start_price, confidence=0.90)
                if looking_for_start_price != None:
                    pyautogui.moveTo(looking_for_start_price, duration=0.1)
                    time.sleep(0.15)
                    pyautogui.click()
                    time.sleep(0.1)
                    pyautogui.write('900')
                    time.sleep(0.1)
                    looking_for_sell = pyautogui.locateOnScreen(searched_sell, confidence=0.95)
                    if looking_for_sell != None:
                        pyautogui.moveTo(looking_for_sell, duration=0.1)
                        time.sleep(0.15)
                        pyautogui.click()
                    else:
                        print(f'Не нашел кнопку "Выставить на продажу"')
                else:
                    print(f'Не нашел кнопку "Стартовая цена"')
            else:
                print(f'Не нашел кнопку "Купить сейчас"')
                time.sleep(1)
            schetchik += 1
        else:
            print(f'Не нашел кнопку "Выставить на тр-ый рынок"')
            schetchik += 1
            time.sleep(1)
except ValueError:
    print(f'Произошла ошибка через {finish_time-start_time} работы')
finally:
    finish_time = time.time()
    print(f'Скрипт работал {(finish_time - start_time)//60} минут {(finish_time - start_time)%60//1} секунд')
    print(f'Количество выставленных лотов: {schetchik}')
