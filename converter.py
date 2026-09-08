"""Local WebP conversion; never overwrite existing files."""
from pathlib import Path
from PIL import Image, ImageColor, ImageOps


def convert(source, output_dir, format="PNG", quality=90, background="#ffffff"):
    source, output_dir = Path(source), Path(output_dir)
    format = format.upper()
    if format not in {"PNG", "JPG", "JPEG"}:
        raise ValueError("PNG 또는 JPG를 선택하세요.")
    if not 1 <= quality <= 100:
        raise ValueError("품질은 1~100이어야 합니다.")
    color = ImageColor.getrgb(background)
    with Image.open(source) as original:
        if original.format != "WEBP":
            raise ValueError("WebP 이미지가 아닙니다.")
        animated = getattr(original, "n_frames", 1) > 1
        original.seek(0)
        picture = ImageOps.exif_transpose(original).convert("RGBA")
        if format != "PNG":
            canvas = Image.new("RGB", picture.size, color)
            canvas.paste(picture, mask=picture.getchannel("A"))
            picture = canvas
        output_dir.mkdir(parents=True, exist_ok=True)
        suffix = ".png" if format == "PNG" else ".jpg"
        index = 0
        while True:
            name = source.stem + (f"_{index}" if index else "") + suffix
            destination = output_dir / name
            try:
                stream = destination.open("xb")
                break
            except FileExistsError:
                index += 1
        try:
            with stream:
                picture.save(stream, format="PNG" if format == "PNG" else "JPEG",
                             **({} if format == "PNG" else {"quality": quality}))
        except BaseException:
            destination.unlink(missing_ok=True)
            raise
    return destination, animated
