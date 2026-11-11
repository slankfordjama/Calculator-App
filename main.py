from decimal import Decimal, DivisionByZero, InvalidOperation

from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


Window.size = (360, 560)
Window.clearcolor = (0.08, 0.09, 0.11, 1)


class CalculatorRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(12), spacing=dp(10), **kwargs)
        self.current_value = ""
        self.left_value = None
        self.operation = None
        self.just_calculated = False

        self.display = Label(
            text="0",
            font_size=dp(42),
            halign="right",
            valign="middle",
            color=(0.96, 0.97, 1, 1),
            size_hint=(1, 0.34),
        )
        self.display.bind(size=self._sync_display_text_size)
        self.add_widget(self.display)

        operations = GridLayout(cols=3, spacing=dp(8), size_hint=(1, 0.13))
        for symbol in ("+", "-", "/"):
            operations.add_widget(self._button(symbol, self._choose_operation, kind="operation"))
        self.add_widget(operations)

        keypad = GridLayout(cols=3, spacing=dp(8), size_hint=(1, 0.53))
        for digit in ("9", "8", "7", "6", "5", "4", "3", "2", "1", "0"):
            keypad.add_widget(self._button(digit, self._append_digit))

        keypad.add_widget(self._button("C", self._clear, kind="utility"))
        keypad.add_widget(self._button("=", self._calculate, kind="calculate"))
        self.add_widget(keypad)

    def _sync_display_text_size(self, *_):
        self.display.text_size = (self.display.width - dp(20), self.display.height)

    def _button(self, text, callback, kind="number"):
        colors = {
            "number": (0.18, 0.20, 0.24, 1),
            "operation": (0.13, 0.30, 0.33, 1),
            "utility": (0.34, 0.18, 0.18, 1),
            "calculate": (0, 0, 1, 1),
        }
        button = Button(
            text=text,
            font_size=dp(26),
            background_normal="",
            background_color=colors[kind],
            color=(1, 1, 1, 1),
        )
        button.bind(on_press=lambda instance: callback(instance.text))
        return button

    def _append_digit(self, digit):
        if self.just_calculated:
            self.current_value = ""
            self.left_value = None
            self.operation = None
            self.just_calculated = False

        if self.current_value == "0":
            self.current_value = digit
        else:
            self.current_value += digit
        self._refresh_display()

    def _choose_operation(self, symbol):
        if self.current_value:
            self.left_value = self.current_value
            self.current_value = ""
        elif self.left_value is None:
            self.left_value = "0"

        self.operation = symbol
        self.just_calculated = False
        self._refresh_display()

    def _calculate(self, _text):
        if self.left_value is None or self.operation is None or not self.current_value:
            return

        try:
            left = Decimal(self.left_value)
            right = Decimal(self.current_value)
            if self.operation == "+":
                result = left + right
            elif self.operation == "-":
                result = left - right
            elif self.operation == "/":
                result = left / right
            else:
                return
        except (DivisionByZero, InvalidOperation):
            self._show_error()
            return

        self.current_value = self._format_decimal(result)
        self.left_value = None
        self.operation = None
        self.just_calculated = True
        self._refresh_display()

    def _clear(self, _text):
        self.current_value = ""
        self.left_value = None
        self.operation = None
        self.just_calculated = False
        self._refresh_display()

    def _refresh_display(self):
        if self.operation and self.left_value is not None:
            right = self.current_value if self.current_value else ""
            self.display.text = f"{self.left_value} {self.operation} {right}".strip()
        else:
            self.display.text = self.current_value or "0"

    def _show_error(self):
        self.current_value = ""
        self.left_value = None
        self.operation = None
        self.just_calculated = False
        self.display.text = "Error"

    @staticmethod
    def _format_decimal(value):
        normalized = value.normalize()
        if normalized == normalized.to_integral():
            return str(normalized.quantize(Decimal(1)))
        return format(normalized, "f")


class SimpleCalculatorApp(App):
    title = "Simple Calculator"

    def build(self):
        return CalculatorRoot()


if __name__ == "__main__":
    SimpleCalculatorApp().run()
