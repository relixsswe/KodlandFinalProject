import random

def gen_pass(pass_length=10):
    elements = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    password = ""
    for i in range(pass_length):
        password += random.choice(elements)
    return password

def gen_emodji():
    emodjis = ["😊", "😂", "😎", "🦊", "🚀", "🐱", "🐶", "🍕"]
    return random.choice(emodjis)

def flip_coin():
    return random.choice(["Орел 🪙", "Решка 🪙"])

def gen_guess():
    return random.randint(1, 10)
