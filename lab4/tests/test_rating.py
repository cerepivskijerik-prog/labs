"""Автоматические тесты пакета university_rating."""

import unittest

from university_rating.calculations import (
    calculate_average,
    determine_letter_grade,
    determine_status,
)
from university_rating.rating import build_rating
from university_rating.validation import validate_scores


class RatingTests(unittest.TestCase):
    """Проверяет расчёты, рейтинг и граничные случаи."""

    def test_empty_average(self):
        self.assertIsNone(calculate_average([]))

    def test_status_boundary(self):
        self.assertEqual(determine_status(49.99), "не допущен")
        self.assertEqual(determine_status(50), "допущен")

    def test_invalid_score(self):
        with self.assertRaises(ValueError):
            validate_scores([80, 101])

    def test_invalid_score_type(self):
        with self.assertRaises(TypeError):
            validate_scores([80, "80"])

    def test_bool_is_not_score(self):
        with self.assertRaises(TypeError):
            validate_scores([80, True])

    def test_source_is_not_changed(self):
        students = [{"id": 1, "name": "Test", "scores": [70, 80]}]
        before = [{"id": 1, "name": "Test", "scores": [70, 80]}]

        build_rating(students)

        self.assertEqual(students, before)

    def test_empty_students(self):
        self.assertEqual(build_rating([]), [])

    def test_letter_grade_a(self):
        self.assertEqual(determine_letter_grade(95), "A")

    def test_letter_grade_b(self):
        self.assertEqual(determine_letter_grade(85), "B")

    def test_letter_grade_c(self):
        self.assertEqual(determine_letter_grade(75), "C")

    def test_letter_grade_d(self):
        self.assertEqual(determine_letter_grade(65), "D")

    def test_letter_grade_f(self):
        self.assertEqual(determine_letter_grade(49.99), "F")

    def test_rating_order(self):
        students = [
            {"id": 1, "name": "Low", "scores": [40, 50]},
            {"id": 2, "name": "High", "scores": [90, 100]},
            {"id": 3, "name": "NoData", "scores": []},
        ]

        rating = build_rating(students)

        self.assertEqual(
            [item["name"] for item in rating],
            ["High", "Low", "NoData"],
        )

    def test_missing_name(self):
        with self.assertRaises(ValueError):
            build_rating([{"id": 1, "scores": [80]}])


if __name__ == "__main__":
    unittest.main()
