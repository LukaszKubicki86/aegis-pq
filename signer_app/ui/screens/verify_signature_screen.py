from __future__ import annotations

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

from signer_app.services.file_verify_service import verify_file_signature
from signer_app.ui.i18n import register_refresh, t


class VerifySignatureScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.file_edit = QLineEdit()
        self.signature_edit = QLineEdit()

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

        signature_row = QHBoxLayout()
        self.signature_browse = QPushButton()
        self.signature_browse.clicked.connect(self._choose_signature)
        signature_row.addWidget(self.signature_edit)
        signature_row.addWidget(self.signature_browse)

        self.file_label = QLabel()
        self.signature_label = QLabel()

        form.addRow(self.file_label, file_row)
        form.addRow(self.signature_label, signature_row)

        root_layout.addLayout(form)

        self.verify_button = QPushButton()
        self.verify_button.clicked.connect(self._verify_signature)
        root_layout.addWidget(self.verify_button)

        root_layout.addSpacing(10)
        root_layout.addWidget(self.result_box)
        root_layout.addStretch()

        register_refresh(self.refresh_texts)
        self.refresh_texts()

    def refresh_texts(self) -> None:
        self.title_label.setText(t("verify.title"))
        self.description_label.setText(t("verify.description"))
        self.file_label.setText(t("verify.file"))
        self.signature_label.setText(t("verify.signature"))
        self.file_browse.setText(t("common.browse"))
        self.signature_browse.setText(t("common.browse"))
        self.verify_button.setText(t("verify.button"))

    def _choose_file(self) -> None:
        selected_file, _ = QFileDialog.getOpenFileName(
            self,
            t("verify.file"),
            "",
            "All Files (*)",
        )
        if selected_file:
            self.file_edit.setText(selected_file)

    def _choose_signature(self) -> None:
        selected_file, _ = QFileDialog.getOpenFileName(
            self,
            t("verify.signature"),
            "",
            "Signature Files (*.sig);;JSON Files (*.json);;All Files (*)",
        )
        if selected_file:
            self.signature_edit.setText(selected_file)

    def _verify_signature(self) -> None:
        file_path = self.file_edit.text().strip()
        signature_path = self.signature_edit.text().strip()

        if not file_path:
            QMessageBox.warning(self, t("verify.warning.file.title"), t("verify.warning.file.body"))
            return

        if not signature_path:
            QMessageBox.warning(
                self,
                t("verify.warning.signature.title"),
                t("verify.warning.signature.body"),
            )
            return

        try:
            result = verify_file_signature(
                file_path=file_path,
                signature_path=signature_path,
            )
        except Exception as exc:
            QMessageBox.critical(self, t("verify.error.title"), str(exc))
            return

        status_line = t("verify.result.valid") if result.is_valid else t("verify.result.invalid")

        self.result_box.setPlainText(
            "\n".join(
                [
                    f"{t('verify.result.title')}: {status_line}",
                    "",
                    f"{t('verify.result.message')}: {result.message}",
                    f"{t('verify.result.file_path')}: {result.file_path}",
                    f"{t('verify.result.signature_path')}: {result.signature_path}",
                    f"{t('verify.result.profile')}: {result.profile_name}",
                    f"{t('verify.result.profile_description')}: {result.profile_description}",
                    f"{t('verify.result.standard')}: {result.signature_standard}",
                    f"{t('verify.result.family')}: {result.signature_family}",
                    f"{t('verify.result.algorithm')}: {result.algorithm_name}",
                    f"{t('verify.result.backend')}: {result.backend_algorithm_name}",
                    f"{t('verify.result.hash_algorithm')}: {result.file_hash_algorithm}",
                    f"{t('verify.result.expected_file_hash')}: {result.file_hash_hex}",
                    f"{t('verify.result.actual_file_hash')}: {result.actual_file_hash_hex}",
                    f"{t('verify.result.public_fingerprint')}: {result.public_key_fingerprint}",
                    f"{t('verify.result.signature_size')}: {result.signature_size}",
                    f"{t('verify.result.created_at')}: {result.created_at_utc}",
                ]
            )
        )