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

app = BUNDLE(
    EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        name='QuickType',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=True,
        target_arch='x86_64',
        codesign_identity=None,
        entitlements_file=None,
    ),
    name='QuickType.app',
    bundle_identifier='com.damku1214.quicktype',
)
