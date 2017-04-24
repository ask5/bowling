
def strike(pins):
    if pins == "10" or pins.lower() == "x":
        return True
    else:
        return False


def spare(first_roll_pins, second_roll_pins):
    if second_roll_pins == "/":
        return True
    elif int(first_roll_pins) + int(second_roll_pins) == 10:
        return True
    else:
        return False
