![GitHub repo size](https://img.shields.io/github/repo-size/cartpoptv/m64-shot)
![GitHub License](https://img.shields.io/github/license/cartpoptv/m64-shot)
![GitHub Created At](https://img.shields.io/github/created-at/cartpoptv/m64-shot)

# m64-shot

Experimental script that turns Elgato screenshot capture back into the original low-res frame.

- it cuts out the game area from the 4K frame
- finds where each game pixel starts and ends
- averages each block into one pixel
- rounds colors to 16-bit, which is what the N64 renders anyway, so most of the JPEG noise is removed
- saves the result as lossless WebP
- I've only tested it on Xibalba 64. Games that use a different resolution will probably need tweaks.

```
pip install pillow numpy
python3 m64shot.py out/ captures/*.jpg
```

## License

[Unlicense](LICENSE)
