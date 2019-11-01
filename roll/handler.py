from urllib import parse
import re
import random

NO_DICE_ERROR_MESSAGE = "To roll a dice specify please specify the number and type of dice to roll, i.e. `/roll 3d6`"
MULTIPLE_DICE_ERROR_MESSAGE = "We can only roll one type of dice per command!"
ROLL_RESULT_MESSAGE = "Rolling {number}d{type} result is {result}"

SHRUG_EMOJI = r"¯\_(ツ)_/¯"

dice_regex = re.compile(r"\d+\W*[d]\W*\d+") # TODO, this incorectly matches [1d201]d10 only in that string - should match both but cant work it out


def roll(dice):
    result = 0
    for x in range(dice[0]):
        result += random.randint(1, dice[1])

    return result


def handle(req):
    data = parse.parse_qs(req)
    try:
        dice = dice_regex.findall(data['text'][0])
        if len(dice) > 1:
            return MULTIPLE_DICE_ERROR_MESSAGE
        elif len(dice) < 1:
            return NO_DICE_ERROR_MESSAGE
        else:
            dice = [int(x) for x in dice[0].split('d')]
    except KeyError:
        return NO_DICE_ERROR_MESSAGE

    # dice should be List of [number, type]
    if 0 in dice:
        return ROLL_RESULT_MESSAGE.format(number=dice[0], type=dice[1], result=SHRUG_EMOJI)

    return ROLL_RESULT_MESSAGE.format(number=dice[0], type=dice[1], result=roll(dice))


if __name__ == "__main__":
    tests = {}

#TODO do a urlencode on the input on the test, rather than manually encode with %2F etc

    tests[''] = NO_DICE_ERROR_MESSAGE
    tests['{"command": ["aa"]}'] = NO_DICE_ERROR_MESSAGE
    tests['command=%2Froll'] = NO_DICE_ERROR_MESSAGE
    tests['command=%2Froll&text='] = NO_DICE_ERROR_MESSAGE
    tests['command=%2Froll&text= '] = NO_DICE_ERROR_MESSAGE
    tests['command=%2Froll&text= 20%20%20400'] = NO_DICE_ERROR_MESSAGE
    tests['command=%2Froll&text= 20%20dice%20400'] = NO_DICE_ERROR_MESSAGE
    tests['command=%2Froll&text=1d10%202d30'] = MULTIPLE_DICE_ERROR_MESSAGE

    tests['command=%2Froll&text=1d10'] = ROLL_RESULT_MESSAGE.format(number=1, type=10, result=8)
    tests['command=%2Froll&text=3 d\n20'] = ROLL_RESULT_MESSAGE.format(number=3, type=20, result=47)
    tests['command=%2Froll&text=10d10d30'] = ROLL_RESULT_MESSAGE.format(number=10, type=10, result=59) # SHOULD BE --> MULTIPLE_DICE_ERROR_MESSAGE see regex at top


    for x in tests.keys():
        # print(f"Input: '{x}'\nExpected: {tests[x]}\nReceived: {handle(x)}\n\n", flush=True)
        random.seed(9)
        try:
            f = handle(x)
            assert(f == tests[x])
        except AssertionError as E:
            raise Exception(f"Input:{x}\n {tests[x]} != {f}")


