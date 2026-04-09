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

from signer_app.services.file_sign_service import sign_file_with_private_key
from signer_app.ui.i18n import register_refresh, t


class SignFileScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.file_edit = QLineEdit()
        self.private_key_edit = QLineEdit()
        self.signature_path_edit = QLineEdit()

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

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

        file_row = QHBoxLayout()
        self.file_browse = QPushButton()
        self.file_browse.clicked.connect(self._choose_file)
        file_row.addWidget(self.file_edit)
        file_row.addWidget(self.file_browse)

        private_key_row = QHBoxLayout()
        self.private_key_browse = QPushButton()
        self.private_key_browse.clicked.connect(self._choose_private_key)
        private_key_row.addWidget(self.private_key_edit)
        private_key_row.addWidget(self.private_key_browse)

        signature_row = QHBoxLayout()
        self.signature_browse = QPushButton()
        self.signature_browse.clicked.connect(self._choose_signature_output)
        signature_row.addWidget(self.signature_path_edit)
        signature_row.addWidget(self.signature_browse)

        self.file_label = QLabel()
        self.private_key_label = QLabel()
        self.password_label = QLabel()
        self.signature_output_label = QLabel()

        form.addRow(self.file_label, file_row)
        form.addRow(self.private_key_label, private_key_row)
        form.addRow(self.password_label, self.password_edit)
        form.addRow(self.signature_output_label, signature_row)

        root_layout.addLayout(form)

        self.sign_button = QPushButton()
        self.sign_button.clicked.connect(self._sign_file)
        root_layout.addWidget(self.sign_button)

        root_layout.addSpacing(10)
        root_layout.addWidget(self.result_box)
        root_layout.addStretch()

        register_refresh(self.refresh_texts)
        self.refresh_texts()

    def refresh_texts(self) -> None:
        self.title_label.setText(t("sign.title"))
        self.description_label.setText(t("sign.description"))
        self.file_label.setText(t("sign.file"))
        self.private_key_label.setText(t("sign.private_key"))
        self.password_label.setText(t("sign.password"))
        self.signature_output_label.setText(t("sign.signature_output"))
        self.password_edit.setPlaceholderText(t("sign.password_placeholder"))
        self.file_browse.setText(t("common.browse"))
        self.private_key_browse.setText(t("common.browse"))
        self.signature_browse.setText(t("common.browse"))
        self.sign_button.setText(t("sign.button"))

    def _set_status(self, title: str, lines: list[str]) -> None:
        self.result_box.setPlainText("\n".join([title, "", *lines]).strip())

    def _choose_file(self) -> None:
        selected_file, _ = QFileDialog.getOpenFileName(
            self,
            t("sign.file"),
            "",
            "All Files (*)",
        )
        if selected_file:
            self.file_edit.setText(selected_file)
            if not self.signature_path_edit.text().strip():
                default_sig = str(Path(selected_file).with_suffix(Path(selected_file).suffix + ".sig"))
                self.signature_path_edit.setText(default_sig)

    def _choose_private_key(self) -> None:
        selected_file, _ = QFileDialog.getOpenFileName(
            self,
            t("sign.private_key"),
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if selected_file:
            self.private_key_edit.setText(selected_file)

    def _choose_signature_output(self) -> None:
        selected_file, _ = QFileDialog.getSaveFileName(
            self,
            t("sign.signature_output"),
            self.signature_path_edit.text().strip() or "",
            "Signature Files (*.sig);;All Files (*)",
        )
        if selected_file:
            self.signature_path_edit.setText(selected_file)

    def _sign_file(self) -> None:
        file_path = self.file_edit.text().strip()
        private_key_path = self.private_key_edit.text().strip()
        signature_path = self.signature_path_edit.text().strip() or None
        password = self.password_edit.text() or None

        if not file_path:
            QMessageBox.warning(self, t("sign.warning.file.title"), t("sign.warning.file.body"))
            return

        if not private_key_path:
            QMessageBox.warning(
                self,
                t("sign.warning.private_key.title"),
                t("sign.warning.private_key.body"),
            )
            return

        self.result_box.clear()

        try:
            result = sign_file_with_private_key(
                file_path=file_path,
                private_key_path=private_key_path,
                signature_path=signature_path,
                password=password,
            )
        except Exception as exc:
            self._set_status(
                t("sign.error.status"),
                [
                    f"Error: {exc}",
                    f"{t('sign.error.file_path')}: {file_path}",
                    f"{t('sign.error.private_key_path')}: {private_key_path}",
                ],
            )
            QMessageBox.critical(self, t("sign.error.title"), str(exc))
            return

        self._set_status(
            t("sign.success.status"),
            [
                f"{t('sign.result.file_path')}: {result.file_path}",
                f"{t('sign.result.signature_path')}: {result.signature_path}",
                f"{t('sign.result.profile')}: {result.profile_name}",
                f"{t('sign.result.profile_description')}: {result.profile_description}",
                f"{t('sign.result.standard')}: {result.signature_standard}",
                f"{t('sign.result.family')}: {result.signature_family}",
                f"{t('sign.result.algorithm')}: {result.algorithm_name}",
                f"{t('sign.result.backend')}: {result.backend_algorithm_name}",
                f"{t('sign.result.hash_algorithm')}: {result.file_hash_algorithm}",
                f"{t('sign.result.file_hash')}: {result.file_hash_hex}",
                f"{t('sign.result.public_fingerprint')}: {result.public_key_fingerprint}",
                f"{t('sign.result.signature_size')}: {result.signature_size}",
                f"{t('sign.result.created_at')}: {result.created_at_utc}",
            ],
        )