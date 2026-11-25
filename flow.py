
import os
import logging
from pathlib import Path
from datetime import datetime, timedelta

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

load_dotenv(PROJECT_DIR / ".env")

PORTAL_URL = os.getenv(
    "PORTAL_URL",
    "http://localhost:8081/login/?next=/"
)

PORTAL_USERNAME = os.getenv("PORTAL_USERNAME")
PORTAL_PASSWORD = os.getenv("PORTAL_PASSWORD")

DOWNLOAD_DIR = PROJECT_DIR / "downloads"
LOG_DIR = PROJECT_DIR / "logs"

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "biometric_automation.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# MAIN AUTOMATION
# --------------------------------------------------

def run() -> str:

    if not PORTAL_USERNAME or not PORTAL_PASSWORD:
        raise ValueError(
            "Portal username or password is missing in .env"
        )

    yesterday = datetime.now() - timedelta(days=1)
    report_date = yesterday.strftime("%Y-%m-%d")

    logger.info("Starting biometric attendance automation")
    logger.info("Report date: %s", report_date)

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=True
        )

        context = None
        popup = None

        try:

            context = browser.new_context(
                accept_downloads=True
            )

            page = context.new_page()
            page.set_default_timeout(30000)

            # ------------------------------------------
            # LOGIN
            # ------------------------------------------

            logger.info("Opening biometric portal")

            page.goto(
                PORTAL_URL,
                wait_until="domcontentloaded"
            )

            page.get_by_role(
                "textbox",
                name="Username"
            ).fill(PORTAL_USERNAME)

            page.get_by_role(
                "textbox",
                name="Password"
            ).fill(PORTAL_PASSWORD)

            page.get_by_role(
                "button",
                name="Login"
            ).click()

            page.wait_for_load_state("domcontentloaded")

            logger.info("Login submitted")

            # ------------------------------------------
            # ATTENDANCE NAVIGATION
            # ------------------------------------------

            attendance_link = page.get_by_role(
                "link",
                name="Attendance",
                exact=True
            )

            attendance_link.wait_for(state="visible")
            attendance_link.click()

            logger.info("Attendance page opened")

            # ------------------------------------------
            # DEBUG REPORTS LINK
            # ------------------------------------------

            report_links = page.locator("a").filter(
                has_text="Reports"
            )

            report_count = report_links.count()

            logger.info(
                "Reports links found: %s",
                report_count
            )

            for index in range(report_count):

                link = report_links.nth(index)

                logger.info(
                    "Reports link %s | Text: %s | Href: %s",
                    index,
                    link.inner_text(),
                    link.get_attribute("href")
                )

            # Save screenshot for debugging
            page.screenshot(
                path=str(PROJECT_DIR / "reports_debug.png"),
                full_page=True
            )

            # ------------------------------------------
            # REPORTS / CALCULATE
            # ------------------------------------------

            # This selector must be verified against
            # the actual Reports link in the debug output.
            reports_link = page.get_by_role(
                "link",
                name="Reports"
            )

            reports_link.wait_for(state="visible")
            reports_link.click()

            calculate_link = page.get_by_role(
                "link",
                name="Calculate"
            )

            calculate_link.wait_for(state="visible")
            calculate_link.click()

            logger.info("Attendance calculation page opened")

            page.locator(
                "#calculation-tree-control"
            ).get_by_title(
                "Select All"
            ).click()

            page.get_by_role(
                "button",
                name="calculate"
            ).click()

            logger.info("Attendance calculation submitted")

            # ------------------------------------------
            # DAILY ATTENDANCE REPORT
            # ------------------------------------------

            page.get_by_role(
                "link",
                name="Reports",
                exact=True
            ).click()

            daily_report = page.locator(
                ".report-box"
            ).filter(
                has_text="Daily Attendance"
            )

            daily_report.wait_for(state="visible")
            daily_report.click()

            logger.info("Daily Attendance report opened")

            page.locator(
                "#dailyAttendanceReport-dept-tree-control"
            ).get_by_title(
                "Select All"
            ).click()

            # ------------------------------------------
            # POSITION FILTER
            # ------------------------------------------

            # Restore the original layout zoom
            page.evaluate("document.body.style.zoom='65%'")

            page.wait_for_timeout(1500)

            position_item = page.get_by_role(
                "listitem"
            ).filter(
                has_text="Position"
            )

            position_item.wait_for(state="visible")
            position_item.scroll_into_view_if_needed()

            # Expand the Position section
            position_item.click()

            page.wait_for_timeout(500)

            # Expand again if required by the original UI workflow
            position_item.click()

            page.wait_for_timeout(500)

            # Select the required position
            position_checkbox = page.locator(
                "#dailyAttendanceReport-tree-position_9_check"
            )

            position_checkbox.wait_for(state="visible")
            position_checkbox.click()

            logger.info("Position filter selected successfully")

            logger.info("Position filter selected")

            # ------------------------------------------
            # DATE FILTER
            # ------------------------------------------

            page.locator(
                "#dailyAttendanceReport-start-date"
            ).fill(report_date)

            page.locator(
                "#dailyAttendanceReport-end-date"
            ).fill(report_date)

            logger.info("Report dates entered")

            # ------------------------------------------

            # ------------------------------------------
            # SEARCH AND EXPORT - DIAGNOSTIC
            # ------------------------------------------

            page.locator(
                ".button-3d.dailyAttendanceReport-search"
            ).click()

            logger.info("Attendance search completed")

            page.locator(
                ".fa.fa-fw.fa-share"
            ).click()

            logger.info("Export menu opened")

            page.get_by_text(
                "Excel Export"
            ).click()

            logger.info("Excel Export selected")

            # Capture the page after selecting Excel Export
            page.screenshot(
                path=str(PROJECT_DIR / "excel_export_debug.png"),
                full_page=True
            )

            # Inspect visible buttons, links and icon elements
            elements = page.locator(
                "button, a, i, span, [class*='layui']"
            )

            logger.info("Inspecting export elements")

            for index in range(elements.count()):

                element = elements.nth(index)

                if element.is_visible():

                    text = element.inner_text().strip()

                    html = element.evaluate(
                        "(el) => el.outerHTML"
                    )

                    if text or "icon" in html.lower() or "fa-" in html.lower():
                        logger.info(
                            "Element %s | Text: %s | HTML: %s",
                            index,
                            text,
                            html[:500]
                        )

            # ------------------------------------------
            # DOWNLOAD EXCEL
            # ------------------------------------------

            logger.info("Starting Excel download")

            with page.expect_download(
                timeout=120000
            ) as download_info:

                with page.expect_popup() as popup_info:

                    page.locator(
                        "//a[text()='Confirm']"
                    ).click()

                popup = popup_info.value

            download = download_info.value

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            file_name = (
                f"Daily Attendance Report_{timestamp}.xlsx"
            )

            file_path = DOWNLOAD_DIR / file_name

            download.save_as(str(file_path))

            # ------------------------------------------
            # VALIDATE DOWNLOAD
            # ------------------------------------------

            if not file_path.exists():
                raise RuntimeError(
                    "Downloaded Excel file was not found"
                )

            if file_path.stat().st_size == 0:
                raise RuntimeError(
                    "Downloaded Excel file is empty"
                )

            if file_path.suffix.lower() != ".xlsx":
                raise RuntimeError(
                    "Downloaded file is not an XLSX file"
                )

            logger.info(
                "Excel report downloaded successfully: %s",
                file_path
            )

            logger.info(
                "File size: %s bytes",
                file_path.stat().st_size
            )

            return str(file_path)

        except Exception:

            logger.exception(
                "Biometric automation failed"
            )

            if context:
                try:
                    page.screenshot(
                        path=str(
                            PROJECT_DIR / "error.png"
                        ),
                        full_page=True
                    )
                except Exception:
                    logger.exception(
                        "Could not save error screenshot"
                    )

            raise

        finally:

            if popup:
                try:
                    popup.close()
                except Exception:
                    pass

            if context:
                context.close()

            browser.close()

            logger.info(
                "Browser resources closed"
            )
