# -*- mode: python ; coding: utf-8 -*-
# PyInstaller build spec: one-file standalone app for Windows and Linux.
# Build it with build_exe.bat (Windows) or build_linux.sh (Linux).
# PyInstaller cannot cross-compile: build each version on its own OS.

import sys

IS_WINDOWS = sys.platform.startswith("win")

# Windows: windowed app (no black console, errors via a message box).
# Linux: keep the console so the user can see the URL / stop the app.
a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=[],
    datas=[("static", "static")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="PythonTutor",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=not IS_WINDOWS,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
