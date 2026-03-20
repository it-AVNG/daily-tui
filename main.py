from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

class StopWatchApp(App):
    """Textual app for a stop watch"""
    
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """"create child widget for the app"""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """Action to switch to dark mode"""

        self.theme = ( "textual-dark" if self.theme == "textual-light" else "textual-light")

if __name__ == "__main__":
    app = StopWatchApp()

    app.run()
