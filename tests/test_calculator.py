"""Approved project 58 requirements exercised against real Kivy widgets.

Run with the qualified Kivy/Xvfb runner, with this directory copied to the
calculator repository. No application modules or Kivy widgets are mocked.
"""

import ast
from pathlib import Path

import pytest
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label

from main import SimpleCalculatorApp


@pytest.fixture
def calculator():
    root = SimpleCalculatorApp().build()
    Window.size = (360, 560)
    Window.add_widget(root)
    for _ in range(4):
        Clock.tick()
    yield root
    Window.remove_widget(root)


def buttons(root):
    return {widget.text: widget for widget in root.walk() if isinstance(widget, Button)}


def press(root, *labels):
    for label in labels:
        buttons(root)[label].trigger_action(duration=0)
    Clock.tick()


def test_addition(calculator):
    press(calculator, "1", "2", "+", "7", "=")
    assert calculator.display.text == "19"


def test_subtraction(calculator):
    press(calculator, "3", "-", "8", "=")
    assert calculator.display.text == "-5"


def test_division(calculator):
    press(calculator, "9", "/", "3", "=")
    assert calculator.display.text == "3"


def test_number_buttons(calculator):
    numeric = [w for w in calculator.walk() if isinstance(w, Button) and w.text.isdigit()]
    assert len(numeric) == 10
    ordered = sorted(numeric, key=lambda w: (-round(w.center_y, 2), w.center_x))
    assert [w.text for w in ordered] == list("9876543210")
    press(calculator, *"9876543210")
    assert calculator.display.text == "9876543210"


def test_calculate_button(calculator):
    keypad = buttons(calculator)
    equals = keypad["="]
    assert equals.center_x == max(w.center_x for w in keypad.values())
    assert equals.center_y == min(w.center_y for w in keypad.values())
    press(calculator, "4", "+", "5")
    assert calculator.display.text != "9"
    press(calculator, "=")
    assert calculator.display.text == "9"


def test_calculate_button_purple(calculator):
    red, green, blue, alpha = buttons(calculator)["="].background_color
    # Purple has both red and blue components above green and an opaque fill.
    assert red > green and blue > green and red > 0.3 and blue > 0.3
    assert alpha == pytest.approx(1)


def test_result_display(calculator):
    display = calculator.display
    assert isinstance(display, Label)
    assert display.center_y >= calculator.y + calculator.height * 2 / 3
    press(calculator, "6", "+", "2", "=")
    assert display.text == "8"


def test_operation_buttons(calculator):
    ops = [buttons(calculator)[symbol] for symbol in ("+", "-", "/")]
    numeric = buttons(calculator)["9"]
    assert len({id(w) for w in ops}) == 3
    assert max(w.top for w in ops) <= calculator.display.y + 1
    assert min(w.y for w in ops) >= numeric.top - 1
    assert max(w.center_y for w in ops) - min(w.center_y for w in ops) < 1


def test_clear_button(calculator):
    press(calculator, "9", "+", "3", "C")
    assert calculator.display.text == "0"
    press(calculator, "2", "+", "4", "=")
    assert calculator.display.text == "6"


def test_python_code_base():
    source = Path("main.py").read_text(encoding="utf-8")
    tree = ast.parse(source, filename="main.py")
    assert any(isinstance(node, ast.ClassDef) and node.name == "SimpleCalculatorApp" for node in tree.body)


def test_kivy_ui(calculator):
    from kivy.uix.widget import Widget

    assert isinstance(calculator, Widget)
    assert isinstance(calculator.display, Label)
    assert buttons(calculator)
