#!/usr/bin/env python3
"""
ANOMIE Advanced (v2.0) - Modular AI Assistant
Author: Azlan
"""

import json
import os
import importlib

CONFIG_FILE = "config.json"

class ANOMIE:
    def __init__(self):
        self.user_name = "User"
        self.commands = {}
        self.load_config()
        self.load_commands()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.user_name = data.get("user_name", "User")
        else:
            self.user_name = input("Enter your name: ").strip() or "User"
            with open(CONFIG_FILE, "w") as f:
                json.dump({"user_name": self.user_name}, f)

    def load_commands(self):
        modules = ["commands.core", "commands.fun", "commands.system", "commands.knowledge", "commands.personal"]
        for mod in modules:
            try:
                m = importlib.import_module(mod)
                if hasattr(m, "register"):
                    m.register(self)
            except Exception as e:
                print(f"Failed to load {mod}: {e}")

    def greet(self):
        print(f"Hello {self.user_name}, I'm ANOMIE. How can I assist you today?")

    def run(self):
        self.greet()
        while True:
            user_input = input("\n> ").strip().lower()
            if user_input in ["exit", "quit", "bye"]:
                print("Goodbye! Shutting down ANOMIE.")
                break
            handled = False
            for cmd, func in self.commands.items():
                if user_input.startswith(cmd):
                    response = func(user_input)
                    if response:
                        print(response)
                    handled = True
                    break
            if not handled:
                print(f"Sorry {self.user_name}, I don’t understand '{user_input}'.")

if __name__ == "__main__":
    ANOMIE().run()
