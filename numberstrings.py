

raw_strings = { 0 : "oh",
                1 : "one",
                2 : "two",
                3 : "three",
                4 : "four",
                5 : "five",
                6 : "six",
                7 : "seven",
                8 : "eight",
                9 : "nine",
                10 : "ten",
                11 : "eleven",
                12 : "twelve",
                13 : "thirteen",
                14 : "fourteen",
                15 : "fifteen",
                16 : "sixteen",
                17 : "seventeen",
                18 : "eighteen",
                19 : "nineteen",
                20 : "twenty",
                30 : "thirty",
                40 : "fourty",
                50 : "fifty",
                60 : "sixty",
                70 : "seventy",
                80 : "eighty",
                90 : "ninety",

   }

clock_cardinals={  0 : "O'Clock",
                 15 : "quarter past",
                 30 : "half past",
                 45 : "quarter to"}

def number_to_text(integer):
    units = integer % 10
    tens = int((integer - units))
    if units != 0:
        unit_word = raw_strings.get(units)
    else:
        unit_word = ""
    if tens != 0:
        tens_word = raw_strings.get(tens)
        if unit_word != "":
            unit_word = "-" + unit_word
    else:
        tens_word = ""
    if 9 >= integer >= 0:
        number_word="{u}".format(u=unit_word)
    elif 20 > integer > 9:
        number_word = raw_strings.get(integer)
    else:
        number_word="{t}{u}".format(u=unit_word, t=tens_word)
    if integer == 0 :
        number_word = raw_strings.get(integer)
    return number_word.strip()
