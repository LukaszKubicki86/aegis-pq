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

from signer_app.services.key_details_service import (
    export_public_key_from_key_file,
    inspect_key_file,
)
from signer_app.ui.i18n import register_refresh, t


def _display(value: object, fallback: str | None = None) -> str:
    if fallback is None:
        fallback = t("common.not_available")
    if value is None:
        return fallback
    if isinstance(value, str) and not value.strip():
        return fallback
    return str(value)


def _policy_state_label(state: str | None) -> str:
    mapping = {
        "ok": t("details.policy.ok"),
        "due_soon": t("details.policy.due_soon"),
        "overdue": t("details.policy.overdue"),
        "rotated": t("details.policy.rotated"),
        "revoked": t("details.policy.revoked"),
        "unknown": t("details.policy.unknown"),
    }
    return mapping.get((state or "").lower(), _display(state))


class KeyDetailsScreen(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.key_file_edit = QLineEdit()
        self.export_path_edit = QLineEdit()

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)

        root_layout = QVBoxLayout(self)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        root_layout.addWidget(self.title_label)

        self.description_label = QLabel()
        self.description_label.setStyleSheet("font-size: 13px; color: #444;")
        self.description_label.setWordWrap(True)
        root_layout.addWidget(self.description_label)

        form = QFormLayout()

        key_file_row = QHBoxLayout()
        self.key_file_browse = QPushButton()
        self.key_file_browse.clicked.connect(self._choose_key_file)
        key_file_row.addWidget(self.key_file_edit)
        key_file_row.addWidget(self.key_file_browse)

        export_row = QHBoxLayout()
        self.export_browse = QPushButton()
        self.export_browse.clicked.connect(self._choose_export_path)
        export_row.addWidget(self.export_path_edit)
        export_row.addWidget(self.export_browse)

        self.key_file_label = QLabel()
        self.export_label = QLabel()

        form.addRow(self.key_file_label, key_file_row)
        form.addRow(self.export_label, export_row)

        root_layout.addLayout(form)

        button_row = QHBoxLayout()

        self.inspect_button = QPushButton()
        self.inspect_button.clicked.connect(self._inspect_key)
        button_row.addWidget(self.inspect_button)

        self.export_button = QPushButton()
        self.export_button.clicked.connect(self._export_public_key)
        button_row.addWidget(self.export_button)

        button_row.addStretch()
        root_layout.addLayout(button_row)

        root_layout.addSpacing(10)
        root_layout.addWidget(self.result_box)
        root_layout.addStretch()

        register_refresh(self.refresh_texts)
        self.refresh_texts()

    def refresh_texts(self) -> None:
        self.title_label.setText(t("details.title"))
        self.description_label.setText(t("details.description"))
        self.key_file_label.setText(t("details.key_file"))
        self.export_label.setText(t("details.export_public_key_to"))
        self.key_file_browse.setText(t("common.browse"))
        self.export_browse.setText(t("common.browse"))
        self.inspect_button.setText(t("details.inspect_button"))
        self.export_button.setText(t("details.export_button"))

    def _choose_key_file(self) -> None:
        selected_file, _ = QFileDialog.getOpenFileName(
            self,
            t("details.key_file"),
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if selected_file:
            self.key_file_edit.setText(selected_file)
            if not self.export_path_edit.text().strip():
                source = Path(selected_file)
                if source.name.endswith(".priv.json"):
                    default_export = source.with_name(source.name.replace(".priv.json", ".pub.json"))
                else:
                    default_export = source.with_suffix(".pub.json")
                self.export_path_edit.setText(str(default_export))

    def _choose_export_path(self) -> None:
        selected_file, _ = QFileDialog.getSaveFileName(
            self,
            t("details.export_public_key_to"),
            self.export_path_edit.text().strip() or "",
            "JSON Files (*.json);;All Files (*)",
        )
        if selected_file:
            self.export_path_edit.setText(selected_file)

    def _inspect_key(self) -> None:
        key_file_path = self.key_file_edit.text().strip()
        if not key_file_path:
            QMessageBox.warning(
                self,
                t("details.warning.key_file.title"),
                t("details.warning.key_file.body"),
            )
            return

        self.result_box.clear()

        try:
            result = inspect_key_file(key_file_path)
        except Exception as exc:
            self.result_box.setPlainText(f"{t('details.error.inspect.title')}.\n\nError: {exc}")
            QMessageBox.critical(self, t("details.error.inspect.title"), str(exc))
            return

        self.result_box.setPlainText(
            "\n".join(
                [
                    t("details.success.loaded"),
                    "",
                    f"{t('details.result.file_path')}: {result.file_path}",
                    f"{t('details.result.key_type')}: {_display(result.key_kind)}",
                    f"{t('details.result.storage_mode')}: {_display(result.storage_mode)}",
                    f"{t('details.result.format_version')}: {_display(result.format_version)}",
                    f"{t('details.result.standard')}: {_display(result.signature_standard)}",
                    f"{t('details.result.family')}: {_display(result.signature_family)}",
                    f"{t('details.result.algorithm')}: {_display(result.algorithm_name)}",
                    f"{t('details.result.backend')}: {_display(result.backend_algorithm_name)}",
                    f"{t('details.result.profile')}: {_display(result.profile_name)}",
                    f"{t('details.result.profile_description')}: {_display(result.profile_description)}",
                    f"{t('details.result.address')}: {_display(result.address)}",
                    f"{t('details.result.public_fingerprint')}: {_display(result.public_key_fingerprint)}",
                    f"{t('details.result.public_key_size')}: {result.public_key_size} bytes",
                    f"{t('details.result.private_key_present')}: {result.private_key_present}",
                    f"{t('details.result.private_key_encrypted')}: {result.private_key_encrypted}",
                    f"{t('details.result.key_status')}: {_display(result.key_status, t('common.active'))}",
                    f"{t('details.result.key_created_at')}: {_display(result.key_created_at_utc)}",
                    f"{t('details.result.rotated_from')}: {_display(result.rotated_from, t('common.not_applicable'))}",
                    f"{t('details.result.rotation_reason')}: {_display(result.rotation_reason, t('common.not_specified'))}",
                    "",
                    f"{t('details.result.rotation_policy')}: {_display(result.rotation_policy_name)}",
                    f"{t('details.result.policy_state')}: {_policy_state_label(result.rotation_policy_state)}",
                    f"{t('details.result.policy_message')}: {_display(result.rotation_policy_message)}",
                    f"{t('details.result.rotation_window')}: {_display(result.recommended_rotation_after_days)} days",
                    f"{t('details.result.key_age')}: {_display(result.key_age_days)} days",
                    f"{t('details.result.rotation_due_at')}: {_display(result.rotation_due_at_utc)}",
                    f"{t('details.result.days_until_due')}: {_display(result.rotation_days_until_due)}",
                ]
            )
        )

    def _export_public_key(self) -> None:
        key_file_path = self.key_file_edit.text().strip()
        export_path = self.export_path_edit.text().strip() or None

        if not key_file_path:
            QMessageBox.warning(
                self,
                t("details.warning.key_file.title"),
                t("details.warning.key_file_export.body"),
            )
            return

        try:
            exported_path = export_public_key_from_key_file(
                source_key_path=key_file_path,
                output_path=export_path,
            )
        except Exception as exc:
            QMessageBox.critical(self, t("details.error.export.title"), str(exc))
            return

        existing_text = self.result_box.toPlainText().strip()
        lines = [existing_text] if existing_text else []
        lines.extend(
            [
                "",
                t("details.success.exported"),
                f"{t('details.result.export_path')}: {exported_path}",
            ]
        )
        self.result_box.setPlainText("\n".join(lines).strip())