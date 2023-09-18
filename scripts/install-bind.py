import os, sys, platform, subprocess
import requests
from util import download


def sdk_url(version: str, os: str, arch: str | None, device: str = "cpu"):
    if arch is not None:
        arch = f"_{arch}"

    return f"https://github.com/VOICEVOX/voicevox_core/releases/download/{version}/voicevox_core-{version}+{device}-cp38-abi3-{os}{arch}.whl"


voicevox_version = (
    os.environ["VOICEVOX_VERSION"] if "VOICEVOX_VERSION" in os.environ else "0.14.4"
)

device_type = sys.argv[1] if len(sys.argv) >= 2 else "cpu"
if not device_type in ("cpu", "cuda", "directml"):
    raise Exception(f"Invalid device type {device_type}.")

os_name = platform.system()
match os_name:
    case "Windows":
        os_name = "win"

    case "Linux":
        os_name = "linux"

    case "Darwin":
        os_name = "macosx"

arch = platform.machine().lower()

print(
    "Download voicevox core binding.\n\n"
    + f"version: {voicevox_version}\n"
    + f"os_name: {os_name}\n"
    + f"device_type: {device_type}\n",
    file=sys.stderr,
)

# 得た情報からライブラリをダウンロードする
match (device_type, os_name, arch):
    # GPU
    case ("cuda", "linux", "amd64" | "x86_64"):
        filename = download(sdk_url(voicevox_version, os_name, "x86_64", device_type))

    case ("directml" | "cuda", "win", "amd64" | "x86_64"):
        filename = download(sdk_url(voicevox_version, os_name, "amd64", device_type))

    # CPU
    case ("cpu", "win", "amd64" | "x86_64"):
        filename = download(sdk_url(voicevox_version, os_name, "amd64", device_type))

    case ("cpu", "win", "x86" | "i386"):
        filename = download(sdk_url(voicevox_version, "win32", None, device_type))

    case ("cpu", "macosx", "amd64" | "x86_64"):
        filename = download(
            sdk_url(voicevox_version, f"{os_name}_10_7", "amd64", device_type),
        )

    case ("cpu", "macosx", "aarch64" | "arm64"):
        filename = download(
            sdk_url(voicevox_version, f"{os_name}_11_0", "arm64", device_type),
        )

    case ("cpu", "linux", "amd64" | "x86_64"):
        filename = download(sdk_url(voicevox_version, os_name, "x86_64", device_type))

    case ("cpu", "linux", "aarch64" | "arm64"):
        filename = download(sdk_url(voicevox_version, os_name, "aarch64", device_type))

    case _ as t:
        raise Exception(f"Invalid library version {t}.")

subprocess.run(["python", "-m", "pip", "install", filename])
