from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QComboBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from signer_app.services.key_service import generate_pq_keypair
from signer_app.ui.i18n import register_refresh, t


class GenerateKeyScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.output_dir_edit = QLineEdit(str(Path("data/signer_keys")))
        self.name_edit = QLineEdit("demo_user")

        self.profile_combo = QComboBox()
        self.profile_combo.addItems(["standard", "hardened", "max"])
        self.profile_combo.setCurrentText("hardened")

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)

        root_layout = QVBoxLayout(self)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        root_layout.addWidget(self.title_label)

        self.description_label = QLabel()
        self.description_label.setStyleSheet("font-size: 13px; color: #444;")
        root_layout.addWidget(self.description_label)

        form = QFormLayout()

        self.output_dir_row = QHBoxLayout()
        self.browse_button = QPushButton()
        self.browse_button.clicked.connect(self._choose_output_dir)
        self.output_dir_row.addWidget(self.output_dir_edit)
        self.output_dir_row.addWidget(self.browse_button)

        self.output_dir_field_label = QLabel()
        self.key_name_field_label = QLabel()
        self.profile_field_label = QLabel()
        self.password_field_label = QLabel()

        form.addRow(self.output_dir_field_label, self.output_dir_row)
        form.addRow(self.key_name_field_label, self.name_edit)
        form.addRow(self.profile_field_label, self.profile_combo)
        form.addRow(self.password_field_label, self.password_edit)

        root_layout.addLayout(form)

        self.generate_button = QPushButton()
        self.generate_button.clicked.connect(self._generate_key)
        root_layout.addWidget(self.generate_button)

        root_layout.addSpacing(10)
        root_layout.addWidget(self.result_box)
        root_layout.addStretch()

        register_refresh(self.refresh_texts)
        self.refresh_texts()

    def refresh_texts(self) -> None:
        self.title_label.setText(t("generate.title"))
        self.description_label.setText(t("generate.description"))
        self.output_dir_field_label.setText(t("generate.output_dir"))
        self.key_name_field_label.setText(t("generate.key_name"))
        self.profile_field_label.setText(t("generate.profile"))
        self.password_field_label.setText(t("generate.password"))
        self.password_edit.setPlaceholderText(t("generate.password_placeholder"))
        self.browse_button.setText(t("common.browse"))
        self.generate_button.setText(t("generate.button"))

    def _choose_output_dir(self) -> None:
        selected_dir = QFileDialog.getExistingDirectory(
            self,
            t("generate.output_dir"),
            self.output_dir_edit.text(),
        )
        if selected_dir:
            self.output_dir_edit.setText(selected_dir)

    def _generate_key(self) -> None:
        output_dir = self.output_dir_edit.text().strip()
        name = self.name_edit.text().strip()
        profile = self.profile_combo.currentText()
        password = self.password_edit.text()

        if not output_dir:
            QMessageBox.warning(
                self,
                t("generate.warning.output_dir.title"),
                t("generate.warning.output_dir.body"),
            )
            return

        if not name:
            QMessageBox.warning(
                self,
                t("generate.warning.key_name.title"),
                t("generate.warning.key_name.body"),
            )
            return

        try:
            result = generate_pq_keypair(
                output_dir=output_dir,
                name=name,
                profile_name=profile,
                password=password or None,
            )
        except Exception as exc:
            QMessageBox.critical(self, t("generate.error.title"), str(exc))
            return

        encryption_status = t("common.encrypted") if password else t("common.plaintext")

        self.result_box.setPlainText(
            "\n".join(
                [
                    t("generate.success.title"),
                    "",
                    f"{t('generate.result.profile')}: {result.profile_name}",
                    f"{t('generate.result.profile_description')}: {result.profile_description}",
                    f"{t('generate.result.algorithm')}: {result.algorithm_name}",
                    f"{t('generate.result.backend')}: {result.backend_algorithm_name}",
                    f"{t('generate.result.storage')}: {encryption_status}",
                    f"{t('generate.result.public_key_size')}: {result.public_key_size}",
                    f"{t('generate.result.private_key_size')}: {result.private_key_size}",
                    f"{t('generate.result.public_fingerprint')}: {result.public_key_fingerprint}",
                    f"{t('generate.result.public_key_path')}: {result.public_key_path}",
                    f"{t('generate.result.private_key_path')}: {result.private_key_path}",
                ]
            )
        )