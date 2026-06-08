# Comprehensive Scientific Calculator for Engineering

## Current Version

**Version:** 1.0.0
**Status:** Stable Release

## Overview

A cross-platform desktop application designed for engineering students and professionals. This software integrates advanced mathematical analysis, linear algebra, numerical methods, statistics, probability, and 2D plotting within a unified offline graphical user interface.

All computations are performed locally without requiring internet access.

---

## Technologies Used

| Component             | Technology              |
| --------------------- | ----------------------- |
| Language              | Python 3.13+            |
| GUI Framework         | PySide6 (Qt for Python) |
| Symbolic Mathematics  | SymPy                   |
| Numerical Computation | NumPy, SciPy            |
| Data Visualization    | Matplotlib              |

---

## Tested Environment

This application has been actively developed and tested on:

* Debian 13
* Python 3.13

Expected to work on:

* Ubuntu 24.04+
* Fedora 42+
* Arch Linux
* Linux Mint 22+
* Windows 10
* Windows 11

---

## Installation

### 1. Clone the Repository

You can clone the repository using either HTTPS or SSH.

#### HTTPS

```bash
git clone https://github.com/santifrias1/EngineeringCalculator.git
cd EngineeringCalculator
```

#### SSH

```bash
git clone git@github.com:santifrias1/EngineeringCalculator.git
cd EngineeringCalculator
```

---

## Linux Distribution Notes

### Debian / Ubuntu

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip libxcb-cursor0
```

### Fedora

```bash
sudo dnf install python3 python3-pip python3-virtualenv
```

### Arch Linux

```bash
sudo pacman -S python python-pip
```

### openSUSE

```bash
sudo zypper install python3 python3-pip python3-virtualenv
```

---

## Execution Steps

It is highly recommended to run the application inside a Python virtual environment to prevent dependency conflicts.

### Create Virtual Environment

#### Linux

```bash
python3 -m venv venv
```

#### Windows

```cmd
python -m venv venv
```

---

### Activate Virtual Environment

#### Bash / Zsh

```bash
source venv/bin/activate
```

#### Fish

```fish
source venv/bin/activate.fish
```

#### Csh / Tcsh

```csh
source venv/bin/activate.csh
```

#### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
venv\Scripts\activate.bat
```

---

### Install Dependencies

Using requirements.txt:

```bash
pip install -r requirements.txt
```

If the file is unavailable:

```bash
pip install PySide6 sympy numpy scipy matplotlib
```

---

### Run the Application

#### Linux

```bash
python3 app.py
```

#### Windows

```cmd
python app.py
```

---

## Common Linux Issue

### Qt xcb Plugin Error

On Debian and Ubuntu systems you may encounter an error related to the Qt xcb platform plugin.

Install the required package:

```bash
sudo apt update
sudo apt install libxcb-cursor0
```

---

## Creating a Standalone Executable

To distribute the application without requiring users to install Python or project dependencies, you can compile it into a standalone executable using PyInstaller.

### Important

PyInstaller does not support cross-compilation.

* Windows executables must be built on Windows.
* Linux executables must be built on Linux.

---

### Build Instructions

Install PyInstaller:

```bash
pip install pyinstaller
```

Generate the executable:

```bash
pyinstaller --noconsole --onefile app.py
```

After the build completes, the executable will be located inside:

```text
dist/
```

Examples:

```text
dist/app
dist/app.exe
```

---

## License

This project is licensed under the MIT License.

See the LICENSE file for details.

