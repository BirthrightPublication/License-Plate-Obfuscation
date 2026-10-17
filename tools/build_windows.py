"""Local Windows entry point for standardized, complete release packages."""
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    if sys.platform != 'win32':
        raise SystemExit('A Windows x64 build host is required; no Windows EXE was built on Linux.')
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix='plate-build-env-') as tmp:
        env = Path(tmp)
        subprocess.run([sys.executable, '-m', 'venv', str(env)], check=True)
        python = env / 'Scripts/python.exe'
        subprocess.run([str(python), '-m', 'pip', 'install', '-r',
                        str(root / 'tools/requirements-windows-build.txt')], check=True)
        subprocess.run([str(python), str(root / 'tools/windows_release.py')], check=True)


if __name__ == '__main__':
    main()
