# Security Policy

## Supported Versions

This is a course project with no versioned releases. Only the latest code on the `main` branch receives fixes.

| Version         | Supported          |
| --------------- | ------------------ |
| `main` (latest) | :white_check_mark: |
| anything older  | :x:                |

## Scope

The project consists of local Jupyter notebooks with algorithms, inline figures and notebook controls, plus course datasets in `data/`. The `models/` directory is reserved for future trained model artifacts. It does not run an MCP server, a separate web viewer or a terminal application.

Reports are most useful when they concern code in these notebooks, such as input validation or unintended file access. Vulnerabilities in Python, `uv`, Jupyter, ipywidgets, pandas or matplotlib themselves should go to those projects.

## Reporting a Vulnerability

Please do not open a public issue for a vulnerability.

Use GitHub's private reporting instead: open the **Security** tab of this repository, choose **Report a vulnerability**, and describe the problem with steps to reproduce it.

This is a small project maintained in spare time, so replies are best effort. I will acknowledge a report as soon as I can, say whether I accept it as a vulnerability, and fix accepted reports on `main`. If a report is declined, I will explain why.
