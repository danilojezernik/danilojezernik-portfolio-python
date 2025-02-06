## Pre-Run Testing Workflow

Before the FastAPI application starts, our startup script automatically executes the entire test suite to ensure that
everything is working correctly. If any tests fail, the application will not launch. This helps us catch issues early
and maintain a high level of code quality.

### How It Works

1. **Test Execution on Startup:**
    - In the main entry point of the application (typically found in `src/__main__.py`), a function named `run_tests()`
      is called.
    - This function uses Python’s `subprocess` module to execute `pytest` with the following command:
    ```bash
    pytest --html=test/html_report/report.html --self-contained-html
    ```
    - The tests are run automatically before starting the server. An HTML report is generated and stored in
      `test/html_report/report.html`.

2. **Test Structure & Organization:**
    - **Test Files:**  
      All test files are located in the `test/` directory. For example, `test_main.py` contains tests for various API
      endpoints.
    - **Fixtures:**  
      Reusable fixtures (like database connections) are defined in `conftest.py` and under the `/fixtures` directory.
    - **Helpers:**  
      Utility functions to aid testing (such as data normalization and endpoint response checking) are stored in
      `src/test/utils/helpers.py`.
    - **HTML Report:**  
      After each test run, an HTML report is generated, making it easier to review the results and diagnose any issues.

3. **Test Outcome and Application Startup:**
    - **If All Tests Pass:**  
      The `run_tests()` function returns `True`, the application prints a success message (e.g., "✅ All tests passed!
      Starting FastAPI application..."), and the server starts using Uvicorn.
    - **If Any Test Fails:**  
      The `run_tests()` function returns `False`, a failure message is printed (e.g., "❌ Tests failed! Fix issues before
      running the application."), and the application exits without starting the server.

4. **Running Tests Manually:**
    - You can run the tests independently of the application startup by executing the following command in your
      project’s root directory:
    ```bash
    pytest --html=test/html_report/report.html --self-contained-html
    ```
    - This is useful during development to verify changes quickly.

### Environment Requirements

- **Dependencies:**  
  Ensure that all required dependencies (e.g., FastAPI, Pytest, Uvicorn, etc.) are installed.
- **Database Connectivity:**  
  The tests rely on a connection to the MongoDB instance. Make sure your database is accessible and properly configured.
- **Configuration Files:**  
  Verify that environment variables and configuration files (like `src/env.py`) are correctly set up to avoid issues
  during testing.

By running tests before launching the application, we ensure that the codebase remains robust and that potential issues
are caught and addressed early in the deployment process.

## Monkeypatching for Test Isolation

### What is Monkeypatching?

Monkeypatching is a technique that allows you to dynamically modify or override attributes, functions, or even
environment variables at runtime during testing. This is especially useful for isolating tests from external
dependencies (such as databases, web services, or authentication systems) by replacing them with controlled, predictable
behaviors (often called "mocks").

### The `monkeypatch` Fixture

Pytest provides a built-in fixture named `monkeypatch` that makes it easy to perform these modifications. When you use
the `monkeypatch` fixture in your tests, it provides a set of methods to temporarily change objects or values.
Importantly, all modifications made by `monkeypatch` are automatically undone after the test function completes,
ensuring that each test runs in a clean environment.

### Key Methods Provided by `monkeypatch`

- **`monkeypatch.setattr(obj, name, value, raising=True)`**  
  Replaces the attribute `name` of the object `obj` with `value`.  
  *Example:*
  ```python
  monkeypatch.setattr("src.routes.login.authenticate_user", lambda username, password: DummyUser())
  ```
  This is used to override the `authenticate_user` function in the login module with a dummy function that returns a
  test user.

- **`monkeypatch.delattr(obj, name, raising=True)`**  
  Deletes the attribute `name` from the object `obj`.

- **`monkeypatch.setitem(mapping, key, value)`**  
  Sets the value for `key` in a dictionary or list-like mapping.

- **`monkeypatch.delitem(mapping, key, raising=True)`**  
  Deletes the key from a dictionary or list-like mapping.

- **`monkeypatch.setenv(name, value, prepend=None)` and `monkeypatch.delenv(name, raising=True)`**  
  Modify environment variables during tests.

- **`monkeypatch.syspath_prepend(path)`**  
  Prepends a directory to the system path (`sys.path`), which can be useful if you need to import modules from a
  non-standard location during tests.

- **`monkeypatch.chdir(path)`**  
  Changes the current working directory for the duration of the test.

- **`monkeypatch.context()`**  
  Returns a context manager that can be used to apply and then automatically undo monkeypatch changes in a contained
  scope.

#### Alternatives to Monkeypatch

While monkeypatch is very convenient and integrated with Pytest, other options exist for modifying behavior during
tests:

- **`unittest.mock.patch()` (and related functions):**  
  Part of Python's standard library, the `unittest.mock` module offers functions like `patch()` which can be used to
  temporarily replace attributes or functions. This approach is widely used, especially in projects that use the
  unittest framework. However, monkeypatch is often preferred in Pytest due to its simplicity and automatic cleanup.

- **Custom Test Fixtures:**  
  You can also create your own test fixtures to set up and tear down test-specific configurations. However, this
  generally involves more boilerplate code compared to using monkeypatch.

#### Example Usage in Our Tests

In our login endpoint tests, we use `monkeypatch.setattr()` to override key functions:

- We replace `authenticate_user` with a lambda that returns a dummy user object when given specific credentials.
- We replace `create_access_token` with a lambda that returns a fixed token value.

This allows our tests to focus solely on the endpoint behavior without depending on the actual database or token
generation logic.

