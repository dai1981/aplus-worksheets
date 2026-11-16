# -*- coding: utf-8 -*-
"""六年級の圓・扇形の図（共通）"""
import math
from tw_common import fig, svg_wrap, text, line, GREEN, FILL, RED, INK


def circle_svg(r_label, kind="r", angle=360, label=""):
    """kind: r=半徑 d=直徑、angle<360 なら扇形"""
    W, H, cx, cy, R = 200, 180, 100, 92, 70
    s = []
    if angle >= 360:
        s.append("<circle cx='%d' cy='%d' r='%d' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, R, FILL, GREEN))
    else:
        a = math.radians(angle)
        x2, y2 = cx + R * math.cos(-a), cy + R * math.sin(-a)
        big = 1 if angle > 180 else 0
        s.append("<path d='M%d %d L%d %d A%d %d 0 %d 0 %.1f %.1f Z' fill='%s' stroke='%s' stroke-width='2'/>" % (cx, cy, cx + R, cy, R, R, big, x2, y2, FILL, GREEN))
        s.append(text(cx + 18 * math.cos(-a / 2) + (4 if angle < 60 else 0), cy + 18 * math.sin(-a / 2) + 5, "%d°" % angle, 12, col=INK))
    s.append("<circle cx='%d' cy='%d' r='2.5' fill='%s'/>" % (cx, cy, INK))
    if kind == "d":
        s.append(line(cx - R, cy, cx + R, cy, RED, 2))
        s.append(text(cx, cy + 18, r_label, 13, col=RED).replace("<text ", "<text stroke='#fff' stroke-width='4' paint-order='stroke' ", 1))
    else:
        s.append(line(cx, cy, cx + R, cy, RED, 2))
        s.append(text(cx + R / 2, cy + 18, r_label, 13, col=RED).replace("<text ", "<text stroke='#fff' stroke-width='4' paint-order='stroke' ", 1))
    return fig(svg_wrap(W, H, "".join(s), label or "圓"))
