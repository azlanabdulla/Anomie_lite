import random

def register(bot):
    bot.commands["joke"] = joke
    bot.commands["story"] = story
    bot.commands["quote"] = quote
    bot.commands["flip"] = coin_flip
    bot.commands["roll"] = dice_roll

def joke(_):
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "Parallel lines have so much in common. Too bad they’ll never meet.",
    ]
    return random.choice(jokes)

def story(_):
    return "Once upon a time, a coder built an AI named ANOMIE that grew smarter every day."

def quote(_):
    quotes = [
        "Dream big. Start small. Act now.",
        "Simplicity is the ultimate sophistication.",
        "Stay hungry, stay foolish."
    ]
    return random.choice(quotes)

def coin_flip(_):
    return "Heads" if random.choice([True, False]) else "Tails"

def dice_roll(_):
    return f"🎲 You rolled a {random.randint(1,6)}"
