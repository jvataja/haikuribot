import json
import re

vo = ['a','e','i','o','u','y','ä','ö',]
ko_l = ['b', 'c', 'f', 'g', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'z']
ko_s = ['w','h','j','v','d','q', 'x']
ko = ko_l + ko_s
dif = ['yi', 'ui', 'oi', 'öi', 'ai', 'äi', 'ay', 'äy', 'au', 'yo', 'yö', 'oy', 'öy', 'uo', 'ou', 'ie', 'ei', 'eu', 'iu', 'ey', 'iy',]

# %% func
def tallenna(s):
    if any(char.isdigit() for char in s):
        return
    s = s.lower()
    s = re.sub(r'[^\w\s]','',s)
    s = re.split('\s+', s)
    syl_cnt = 0; word_cnt = 0
    for word in s:
        if all(char in ko for char in word):
            return
        syls = re.split(r'(?:' + '|'.join(ko) + r')', word)
        syls = list2 = [x for x in syls if x]
        for syl in syls:
            if len(syl) == 1:
                syl_cnt += 1
            elif len(syl) == 2:
                if syl in dif or syl[0] == syl[1]:
                    syl_cnt += 1
                else:
                    syl_cnt += 2
            else:
                return
        word_cnt += 1
        if syl_cnt == 5:
            print("valid")
            with open("5.csv", "a") as f:
                f.write(" ".join(s[:word_cnt]) + "\n")
        if syl_cnt == 7:
            print("valid")
            with open("7.csv", "a") as f:
                f.write(" ".join(s[:word_cnt]) + "\n")
                return
        if syl_cnt > 7:
            return

def main():

    # %% load data
    with open("result3.json", "r") as f:
        data = json.load(f)
        #pk = data['chats']['list'][0]['messages']
        pk = data['messages']
        for el in pk:
            text = el['text']
            if isinstance(text, str):
                tallenna(text)
