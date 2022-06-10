import dataclasses
from re import L
import typing

from PyQt6 import QtGui

@dataclasses.dataclass(kw_only=True, frozen=True)
class Font:
    name: str
    point_size: int
    is_bold: bool
    is_italic: bool

# It appears that creating the 'QFont' and 'QFontMetricsF' objects is non-trivial.
# We cache all the fonts we encounter in this cache and use a more light weight font to pass around.
# This also means that we only need to actually load fonts that are visible on screen, further improving culling.
class FontCache:
    def __init__(self):
        self._qfonts: typing.Dict[Font, QtGui.QFont] = {}
        self._qfont_metrics: typing.Dict[Font, QtGui.QFontMetricsF] = {}

    def get_qfont(self, font: Font):
        try:
            return self._qfonts[font]
        except KeyError:
            weight = QtGui.QFont.Weight.Normal
            if font.is_bold:
                weight = QtGui.QFont.Weight.Bold

            qfont = QtGui.QFont(font.name, font.point_size, weight, font.is_italic)
            self._qfonts[font] = qfont

            return qfont

    def get_qfont_metrics(self, font: Font):
        try:
            return self._qfont_metrics[font]
        except KeyError:
            qfont = self.get_qfont(font)

            qfont_metrics = QtGui.QFontMetricsF(qfont)
            self._qfont_metrics[font] = qfont_metrics

            return qfont_metrics

global_font_cache = FontCache()
