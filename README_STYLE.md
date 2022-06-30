<div align="center">
  <h1> Style Guide </h1>
</div>
<br>

# [Python Naming Conventions](https://pep8.org/#prescriptive-naming-conventions) - Cheat Sheet

* Avoid single letter variable names such as ‘l’ (lowercase letter el), ‘O’ (uppercase letter oh), or ‘I’ (uppercase letter eye) characters as these can be mistaken for 1 and 0 depending on typeface.
* Use lower case and snake case (underscore_separated) convention for function names and variable names as in `some_function` and `some_variable`, respectively.
* Use lower case and snake case convention for method names as in `method` or `some_method`, respectively.
* Use lower case and snake case convention for module names as in `module.py` or `some_module.py`, respectively.
* Use CamelCase (CapWords) convention for class names as in `ClassName` or `SomeClass`.
* Use only capital letters (uppercase) for constants as in `CONSTANT` or `SOME_CONSTANT`.

# Code Formatting

## Indentation

- Use 2 spaces per indentation level.

```python
def some_function(arg1):
  '''
  Check for empty and None values in a variable.
  '''
  if bool(arg1)==False: # 1st identation level.
    pass # 2nd identation level.
  else:
    return arg1
```

## Backslash

- Use a backslash (escape character) to break lines that are just too long:

```python
from some_package import example1, example2 \
  example3
```

## [F-strings](https://realpython.com/python-f-strings/#f-strings-a-new-and-improved-way-to-format-strings-in-python)

- Use Python f-strings to speed up readability over %-formatting and str.format().

Example with a Python expression:
```python
method_name = 'Some_Method'
f"{method_name.lower()} is the correct convention."
```

## Leading and trailing whitespace/characters

Remove spaces at the beginning (left) and at the end (right) of a string variable using Python's strip() method:

```python
string_variable= f" some text  "
string_variable = string_variable.strip()
```

Remove Leading and trailing characters of a string variable:

```python
string_variable= f",##,,,some text...rr..."
string_variable = string_variable.strip(",.#r")
```

## General rules for Docstrings

This project standard is built in close resemblance to the [pandas docstring guide](https://pandas.pydata.org/docs/development/contributing_docstring.html).

- The short summary of the function, method or class must start with a capital letter, end with a dot, and fit in a single line.
- Use the backtick symbol (\`) to convey a Python variable, function, method, class, or module.
- Remove blank lines at the opening and closing quotes of the docstring. i.e, remove all blank lines after the signature `def func():`.
- The opening and closing quotes must be kept isolated from the description message.
- Use parentheses after the variable name to indicate its data type.

**Good example:**
```python
def sum_ab(a, b):
  """
  This line should provide a short and concise summary of the function. Example: Add up two integer numbers.

  This line is dedicated to providing further details that are not too verbose.

  Args:
    - num1 (int): short description of the first variable.
    - num2 (int): short description of the second variable.

  Returns:
    - variable_name (int): The sum of `num1` and `num2`.

  Examples:
    >>> add(2, 2)
    4
  """
  variable_name = a + b
  return variable_name
```

# Contributors 

Created and maintained by [@camponogaraviera][1].

[1]: https://github.com/camponogaraviera
