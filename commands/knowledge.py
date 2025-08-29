import requests, urllib.parse
import wikipedia

def register(bot):
    bot.register("weather", weather_cmd, "Get weather (wttr.in): weather [city]")
    bot.register("wiki", wiki_cmd, "Wikipedia summary: wiki <topic>")
    bot.register("news", news_cmd, "Top tech news (HN front page)")

def weather_cmd(user_input):
    # Uses wttr.in (no API key). Format 3 = concise one-liner.
    parts = user_input.split(maxsplit=1)
    city = parts[1] if len(parts) > 1 else ""
    endpoint = "https://wttr.in/"
    url = endpoint + (urllib.parse.quote(city) if city else "")
    try:
        r = requests.get(url, params={"format": 3}, timeout=8)
        return "Weather: " + r.text.strip()
    except Exception:
        return "Unable to fetch weather right now."

def wiki_cmd(user_input):
    query = user_input[len("wiki"):].strip()
    if not query:
        return "Usage: wiki <topic>"
    try:
        wikipedia.set_lang("en")
        summary = wikipedia.summary(query, sentences=2, auto_suggest=True, redirect=True)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        opts = ", ".join(e.options[:5])
        return f"Topic is ambiguous. Did you mean: {opts} ..."
    except Exception:
        return "Couldn't fetch Wikipedia summary."

def news_cmd(_):
    # Hacker News front page via Algolia API
    try:
        r = requests.get("https://hn.algolia.com/api/v1/search?tags=front_page", timeout=8)
        hits = r.json().get("hits", [])[:10]
        if not hits:
            return "No news found."
        lines = []
        for i, h in enumerate(hits, 1):
            title = h.get("title") or h.get("story_title") or "Untitled"
            url = h.get("url") or h.get("story_url") or ""
            if url:
                lines.append(f"{i}. {title} — {url}")
            else:
                lines.append(f"{i}. {title}")
        return "\n".join(lines)
    except Exception:
        return "Unable to fetch news."
