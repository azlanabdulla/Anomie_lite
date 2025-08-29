#!/usr/bin/env python3
"""
ANOMIE Advanced (v2.0) - Modular CLI Assistant
Author: Azlan
"""
import json, os, importlib

CONFIG_FILE = "config.json"

class ANOMIE:
    def __init__(self):
        self.user_name = "User"
        self.commands = {}        # "keyword": callable(user_input) -> str
        self.helps = {}           # "keyword": "help text"
        self.ensure_data_dir()
        self.load_config()
        self.load_commands()

    def ensure_data_dir(self):
        os.makedirs("data", exist_ok=True)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                self.user_name = json.load(f).get("user_name", "User")
        else:
            self.user_name = input("Enter your name: ").strip() or "User"
            with open(CONFIG_FILE, "w") as f:
                json.dump({"user_name": self.user_name}, f, indent=2)

    def register(self, keyword, func, help_text=""):
        self.commands[keyword] = func
        if help_text:
            self.helps[keyword] = help_text

    def load_commands(self):
        modules = [
            "commands.core",
            "commands.fun",
            "commands.system",
            "commands.knowledge",
            "commands.personal",
        ]
        for mod in modules:
            try:
                m = importlib.import_module(mod)
                if hasattr(m, "register"):
                    m.register(self)
            except Exception as e:
                print(f"[!] Failed to load {mod}: {e}")

    def greet(self):
        print(f"Hello {self.user_name}, I'm ANOMIE. How can I assist you today? (type 'help')")

    def show_help(self):
        print("\nAvailable commands:")
        for k in sorted(self.helps):
            print(f"  {k:<15} - {self.helps[k]}")
        print("  exit/quit/bye - Exit ANOMIE")

    def run(self):
        self.greet()
        while True:
            user_input = input("\n> ").strip()
            low = user_input.lower()
            if low in ["exit", "quit", "bye"]:
                print("Goodbye! Shutting down ANOMIE.")
                break
            if low == "help":
                self.show_help()
                continue

            handled = False
            for cmd, func in self.commands.items():
                if low.startswith(cmd):
                    try:
                        out = func(user_input)  # pass raw input so modules can parse args
                        if out:
                            print(out)
                    except Exception as e:
                        print(f"[!] Error in '{cmd}': {e}")
                    handled = True
                    break

            if not handled:
                print(f"Sorry {self.user_name}, I don’t understand '{user_input}'. Type 'help'.")

if __name__ == "__main__":
    ANOMIE().run()
