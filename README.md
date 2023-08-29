# plagiarism-checker
This tool is just parser and unzipper for checking plagiarism in coding test. Currently only available for windows.

# Depedency
If only using executable in my repo, only need these two to be installed.
* Dolos (https://dolos.ugent.be/guide/installation.html)
* NodeJS (LTS Most Recommended Ver)

Else you need all of these to this simple app to work.
* Python 3.x
* Visual Studio Build Tools 2022
* pyunpack

    > pip install pyunpack

# How to compile
Just click compile on your favorite IDE.

# How to use
* Open plagiarism-checker.exe / Compile plagiarism-checker.py
* Select which folder contain zip of assignment
* Press Run Check, and there's should be webpage
* Enjoy

    > Don't forget to close dolos after run, or your localhost port 3000 will be occupied

# QNA
* What happen if i re-run same folder that this app already check?
  > It will automatically open .csv file available in that folder, and proceed to open your default browser to display the data.
