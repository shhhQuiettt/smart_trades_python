from scripts.logic.helpers import floor_decimal, absolute_error


def test_floor_decimals():
    inputs = [1, 2.3, 3.6999, 12341, 2.000164]
    decimals = [0, 0, 2, 2, 4]
    expected_values = [1, 2, 3.69, 12341, 2.0001]

    for i in range(len(inputs)):
        assert floor_decimal(inputs[i], decimals[i]) == expected_values[i]


def test_absolute_error():
    given = [1, 2.3, 3.6999, 12]
    exact = [1.1, 2, 3.7001, 2]
    expected_values = [0.1, 0.3, 0.0002, 10]

    for i in range(len(given)):
        assert absolute_error(given[i], exact[i]) == expected_values[i]
