# Just Organize My Photos - `jomp`

– *A simple PyQt6 program that helps you manually sort photos into folders using keyboard shortcuts.*

`jomp` currently features a minimalist design and basic functionality: sorting photos from one folder into multiple others. Future updates may include additional features such as duplicate detection and corrupted file handling.

> [!TIP]
> This tool is particularly handy when you've recovered data from a damaged drive, leaving thousands of files jumbled together that need to be neatly reorganized into folders.
> 
Russian version of this README can be found [here](README_RU.md).

Main screen of the app:

![app](/images/app.png)

## Features:

* Drag-and-drop folder opening.
* Display of file information: size, date, resolution.
* Corrupted file detection.
* Deletion to recycle bin or permanent deletion (<kbd>Ctrl</kbd> + <kbd>Del</kbd>).
* Smart file renaming on move (both files are preserved if they have identical names).
* Folder selection on first button click, or via <kbd>RMB</kbd> or <kbd>Ctrl</kbd> + <kbd>LMB</kbd>.
* File preview with the ability to open in the default photo viewer (<kbd>LMB</kbd>) or file explorer (<kbd>RMB</kbd>).

## Planned Features:

* Settings! More settings!!!
* Hotkey customization and quantity adjustments.
* More informative (color-coded) photo resolution indicators.
* Sorting by size/name/resolution.
* Opening multiple folders simultaneously.
* Scanning for photos in subdirectories.
* Option to delete/move all corrupted files at once.
* Distribution as an executable file.

## How to Run

There are two ways to run the application: using Poetry or by building and installing it locally. I recommend the second method because it allows you to run the application from anywhere on your system.

### Run Locally with Poetry

1. Clone the repository:

   ```bash
   git clone https://github.com/potat-dev/just-organize-my-photos.git
   cd just-organize-my-photos
   ```

2. Install dependencies:

   ```bash
   poetry install
   ```

3. Run the application using Poetry:

   ```bash
   poetry run jomp
   ```

### Building and Installing

1. Build a distributable wheel file:

   ```bash
   poetry build
   ```

2. Install the application locally:

   ```bash
   pip install .
   ```

3. Now you can run the application from anywhere on your system:

   ```bash
   jomp
   ```

   You can also specify the path to the folder you want to sort: `--dir /path/to/folder`
