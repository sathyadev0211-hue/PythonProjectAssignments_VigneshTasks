# conftest.py
# Pytest configuration file.
# Automatically generates an HTML report when the test suite is executed.

def pytest_configure(config):
    """Hook to set the default HTML report path if not provided on CLI."""
    # Only set the report path if pytest-html is installed and no path was given
    if not config.option.__dict__.get("htmlpath"):
        config.option.htmlpath = "report.html"
