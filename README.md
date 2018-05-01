# kainosSteg

A tutorial on Steganography and Python


# Dependencies

### Python 3

```
brew install python
```

### Pillow Image Library

```
pip install Pillow
```

### Installation Proof

To prove your environment is ready for this tutorial, run the following code.

```python
from PIL import Image, ImageDraw

img = Image.new('RGB', (100, 30), color = (73, 109, 137))

d = ImageDraw.Draw(img)
d.text((10,10), "Hello Kainos", fill=(255,255,0))

img.save('install_proof.png')
```