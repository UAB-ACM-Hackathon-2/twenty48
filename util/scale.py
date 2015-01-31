_scalex = 1.0
_scaley = 1.0


def dpx(px):
    return int(px * _scalex)


def dpy(px):
    return int(px * _scaley)


def set_scale(scalex, scaley):
    global _scalex, _scaley
    _scalex = float(scalex)
    _scaley = float(scaley)