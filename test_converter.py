import tempfile
import unittest
from pathlib import Path
from PIL import Image
from converter import convert


class ConversionTests(unittest.TestCase):
    def test_formats_transparency_and_collision(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "한글.webp"
            Image.new("RGBA", (8, 6), (255, 0, 0, 0)).save(source, lossless=True)
            png, animated = convert(source, root)
            self.assertFalse(animated)
            with Image.open(png) as result:
                self.assertEqual(result.format, "PNG")
                self.assertEqual(result.getpixel((0, 0))[3], 0)
            second, _ = convert(source, root)
            self.assertNotEqual(png, second)
            jpg, _ = convert(source, root, "JPG")
            with Image.open(jpg) as result:
                self.assertEqual(result.format, "JPEG")
                self.assertEqual(result.size, (8, 6))
                self.assertEqual(result.getpixel((0, 0)), (255, 255, 255))

    def test_rejects_other_formats_and_corruption(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "fake.webp"
            Image.new("RGB", (2, 2)).save(source, format="PNG")
            with self.assertRaises(ValueError):
                convert(source, directory)
            source.write_bytes(b"broken")
            with self.assertRaises(OSError):
                convert(source, directory)

    def test_animation_first_frame(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "animation.webp"
            Image.new("RGB", (2, 2), "red").save(
                source, save_all=True, append_images=[Image.new("RGB", (2, 2), "blue")],
                duration=100, lossless=True)
            output, animated = convert(source, directory)
            self.assertTrue(animated)
            with Image.open(output) as result:
                self.assertEqual(result.getpixel((0, 0)), (255, 0, 0, 255))


if __name__ == "__main__":
    unittest.main()
