"""
TS-DET1
micro:bit toy synth with 5x5 keypad and detuning.
Works best in combination with a power amplifier and a low-pass filter.

Find out more:
https://turiscandurra.com/circuits
"""
from microbit import pin1, pin2, pin8, pin9, pin10
from microbit import pin12, pin13, pin14, pin15, pin16
from microbit import display, Image, accelerometer
import music

# Frequency of musical notes, in Hz
# From https://en.wikipedia.org/wiki/Scientific_pitch_notation
# Please note that micro:bit's music.pitch() processes int and not float,
# so these values will be approximated even more.
frequencies = [
    261.63, 277.18, 293.66, 311.13, 329.63,
    349.23, 369.99, 392.00, 415.30, 440.00,
    466.16, 493.88, 523.25, 554.37, 587.33,
    622.25, 659.26, 698.46, 739.99, 783.99,
    830.61, 880.00, 932.33, 987.77, 1046.50
]

# Define here the pins of the keypad matrix
row_pins = [pin1, pin8, pin9, pin10, pin12]
col_pins = [pin2, pin13, pin14, pin15, pin16]

# Animation frames
star0 = Image("00000:"
              "00000:"
              "00300:"
              "00000:"
              "00000")

star1 = Image("00000:"
              "00200:"
              "02920:"
              "00200:"
              "00000")

star2 = Image("00000:"
              "00500:"
              "05050:"
              "00500:"
              "00000")

star3 = Image("00500:"
              "05550:"
              "55055:"
              "00500:"
              "00500")

star4 = Image("05550:"
              "50005:"
              "50005:"
              "50005:"
              "05550")

star5 = Image("50005:"
              "00000:"
              "00000:"
              "00000:"
              "50005")

# Pitch display
line0 = Image("90000:"
              "90000:"
              "90000:"
              "90000:"
              "90000")

line1 = Image("09000:"
              "09000:"
              "09000:"
              "09000:"
              "09000")

line2 = Image("00900:"
              "00900:"
              "00900:"
              "00900:"
              "00900")

line3 = Image("00090:"
              "00090:"
              "00090:"
              "00090:"
              "00090")

line4 = Image("00009:"
              "00009:"
              "00009:"
              "00009:"
              "00009")

stars = [star0, star1, star2, star3, star4, star5]


# Routine to scan the keypad matrix and return the first key found.
# The display must be switched on and off as we're using pins
# that are also connected to the display. This causes flickering.
def scan_keypad():
    display.off()
    key_code = -1
    for row, row_pin in enumerate(row_pins):
        row_pin.write_digital(1)
        for col, col_pin in enumerate(col_pins):
            if col_pin.read_digital():
                key_code = row*len(col_pins)+col
                break
        row_pin.write_digital(0)
    display.on()
    return key_code


def detune(pitch, amount):
    """
    Detune a given pitch by a specified amount.

    :param pitch: float
    :param amount: int
    :return: float
    """
    factor = float(-1) + (float(amount + 1023) / float(2046)) * float(2)
    semitone = pitch * float(0.06)
    return pitch + semitone * float(factor)


def update_display(x):
    if(x < -614):
        display.show(line0)
    elif(x < -205):
        display.show(line1)
    elif(x < 205):
        display.show(line2)
    elif(x < 614):
        display.show(line3)
    else:
        display.show(line4)


def io_loop():
    x = accelerometer.get_x()
    update_display(x)
    key = scan_keypad()
    if (key is not -1):
        note = frequencies[key]
        freq = detune(note, x)
        music.pitch(int(freq))
    else:
        # No keys are being pressed
        music.stop()

# Intro animation
display.show(stars, delay=200)

while True:
    io_loop()