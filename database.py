#some of this code was generated from AI. My dad gave tips for my code too. I reviewed and edited it for the assignment requirements.


from pathlib import Path
import csv
from typing import List, Dict, Optional


class RecipeDB:
    """Simple CSV recipe database.

    CSV file with the headers: Drink,Size,Instructions,Image
    """

    def __init__(self, csv_path: Optional[Path] = None):
        """Initialize the database and load recipes from CSV."""
        if csv_path is None:
            csv_path = Path(__file__).parent / "Instructions.csv"
        self.csv_path = Path(csv_path)
        self._rows: List[Dict[str, str]] = []
        self._load()

    def _load(self) -> None:
        """Load recipes from the CSV file."""
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Instructions CSV not found: {self.csv_path}")

        with self.csv_path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                drink = row.get("Drink", "").strip()
                size = row.get("Size", "").strip()
                instructions = row.get("Instructions", "")
                image_field = row.get("Image", "").strip()

                img_path = Path(image_field)
                if not img_path.is_absolute():
                    img_path = (self.csv_path.parent / img_path).resolve()

                self._rows.append({
                    "Drink": drink,
                    "Size": size,
                    "Instructions": instructions,
                    "Image": str(img_path),
                })

    def get_drinks(self) -> List[str]:
        """Return sorted list of unique drink names."""
        return sorted({recipe["Drink"] for recipe in self._rows})

    def get_sizes(self, drink: str) -> List[str]:
        """Return sizes available for the given drink in the order found."""
        return [recipe["Size"] for recipe in self._rows if recipe["Drink"] == drink]
    def get_recipe(self, drink: str, size: str) -> Optional[Dict[str, str]]:
        """Return the row matching drink+size or None if not found."""
        for recipe in self._rows:
            if recipe["Drink"] == drink and recipe["Size"] == size:
                return recipe
        return None
