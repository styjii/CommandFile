# File Manager CLI

This project provides a command-line interface (CLI) to manage files—supporting search, delete, copy, and move operations based on file extensions.

### Table of Contents

- [File Manager CLI](#file-manager-cli)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contribution](#contribution)
  - [License](#license)
  - [Screenshot](#screenshot)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/styjii/CommandFile.git
```

2. Install dependencies:

```bash
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

### Usage

To explore available commands and their options, use:

```bash
python3 app.py --help
python3 app.py run --help         # Main CLI entry point
python3 app.py list-files --help  # Lists files by extension
python3 app.py copy-files --help  # Copies files
python3 app.py move-files --help  # Moves files
python3 app.py remove-files --help # Deletes files
```

#### Example usage

```bash
# Search for .txt files in a directory
python3 app.py run search txt my_folder

# Copy .csv files from one directory to another
python3 app.py run copy csv src_folder dst_folder

# Move .log files with filename prefix 'error'
python3 app.py run move log logs_folder archived_logs --filename-prefix error

# Remove all .tmp files from a folder
python3 app.py run remove tmp temp_folder
```

### Contribution

1. Fork the repository.
2. Create a new branch.
3. Add your changes.
4. Push your branch.
5. Open a pull request.

### License

This project is under the MIT license.

### Screenshot

**Help Command Output Example**

![Help Output](image/README/1740786478955.png "Help command output representation")