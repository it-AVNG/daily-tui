from textual.app import App, ComposeResult
from textual.widgets import Footer, Header


class MyProjectApp(App):
    def compose(self) -> ComposeResult:
        """Create child widget for the app"""
        yield Header()
        yield Footer()


if __name__ == "__main__":
    app = MyProjectApp()

    app.run
