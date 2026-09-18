#!/usr/bin/env python3
"""Версионная поставка law-cli + package.py; установка только по внешнему SHA-256.

Python 3.12+, стандартная библиотека. Для download нужен gh с доступом
к Releases указанного репозитория; install работает с локальным архивом.
Никакие файлы из архива не исполняются при установке.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import stat
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
TARGET = "x86_64-unknown-linux-musl"
FILES = {"law-cli", "package.py", "LICENSE"}
MAX_ARCHIVE = 64 * 1024 * 1024
MAX_UNPACKED = 128 * 1024 * 1024


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def validate_lock(lock: dict) -> dict:
    if not isinstance(lock, dict) or set(lock) != {
        "format", "version", "target", "sourceCommit", "repository", "tag", "asset", "sha256"
    } or lock["format"] != "law.package-toolchain-lock/0.1":
        raise ValueError("неподдержанный формат toolchain lock")
    if not all(isinstance(v, str) for v in lock.values()):
        raise ValueError("поля toolchain lock должны быть строками")
    if (not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", lock["version"])
            or not re.fullmatch(r"[a-f0-9]{40}", lock["sourceCommit"])
            or not re.fullmatch(r"[a-f0-9]{64}", lock["sha256"])
            or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", lock["repository"])
            or lock["target"] != TARGET
            or lock["tag"] != f"law-package-tools@{lock['version']}"
            or lock["asset"] != f"law-package-tools-{lock['version']}-{TARGET}.zip"):
        raise ValueError("неверные координаты/хэши toolchain lock")
    return lock


def pack(root: Path, binary: Path, version: str, commit: str, repository: str, out: Path) -> dict:
    lock = validate_lock({"format": "law.package-toolchain-lock/0.1", "version": version,
                          "target": TARGET, "sourceCommit": commit, "repository": repository,
                          "tag": f"law-package-tools@{version}", "sha256": "0" * 64,
                          "asset": f"law-package-tools-{version}-{TARGET}.zip"})
    payloads = {"law-cli": binary.read_bytes(),
                "package.py": (root / "apps/registry/package.py").read_bytes(),
                "LICENSE": (root / "LICENSE").read_bytes()}
    # ELF64 little endian, AMD64. Статическую линковку проверяет readelf в build job.
    binary_header = payloads["law-cli"][:20]
    if binary_header[:6] != b"\x7fELF\x02\x01" or binary_header[18:20] != b"\x3e\x00":
        raise ValueError("ожидается Linux ELF64 x86_64 law-cli")
    manifest = {"format": "law.package-toolchain/0.1", "version": version,
                "target": TARGET, "sourceCommit": commit,
                "files": {name: sha(data) for name, data in sorted(payloads.items())}}
    payloads["toolchain.json"] = encoded(manifest)
    out.parent.mkdir(parents=True, exist_ok=True)
    # 'x': опубликованные байты не перезаписываются даже локально.
    with zipfile.ZipFile(out, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(payloads.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | (0o755 if name == "law-cli" else 0o644)) << 16
            archive.writestr(info, data)
    lock["sha256"] = sha(out.read_bytes())
    return lock


def install(archive: Path, lock: dict, out: Path) -> dict:
    validate_lock(lock)
    if platform.system() != "Linux" or platform.machine() not in {"x86_64", "amd64"}:
        raise ValueError("этот выпуск поддерживает только Linux x86_64")
    if out.exists() or out.is_symlink():
        raise ValueError("каталог установки должен быть новым")
    if archive.stat().st_size > MAX_ARCHIVE or sha(archive.read_bytes()) != lock["sha256"]:
        raise ValueError("SHA-256/размер архива не соответствует пину")
    with zipfile.ZipFile(archive) as bundle:
        entries = bundle.infolist()
        names = [entry.filename for entry in entries]
        if len(names) != 4 or set(names) != FILES | {"toolchain.json"}:
            raise ValueError("недопустимые пути/состав/дубликаты в архиве")
        if sum(entry.file_size for entry in entries) > MAX_UNPACKED:
            raise ValueError("превышен размер распакованных файлов")
        if any(stat.S_IFMT(entry.external_attr >> 16) != stat.S_IFREG for entry in entries):
            raise ValueError("в архиве разрешены только обычные файлы")
        payloads = {name: bundle.read(name) for name in names}
    manifest = json.loads(payloads.pop("toolchain.json"))
    expected = {"format": "law.package-toolchain/0.1",
                **{key: lock[key] for key in ("version", "target", "sourceCommit")},
                "files": {name: sha(data) for name, data in sorted(payloads.items())}}
    if manifest != expected:
        raise ValueError("состав/identity/хэши файлов тулчейна расходятся с пином")
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="law-toolchain-", dir=out.parent) as temp:
        staged = Path(temp) / "tools"
        staged.mkdir()
        for name, data in {**payloads, "toolchain.json": encoded(manifest)}.items():
            path = staged / name
            path.write_bytes(data)
            path.chmod(0o755 if name == "law-cli" else 0o644)
        os.rename(staged, out)
    return manifest


def download(lock: dict, out: Path) -> dict:
    validate_lock(lock)
    with tempfile.TemporaryDirectory(prefix="law-toolchain-download-") as temp:
        subprocess.run(["gh", "release", "download", lock["tag"], "--repo", lock["repository"],
                        "--pattern", lock["asset"], "--dir", temp], check=True, timeout=180)
        return install(Path(temp) / lock["asset"], lock, out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    build = sub.add_parser("pack")
    build.add_argument("--root", type=Path, default=ROOT)
    build.add_argument("--lawc", type=Path, required=True)
    build.add_argument("--version", required=True)
    build.add_argument("--commit", required=True)
    build.add_argument("--repository", default="arxohq/law")
    build.add_argument("--out", type=Path, required=True)
    for mode in ("install", "download"):
        command = sub.add_parser(mode)
        command.add_argument("--lock", type=Path, required=True)
        command.add_argument("--out", type=Path, required=True)
        if mode == "install":
            command.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.mode == "pack":
            result = pack(args.root, args.lawc, args.version, args.commit, args.repository, args.out)
        else:
            lock = validate_lock(json.loads(args.lock.read_bytes()))
            result = (install(args.archive, lock, args.out) if args.mode == "install"
                      else download(lock, args.out))
        print(encoded(result).decode(), end="")
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.SubprocessError) as error:
        parser.exit(1, f"toolchain: ОТКАЗ: {error}\n")


if __name__ == "__main__":
    main()
