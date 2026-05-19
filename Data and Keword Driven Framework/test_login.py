# tests/test_login.py
# OrangeHRM Login Automation — Data Driven Testing Framework (DDTF)
#
# Framework components used:
#   • DDTF            — Test data is driven from Excel file (test_data.xlsx)
#   • POM             — LoginPage class encapsulates page interactions
#   • Explicit Wait   — WebDriverWait + Expected Conditions throughout
#   • Pytest          — Test runner with parametrize and HTML reporting
#
# Run command:
#   pytest tests/test_login.py -v --html=reports/report.html --self-contained-html

import pytest
from pages.login_page import LoginPage
from utils.excel_utils import get_test_data, write_test_result


# ─── Load Excel Data at Collection Time ───────────────────────────────────────
def load_login_test_data():
    """
    Read all test rows from Excel and format them for pytest.parametrize.

    Returns:
        List of pytest.param objects — each carries the test row dict,
        and uses the Test ID as the readable test case ID.
    """
    rows = get_test_data()
    return [
        pytest.param(row, id=row["test_id"])
        for row in rows
    ]


# ─── Test Class ───────────────────────────────────────────────────────────────
class TestOrangeHRMLogin:
    """
    Test suite for OrangeHRM portal login using Data Driven Testing Framework.
    Each parametrized case represents one row from the Excel test data sheet.
    """

    @pytest.mark.login
    @pytest.mark.parametrize("test_data", load_login_test_data())
    def test_login_with_credentials(self, driver, test_data):
        """
        Test Case: Attempt login with Username and Password from Excel.

        Steps:
            1. Navigate to OrangeHRM login URL
            2. Enter Username from Excel row
            3. Enter Password from Excel row
            4. Click the Login button
            5. Verify login result (Pass / Fail)
            6. Write result back into the Excel file

        Args:
            driver    : Chrome WebDriver (injected by conftest.py fixture)
            test_data : Dict with row data from Excel (injected by parametrize)
        """
        # ── Arrange ───────────────────────────────────────────────────────────
        username    = test_data["username"]
        password    = test_data["password"]
        row_number  = test_data["row_number"]
        test_id     = test_data["test_id"]
        tester_name = test_data["tester_name"]

        print(f"\n[{test_id}] Tester: {tester_name} | User: {username}")

        # ── Act ───────────────────────────────────────────────────────────────
        login_page = LoginPage(driver)
        login_page.perform_login(username, password)  # Navigate + enter creds + click login

        # ── Assert & Write Result ─────────────────────────────────────────────
        if login_page.is_login_successful():
            # Login succeeded — Dashboard header was found
            result = "Passed"
            print(f"[{test_id}] ✓ Login PASSED for username='{username}'")
            write_test_result(row_number, result)      # Write "Passed" to Excel
            assert True, f"{test_id}: Login succeeded as expected."

        else:
            # Login failed — collect error message for reporting
            error_msg = login_page.get_error_message()
            result = "Failed"
            print(f"[{test_id}] ✗ Login FAILED for username='{username}'. Error: '{error_msg}'")
            write_test_result(row_number, result)      # Write "Failed" to Excel

            # Fail the test so pytest marks it red in the HTML report
            pytest.fail(
                f"{test_id}: Login FAILED for user='{username}'. "
                f"Portal error: '{error_msg}'"
            )
