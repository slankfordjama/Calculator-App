from test_calculator import calculator, press


def test_requirement_11550(calculator):
    press(calculator, "1", "2", "*", "3", "=")
    assert calculator.display.text == "36"
