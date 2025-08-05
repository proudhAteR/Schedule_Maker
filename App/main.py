from App.TerminalApp import TerminalApp

__instance = TerminalApp()
app = __instance.app

if __name__ == "__main__":
    __instance.run()
