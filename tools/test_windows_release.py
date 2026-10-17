"""Run the actual packaged executables and installation/recovery on a Windows runner."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import uuid

from github_updater import (control, extract_package, install, native_probe, parse_checksum,
                            recover, sha256, verify_app, atomic_json)


def main():
    if sys.platform != 'win32':
        raise SystemExit('This native test must run on Windows, not be simulated on Linux')
    parser = argparse.ArgumentParser()
    parser.add_argument('archive', type=Path)
    parser.add_argument('--browser', action='store_true')
    args = parser.parse_args()
    archive = args.archive.resolve()
    expected = parse_checksum(archive.with_name(archive.name+'.sha256').read_bytes(),archive.name)
    assert sha256(archive)==expected
    import zipfile
    with zipfile.ZipFile(archive) as z:
        version=json.loads(z.read('app/manifest.json'))['version']
    result={'platform':'Windows','package':archive.name,'version':version,'sha256':expected,'checks':[]}
    with tempfile.TemporaryDirectory(prefix='Plate Studio Windows Test ') as tmp:
        base=Path(tmp);stage=base/'extract'
        extract_package(archive,stage,version)
        for exe in ['PlateStudio.exe','PlateUpdater.exe']:
            subprocess.run([str(stage/'app'/exe),'--check'],check=True,timeout=60)
        subprocess.run('call "' + str(stage/'Start Plate.bat') + '" --check',
                       shell=True,check=True,cwd=stage,timeout=60)
        result['checks'].append('ZIP/checksum complete; both native EXEs and Start Plate.bat execute')
        root=base/'License Plate Studio';root.mkdir()
        personal={}
        for name in ['Projects/keep.json','Original Media/original.jpg','Processed Media/processed.png',
                     'Output/export.dat','Presets/custom.json','settings.json','export-preferences.json','history.json']:
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'preserve-'+name.encode());personal[name]=p.read_bytes()
        install(root,archive,version)
        verify_app(root/'app');native_probe(root/'app')
        result['checks'].append('real native package installed and runtime verified')
        ctl=control(root);txn=uuid.uuid4().hex;backup=ctl/'backups'/txn/'app';backup.parent.mkdir(parents=True)
        shutil.move(root/'app',backup)
        atomic_json(ctl/'transaction.json',{'id':txn,'status':'prepared','hadApp':True,'oldVersion':version})
        recover(root);native_probe(root/'app')
        assert not (ctl/'transaction.json').exists()
        for name,data in personal.items():assert(root/name).read_bytes()==data
        result['checks'].append('interrupted rename recovered native app; all personal marker files intact')
        process=subprocess.Popen([str(root/'app/PlateStudio.exe'),'--no-browser','--port','4186'],
                                 stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        try:
            deadline=time.monotonic()+60
            while True:
                if process.poll() is not None:raise AssertionError(process.stdout.read())
                try:
                    with urllib.request.urlopen('http://localhost:4186',timeout=2) as response:
                        assert ('v'+version).encode() in response.read()
                    break
                except OSError:
                    if time.monotonic()>deadline:raise
                    time.sleep(.2)
            with urllib.request.urlopen('http://localhost:4186/src/app.js') as response:
                assert response.headers.get_content_type()=='text/javascript'
            if args.browser:
                env=dict(os.environ);env['STUDIO_URL']='http://localhost:4186'
                subprocess.run(['node',str(Path(__file__).with_name('smoke.cjs'))],check=True,env=env)
                result['checks'].append('Chromium browser editing/save/reopen/export/import on frozen Windows host')
            result['checks'].append('native process serves real UI and ES module assets over loopback HTTP')
        finally:
            # Kill bootloader and child host together; terminate() alone can orphan a PyInstaller onefile child.
            subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True)
            process.communicate(timeout=15)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    try:
        main()
    except Exception:
        import traceback
        message=traceback.format_exc().replace('%','%25').replace('\r','%0D').replace('\n','%0A')
        print('::error::'+message,flush=True)
        raise
