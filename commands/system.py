import os, platform, webbrowser, shutil

def register(bot):
    bot.register("sysinfo", sysinfo_cmd, "Show system information")
    bot.register("open", open_cmd, "Open a URL/file/app: open https://..., open README.md")
    bot.register("where", where_cmd, "Show current working directory")
    bot.register("ls", ls_cmd, "List files in current directory")
    # Safer: print the commands rather than execute shutdown/restart accidentally
    bot.register("shutdown", lambda _ : "Run manually: Windows: shutdown /s /t 0 | macOS: sudo shutdown -h now | Linux: sudo shutdown -h now", "Show shutdown command (safe)")
    bot.register("restart",  lambda _ : "Run manually: Windows: shutdown /r /t 0 | macOS: sudo shutdown -r now | Linux: sudo reboot", "Show restart command (safe)")

def sysinfo_cmd(_):
    return (
        f"OS: {platform.system()} {platform.release()}\n"
        f"Python: {platform.python_version()}\n"
        f"Machine: {platform.machine()}\n"
        f"Processor: {platform.processor()}\n"
        f"CWD: {os.getcwd()}"
    )

def open_cmd(user_input):
    target = user_input[len("open"):].strip()
    if not target:
        return "Usage: open <url/file/app>"
    # URL?
    if target.startswith(("http://", "https://")):
        webbrowser.open(target)
        return f"Opened URL: {target}"
    # File/app
    if os.path.exists(target):
        try:
            if os.name == "nt":
                os.startfile(target)  # type: ignore[attr-defined]
            elif sys_platform() == "Darwin":
                os.system(f"open '{target}'")
            else:
                os.system(f"xdg-open '{target}'")
            return f"Opened: {target}"
        except Exception as e:
            return f"Could not open: {e}"
    # Try launching from PATH
    exe = shutil.which(target)
    if exe:
        os.system(exe)
        return f"Launched: {exe}"
    return "Target not found as URL, file, or executable."

def where_cmd(_):
    return os.getcwd()

def ls_cmd(_):
    try:
        files = os.listdir(os.getcwd())
        return "\n".join(files) if files else "(empty)"
    except Exception as e:
        return f"Error: {e}"

def sys_platform():
    return platform.system()
