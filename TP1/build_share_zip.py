"""Create a source-only ZIP that another Windows PC can install and run."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

project = Path(__file__).resolve().parent
archive_path = project.parent / "TP1-partage.zip"
files = [
    ".env.example",
    ".gitignore",
    ".vscode/settings.json",
    "README.md",
    "README_PARTAGE.md",
    "app.py",
    "build_share_zip.py",
    "exemples/bibliotheque.sql",
    "package-lock.json",
    "package.json",
    "poetry.lock",
    "pyproject.toml",
    "requirements.txt",
    "static/css/custom.css",
    "static/css/input.css",
    "static/dist/css/style.css",
    "templates/index.html",
    "tests/test_app.py",
]

with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as archive:
    for relative in files:
        source = project / relative
        if not source.is_file():
            raise FileNotFoundError(source)
        archive.write(source, arcname=str(Path("TP1") / relative))

with ZipFile(archive_path) as archive:
    if archive.testzip() is not None:
        raise RuntimeError("ZIP verification failed")

print(f"Created {archive_path} ({archive_path.stat().st_size:,} bytes)")
