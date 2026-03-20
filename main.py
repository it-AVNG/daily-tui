from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Digits
from textual.containers import HorizontalGroup, VerticalScroll


class TimeDisplay(Digits):
    """AWidget to display the time"""
    pass


class StopWatch(HorizontalGroup):
    """A stop watch widget"""
    def compose(self) -> ComposeResult:
        """Create a child widget for stop watch"""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")

        yield TimeDisplay("00:00:00:00")



class StopWatchApp(App):
    """Textual app for a stop watch"""
    
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """"create child widget for the app"""
        yield Header()
        yield Footer()
        yield VerticalScroll(StopWatch(), StopWatch(), StopWatch())

    def action_toggle_dark(self) -> None:
        """Action to switch to dark mode"""

        self.theme = ( "textual-dark" if self.theme == "textual-light" else "textual-light")

if __name__ == "__main__":
    app = StopWatchApp()

    app.run()
