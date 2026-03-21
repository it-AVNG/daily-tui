from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Button, Digits
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from time import monotonic


class TimeDisplay(Digits):
    """AWidget to display the time"""

    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)

    def update_time(self) -> None:
        """method to update time to the current time"""
        self.time = self.total + (monotonic() - self.start_time)

    def on_mount(self) -> None:
        """event handler call when widget is added to the class"""
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def start(self) -> None:
        """method to start the time"""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        """method to stop the time updating"""
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        self.total = 0
        self.time = 0

    def watch_time(self, time: float) -> None:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")


class Stopwatch(HorizontalGroup):
    """A stop watch widget"""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Even handler for button pressed"""
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)
        if button_id == "start":
            time_display.start()
            self.add_class("started")
        elif event.button.id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()
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
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("a", "add_stopwatch", "Add"),
        ("r", "remove_stopwatch", "Remove"),
    ]

    def compose(self) -> ComposeResult:
        """ "create child widget for the app"""
        yield Header()
        yield Footer()
        yield VerticalScroll(Stopwatch(), Stopwatch(), Stopwatch(), id="timers")

    def action_toggle_dark(self) -> None:
        """Action to switch to dark mode"""

        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_add_stopwatch(self) ->None:
        """An action to add Timer"""

        new_stopwatch =Stopwatch()
        self.query_one("#timers").mount(new_stopwatch)
        new_stopwatch.scroll_visible()

    def action_remove_stopwatch(self):
        timers = self.query("Stopwatch")
        if timers:
            timers.last().remove()

    



if __name__ == "__main__":
    app = StopWatchApp()

    app.run()
