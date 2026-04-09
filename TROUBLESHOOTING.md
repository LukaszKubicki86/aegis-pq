# Troubleshooting

## Recommended environment

Use a **clean virtual environment** for the public demo.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements-demo.txt
```

## `QFont::setPointSize: Point size <= 0 (-1)`

This can appear as a Qt runtime warning on some systems. If the UI still renders and works correctly, it is usually not a functional blocker for the demo.

## `liboqs-python faulthandler is disabled`

This can appear as an informational runtime message from the dependency layer. If key generation, signing, and verification still work, treat it as a dependency-level note rather than an application failure.

## `pytest` fails with `collections.Callable`

On some Windows systems, an old global `pyreadline` installation can break `pytest` under newer Python versions.

### Recommended fix

Use a clean virtual environment and run pytest through Python:

```powershell
python -m pytest tests/test_signer_key_service.py tests/test_signer_file_sign_service.py tests/test_signer_file_verify_service.py tests/test_demo_signer_flow_service.py tests/test_key_rotation_policy.py -q
```

### Optional cleanup of global environment

```powershell
python -m pip uninstall pyreadline -y
```
