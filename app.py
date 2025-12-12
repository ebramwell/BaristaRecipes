#some of this code was generated from AI. My dad also reviewed all my code. I reviewed and edited it for the assignment requirements.

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QTextBrowser,
    QSizePolicy,
    QPushButton,
    QStackedWidget,
    QMessageBox,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from database import RecipeDB


class CoffeeApp(QMainWindow):
    """Main window with a simple home page and a recipes page.

    The home page contains a title and a button to show the recipes page.
    The recipes page contains the Drink/Size dropdowns, instructions, image,
    and a Close button to exit the app.
    """

    def __init__(self) -> None:
        """Initialize the application and load the recipe database."""
        super().__init__()
        self.setWindowTitle("Coffee Company Barista Recipes")

        # Initialize the CSV database; show an error if it fails
        try:
            self.db = RecipeDB()
        except Exception as exc:  # pragma: no cover - defensive
            QMessageBox.critical(self, "Error", f"Failed to load recipes: {exc}")
            raise

        self._setup_ui()
        self._load_drinks()
        self.resize(900, 600)
        self.show()

    def _setup_ui(self) -> None:
        """Set up the user interface with home page and recipes page."""
        #QstackedWidget for homepage and recipes page
        stacked = QStackedWidget()
        self.stacked = stacked
        self.setCentralWidget(self.stacked)

        #homepage
        home = QWidget()
        home_layout = QVBoxLayout()
        home.setLayout(home_layout)
        title = QLabel("☕Coffee Company Barista Recipes")
        title.setStyleSheet("font-size: 26pt; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        home_layout.addStretch()
        home_layout.addWidget(title)
        home_layout.addStretch()
        go_button = QPushButton("☕ Recipes")
        go_button.setFixedWidth(320)
        home_layout.addWidget(go_button, alignment=Qt.AlignmentFlag.AlignCenter)
        home_layout.addStretch()

        #recipes page
        recipes_page = QWidget()
        recipes_layout_outer = QHBoxLayout()
        recipes_page.setLayout(recipes_layout_outer)

        #left controls
        controls = QWidget()
        controls_layout = QVBoxLayout()
        controls.setLayout(controls_layout)
        controls_layout.addWidget(QLabel("Drink:"))
        self.drink_cb = QComboBox()
        controls_layout.addWidget(self.drink_cb)
        controls_layout.addWidget(QLabel("Size:"))
        self.size_cb = QComboBox()
        controls_layout.addWidget(self.size_cb)
        #back button for the homepage
        close_btn = QPushButton("Back")
        close_btn.setStyleSheet("background-color: #2B2B2D")
        close_btn.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        controls_layout.addWidget(close_btn)
        controls_layout.addStretch()
        recipes_layout_outer.addWidget(controls, 0)

        #Right display
        display = QWidget()
        display_layout = QVBoxLayout()
        display.setLayout(display_layout)
        self.instructions = QTextBrowser()
        self.instructions.setOpenExternalLinks(True)
        # give instructions more vertical space than the image below
        display_layout.addWidget(self.instructions, 3)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        display_layout.addWidget(self.image_label, 1)
        recipes_layout_outer.addWidget(display, 1)

        #pages and background color
        home.setStyleSheet("background-color: #00704A;")
        recipes_page.setStyleSheet("background-color: #00704A;")

        self.stacked.addWidget(home)
        self.stacked.addWidget(recipes_page)
        go_button.clicked.connect(lambda: self.stacked.setCurrentWidget(recipes_page))

        # for changing the drinks and sizes
        self.drink_cb.currentTextChanged.connect(self.on_drink_changed)
        self.size_cb.currentTextChanged.connect(self.on_size_changed)

    def _load_drinks(self) -> None:
        """Load drinks from the database for the drink combobox."""
        try:
            drinks = self.db.get_drinks()
        except Exception as exc:
            QMessageBox.warning(self, "Warning", f"Could not load drinks: {exc}")
            drinks = []

        self.drink_cb.blockSignals(True)
        self.drink_cb.clear()
        self.drink_cb.addItems(drinks)
        self.drink_cb.blockSignals(False)
        if drinks:
            self.drink_cb.setCurrentIndex(0)
            #sizes for the first drink
            self.on_drink_changed(drinks[0])

    def on_drink_changed(self, drink: str) -> None:
        """Handle drink selection change and update sizes."""
        sizes = self.db.get_sizes(drink)
        self.size_cb.blockSignals(True)
        self.size_cb.clear()
        self.size_cb.addItems(sizes)
        self.size_cb.blockSignals(False)
        if sizes:
            self.size_cb.setCurrentIndex(0)
            self.on_size_changed(sizes[0])
        else:
            self.instructions.clear()
            self.image_label.clear()

    def on_size_changed(self, size: str) -> None:
        """Handle size selections and display recipe instructions and image."""
        drink = self.drink_cb.currentText()
        recipe = self.db.get_recipe(drink, size)
        if recipe:
            #instructions and wrap in HTML tags
            instructions_text = recipe.get("Instructions", "")
            steps = instructions_text.split(",")
            instructions_text = "<br>".join(f"• {step.strip()}" for step in steps)
            html_formatted = f"<p>{instructions_text}</p>"
            self.instructions.setHtml(recipe.get("Instructions", ""))
            
            img_path = recipe.get("Image", "")
            pix = QPixmap(img_path)
            if pix.isNull():
                self.image_label.setText("Image not found")
                self.image_label.setPixmap(QPixmap())
            else:
                self._set_pixmap(pix)
        else:
            self.instructions.clear()
            self.image_label.clear()

    def _set_pixmap(self, pix: QPixmap) -> None:
        """Scale and set the pixmap for the image label."""
        w = max(200, self.image_label.width())
        h = max(150, self.image_label.height())
        scaled = pix.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled)

    def resizeEvent(self, event) -> None:
        """Handle window resize events by rescaling the current image."""
        #if window resizes, rescale the current imaage
        pm = self.image_label.pixmap()
        if pm and not pm.isNull():
            self._set_pixmap(pm)
        super().resizeEvent(event)


def main() -> None:
    """Create and run the app."""
    app = QApplication(sys.argv)
    try:
        window = CoffeeApp()
        sys.exit(app.exec())
    except Exception as exc:  # this is in case the whole thing fails
        QMessageBox.critical(None, "Fatal Error", f"Application failed: {exc}")
        raise


if __name__ == "__main__":
    main()
