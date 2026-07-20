# Biometric Automation

## Overview

Biometric Automation is a Python-based automation project developed using **Microsoft Playwright**. The application automates interactions with the biometric attendance system to retrieve, process, and manage attendance data, reducing manual effort and improving accuracy.

---

## Purpose

This project was developed to:

- Automate attendance-related tasks.
- Reduce manual intervention.
- Improve the reliability of attendance processing.
- Enable consistent execution through browser automation.

---

## Technology Stack

| Component | Technology |
|----------|------------|
| Language | Python 3.x |
| Automation Framework | Playwright |
| IDE | PyCharm |
| Version Control | Git & GitHub |

---

## Project Structure

```
Biometric_automation/
│
├── downloads/             # Files downloaded during automation
├── main.py                # Entry point of the application
├── flow.py                # Core automation workflow
├── requirements.txt       # Python dependencies
├── README.md
└── .gitignore
```

---

## Project Workflow

```
Jenkins Job
      │
      ▼
Checkout Latest Code
      │
      ▼
Create/Activate Python Environment
      │
      ▼
Install Dependencies
      │
      ▼
Launch Playwright Browser
      │
      ▼
Login to Application
      │
      ▼
Execute Automation Flow
      │
      ▼
Download / Process Attendance Data
      │
      ▼
Generate Logs
      │
      ▼
End Job
```

---

## Prerequisites

- Python 3.10 or later
- Playwright
- Git

---

## Installation

### Clone the repository

```bash
git clone https://github.com/oliviasmith4828-code/Biometric_automation.git
cd Biometric_automation
```

### Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright browsers

```bash
playwright install
```

---

## Running the Project

Execute the main script:

```bash
python main.py
```

---

## Main Files

### `main.py`

- Starts the automation process.
- Initializes Playwright.
- Calls the workflow in `flow.py`.

### `flow.py`

Contains the core automation logic, such as:

- Launching the browser.
- Logging into the application.
- Navigating through the system.
- Performing attendance-related operations.
- Downloading or processing data.
- Handling errors and retries.

---

## Configuration

Update the required configuration before running the project:

- Application URL
- Username and password
- Download directory
- Timeouts (if required)

**Important:** Do not store production credentials directly in the source code. Use environment variables or a local configuration file that is not committed to Git.

---

## Dependencies

Example `requirements.txt`:

```
playwright
```

If additional libraries are used (for example `pandas`, `openpyxl`, or `python-dotenv`), list them in `requirements.txt`.

---

## Error Handling

The project handles common automation issues such as:

- Login failures
- Element not found
- Timeout exceptions
- Network interruptions
- Download failures

Review the console output or logs for troubleshooting.

---

## Maintenance Guidelines

When updating this project:

- Keep selectors centralized if possible.
- Update Playwright selectors if the application UI changes.
- Test the complete workflow after any modifications.
- Update this README when adding new features or changing setup steps.

---

## Future Enhancements

- Configuration through `.env` files.
- Scheduled execution.
- Detailed logging.
- Email notifications.
- Automated report generation.

---

## Repository

https://github.com/oliviasmith4828-code/Biometric_automation

---

## Author

Developed for internal organizational use. This repository serves as the source code and documentation for ongoing maintenance and future enhancements.
