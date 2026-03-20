from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Digits
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from time import monotonic

class TimeDisplay(Digits):
    """AWidget to display the time"""

    start_time = reactive(monotonic)
    time = reactive(0.0)

    def update_time(self) -> None:
        """method to update time to the current time"""
        self.time = monotonic() - self.start_time

    def on_mount(self) -> None:
        """event handler call when widget is added to the class"""
        self.set_interval(1 / 60, self.update_time)

    def watch_time(self, time:float)-> None:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")



class StopWatch(HorizontalGroup):
    """A stop watch widget"""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Even handler for button pressed"""
        if event.button.id == "start":
            self.add_class("started")
        elif event.button.id == "stop":
            self.remove_class("started")
        return

    def compose(self) -> ComposeResult:
        """Create a child widget for stop watch"""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")

        yield TimeDisplay()


class StopWatchApp(App):
    """Textual app for a stop watch"""

    CSS_PATH = "stopwatch03.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """ "create child widget for the app"""
        yield Header()
        yield Footer()
        yield VerticalScroll(StopWatch(), StopWatch(), StopWatch())

    def action_toggle_dark(self) -> None:
        """Action to switch to dark mode"""

        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = StopWatchApp()

    app.run()
