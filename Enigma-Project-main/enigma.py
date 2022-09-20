# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by
# Wehrmacht and Luftwaffe, Nazi Germany.
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components, alpabat
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I": {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21
    }
}

# reflactor
UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
# SETTINGS = {
#     "UKW": None,
#     "WHEELS": [],
#     "WHEEL_POS": [],
#     "ETW": ETW,
#     "PLUGBOARD": []
# }

SETTINGS = {
    "UKW": UKW["C"],
    "WHEELS": [WHEELS["III"], WHEELS["I"], WHEELS["II"]],
    "WHEEL_POS": [0, 0, 0],
    "ETW": ETW,
    "PLUGBOARD": []
}


def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))

    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(
                f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)

# Enigma Logics Start

# Plugboard


def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input

# ETW


def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]

# Wheels


def pass_wheels(input, reverse=False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    if (reverse == False):
        # right wheel
        input_num = (ord(input) - ord('A') + SETTINGS["WHEEL_POS"][2]) % 26
        input = SETTINGS["WHEELS"][2]["wire"][input_num]

        # middle wheel
        input_num = (ord(input) - ord('A') -
                     SETTINGS["WHEEL_POS"][2] + SETTINGS["WHEEL_POS"][1])

        if (input_num < 0):
            input_num += 26
        else:
            input_num %= 26
        input = SETTINGS["WHEELS"][1]["wire"][input_num]

        # # left wheel
        input_num = ord(input) - ord('A') - \
            SETTINGS["WHEEL_POS"][1] + SETTINGS["WHEEL_POS"][0]

        if (input_num < 0):
            input_num += 26
        else:
            input_num %= 26

        input = SETTINGS["WHEELS"][0]["wire"][input_num]

    else:
        # wheel section
        for index in range(3):
            reverse_input_index = (
                ord(input) - ord('A') + SETTINGS["WHEEL_POS"][index]) % 26

            reverse_output_index = SETTINGS["WHEELS"][index]["wire"].find(
                chr(reverse_input_index + ord('A')))

            input = chr(reverse_output_index + ord('A'))

        # ETW section
        roter_I_index = ord(input) - ord('A') - SETTINGS["WHEEL_POS"][2]

        if (roter_I_index < 0):
            roter_I_index = 26 + roter_I_index

        input = chr(roter_I_index + ord('A'))

    return input

# UKW


def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]

# Wheel Rotation


def rotate_wheels():
    SETTINGS["WHEEL_POS"][2] = (SETTINGS["WHEEL_POS"][2] + 1) % 26
    SETTINGS["WHEELS"][2]["turn"] -= 1

    if SETTINGS["WHEELS"][2]["turn"] == 0:
        SETTINGS["WHEELS"][2]["turn"] = 26

        SETTINGS["WHEEL_POS"][1] += 1
        SETTINGS["WHEELS"][1]["turn"] -= 1

        if SETTINGS["WHEELS"][1]["turn"] == 0:
            SETTINGS["WHEELS"][1]["turn"] = 26

            SETTINGS["WHEEL_POS"][0] += 1
            SETTINGS["WHEELS"][0]["turn"] -= 1

            SETTINGS["WHEELS"][0]["turn"] %= 26

    # Implement Wheel Rotation Logics
    pass


# Enigma Exec Start
plaintext = input("Plaintext to Encode: ")
# ukw_select = input("Set Reflector (A, B, C): ")
# wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
# wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
# plugboard_setup = input("Plugboard Setup: ")

# apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse=True)
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='')
