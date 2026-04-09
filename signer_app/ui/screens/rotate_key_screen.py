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
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from signer_app.services.key_rotation_service import rotate_key_file
from signer_app.ui.i18n import register_refresh, t


class RotateKeyScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.private_key_edit = QLineEdit()
        self.output_dir_edit = QLineEdit()
        self.new_name_edit = QLineEdit()

        self.current_password_edit = QLineEdit()
        self.current_password_edit.setEchoMode(QLineEdit.Password)

        self.new_password_edit = QLineEdit()
        self.new_password_edit.setEchoMode(QLineEdit.Password)

        self.reason_edit = QLineEdit()

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)

        root_layout = QVBoxLayout(self)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        root_layout.addWidget(self.title_label)

        self.description_label = QLabel()
        self.description_label.setStyleSheet("font-size: 13px; color: #888;")
        self.description_label.setWordWrap(True)
        root_layout.addWidget(self.description_label)

        form = QFormLayout()

        private_key_row = QHBoxLayout()
        self.private_key_browse = QPushButton()
        self.private_key_browse.clicked.connect(self._choose_private_key)
        private_key_row.addWidget(self.private_key_edit)
        private_key_row.addWidget(self.private_key_browse)

        output_dir_row = QHBoxLayout()
        self.output_dir_browse = QPushButton()
        self.output_dir_browse.clicked.connect(self._choose_output_dir)
        output_dir_row.addWidget(self.output_dir_edit)
        output_dir_row.addWidget(self.output_dir_browse)

        self.private_key_label = QLabel()
        self.output_dir_label = QLabel()
        self.new_name_label = QLabel()
        self.current_password_label = QLabel()
        self.new_password_label = QLabel()
        self.reason_label = QLabel()

        form.addRow(self.private_key_label, private_key_row)
        form.addRow(self.output_dir_label, output_dir_row)
        form.addRow(self.new_name_label, self.new_name_edit)
        form.addRow(self.current_password_label, self.current_password_edit)
        form.addRow(self.new_password_label, self.new_password_edit)
        form.addRow(self.reason_label, self.reason_edit)

        root_layout.addLayout(form)

        self.rotate_button = QPushButton()
        self.rotate_button.clicked.connect(self._rotate_key)
        root_layout.addWidget(self.rotate_button)

        root_layout.addSpacing(10)
        root_layout.addWidget(self.result_box)
        root_layout.addStretch()

        register_refresh(self.refresh_texts)
        self.refresh_texts()

    def refresh_texts(self) -> None:
        self.title_label.setText(t("rotate.title"))
        self.description_label.setText(t("rotate.description"))
        self.private_key_label.setText(t("rotate.private_key"))
        self.output_dir_label.setText(t("rotate.output_dir"))
        self.new_name_label.setText(t("rotate.new_key_name"))
        self.current_password_label.setText(t("rotate.current_password"))
        self.new_password_label.setText(t("rotate.new_password"))
        self.reason_label.setText(t("rotate.reason"))
        self.current_password_edit.setPlaceholderText(t("rotate.current_password_placeholder"))
        self.new_password_edit.setPlaceholderText(t("rotate.new_password_placeholder"))
        self.reason_edit.setPlaceholderText(t("rotate.reason_placeholder"))
        self.private_key_browse.setText(t("common.browse"))
        self.output_dir_browse.setText(t("common.browse"))
        self.rotate_button.setText(t("rotate.button"))

    def _set_status(self, title: str, lines: list[str]) -> None:
        self.result_box.setPlainText("\n".join([title, "", *lines]).strip())

    def _choose_private_key(self) -> None:
        selected_file, _ = QFileDialog.getOpenFileName(
            self,
            t("rotate.private_key"),
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if selected_file:
            self.private_key_edit.setText(selected_file)

            source = Path(selected_file)
            if not self.output_dir_edit.text().strip():
                self.output_dir_edit.setText(str(source.parent))

            if not self.new_name_edit.text().strip():
                base_name = source.name.replace(".priv.json", "")
                self.new_name_edit.setText(f"{base_name}_v2")

    def _choose_output_dir(self) -> None:
        selected_dir = QFileDialog.getExistingDirectory(
            self,
            t("rotate.output_dir"),
            self.output_dir_edit.text().strip() or "",
        )
        if selected_dir:
            self.output_dir_edit.setText(selected_dir)

    def _rotate_key(self) -> None:
        private_key_path = self.private_key_edit.text().strip()
        output_dir = self.output_dir_edit.text().strip() or None
        new_key_name = self.new_name_edit.text().strip()
        current_password = self.current_password_edit.text() or None
        new_password = self.new_password_edit.text() or None
        rotation_reason = self.reason_edit.text().strip() or None

        if not private_key_path:
            QMessageBox.warning(
                self,
                t("rotate.warning.private_key.title"),
                t("rotate.warning.private_key.body"),
            )
            return

        if not new_key_name:
            QMessageBox.warning(
                self,
                t("rotate.warning.new_name.title"),
                t("rotate.warning.new_name.body"),
            )
            return

        self.result_box.clear()

        try:
            result = rotate_key_file(
                private_key_path=private_key_path,
                new_key_name=new_key_name,
                output_dir=output_dir,
                password=current_password,
                new_password=new_password,
                rotation_reason=rotation_reason,
            )
        except Exception as exc:
            self._set_status(
                t("rotate.error.status"),
                [
                    f"Error: {exc}",
                    f"{t('rotate.private_key')}: {private_key_path}",
                ],
            )
            QMessageBox.critical(self, t("rotate.error.title"), str(exc))
            return

        encryption_status = t("common.encrypted") if result.new_private_key_encrypted else t("common.plaintext")

        self._set_status(
            t("rotate.success.status"),
            [
                f"{t('rotate.result.old_private_key')}: {result.updated_old_private_key_path}",
                f"{t('rotate.result.new_private_key')}: {result.new_private_key_path}",
                f"{t('rotate.result.new_public_key')}: {result.new_public_key_path}",
                f"{t('rotate.result.old_address')}: {result.old_address}",
                f"{t('rotate.result.new_address')}: {result.new_address}",
                f"{t('rotate.result.profile')}: {result.profile_name}",
                f"{t('rotate.result.profile_description')}: {result.profile_description}",
                f"{t('rotate.result.algorithm')}: {result.algorithm_name}",
                f"{t('rotate.result.backend')}: {result.backend_algorithm_name}",
                f"{t('rotate.result.public_fingerprint')}: {result.public_key_fingerprint}",
                f"{t('rotate.result.private_storage')}: {encryption_status}",
                f"{t('rotate.result.key_status')}: {result.key_status}",
                f"{t('rotate.result.key_created_at')}: {result.key_created_at_utc}",
                f"{t('rotate.result.rotated_from')}: {result.rotated_from}",
                f"{t('rotate.result.rotation_reason')}: {result.rotation_reason}",
            ],
        )