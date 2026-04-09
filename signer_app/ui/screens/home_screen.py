from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget

from signer_app.ui.i18n import register_refresh, t


class HomeScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()

        self.logo_label = QLabel()
        logo_path = Path(__file__).resolve().parent.parent / "assets" / "aegis-logo.png"
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            if not pixmap.isNull():
                self.logo_label.setPixmap(
                    pixmap.scaled(
                        156,
                        156,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )

        text_layout = QVBoxLayout()

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold;")

        self.subtitle_label = QLabel()
        self.subtitle_label.setStyleSheet("font-size: 14px; color: #666;")
        self.subtitle_label.setWordWrap(True)

        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.subtitle_label)
        text_layout.addSpacing(14)

        header_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignTop)
        header_layout.addSpacing(20)
        header_layout.addLayout(text_layout)
        header_layout.addStretch()

        layout.addLayout(header_layout)
        layout.addSpacing(18)

        self.overview_title = QLabel()
        self.overview_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.overview_body = QLabel()
        self.overview_body.setWordWrap(True)

        self.standard_title = QLabel()
        self.standard_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.standard_body = QLabel()
        self.standard_body.setWordWrap(True)

        self.profiles_title = QLabel()
        self.profiles_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.profiles_body = QLabel()
        self.profiles_body.setWordWrap(True)

        self.rotation_title = QLabel()
        self.rotation_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.rotation_body = QLabel()
        self.rotation_body.setWordWrap(True)

        self.demo_title = QLabel()
        self.demo_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.demo_body = QLabel()
        self.demo_body.setWordWrap(True)

        for widget in [
            self.overview_title,
            self.overview_body,
            self.standard_title,
            self.standard_body,
            self.profiles_title,
            self.profiles_body,
            self.rotation_title,
            self.rotation_body,
            self.demo_title,
            self.demo_body,
        ]:
            layout.addWidget(widget)

        layout.addStretch()

        register_refresh(self.refresh_texts)
        self.refresh_texts()

    def refresh_texts(self) -> None:
        self.title_label.setText(t("home.title"))
        self.subtitle_label.setText(t("home.subtitle"))

        self.overview_title.setText(t("home.section.overview.title"))
        self.overview_body.setText(t("home.section.overview.body"))

        self.standard_title.setText(t("home.section.standard.title"))
        self.standard_body.setText(t("home.section.standard.body"))

        self.profiles_title.setText(t("home.section.profiles.title"))
        self.profiles_body.setText(t("home.section.profiles.body"))

        self.rotation_title.setText(t("home.section.rotation.title"))
        self.rotation_body.setText(t("home.section.rotation.body"))

        self.demo_title.setText(t("home.section.demo.title"))
        self.demo_body.setText(t("home.section.demo.body"))