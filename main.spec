# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\PC\\Documents\\GitHub\\NaverCafe_Macro'],
             binaries=[('./driver/chromedriver.exe', './driver')],
             datas=[('./ui_files/login.ui', './ui_files'), ('./ui_files/editwindow.ui', './ui_files'), ('./ui_files/mainwindow_ex.ui', './ui_files'), ('./ui_files/naverlogin.ui', './ui_files')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='icon.ico')