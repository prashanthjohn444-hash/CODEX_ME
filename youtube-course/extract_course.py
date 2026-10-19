"""Extract embedded course data without executing the uploaded JavaScript."""
import json
from html.parser import HTMLParser
from pathlib import Path

SOURCE = Path(r"C:\Users\lms-work\Downloads\PYTHON_30_DAYS_LAB_WITH_MIND_MAPS_FIXED.html")
OUT = Path(__file__).resolve().parent


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"p", "h1", "h2", "h3", "h4", "li", "pre", "tr", "br"}:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)


def main():
    html = SOURCE.read_text(encoding="utf-8")
    lessons, _ = json.JSONDecoder().raw_decode(html.split("const lessons = ", 1)[1])
    assert [x["day"] for x in lessons] == list(range(1, 31))
    (OUT / "source").mkdir(parents=True, exist_ok=True)
    for lesson in lessons:
        parser = Text()
        parser.feed(lesson["html"])
        lesson["text"] = "".join(parser.parts)
        (OUT / "source" / f"{lesson['id']}.txt").write_text(lesson["text"], encoding="utf-8")
    (OUT / "source" / "lessons.json").write_text(json.dumps(lessons, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Extracted {len(lessons)} lessons into {OUT / 'source'}")


if __name__ == "__main__":
    main()
