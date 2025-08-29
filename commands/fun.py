import random

JOKES = [
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "I told my computer I needed a break, and it said 'No problem — I’ll go to sleep.'",
]
STORIES = [
    "Once upon a time, a coder built ANOMIE — a tiny assistant with giant potential.",
    "In a quiet lab, a script gained a voice and became a friend.",
]
QUOTES = [
    "Dream big. Start small. Act now.",
    "Simplicity is the ultimate sophistication.",
    "Stay hungry, stay foolish.",
]

def register(bot):
    bot.register("joke", lambda _ : random.choice(JOKES), "Tell a joke")
    bot.register("story", lambda _ : random.choice(STORIES), "Tell a short story")
    bot.register("quote", lambda _ : random.choice(QUOTES), "Random motivational quote")
    bot.register("flip", flip_cmd, "Coin flip (Heads/Tails)")
    bot.register("roll", roll_cmd, "Roll a dice (1–6)")
    bot.register("password", password_cmd, "Generate random password: password 16")

def flip_cmd(_):
    return "Heads" if random.choice([True, False]) else "Tails"

def roll_cmd(_):
    return f"🎲 You rolled a {random.randint(1,6)}"

def password_cmd(user_input):
    import string
    parts = user_input.split()
    length = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 12
    pool = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(pool) for _ in range(length))
