# Everyone knows passphrases. One can choose passphrases from poems, songs, movies names and so on but frequently
# they can be guessed due to common cultural references. You can get your passphrases stronger by different means.
# One is the following:
# choose a text in capital letters including or not digits and non alphabetic characters,
# shift each letter by a given number but the transformed letter must be a letter (circular shift),
# replace each digit by its complement to 9,
# keep such as non alphabetic and non digit characters,
# downcase each letter in odd position, upcase each letter in even position (the first character is in position 0),
# reverse the whole result.
# Example:
# your text: "BORN IN 2015!", shift 1
# 1 + 2 + 3 -> "CPSO JO 7984!"
# 4 "CpSo jO 7984!"
# 5 "!4897 Oj oSpC"
# With longer passphrases it's better to have a small and easy program. Would you write it?


import re


testData = "MY GRANMA CAME FROM NY ON THE 23RD OF APRIL 2015"


def play_pass(s, n):
    pattern = re.compile(r'[0-9]')
    newList = []
    testList = [s[i] for i in range(len(s))]

    for i in testList:
        if re.search(pattern, i):
            newList.append(i.replace(i, str(abs(int(i)-9))))
        elif ord(i) >= 65 and ord(i) <= 90: #space
            newOrd = ord(i) + n
            if newOrd > 90:
                newOrd = 64 + (newOrd - 90)
            newList.append(i.replace(i, chr(newOrd)))
        else:
            newList.append(i)

    for i in range(len(newList)):
        if i % 2 == 0:
            newList[i] = newList[i].upper()
        else:
            newList[i] = newList[i].lower()

    return ('').join(newList[::-1])


print(play_pass(testData, 2))