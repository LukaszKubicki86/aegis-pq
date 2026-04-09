from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from signer_app.ui.i18n import get_language, register_refresh, set_language, t
from signer_app.ui.screens.generate_key_screen import GenerateKeyScreen
from signer_app.ui.screens.home_screen import HomeScreen
from signer_app.ui.screens.key_details_screen import KeyDetailsScreen
from signer_app.ui.screens.rotate_key_screen import RotateKeyScreen
from signer_app.ui.screens.sign_file_screen import SignFileScreen
from signer_app.ui.screens.verify_signature_screen import VerifySignatureScreen


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.nav_list = QListWidget()
        self.nav_list.setMinimumWidth(240)

        self.language_label = QLabel()
        self.language_combo = QComboBox()
        self.language_combo.addItem("Polski", "pl")
        self.language_combo.addItem("English", "en")
        current_index = self.language_combo.findData(get_language())
        if current_index >= 0:
            self.language_combo.setCurrentIndex(current_index)
        self.language_combo.currentIndexChanged.connect(self._on_language_changed)

        self.stack = QStackedWidget()
        self.stack.addWidget(HomeScreen())
        self.stack.addWidget(GenerateKeyScreen())
        self.stack.addWidget(KeyDetailsScreen())
        self.stack.addWidget(RotateKeyScreen())
        self.stack.addWidget(SignFileScreen())
        self.stack.addWidget(VerifySignatureScreen())

        self.nav_list.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav_list.setCurrentRow(0)

        splitter = QSplitter()
        splitter.addWidget(self._build_left_panel())
        splitter.addWidget(self.stack)
        splitter.setSizes([260, 840])

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(splitter)

        logo_path = Path(__file__).resolve().parent / "assets" / "aegis-logo.png"
        if logo_path.exists():
            self.setWindowIcon(QIcon(str(logo_path)))

        self.setCentralWidget(container)
        self.resize(1180, 760)

        register_refresh(self.refresh_texts)
        self.refresh_texts()

    def _build_left_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)

        language_row = QHBoxLayout()
        language_row.addWidget(self.language_label)
        language_row.addWidget(self.language_combo)

        layout.addLayout(language_row)
        layout.addWidget(self.nav_list)
        return panel

    def _on_language_changed(self) -> None:
        selected_language = self.language_combo.currentData()
        if isinstance(selected_language, str):
            set_language(selected_language)

    def refresh_texts(self) -> None:
        self.setWindowTitle(f"{t('app.window_title')} · {t('app.version')}")

        self.language_label.setText(f"{t('app.language')}:")
        self._set_combo_item_text("pl", t("language.polish"))
        self._set_combo_item_text("en", t("language.english"))

        labels = [
            t("app.nav.home"),
            t("app.nav.generate_key"),
            t("app.nav.key_details"),
            t("app.nav.rotate_key"),
            t("app.nav.sign_file"),
            t("app.nav.verify_signature"),
        ]

        current_row = self.nav_list.currentRow()
        self.nav_list.clear()
        for label in labels:
            self.nav_list.addItem(QListWidgetItem(label))

        if current_row < 0:
            current_row = 0
        self.nav_list.setCurrentRow(current_row)

    def _set_combo_item_text(self, data_value: str, text: str) -> None:
        index = self.language_combo.findData(data_value)
        if index >= 0:
            self.language_combo.setItemText(index, text)


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(
        """
        QWidget {
            font-size: 13px;
        }
        QListWidget {
            padding: 8px;
        }
        QTextEdit {
            padding: 8px;
        }
        """
    )
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()