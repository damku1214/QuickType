# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['quicktype.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],                  # <-- empty! binaries/datas go to COLLECT instead
    exclude_binaries=True,  # <-- required for onedir mode
    name='QuickType',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch='x86_64',
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='QuickType',
)

app = BUNDLE(
    coll,                # <-- pass COLLECT, not EXE
    name='QuickType.app',
    bundle_identifier='com.damku1214.quicktype',
)