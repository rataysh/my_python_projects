import os, pyautogui, time, random, sys, pyglet


start_time = time.time()
schetchik = 0
# schetchik_funk = 0
pyautogui.PAUSE = 0.05
pyautogui.FAILSAFE = True
searched_list_down = r'screen\list_down.png'
searched_free_bet_min = r'screen\free_bet_min.png'
searched_chek_min_bet = r'screen\chek_min_bet.png'
searched_go_to_bet = r'screen\go_to_bet.png'
searched_next_page = r'screen\next_page.png'

time.sleep(2)
# looking_for_list_down = pyautogui.locateOnScreen(searched_list_down, confidence= 0.9)
# pyautogui.moveTo(looking_for_list_down, duration=0.5)
# time.sleep(0.15)
# pyautogui.click()


# def get_bet():
    # pyautogui.moveTo(searched_free_bet_min, duration=0.3)
    # time.sleep(0.1)
    # pyautogui.click()
    # time.sleep(0.3)
    # looking_for_chek_min_bet = pyautogui.locateOnScreen(searched_chek_min_bet, confidence=0.95)
    # if looking_for_chek_min_bet != None:
    #     looking_for_searched_go_to_bet = pyautogui.locateOnScreen(searched_go_to_bet, confidence=0.95)
    #     if looking_for_searched_go_to_bet != None:
    #         pyautogui.moveTo(looking_for_searched_go_to_bet, duration=0.2)
    #         time.sleep(0.1)
    #         pyautogui.click()
    #         schetchik += 1
    #     else:
    #         print(f'Не нашел кнопку "Сделать ставку"')
    # else:
    #     print(f'Не нашел кнопку "Ставку повысили"')
    #     time.sleep(1)


def page_down():
    looking_for_list_down = pyautogui.locateOnScreen(searched_list_down, confidence=0.95)
    pyautogui.moveTo(looking_for_list_down, duration=0.3)
    time.sleep(0.1)
    pyautogui.click()





try:
    while schetchik <= 100: #int(input(f'Введите количество лотов:\n')):
        looking_for_free_bet_min = pyautogui.locateOnScreen(searched_free_bet_min, confidence=0.95)
        if looking_for_free_bet_min != None:
            pyautogui.moveTo(looking_for_free_bet_min, duration=0.3)
            time.sleep(0.1)
            pyautogui.click()
            time.sleep(0.2)
            looking_for_searched_go_to_bet = pyautogui.locateOnScreen(searched_go_to_bet, confidence=0.95)
            if looking_for_searched_go_to_bet != None:
                pyautogui.moveTo(looking_for_searched_go_to_bet, duration=0.2)
                time.sleep(0.1)
                looking_for_chek_min_bet = pyautogui.locateOnScreen(searched_chek_min_bet, confidence=0.99)
                if looking_for_chek_min_bet != None:
                    pyautogui.click()
                    schetchik += 1
                else:
                    print(f'Ставку повысили')
                    time.sleep(1)
            else:
                print(f'Не нашел кнопку "Сделать ставку"')
        else:
            print("error")
            # for i in range(2):
            #     page_down()
            #     bet_to_contract()
            # looking_for_next_page = pyautogui.locateOnScreen(searched_next_page, confidence=0.95)
            # pyautogui.moveTo(looking_for_next_page, duration=0.3)
            # time.sleep(0.1)
            # pyautogui.click()
            schetchik += 1
except ValueError:
    print(f'Произошла ошибка через {finish_time-start_time} работы')
finally:
    finish_time = time.time()
    print(f'Скрипт работал {(finish_time - start_time)//60} минут {(finish_time - start_time)%60//1} секунд')
    print(f'Количество: {schetchik}')
