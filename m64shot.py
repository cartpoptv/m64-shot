import sys, os, numpy as np
from PIL import Image

X0, Y0, W, H = 672, 120, 2500, 1920
WIDTHS = {8: 0.0, 4: 0.3, 7: 0.5, 9: 0.5}

def boundaries(energy, length):
    e = energy / (energy.mean() + 1e-9)
    best = np.full(length + 1, -1e18); prev = np.zeros(length + 1, int); best[0] = 0
    for p in range(1, length + 1):
        gain = e[p - 1] if p < length else 0
        for w, pen in WIDTHS.items():
            if p - w >= 0 and best[p - w] > -1e17:
                v = best[p - w] + gain - pen * 8
                if v > best[p]: best[p], prev[p] = v, p - w
    b = [length]
    while b[-1] > 0: b.append(prev[b[-1]])
    return b[::-1]

def process(src, dst):
    a = np.asarray(Image.open(src).convert('RGB')).astype(float)
    f = a[Y0:Y0 + H, X0:X0 + W]
    xb = boundaries(np.abs(np.diff(f, axis=1)).sum(axis=(0, 2)), W)
    yb = boundaries(np.abs(np.diff(f, axis=0)).sum(axis=(1, 2)), H)
    out = np.zeros((len(yb) - 1, len(xb) - 1, 3)); spread = []
    for j, (y0, y1) in enumerate(zip(yb, yb[1:])):
        for i, (x0, x1) in enumerate(zip(xb, xb[1:])):
            blk = f[y0 + 1:y1 - 1, x0 + 1:x1 - 1]
            out[j, i] = blk.mean(axis=(0, 1)); spread.append(blk.std(axis=(0, 1)).mean())
    q = np.round(np.round(out / 255 * 31) * 255 / 31).astype(np.uint8)
    Image.fromarray(q).save(dst, lossless=True, quality=100, method=6)
    wx = np.diff(xb); wy = np.diff(yb)
    odd_x = [(xb[k], int(w)) for k, w in enumerate(wx) if w != 8]
    odd_y = [(yb[k], int(w)) for k, w in enumerate(wy) if w != 8]
    return q.shape[1], q.shape[0], np.mean(spread), odd_x, odd_y, os.path.getsize(dst)

if __name__ == '__main__':
    outdir = sys.argv[1]
    for src in sys.argv[2:]:
        name = os.path.splitext(os.path.basename(src))[0] + '.webp'
        w, h, s, ox, oy, size = process(src, os.path.join(outdir, name))
        print(f'{name}\t{w}x{h}\tblur={s:.2f}\t{size//1024} KB\tx:{ox}\ty:{oy}')
