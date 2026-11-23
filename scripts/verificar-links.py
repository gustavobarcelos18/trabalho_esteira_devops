from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
PAGES_PREFIX = "/trabalho_esteira_devops/"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()
        self.references = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag in {"a", "area", "link"} and "href" in attrs:
            self.references.append((self.getpos()[0], attrs["href"]))
        if tag in {"img", "source"} and "src" in attrs:
            self.references.append((self.getpos()[0], attrs["src"]))
        if tag in {"img", "source"} and "srcset" in attrs:
            candidates = re.findall(r"(?:^|,)\s*(\S+?)(?=\s|,|$)", attrs["srcset"] or "")
            self.references.extend((self.getpos()[0], url) for url in candidates or [None])


def check_external(url):
    request = Request(url, headers={"User-Agent": "Portfolio-CI/1.0"})
    with urlopen(request, timeout=15) as response:
        if response.status >= 400:
            raise ValueError(f"HTTP {response.status}")


def check_local(page, target, pages):
    raw_path = unquote(target.path)
    if raw_path.startswith(PAGES_PREFIX):
        path = ROOT / raw_path.removeprefix(PAGES_PREFIX)
    elif raw_path.startswith("/"):
        raise ValueError("o caminho absoluto deve começar com o prefixo do projeto no Pages")
    else:
        path = page.path.parent / raw_path if raw_path else page.path

    path = path.resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("o caminho sai do projeto")
    if path.is_dir():
        path /= "index.html"
    relative_path = path.relative_to(ROOT)
    root_asset = len(relative_path.parts) == 1 and path.suffix in {".html", ".css"}
    if not root_asset and relative_path.parts[0] != "imagens":
        raise ValueError("o arquivo não faz parte do site publicado")
    if not path.is_file():
        raise ValueError("arquivo local ausente")
    if target.fragment and path in pages and unquote(target.fragment) not in pages[path].ids:
        raise ValueError("âncora local ausente")


def main():
    html_files = sorted(ROOT.glob("*.html")) + sorted((ROOT / "imagens").rglob("*.html"))
    pages = {path: Page(path) for path in html_files}
    external_results = {}
    errors = []

    for page in pages.values():
        for line, url in page.references:
            try:
                if not url or not url.strip():
                    raise ValueError("referência vazia")
                url = url.strip()
                target = urlsplit(url)
                if target.scheme in {"http", "https"} or (not target.scheme and target.netloc):
                    if not target.hostname:
                        raise ValueError("endereço externo sem domínio")
                    address = target._replace(fragment="").geturl()
                    if not target.scheme:
                        address = "https:" + address
                    if address not in external_results:
                        try:
                            check_external(address)
                            external_results[address] = None
                        except (OSError, ValueError) as error:
                            external_results[address] = str(error)
                    if external_results[address]:
                        raise ValueError(external_results[address])
                elif target.scheme in {"mailto", "tel"}:
                    if not target.path:
                        raise ValueError("endereço de contato vazio")
                elif target.scheme:
                    raise ValueError(f"protocolo não aceito: {target.scheme}")
                else:
                    check_local(page, target, pages)
            except (OSError, ValueError) as error:
                errors.append(f"{page.path.relative_to(ROOT)}:{line}: {url!r}: {error}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Referências válidas em {len(pages)} página(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
