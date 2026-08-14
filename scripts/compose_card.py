"""Compose a Chinese idiom study card from a generated illustration.

The illustration should be generated without text. This script adds exact Chinese
copy deterministically so the final card contains the title, meaning, source, and
exam reminder without relying on image-model typography.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


CANVAS = (1080, 1350)
INK = (48, 45, 40)
SECONDARY = (93, 88, 79)
VERMILION = (157, 62, 45)
PAPER = (248, 242, 228)


def find_font(explicit: str | None) -> Path:
    candidates = [
        explicit,
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        r"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return Path(candidate)
    raise FileNotFoundError("No usable CJK font found; pass --font explicitly.")


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for char in text:
        if char == "\n":
            lines.append(current)
            current = ""
            continue
        trial = current + char
        if current and draw.textlength(trial, font=face) > width:
            lines.append(current)
            current = char
        else:
            current = trial
    if current or not lines:
        lines.append(current)
    return lines


def draw_centered(draw: ImageDraw.ImageDraw, text: str, y: int, face: ImageFont.FreeTypeFont, fill: tuple[int, int, int]) -> None:
    box = draw.textbbox((0, 0), text, font=face)
    x = (CANVAS[0] - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=face, fill=fill)


def add_block(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    label: str,
    content: str,
    label_face: ImageFont.FreeTypeFont,
    body_face: ImageFont.FreeTypeFont,
    max_width: int,
) -> int:
    draw.text((x, y), label, font=label_face, fill=VERMILION)
    label_width = int(draw.textlength(label, font=label_face))
    content_x = x + label_width + 12
    available = max_width - label_width - 12
    first_line = wrap_text(draw, content, body_face, available)
    if first_line:
        draw.text((content_x, y + 2), first_line[0], font=body_face, fill=INK)
    line_height = body_face.size + 12
    for line in first_line[1:]:
        y += line_height
        draw.text((x, y + 2), line, font=body_face, fill=INK)
    return y + line_height + 8


def compose(args: argparse.Namespace) -> None:
    font_path = find_font(args.font)
    image = Image.open(args.input).convert("RGB")
    fitted = ImageOps.contain(image, CANVAS, method=Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", CANVAS, PAPER)
    canvas.paste(fitted, ((CANVAS[0] - fitted.width) // 2, (CANVAS[1] - fitted.height) // 2))
    draw = ImageDraw.Draw(canvas, "RGBA")

    # Keep the generated illustration visible while giving text a quiet paper field.
    draw.rounded_rectangle((42, 36, 1038, 205), radius=18, fill=(250, 246, 235, 218), outline=(114, 93, 68, 80), width=2)
    draw.rounded_rectangle((42, 1000, 1038, 1310), radius=18, fill=(250, 246, 235, 235), outline=(114, 93, 68, 90), width=2)

    title = font(font_path, 68)
    pinyin = font(font_path, 26)
    label_face = font(font_path, 25)
    body_face = font(font_path, 27)
    small_face = font(font_path, 22)

    draw_centered(draw, args.idiom, 60, title, INK)
    draw_centered(draw, args.pinyin, 143, pinyin, SECONDARY)

    x = 76
    y = 1030
    width = 928
    y = add_block(draw, x, y, "核心释义", args.meaning, label_face, body_face, width)
    if args.source:
        y = add_block(draw, x, y, "成语来源", args.source, label_face, small_face, width)
    add_block(draw, x, y, "易错提醒", args.warning, label_face, body_face, width)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, format="PNG", optimize=True)
    print(output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--idiom", required=True)
    parser.add_argument("--pinyin", required=True)
    parser.add_argument("--meaning", required=True)
    parser.add_argument("--warning", required=True)
    parser.add_argument("--source", default="")
    parser.add_argument("--font")
    compose(parser.parse_args())


if __name__ == "__main__":
    main()
