# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for לימוד קליל — builds a single standalone Windows .exe."""
from PyInstaller.utils.hooks import collect_all

datas = [("static", "static")]
binaries = []
hiddenimports = []

# bundle packages that load resources / submodules dynamically
for pkg in ("webview", "anthropic", "pptx", "docx", "pypdf"):
    d, b, h = collect_all(pkg)
    datas += d
    binaries += b
    hiddenimports += h

a = Analysis(
    ["desktop.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports + ["clr_loader", "bottle"],
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter", "pyinstaller"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="LimodKalil",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,           # no black console window
    icon="app.ico",
)
