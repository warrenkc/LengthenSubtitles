# SRT Subtitle Lengthener

This tool lengthens the duration of subtitle blocks in an SRT file so that each subtitle stays on screen until shortly before the next one starts. This is particularly useful for dual-language videos where you want the text to remain visible for easier reading.

You can use it now: [https://warrenkc.github.io/LengthenSubtitles/] (https://warrenkc.github.io/LengthenSubtitles/)

## Features
- Lengthens subtitle duration to end **0.2 seconds** before the next subtitle begins.
- Preserves original start times.
- Handles standard SRT formatting.

## Usage

### 1. Web Version (Recommended)
Open `index.html` in any modern web browser.
- Select your `.srt` file.
- Click **Process and Download**.
- The processed file will be downloaded automatically with `-lengthened` added to the filename.

### 2. Python Script (With GUI)
A user-friendly desktop application:
1. Ensure you have Python installed.
2. Run the script:
   ```bash
   python main.py
   ```
3. Use the **Browse** buttons to select your input `.srt` file and choose where to save the output.
4. Click **Process SRT** to generate the lengthened file.

## Project Structure
- `index.html`: A standalone web tool using vanilla JavaScript.
- `main.py`: Python implementation with a Tkinter GUI.
- `new-english.ind.srt`: Example input file.
- `new-english-lengthened.ind.srt`: Example output file.
