import pytest
from preprocessor import preprocess_ignore_line


@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        (
            """
            これはテストです
            ; この行は無視します
            ; この行は無視します
            この行は読み上げます
            ; この行は無視します
            """,
            """
            これはテストです
            この行は読み上げます
            """,
        ),
        (
            """
            ;先頭を無視するテストです
            この行は読み上げます
            """,
            """
            この行は読み上げます
            """,
        ),
    ],
)
def test_preprocess_ignore_line(input_string, expected_output):
    output_string = preprocess_ignore_line(input_string)
    assert output_string == expected_output
