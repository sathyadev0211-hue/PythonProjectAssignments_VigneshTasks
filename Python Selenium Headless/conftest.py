"""
conftest.py
===========
Pytest configuration file for the GUVI Login Automation Suite.

- Adds project metadata to the HTML report
- Configures pytest-html report title and environment info
"""

import pytest


# ── HTML Report Metadata ──────────────────────────────────────────────────────
def pytest_configure(config):
    """Attach project-level metadata visible in the HTML report header."""
    config._metadata = {
        "Project"    : "GUVI Login Automation",
        "Base URL"   : "https://www.guvi.in/",
        "Login URL"  : "https://www.guvi.in/sign-in/",
        "Framework"  : "Python + Selenium + Pytest",
        "Report Type": "pytest-html (self-contained)",
    }


@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report):
    """Set the HTML report page title."""
    report.title = "GUVI Login Automation — Test Report"
