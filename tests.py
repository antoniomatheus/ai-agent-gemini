import unittest
from functions.get_files_info import get_files_info

class TestFunctions(unittest.TestCase):
    def test_outside_working_dir(self):
        info = get_files_info("calculator", "/bin")

        expected_msg = """Result for '/bin' directory:
    Error: Cannot list "/bin" as it is outside the permitted working directory"""

        self.assertEqual(expected_msg, info)

    def test_directory_is_really_a_directory(self):
        info = get_files_info("calculator", "lorem.txt")

        expected_msg = """Result for 'lorem.txt' directory:
    Error: "calculator/lorem.txt" is not a directory"""
        self.assertEqual(expected_msg, info)

    def test_response_structure(self):
        files_info = get_files_info("calculator", ".")
        self.assertIn("file_size=", files_info)
        self.assertIn("is_dir=", files_info)


if __name__ == "__main__":
    unittest.main()