from test_calculator import calculator, press


def test_requirement_11562(calculator):
    press(calculator, "1", ".", "2", "+", "0", ".", "3", "=")
    assert calculator.display.text == "1.5"

    press(calculator, "C", ".", ".", "5")
    assert calculator.display.text == "0.5"
