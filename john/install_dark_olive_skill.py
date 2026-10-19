"""Install the user-provided local skill without executing packaged content."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import stat
import zipfile

PACKAGE = Path(r"C:\Users\lms-work\Downloads\dark-olive-broll.skill")
PROJECT = Path(__file__).resolve().parents[1]
NAME = "dark-olive-broll"
DESTINATIONS = [PROJECT / ".agents" / "skills" / NAME,
                Path(r"C:\Users\lms-work\.codex\skills") / NAME]


def main():
    files = {}
    with zipfile.ZipFile(PACKAGE) as archive:
        assert sum(i.file_size for i in archive.infolist()) < 10_000_000
        for item in archive.infolist():
            path = PurePosixPath(item.filename)
            if (path.is_absolute() or ".." in path.parts or "\\" in item.filename
                    or ":" in item.filename or path.parts[0] != NAME
                    or stat.S_ISLNK(item.external_attr >> 16)):
                raise ValueError(f"Unsafe archive entry: {item.filename}")
            if item.is_dir():
                continue
            relative = Path(*path.parts[1:])
            if relative in files:
                raise ValueError(f"Duplicate entry: {item.filename}")
            files[relative] = archive.read(item)
    assert Path("SKILL.md") in files
    for destination in DESTINATIONS:
        for relative, content in files.items():
            target = destination / relative
            if not target.resolve().is_relative_to(destination.resolve()):
                raise ValueError(f"Target escapes destination: {target}")
            if target.exists() and target.read_bytes() != content:
                raise FileExistsError(f"Existing different skill file; preserved: {target}")
    for destination in DESTINATIONS:
        for relative, content in files.items():
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_bytes(content)
            assert target.read_bytes() == content
    report = {"package": str(PACKAGE),
              "package_sha256": hashlib.sha256(PACKAGE.read_bytes()).hexdigest(),
              "destinations": [str(p) for p in DESTINATIONS],
              "files": {p.as_posix(): hashlib.sha256(data).hexdigest()
                        for p, data in files.items()}, "verified": True}
    (PROJECT / "john" / "skill-installation.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
