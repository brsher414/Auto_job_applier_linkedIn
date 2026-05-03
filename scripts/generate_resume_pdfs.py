from __future__ import annotations

import base64
import json
import shutil
import subprocess
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path

import websocket


ROOT = Path(__file__).resolve().parents[1]
CHROME_PATH = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")

RESUMES = [
    (ROOT / "resume" / "resume_zhibi_liu_en.html", ROOT / "resume" / "resume_zhibi_liu_en.pdf"),
    (ROOT / "resume" / "resume_zhibi_liu.html", ROOT / "resume" / "简历_刘之璧_v.pdf"),
]


class ChromePDF:
    def __init__(self) -> None:
        if not CHROME_PATH.exists():
            raise FileNotFoundError(f"Chrome not found: {CHROME_PATH}")
        self.profile_dir = Path(tempfile.mkdtemp(prefix="resume-pdf-chrome-"))
        self.process = subprocess.Popen(
            [
                str(CHROME_PATH),
                "--headless=new",
                "--disable-gpu",
                "--no-first-run",
                "--no-default-browser-check",
                "--allow-file-access-from-files",
                "--remote-allow-origins=*",
                "--remote-debugging-port=0",
                f"--user-data-dir={self.profile_dir}",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.port = self._wait_for_port()

    def _wait_for_port(self) -> str:
        active_port = self.profile_dir / "DevToolsActivePort"
        deadline = time.time() + 20
        while time.time() < deadline:
            if active_port.exists():
                return active_port.read_text(encoding="utf-8").splitlines()[0].strip()
            time.sleep(0.1)
        raise TimeoutError("Chrome DevTools port was not created.")

    def close(self) -> None:
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
        shutil.rmtree(self.profile_dir, ignore_errors=True)

    def new_page_websocket(self, url: str) -> str:
        encoded_url = urllib.parse.quote(url, safe=":/%")
        request = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/json/new?{encoded_url}",
            method="PUT",
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            target = json.loads(response.read().decode("utf-8"))
        return target["webSocketDebuggerUrl"]


class CDPSession:
    def __init__(self, websocket_url: str) -> None:
        self.ws = websocket.create_connection(websocket_url, timeout=20)
        self.next_id = 1

    def close(self) -> None:
        self.ws.close()

    def call(self, method: str, params: dict | None = None) -> dict:
        message_id = self.next_id
        self.next_id += 1
        self.ws.send(json.dumps({"id": message_id, "method": method, "params": params or {}}))
        while True:
            response = json.loads(self.ws.recv())
            if response.get("id") == message_id:
                if "error" in response:
                    raise RuntimeError(response["error"])
                return response.get("result", {})

    def wait_for_load(self) -> None:
        deadline = time.time() + 20
        while time.time() < deadline:
            event = json.loads(self.ws.recv())
            if event.get("method") == "Page.loadEventFired":
                return
        raise TimeoutError("Timed out waiting for page load.")


def html_to_pdf(chrome: ChromePDF, html_path: Path, pdf_path: Path) -> None:
    session = CDPSession(chrome.new_page_websocket(html_path.resolve().as_uri()))
    try:
        session.call("Page.enable")
        session.wait_for_load()
        session.call("Emulation.setEmulatedMedia", {"media": "print"})
        result = session.call(
            "Page.printToPDF",
            {
                "printBackground": True,
                "preferCSSPageSize": True,
                "marginTop": 0,
                "marginBottom": 0,
                "marginLeft": 0,
                "marginRight": 0,
                "scale": 1,
            },
        )
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.write_bytes(base64.b64decode(result["data"]))
    finally:
        session.close()


def build_pdfs() -> None:
    chrome = ChromePDF()
    try:
        for html_path, pdf_path in RESUMES:
            html_to_pdf(chrome, html_path, pdf_path)
            print(pdf_path)
    finally:
        chrome.close()


if __name__ == "__main__":
    build_pdfs()
