# Coffee Shop GUI (PyQt6)

Simple PyQt6 application that reads `Instructions.csv` and displays coffee recipes.

Files:
- `app.py` — GUI application (loads `database.py`).
- `database.py` — CSV reader and simple query API.
- `Instructions.csv` — Provided CSV with Drink/Size/Instructions/Image columns.
- `images/` — Folder with images referenced by the CSV.

Setup (Windows PowerShell):

```powershell
python -m pip install -r requirements.txt
python app.py
```

Notes:
- The app resolves image paths relative to the location of `Instructions.csv`.
- `Instructions` column supports basic HTML which is rendered in the app.

AI-assisted work disclosure:
- Portions of the code were generated with the assistance of an AI (GitHub Copilot / GPT) and were reviewed and edited by the developer. Inline comments in the source indicate where assistance was used.

Submission notes:
- Ensure all project files (python files, `Instructions.csv`, `images/`, and this README) are pushed to the `main` branch of your public GitHub repository before submission.
