
import logging
from flow import run


def main():

    print("Starting biometric attendance automation...")

    report_path = run()

    print("\nBiometric automation completed successfully.")
    print(f"Downloaded report: {report_path}")


if __name__ == "__main__":

    try:
        main()

    except Exception:

        logging.exception(
            "Biometric automation execution failed"
        )

        raise
