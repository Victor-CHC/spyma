# pyinstaller mac terminal command
# pyinstaller --onefile buyma_spy_compact.spec --exclude-module matplotlib --exclude-module scipy --exclude-module matplotlib --exclude-module pyqt5

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
             excludes=[

             ],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

maybe_wanted = [
('libtbb.dylib', '/opt/anaconda3/lib/libtbb.dylib', 'BINARY'),
('libiomp5.dylib', '/opt/anaconda3/lib/libiomp5.dylib', 'BINARY'),
('liblzma.5.dylib', '/opt/anaconda3/lib/liblzma.5.dylib', 'BINARY'),
('libz.1.dylib', '/opt/anaconda3/lib/libz.1.dylib', 'BINARY'),
('libcrypto.1.1.dylib', '/opt/anaconda3/lib/libcrypto.1.1.dylib', 'BINARY'),
('libreadline.7.dylib', '/opt/anaconda3/lib/libreadline.7.dylib', 'BINARY'),
('libffi.6.dylib', '/opt/anaconda3/lib/libffi.6.dylib', 'BINARY'),
('libjpeg.9.dylib', '/opt/anaconda3/lib/libjpeg.9.dylib', 'BINARY'),
('libtiff.5.dylib', '/opt/anaconda3/lib/libtiff.5.dylib', 'BINARY'),
('libfreetype.6.dylib', '/opt/anaconda3/lib/libfreetype.6.dylib', 'BINARY'),
('libexslt.0.dylib', '/opt/anaconda3/lib/libexslt.0.dylib', 'BINARY'),
('libxslt.1.dylib', '/opt/anaconda3/lib/libxslt.1.dylib', 'BINARY'),
('libxml2.2.dylib', '/opt/anaconda3/lib/libxml2.2.dylib', 'BINARY'),
('libncursesw.6.dylib', '/opt/anaconda3/lib/libncursesw.6.dylib', 'BINARY'),
('libc++.1.dylib', '/opt/anaconda3/lib/libc++.1.dylib', 'BINARY'),
('libgfortran.3.dylib', '/opt/anaconda3/lib/libgfortran.3.dylib', 'BINARY'),
('libzmq.5.dylib', '/opt/anaconda3/lib/libzmq.5.dylib', 'BINARY'),
('libhdf5.103.dylib', '/opt/anaconda3/lib/libhdf5.103.dylib', 'BINARY'),
('libbz2.dylib', '/opt/anaconda3/lib/libbz2.dylib', 'BINARY'),
('liblzo2.2.dylib', '/opt/anaconda3/lib/liblzo2.2.dylib', 'BINARY'),
('libblosc.1.dylib', '/opt/anaconda3/lib/libblosc.1.dylib', 'BINARY'),
('libtk8.6.dylib', '/opt/anaconda3/lib/libtk8.6.dylib', 'BINARY'),
('libtcl8.6.dylib', '/opt/anaconda3/lib/libtcl8.6.dylib', 'BINARY'),
('libtinfow.6.dylib', '/opt/anaconda3/lib/libtinfow.6.dylib', 'BINARY'),
('libzstd.1.3.7.dylib', '/opt/anaconda3/lib/libzstd.1.3.7.dylib', 'BINARY'),
('libiconv.2.dylib', '/opt/anaconda3/lib/libiconv.2.dylib', 'BINARY'),
('libc++abi.1.dylib', '/opt/anaconda3/lib/libc++abi.1.dylib', 'BINARY'),
('libgcc_s.1.dylib', '/opt/anaconda3/lib/libgcc_s.1.dylib', 'BINARY'),
('libquadmath.0.dylib', '/opt/anaconda3/lib/libquadmath.0.dylib', 'BINARY'),
('libsodium.23.dylib', '/opt/anaconda3/lib/libsodium.23.dylib', 'BINARY'),
('libicudata.58.dylib', '/opt/anaconda3/lib/libicudata.58.dylib', 'BINARY'),
('libicuuc.58.dylib', '/opt/anaconda3/lib/libicuuc.58.dylib', 'BINARY'),
('libicui18n.58.dylib', '/opt/anaconda3/lib/libicui18n.58.dylib', 'BINARY'),
('liblz4.1.dylib', '/opt/anaconda3/lib/liblz4.1.dylib', 'BINARY'),
('libpng16.16.dylib', '/opt/anaconda3/lib/libpng16.16.dylib', 'BINARY'),
('libsnappy.1.dylib', '/opt/anaconda3/lib/libsnappy.1.dylib', 'BINARY')
]

unwanted = [

('libsqlite3.0.dylib', '/opt/anaconda3/lib/libsqlite3.0.dylib', 'BINARY'),
('libQt5Widgets.5.dylib', '/opt/anaconda3/lib/libQt5Widgets.5.dylib', 'BINARY'),
('libQt5Gui.5.dylib', '/opt/anaconda3/lib/libQt5Gui.5.dylib', 'BINARY'),
('libQt5Core.5.dylib', '/opt/anaconda3/lib/libQt5Core.5.dylib', 'BINARY'),
('libQt5Svg.5.dylib', '/opt/anaconda3/lib/libQt5Svg.5.dylib', 'BINARY'),
]

a.binaries = [x for x in a.binaries if x not in unwanted]

print('scripts')
for s in a.scripts:
    print(s)

print('zipfiles')
for z in a.zipfiles:
    print(z)

print('hiddenimports')
for hi in a.hiddenimports:
    print(hi)

print('datas')
for d in a.datas:
    print(d)

print('excludes')
for e in a.excludes:
    print(e)
    
print('hookspath')
for hp in a.hookspath:
    print(hp)

scripts_keep = [
('pyi_rth_twisted', '/opt/anaconda3/lib/python3.7/site-packages/_pyinstaller_hooks_contrib/hooks/rthooks/pyi_rth_twisted.py', 'PYSOURCE'),
('pyi_rth__tkinter', '/opt/anaconda3/lib/python3.7/site-packages/PyInstaller/hooks/rthooks/pyi_rth__tkinter.py', 'PYSOURCE'),
('buyma_spy_compact', '/Users/victorchuah/Documents/python/spyma/Scraper/mac_compact/buyma_spy_compact.py', 'PYSOURCE')
]

a.scripts = [x for x in a.scripts if x in scripts_keep]

datas_keep = [
('base_library.zip', '/Users/victorchuah/Documents/python/spyma/Scraper/mac_compact/build/buyma_spy_compact/base_library.zip', 'DATA')
]

#a.datas = [x for x in a.datas if x in datas_keep]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.excludes,
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
