from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button

from main import SimpleCalculatorApp


def test_requirement_13616():
    root = SimpleCalculatorApp().build()
    Window.size = (360, 560)
    Window.add_widget(root)
    try:
        for _ in range(4):
            Clock.tick()
        buttons = [widget for widget in root.walk() if isinstance(widget, Button)]
        rows = {}
        for button in buttons:
            rows.setdefault(round(button.center_y, 2), []).append(button)
        ordered_rows = [
            [button.text for button in sorted(row, key=lambda item: item.center_x)]
            for _, row in sorted(rows.items(), reverse=True)
        ]
        assert ordered_rows == [
            ["+", "-", "/", "*", "C"],
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "3", "2"],
            ["0", ".", "="],
        ]
    finally:
        Window.remove_widget(root)
