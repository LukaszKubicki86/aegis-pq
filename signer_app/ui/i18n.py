from __future__ import annotations

from typing import Callable

_CURRENT_LANGUAGE = "pl"
_REFRESH_CALLBACKS: list[Callable[[], None]] = []


_TRANSLATIONS: dict[str, dict[str, str]] = {
    "pl": {
        "app.window_title": "Aegis Signer",
        "app.version": "Demo build",
        "app.language": "Język",
        "app.nav.home": "Start",
        "app.nav.generate_key": "Generowanie klucza",
        "app.nav.key_details": "Szczegóły klucza",
        "app.nav.rotate_key": "Rotacja klucza",
        "app.nav.sign_file": "Podpis pliku",
        "app.nav.verify_signature": "Weryfikacja podpisu",

        "language.polish": "Polski",
        "language.english": "English",

        "common.browse": "Przeglądaj",
        "common.inspect": "Sprawdź",
        "common.export": "Eksportuj",
        "common.sign": "Podpisz",
        "common.verify": "Zweryfikuj",
        "common.not_available": "Brak danych",
        "common.not_applicable": "Nie dotyczy",
        "common.not_specified": "Nie podano",
        "common.active": "Aktywny",
        "common.encrypted": "zaszyfrowany",
        "common.plaintext": "jawny",

        "home.title": "Aegis Signer",
        "home.subtitle": "Podpisy post-quantum, weryfikacja oraz zarządzanie kluczami zgodne z FIPS 204",
        "home.section.overview.title": "Do czego służy ta aplikacja",
        "home.section.overview.body": (
            "Aegis Signer pozwala generować klucze post-quantum ML-DSA, sprawdzać metadane kluczy, "
            "podpisywać pliki i weryfikować podpisy. Aplikacja korzysta z jasnych zasad rotacji kluczy "
            "i pokazuje, czy dany klucz może być jeszcze używany do podpisu."
        ),
        "home.section.standard.title": "Standard i zgodność",
        "home.section.standard.body": (
            "Podpisy opierają się na FIPS 204 i rodzinie ML-DSA. "
            "UI jest przygotowane pod demo, ale zachowuje twarde zasady projektu."
        ),
        "home.section.profiles.title": "Profile bezpieczeństwa",
        "home.section.profiles.body": (
            "standard → ML-DSA-44: najmniejszy i najszybszy profil\n"
            "hardened → ML-DSA-65: mocniejszy profil z dobrym balansem\n"
            "max → ML-DSA-87: największy i najbardziej konserwatywny profil"
        ),
        "home.section.rotation.title": "Polityka rotacji",
        "home.section.rotation.body": (
            "Klucze mają status, datę utworzenia i ocenę polityki rotacji. "
            "Klucz przeterminowany, zrotowany, cofnięty lub niekompletny nie powinien być użyty do podpisu."
        ),
        "home.section.demo.title": "Co pokazać na demo",
        "home.section.demo.body": (
            "1. Wygeneruj klucz\n"
            "2. Pokaż szczegóły i stan polityki\n"
            "3. Podpisz plik\n"
            "4. Zweryfikuj podpis\n"
            "5. Zrób rotację klucza i pokaż blokadę starego klucza"
        ),

        "generate.title": "Generowanie klucza PQ",
        "generate.description": "Utwórz parę kluczy post-quantum dla wybranego profilu bezpieczeństwa.",
        "generate.output_dir": "Katalog wyjściowy",
        "generate.key_name": "Nazwa klucza",
        "generate.profile": "Profil bezpieczeństwa",
        "generate.password": "Hasło (opcjonalnie)",
        "generate.password_placeholder": "Opcjonalnie: zaszyfruj klucz prywatny hasłem",
        "generate.button": "Wygeneruj klucz PQ",
        "generate.warning.output_dir.title": "Brak katalogu wyjściowego",
        "generate.warning.output_dir.body": "Wybierz katalog wyjściowy.",
        "generate.warning.key_name.title": "Brak nazwy klucza",
        "generate.warning.key_name.body": "Podaj nazwę klucza.",
        "generate.error.title": "Generowanie klucza nie powiodło się",
        "generate.success.title": "Klucz PQ został wygenerowany poprawnie.",
        "generate.result.profile": "Profil",
        "generate.result.profile_description": "Opis profilu",
        "generate.result.algorithm": "Algorytm",
        "generate.result.backend": "Backend",
        "generate.result.storage": "Sposób przechowywania klucza prywatnego",
        "generate.result.public_key_size": "Rozmiar klucza publicznego",
        "generate.result.private_key_size": "Rozmiar klucza prywatnego",
        "generate.result.public_fingerprint": "Fingerprint klucza publicznego",
        "generate.result.public_key_path": "Ścieżka klucza publicznego",
        "generate.result.private_key_path": "Ścieżka klucza prywatnego",

        "details.title": "Szczegóły klucza",
        "details.description": (
            "Sprawdź plik klucza publicznego lub prywatnego, aktywny profil bezpieczeństwa "
            "oraz stan polityki rotacji."
        ),
        "details.key_file": "Plik klucza",
        "details.export_public_key_to": "Eksport klucza publicznego do",
        "details.inspect_button": "Sprawdź klucz",
        "details.export_button": "Eksportuj klucz publiczny",
        "details.warning.key_file.title": "Brak pliku klucza",
        "details.warning.key_file.body": "Wybierz plik klucza.",
        "details.warning.key_file_export.body": "Najpierw wybierz plik klucza.",
        "details.error.inspect.title": "Sprawdzenie klucza nie powiodło się",
        "details.error.export.title": "Eksport klucza publicznego nie powiódł się",
        "details.success.loaded": "Plik klucza został wczytany poprawnie.",
        "details.success.exported": "Klucz publiczny został wyeksportowany poprawnie.",
        "details.result.file_path": "Ścieżka pliku",
        "details.result.key_type": "Typ klucza",
        "details.result.storage_mode": "Tryb przechowywania",
        "details.result.format_version": "Wersja formatu",
        "details.result.standard": "Standard",
        "details.result.family": "Rodzina",
        "details.result.algorithm": "Algorytm",
        "details.result.backend": "Algorytm bazowy",
        "details.result.profile": "Profil bezpieczeństwa",
        "details.result.profile_description": "Opis profilu",
        "details.result.address": "Adres",
        "details.result.public_fingerprint": "Fingerprint klucza publicznego",
        "details.result.public_key_size": "Rozmiar klucza publicznego",
        "details.result.private_key_present": "Czy jest klucz prywatny",
        "details.result.private_key_encrypted": "Czy klucz prywatny jest zaszyfrowany",
        "details.result.key_status": "Status klucza",
        "details.result.key_created_at": "Data utworzenia klucza",
        "details.result.rotated_from": "Zrotowany z",
        "details.result.rotation_reason": "Powód rotacji",
        "details.result.rotation_policy": "Polityka rotacji",
        "details.result.policy_state": "Stan polityki",
        "details.result.policy_message": "Komunikat polityki",
        "details.result.rotation_window": "Zalecane okno rotacji",
        "details.result.key_age": "Wiek klucza",
        "details.result.rotation_due_at": "Zalecana data rotacji",
        "details.result.days_until_due": "Dni do zalecanej rotacji",
        "details.result.export_path": "Ścieżka eksportu",

        "details.policy.ok": "W ramach polityki",
        "details.policy.due_soon": "Rotacja wkrótce",
        "details.policy.overdue": "Rotacja wymagana",
        "details.policy.rotated": "Klucz już zrotowany",
        "details.policy.revoked": "Klucz cofnięty",
        "details.policy.unknown": "Stan nieznany",

        "rotate.title": "Rotacja klucza",
        "rotate.description": (
            "Wykonaj rotację prywatnego klucza PQ. Bieżący klucz zostanie oznaczony jako zrotowany, "
            "a nowa para kluczy zostanie utworzona z tym samym profilem."
        ),
        "rotate.private_key": "Klucz prywatny",
        "rotate.output_dir": "Katalog wyjściowy",
        "rotate.new_key_name": "Nowa nazwa klucza",
        "rotate.current_password": "Hasło bieżącego klucza",
        "rotate.current_password_placeholder": "Wymagane tylko wtedy, gdy bieżący klucz jest zaszyfrowany",
        "rotate.new_password": "Hasło nowego klucza",
        "rotate.new_password_placeholder": "Opcjonalne hasło dla nowego zrotowanego klucza prywatnego",
        "rotate.reason": "Powód rotacji",
        "rotate.reason_placeholder": "Przykład: planowa rotacja, podejrzenie ujawnienia, zmiana polityki",
        "rotate.button": "Wykonaj rotację klucza",
        "rotate.warning.private_key.title": "Brak klucza prywatnego",
        "rotate.warning.private_key.body": "Wybierz plik klucza prywatnego.",
        "rotate.warning.new_name.title": "Brak nowej nazwy klucza",
        "rotate.warning.new_name.body": "Podaj nową nazwę klucza.",
        "rotate.error.title": "Rotacja klucza nie powiodła się",
        "rotate.error.status": "Rotacja klucza nie powiodła się.",
        "rotate.success.status": "Rotacja klucza zakończona powodzeniem.",
        "rotate.result.old_private_key": "Zaktualizowany stary klucz prywatny",
        "rotate.result.new_private_key": "Ścieżka nowego klucza prywatnego",
        "rotate.result.new_public_key": "Ścieżka nowego klucza publicznego",
        "rotate.result.old_address": "Stary adres",
        "rotate.result.new_address": "Nowy adres",
        "rotate.result.profile": "Profil",
        "rotate.result.profile_description": "Opis profilu",
        "rotate.result.algorithm": "Algorytm",
        "rotate.result.backend": "Backend",
        "rotate.result.public_fingerprint": "Nowy fingerprint klucza publicznego",
        "rotate.result.private_storage": "Nowy sposób przechowywania klucza prywatnego",
        "rotate.result.key_status": "Status nowego klucza",
        "rotate.result.key_created_at": "Data utworzenia klucza",
        "rotate.result.rotated_from": "Zrotowany z",
        "rotate.result.rotation_reason": "Powód rotacji",

        "sign.title": "Podpis pliku",
        "sign.description": (
            "Podpisz plik kluczem prywatnym. Podpis potwierdza autentyczność i integralność, "
            "ale nie szyfruje pliku."
        ),
        "sign.file": "Plik",
        "sign.private_key": "Klucz prywatny",
        "sign.password": "Hasło (opcjonalnie)",
        "sign.password_placeholder": "Wymagane tylko dla zaszyfrowanych kluczy prywatnych",
        "sign.signature_output": "Plik wyjściowy podpisu (opcjonalnie)",
        "sign.button": "Podpisz",
        "sign.warning.file.title": "Brak pliku",
        "sign.warning.file.body": "Wybierz plik do podpisania.",
        "sign.warning.private_key.title": "Brak klucza prywatnego",
        "sign.warning.private_key.body": "Wybierz plik klucza prywatnego.",
        "sign.error.title": "Podpisywanie nie powiodło się",
        "sign.error.status": "Podpisywanie nie powiodło się.",
        "sign.error.file_path": "Ścieżka pliku",
        "sign.error.private_key_path": "Ścieżka klucza prywatnego",
        "sign.success.status": "Plik został podpisany poprawnie.",
        "sign.result.file_path": "Ścieżka pliku",
        "sign.result.signature_path": "Ścieżka podpisu",
        "sign.result.profile": "Profil",
        "sign.result.profile_description": "Opis profilu",
        "sign.result.standard": "Standard",
        "sign.result.family": "Rodzina",
        "sign.result.algorithm": "Algorytm",
        "sign.result.backend": "Backend",
        "sign.result.hash_algorithm": "Algorytm skrótu",
        "sign.result.file_hash": "Skrót pliku",
        "sign.result.public_fingerprint": "Fingerprint klucza publicznego",
        "sign.result.signature_size": "Rozmiar podpisu",
        "sign.result.created_at": "Data utworzenia",

        "verify.title": "Weryfikacja podpisu",
        "verify.description": (
            "Sprawdź, czy podpis pasuje do wskazanego pliku. "
            "Jeśli plik został zmieniony po podpisaniu, weryfikacja powinna się nie udać."
        ),
        "verify.file": "Plik",
        "verify.signature": "Podpis",
        "verify.button": "Zweryfikuj",
        "verify.warning.file.title": "Brak pliku",
        "verify.warning.file.body": "Wybierz plik do weryfikacji.",
        "verify.warning.signature.title": "Brak podpisu",
        "verify.warning.signature.body": "Wybierz plik podpisu.",
        "verify.error.title": "Weryfikacja nie powiodła się",
        "verify.result.valid": "POPRAWNY",
        "verify.result.invalid": "NIEPOPRAWNY",
        "verify.result.title": "Wynik weryfikacji",
        "verify.result.message": "Komunikat",
        "verify.result.file_path": "Ścieżka pliku",
        "verify.result.signature_path": "Ścieżka podpisu",
        "verify.result.profile": "Profil",
        "verify.result.profile_description": "Opis profilu",
        "verify.result.standard": "Standard",
        "verify.result.family": "Rodzina",
        "verify.result.algorithm": "Algorytm",
        "verify.result.backend": "Backend",
        "verify.result.hash_algorithm": "Algorytm skrótu",
        "verify.result.expected_file_hash": "Oczekiwany skrót pliku",
        "verify.result.actual_file_hash": "Rzeczywisty skrót pliku",
        "verify.result.public_fingerprint": "Fingerprint klucza publicznego",
        "verify.result.signature_size": "Rozmiar podpisu",
        "verify.result.created_at": "Data utworzenia",
    },
    "en": {
        "app.window_title": "Aegis Signer",
        "app.version": "Demo build",
        "app.language": "Language",
        "app.nav.home": "Home",
        "app.nav.generate_key": "Generate Key",
        "app.nav.key_details": "Key Details",
        "app.nav.rotate_key": "Rotate Key",
        "app.nav.sign_file": "Sign File",
        "app.nav.verify_signature": "Verify Signature",

        "language.polish": "Polski",
        "language.english": "English",

        "common.browse": "Browse",
        "common.inspect": "Inspect",
        "common.export": "Export",
        "common.sign": "Sign",
        "common.verify": "Verify",
        "common.not_available": "Not available",
        "common.not_applicable": "Not applicable",
        "common.not_specified": "Not specified",
        "common.active": "Active",
        "common.encrypted": "encrypted",
        "common.plaintext": "plaintext",

        "home.title": "Aegis Signer",
        "home.subtitle": "Post-quantum signing, verification, and key management aligned with FIPS 204",
        "home.section.overview.title": "What this app does",
        "home.section.overview.body": (
            "Aegis Signer lets you generate ML-DSA post-quantum keys, inspect key metadata, "
            "sign files, and verify signatures. The app also applies a clear key-rotation policy "
            "and shows whether a key is still acceptable for signing."
        ),
        "home.section.standard.title": "Standard and alignment",
        "home.section.standard.body": (
            "Signatures are based on FIPS 204 and the ML-DSA family. "
            "The UI is demo-ready, but it still preserves the project's hard security rules."
        ),
        "home.section.profiles.title": "Security profiles",
        "home.section.profiles.body": (
            "standard → ML-DSA-44: smallest and fastest profile\n"
            "hardened → ML-DSA-65: stronger balanced profile\n"
            "max → ML-DSA-87: largest and most conservative profile"
        ),
        "home.section.rotation.title": "Rotation policy",
        "home.section.rotation.body": (
            "Keys carry a status, creation date, and policy evaluation. "
            "An overdue, rotated, revoked, or incomplete key should not be used for signing."
        ),
        "home.section.demo.title": "Recommended demo flow",
        "home.section.demo.body": (
            "1. Generate a key\n"
            "2. Show key details and policy state\n"
            "3. Sign a file\n"
            "4. Verify the signature\n"
            "5. Rotate the key and show that the old key is blocked"
        ),

        "generate.title": "Generate PQ Key",
        "generate.description": "Create a post-quantum key pair for the selected security profile.",
        "generate.output_dir": "Output directory",
        "generate.key_name": "Key name",
        "generate.profile": "Security profile",
        "generate.password": "Password (optional)",
        "generate.password_placeholder": "Optional: encrypt the private key with a password",
        "generate.button": "Generate PQ Key",
        "generate.warning.output_dir.title": "Missing output directory",
        "generate.warning.output_dir.body": "Please choose an output directory.",
        "generate.warning.key_name.title": "Missing key name",
        "generate.warning.key_name.body": "Please enter a key name.",
        "generate.error.title": "Key generation failed",
        "generate.success.title": "PQ key generated successfully.",
        "generate.result.profile": "Profile",
        "generate.result.profile_description": "Profile description",
        "generate.result.algorithm": "Algorithm",
        "generate.result.backend": "Backend",
        "generate.result.storage": "Private key storage",
        "generate.result.public_key_size": "Public key size",
        "generate.result.private_key_size": "Private key size",
        "generate.result.public_fingerprint": "Public fingerprint",
        "generate.result.public_key_path": "Public key path",
        "generate.result.private_key_path": "Private key path",

        "details.title": "Key Details",
        "details.description": (
            "Inspect a public or private key file, review the active security profile, "
            "and check whether the key is still within the recommended rotation window."
        ),
        "details.key_file": "Key file",
        "details.export_public_key_to": "Export public key to",
        "details.inspect_button": "Inspect Key",
        "details.export_button": "Export Public Key",
        "details.warning.key_file.title": "Missing key file",
        "details.warning.key_file.body": "Please choose a key file.",
        "details.warning.key_file_export.body": "Please choose a key file first.",
        "details.error.inspect.title": "Key inspection failed",
        "details.error.export.title": "Public key export failed",
        "details.success.loaded": "Key file loaded successfully.",
        "details.success.exported": "Public key exported successfully.",
        "details.result.file_path": "File path",
        "details.result.key_type": "Key type",
        "details.result.storage_mode": "Storage mode",
        "details.result.format_version": "Format version",
        "details.result.standard": "Standard",
        "details.result.family": "Family",
        "details.result.algorithm": "Algorithm",
        "details.result.backend": "Underlying algorithm",
        "details.result.profile": "Security profile",
        "details.result.profile_description": "Profile description",
        "details.result.address": "Address",
        "details.result.public_fingerprint": "Public fingerprint",
        "details.result.public_key_size": "Public key size",
        "details.result.private_key_present": "Private key present",
        "details.result.private_key_encrypted": "Private key encrypted",
        "details.result.key_status": "Key status",
        "details.result.key_created_at": "Key created at",
        "details.result.rotated_from": "Rotated from",
        "details.result.rotation_reason": "Rotation reason",
        "details.result.rotation_policy": "Rotation policy",
        "details.result.policy_state": "Policy state",
        "details.result.policy_message": "Policy message",
        "details.result.rotation_window": "Recommended rotation window",
        "details.result.key_age": "Key age",
        "details.result.rotation_due_at": "Recommended rotation date",
        "details.result.days_until_due": "Days until rotation due",
        "details.result.export_path": "Export path",

        "details.policy.ok": "Within policy",
        "details.policy.due_soon": "Rotation due soon",
        "details.policy.overdue": "Rotation overdue",
        "details.policy.rotated": "Already rotated",
        "details.policy.revoked": "Revoked",
        "details.policy.unknown": "Unknown",

        "rotate.title": "Rotate Key",
        "rotate.description": (
            "Rotate a private PQ key. The current key will be marked as rotated, "
            "and a new key pair will be generated with the same profile."
        ),
        "rotate.private_key": "Private key",
        "rotate.output_dir": "Output directory",
        "rotate.new_key_name": "New key name",
        "rotate.current_password": "Current key password",
        "rotate.current_password_placeholder": "Required only if the current key is encrypted",
        "rotate.new_password": "New key password",
        "rotate.new_password_placeholder": "Optional password for the new rotated private key",
        "rotate.reason": "Rotation reason",
        "rotate.reason_placeholder": "Example: scheduled rotation, suspected exposure, policy update",
        "rotate.button": "Rotate Key",
        "rotate.warning.private_key.title": "Missing private key",
        "rotate.warning.private_key.body": "Please choose a private key file.",
        "rotate.warning.new_name.title": "Missing new key name",
        "rotate.warning.new_name.body": "Please enter a new key name.",
        "rotate.error.title": "Key rotation failed",
        "rotate.error.status": "Key rotation failed.",
        "rotate.success.status": "Key rotated successfully.",
        "rotate.result.old_private_key": "Updated old private key",
        "rotate.result.new_private_key": "New private key path",
        "rotate.result.new_public_key": "New public key path",
        "rotate.result.old_address": "Old address",
        "rotate.result.new_address": "New address",
        "rotate.result.profile": "Profile",
        "rotate.result.profile_description": "Profile description",
        "rotate.result.algorithm": "Algorithm",
        "rotate.result.backend": "Backend",
        "rotate.result.public_fingerprint": "New public fingerprint",
        "rotate.result.private_storage": "New private key storage",
        "rotate.result.key_status": "New key status",
        "rotate.result.key_created_at": "Key created at",
        "rotate.result.rotated_from": "Rotated from",
        "rotate.result.rotation_reason": "Rotation reason",

        "sign.title": "Sign File",
        "sign.description": (
            "Sign a file with your private key. Signing proves authenticity and integrity. "
            "It does not encrypt the file."
        ),
        "sign.file": "File",
        "sign.private_key": "Private key",
        "sign.password": "Password (optional)",
        "sign.password_placeholder": "Required only for encrypted private keys",
        "sign.signature_output": "Signature output (optional)",
        "sign.button": "Sign",
        "sign.warning.file.title": "Missing file",
        "sign.warning.file.body": "Please choose a file to sign.",
        "sign.warning.private_key.title": "Missing private key",
        "sign.warning.private_key.body": "Please choose a private key file.",
        "sign.error.title": "Signing failed",
        "sign.error.status": "Signing failed.",
        "sign.error.file_path": "File path",
        "sign.error.private_key_path": "Private key path",
        "sign.success.status": "File signed successfully.",
        "sign.result.file_path": "File path",
        "sign.result.signature_path": "Signature path",
        "sign.result.profile": "Profile",
        "sign.result.profile_description": "Profile description",
        "sign.result.standard": "Standard",
        "sign.result.family": "Family",
        "sign.result.algorithm": "Algorithm",
        "sign.result.backend": "Backend",
        "sign.result.hash_algorithm": "Hash algorithm",
        "sign.result.file_hash": "File hash",
        "sign.result.public_fingerprint": "Public fingerprint",
        "sign.result.signature_size": "Signature size",
        "sign.result.created_at": "Created at",

        "verify.title": "Verify Signature",
        "verify.description": (
            "Verify whether a signature matches the selected file. "
            "If the file changes after signing, verification should fail."
        ),
        "verify.file": "File",
        "verify.signature": "Signature",
        "verify.button": "Verify",
        "verify.warning.file.title": "Missing file",
        "verify.warning.file.body": "Please choose a file to verify.",
        "verify.warning.signature.title": "Missing signature",
        "verify.warning.signature.body": "Please choose a signature file.",
        "verify.error.title": "Verification failed",
        "verify.result.valid": "VALID",
        "verify.result.invalid": "INVALID",
        "verify.result.title": "Verification result",
        "verify.result.message": "Message",
        "verify.result.file_path": "File path",
        "verify.result.signature_path": "Signature path",
        "verify.result.profile": "Profile",
        "verify.result.profile_description": "Profile description",
        "verify.result.standard": "Standard",
        "verify.result.family": "Family",
        "verify.result.algorithm": "Algorithm",
        "verify.result.backend": "Backend",
        "verify.result.hash_algorithm": "Hash algorithm",
        "verify.result.expected_file_hash": "Expected file hash",
        "verify.result.actual_file_hash": "Actual file hash",
        "verify.result.public_fingerprint": "Public fingerprint",
        "verify.result.signature_size": "Signature size",
        "verify.result.created_at": "Created at",
    },
}


def get_language() -> str:
    return _CURRENT_LANGUAGE


def set_language(language: str) -> None:
    global _CURRENT_LANGUAGE

    if language not in _TRANSLATIONS:
        return

    if language == _CURRENT_LANGUAGE:
        return

    _CURRENT_LANGUAGE = language
    for callback in list(_REFRESH_CALLBACKS):
        callback()


def t(key: str, default: str | None = None) -> str:
    language_map = _TRANSLATIONS.get(_CURRENT_LANGUAGE, {})
    if key in language_map:
        return language_map[key]

    english_map = _TRANSLATIONS.get("en", {})
    if key in english_map:
        return english_map[key]

    return default if default is not None else key


def register_refresh(callback: Callable[[], None]) -> None:
    if callback not in _REFRESH_CALLBACKS:
        _REFRESH_CALLBACKS.append(callback)