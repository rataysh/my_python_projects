import os, pyautogui, time, random, sys, pyglet, pyperclip, json

schetchik = 0
start_time = time.time()

gm_or_gn = "gn" #Изменить gm/gn
count_channel = 15 # количество каналов которые не помещаются на главном экране
start_coordinate_x = 36
start_coordinate_y = 114
range_to_next_channel = 57
directiry_gm_gn = (start_coordinate_x, start_coordinate_y) #Папка должна быть первой сверху


def scroll(count):
    pyautogui.scroll(-66 * count)


def end_gm_gn(count):
    pyautogui.scroll(1000 * count)
    start_coordinate_x = 36
    start_coordinate_y = 114
    directiry_gm_gn = (start_coordinate_x, start_coordinate_y)
    pyautogui.moveTo(directiry_gm_gn, duration=0.5)
    pyautogui.click(button='right')
    start_coordinate_x = 130
    start_coordinate_y = 211
    close_all_directory = (start_coordinate_x, start_coordinate_y)
    pyautogui.moveTo(close_all_directory, duration=0.5)
    pyautogui.click()


def write_gm():
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.write(gm_or_gn)
    time.sleep(0.1)
    pyautogui.press('enter')
    time.sleep(0.1)


time.sleep(2)
## MAIN SKRIPT
pyautogui.moveTo(directiry_gm_gn, duration=0.5)
pyautogui.click()
while schetchik < 15:
    start_coordinate_y += range_to_next_channel
    new_channel_coordinate = (start_coordinate_x, start_coordinate_y)
    pyautogui.moveTo(new_channel_coordinate, duration=0.3)
    write_gm()
    schetchik += 1
pyautogui.click()
scroll(count_channel)

time.sleep(1)
new_channel_coordinate = (start_coordinate_x, start_coordinate_y-(count_channel-2)*66)
pyautogui.moveTo(new_channel_coordinate, duration=1)

schetchik = 0
start_coordinate_x, start_coordinate_y = pyautogui.position()
while schetchik < count_channel:
    start_coordinate_y += range_to_next_channel
    new_channel_coordinate = (start_coordinate_x, start_coordinate_y)
    pyautogui.moveTo(new_channel_coordinate, duration=0.3)
    write_gm()
    schetchik += 1
time.sleep(1)
end_gm_gn(count_channel)

# ТЕСТ БЕЗ ОТПРАВКИ
# pyautogui.moveTo(directiry_gm_gn, duration=0.5)
# pyautogui.click()
# while schetchik < 15:
#     start_coordinate_y += range_to_next_channel
#     new_channel_coordinate = (start_coordinate_x, start_coordinate_y)
#     pyautogui.moveTo(new_channel_coordinate, duration=0.1)
#     time.sleep(0.1)
#     # pyautogui.click()
#     # pyautogui.write(gm_or_gn)
#     # pyautogui.press('enter')
#     # time.sleep(0.3)
#     schetchik += 1
# pyautogui.click()
# scroll(count_channel)
#
# time.sleep(1)
# new_channel_coordinate = (start_coordinate_x, start_coordinate_y-(count_channel-2)*66)
# pyautogui.moveTo(new_channel_coordinate, duration=1)
#
# schetchik = 0
# start_coordinate_x, start_coordinate_y = pyautogui.position()
# while schetchik < count_channel:
#     start_coordinate_y += range_to_next_channel
#     new_channel_coordinate = (start_coordinate_x, start_coordinate_y)
#     pyautogui.moveTo(new_channel_coordinate, duration=0.1)
#     time.sleep(0.1)
#     # pyautogui.click()
#     # pyautogui.write(gm_or_gn)
#     # pyautogui.press('enter')
#     # time.sleep(0.3)
#     schetchik += 1
# time.sleep(1)
# end_gm_gn(count_channel)
