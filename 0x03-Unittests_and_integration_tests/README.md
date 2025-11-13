Project 0x03 - Unittests


# 0x03. Unittests and Integration Tests

## 📖 Project Overview
This project focuses on mastering **Unit Testing** and **Integration Testing** in Python.  
You will learn how to write test cases using the `unittest` framework and how to ensure your functions behave correctly under various conditions.  

The project simulates real-world testing scenarios commonly used by backend developers in production systems.

---

## 🧩 Learning Objectives
By the end of this project, you should be able to:

- Understand the difference between **unit tests** and **integration tests**  
- Use the **`unittest`** module to create structured test cases  
- Apply the **`parameterized`** library to simplify multiple test inputs  
- Mock external dependencies during testing  
- Run automated tests to validate backend logic  
- Maintain **PEP 8** code style for clean, readable, and consistent Python code

---

## 🧠 Key Concept: Access Nested Map
The main function tested in this project is `access_nested_map()` which retrieves values from a nested dictionary using a sequence of keys.  

### Example:
```python
access_nested_map({"a": {"b": 2}}, ("a", "b"))
# Output: 2


Unit Test: test_utils.py

The unit tests ensure that access_nested_map() behaves as expected using the @parameterized.expand decorator for multiple test cases.

Example test structure:

@parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ({"a": {"b": 2}}, ("a", "b"), 2),
])
def test_access_nested_map(self, nested_map, path, expected):
    self.assertEqual(access_nested_map(nested_map, path), expected)

🧰 Technologies Used

Python 3.8+

unittest (built-in module)

parameterized (for testing multiple inputs)

pycodestyle (for PEP 8 compliance)

VS Code / Ubuntu / GitHub

⚙️ How to Run the Tests

Activate your virtual environment:

source venv/bin/activate


Run the tests:

python -m unittest test_utils.py


You should see:

...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK

✅ PEP 8 Style Check

Ensure your code follows the PEP 8 style guide:

pycodestyle utils.py test_utils.py

📂 Project Structure
0x03-Unittests_and_integration_tests/
├── utils.py
├── test_utils.py
├── README.md
└── __init__.py  (optional)



🏁 Summary

This project demonstrates how to:

Write clean, parameterized unit tests

Implement and validate backend helper functions

Follow PEP 8 conventions for maintainable, professional code

Prepare for real-world backend testing and continuous integration environments


🧑‍💻 Author
Fred Danjuma
Junior Backend Developer
GitHub: @Freddanjuma