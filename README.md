# Plagiarism Checker

This tool serves as a parser and unzipper designed for checking plagiarism in coding tests. Currently, it is only available for Windows.

## Dependencies

If you're using the executable from my repository, you only need to install the following two dependencies:
* [Dolos](https://dolos.ugent.be/guide/installation.html)
* [Node.js (LTS)](https://nodejs.org/en/download/current)

Otherwise, you'll need all of the following for this simple app to function:
* Python 3.x
* Visual Studio Build Tools 2022

## Installing Packages

To use this tool, please follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/byonicku/plagiarism-checker.git
    ```

2. Navigate to the repository directory:

    ```bash
    cd plagiarism-checker
    ```

3. Install the required packages using `pip` and the provided `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

This will install all the necessary dependencies for running the Plagiarism Checker tool.

## How to Compile

Simply click "compile" in your favorite IDE.

## How to Use

* Open `plagiarism-checker.exe` or compile `plagiarism-checker.py`.
* Select the folder containing the assignment zip file.
* Press "Run Check," and a webpage should appear.
* Enjoy!

    > Remember to close Dolos after running, or your localhost port 3000 will remain occupied.

## Q&A

* What happens if I re-run the same folder that this app has already checked?
  > It will automatically open the `.csv` file available in that folder and proceed to open your default browser to display the data.
