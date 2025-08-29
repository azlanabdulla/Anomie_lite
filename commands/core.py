import datetime, math, webbrowser, urllib.parse

def register(bot):
    bot.register("time", time_cmd, "Show current time")
    bot.register("date", date_cmd, "Show current date")
    bot.register("calc", calc_cmd, "Calculate: calc 2+2, calc sqrt(16)")
    bot.register("search", search_cmd, "Open a Google search: search your query")
    # inline help uses bot.helps from main; nothing else to do

def time_cmd(_):
    return datetime.datetime.now().strftime("The current time is %H:%M:%S.")

def date_cmd(_):
    return datetime.datetime.now().strftime("Today's date is %Y-%m-%d.")

def calc_cmd(user_input):
    expr = user_input[len("calc"):].strip()
    if not expr:
        return "Usage: calc <expression>   e.g., calc 2+2 or calc sqrt(81)"
    expr = expr.replace("^", "**")
    try:
        result = eval(expr, {"__builtins__": None}, math.__dict__)
        return f"Answer: {result}"
    except Exception:
        return "Sorry, I couldn't evaluate that expression."

def search_cmd(user_input):
    q = user_input[len("search"):].strip()
    if not q:
        return "Usage: search <query>"
    url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(q)
    webbrowser.open(url)
    return f"I've searched Google for '{q}'."
