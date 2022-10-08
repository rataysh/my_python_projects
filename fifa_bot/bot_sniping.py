import os, pyautogui, time, random, sys, pyglet


start_time = time.time()
t_end = time.time() + 60 * 60 * 3
schetchik_if = 0
schetchik_else = 0
sound_uved = pyglet.media.load(r'screen\uved.mp3', streaming=False)

# Программа для определения координат на экране
# print('Press Ctrl-C to quit.')
# try:
#     while True:
#         x, y = pyautogui.position()
#         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
#         print(positionStr, end='')
#         print('\b' * len(positionStr), end='', flush=True)
# except KeyboardInterrupt:
#     print('\n')


# pyautogui.PAUSE = 0.8
pyautogui.FAILSAFE = True
searched_example = r'screen\searched_example.png'
go_to_transfer = r'screen\go_to_transfer.PNG'
try:
    while time.time() < t_end:
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.moveTo(random.randint(1030, 1594), random.randint(939, 962), duration=random.uniform(0.2, 0.4))
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.click()
        time.sleep(random.uniform(0.3, 0.4))
        # Условие при котором распознается текст, и если отвечает условия то:
        # # im = pyautogui.screenshot(region=(840, 450, 340, 340))
        # # im.save("searched_example.png")
        looking_for = pyautogui.locateOnScreen(searched_example, confidence= 0.9)
        time.sleep(random.uniform(0.2, 0.3))
        if looking_for == None:
            pyautogui.moveTo(random.randint(1293, 1583), random.randint(695, 715), duration=0.1)
            time.sleep(0.1)
            pyautogui.click()
            time.sleep(0.05)
            pyautogui.press('enter')
            time.sleep(random.uniform(0.8, 1))
            ### Отправляем в список продаж
            looking_for = pyautogui.locateOnScreen(go_to_transfer, confidence=0.9)
            if looking_for == None:
                ### Возращаемся к фильтрам
                pyautogui.moveTo(random.randint(121, 138), random.randint(142, 160), duration=random.uniform(0.2, 0.5))
                time.sleep(random.uniform(0.2, 0.4))
            else:
                sound_uved.play()
                time.sleep(random.uniform(0.05, 0.1))
                result_screen = pyautogui.screenshot(
                    'resutl_screen\\try_nomber' + str(
                        schetchik_if) + '.png')
                pyautogui.moveTo(go_to_transfer, duration=0.1)
                time.sleep(0.1)
                pyautogui.click()

            ### Возращаемся к фильтрам
            pyautogui.moveTo(random.randint(121, 138), random.randint(142, 160), duration=random.uniform(0.2, 0.5))
            time.sleep(random.uniform(0.2, 0.4))
            pyautogui.click()
            schetchik_if += 1
            print(f'Количество удачных попыток на данный момент: {schetchik_if}')
        else:
            time.sleep(1)
            pyautogui.moveTo(random.randint(121, 138), random.randint(142, 160), duration=random.uniform(0.2, 0.3))
            time.sleep(0.2)
            pyautogui.click()
            schetchik_else += 1
except ValueError:
    finish_time = time.time()
    print(f'Произошла ошибка через {finish_time-start_time} работы')
finally:
    finish_time = time.time()
    print(f'Скрипт работал {(finish_time - start_time)//60} минут {(finish_time - start_time)%60//1} секунд')
    print(f'Количество удачных попыток всего: {schetchik_if}')
    print(f'Количество неудачных попыток всего: {schetchik_else}')





