# Typing Speed Test Application

Created by Nana Kwame Amporful

## Description
A modern typing speed test application with both GUI and terminal interfaces. Test and improve your typing speed with customizable difficulty levels and real-time performance metrics.

## Features
- Multiple difficulty levels (Easy, Medium, Hard)
- Real-time WPM (Words Per Minute) calculation
- Accuracy tracking
- Time elapsed monitoring
- Modern graphical user interface
- Customizable text samples

## Requirements
- Python 3.x
- tkinter (usually comes with Python)
- windows-curses (for Windows systems)

## Installation
1. Clone or download this repository
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the GUI version:
```
python typing_test_gui.py
```

## How to Use
1. Select your desired difficulty level (Easy, Medium, or Hard)
2. The text to type will appear in the top text box
3. Start typing in the lower text box
4. Your statistics will update in real-time:
   - Words Per Minute (WPM)
   - Accuracy percentage
   - Time elapsed
5. Use the Reset button to start over or New Text to try a different text

## File Structure
- `typing_test_gui.py`: Main GUI application
- `texts.json`: Collection of typing texts
- `requirements.txt`: Required Python packages

## Author
Nana Kwame Amporful

## License
This project is open source and available under the MIT License.

## Contributing
Feel free to fork this repository and submit pull requests for any improvements.
