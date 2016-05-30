def test_sum(number_one, number_two):
    number_one = convert_integer(number_one)
    number_two = convert_integer(number_two)

    result = number_one + number_two

    return result


def convert_integer(number_string):
    converted_integer = int(number_string)

    return converted_integer


answer = test_sum("1", "2")
