import sys
sys.setrecursionlimit(5000)

block_cipher = None




a = Analysis(['buyma_spy_compact.py'],
             pathex=['/Users/victorchuah/Documents/python/spyma/Scraper/mac'],
             binaries=[],
             datas=[],
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
          name='buyma_spy',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='icon_purple.icns')
app = BUNDLE(exe,
             name='buyma_spy.app',
             icon='icon_purple.icns',
             bundle_identifier=None)
