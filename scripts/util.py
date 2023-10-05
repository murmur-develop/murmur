import requests, urllib.parse, os.path


def download(url: str):
    res = requests.get(url)
    if not (res.status_code >= 200 and res.status_code < 300):
        raise Exception(
            f"Failed to download file from url.\nstatus_code: {res.status_code}.\nurl: {url}"
        )

    filename = os.path.basename(urllib.parse.urlparse(url).path)

    with open(filename, "w+b") as f:
        f.write(res.content)

    return filename
