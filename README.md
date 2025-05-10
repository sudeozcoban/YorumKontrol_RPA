# Comment Check RPA Project

This project is an RPA automation that checks comment lines in Python codes using Python and UiPath.

## 💡 Purpose

- Check if code comments comply with the spelling rules:
- Does it start with a capital letter?
- Does it contain a keyword (for, if, while, function, etc.)?
- Does it end with a dot?
- Does it have at least 3 words?

## 📁 Project Structure
CommentControlProject/
├── example_code.py # Example Python code to check
├── comment_control_example.py # Python function to check comments
├── report.json # Output (automatically generated)
├── report.xml # XML output
├── example_code_color.py # Output with erroneous comments marked with ⚠️
├── CommentControlRPA/ # UiPath project (includes Main.xaml)

## 🔧 Technologies Used

- Python 3.x
- Regex (comment analysis with DFA logic)
- UiPath (Invoke Python, JSON operations, message display)
- GitHub Desktop

## 🚀 How to Run?

1. In the `comment_control_example.py` file, the `comments_control_et` function checks the Python codes.

2. The UiPath project calls this function in `Main.xaml`.

3. JSON output is taken and each comment line is displayed to the user as a message box.

## 📷 Sample Output
```json
[
  {
    "satir": 1,
    "yorum": "# Bu for dongusu listeyi gezer.",
    "sonuc": "Doğru"
  },
  ...
]
