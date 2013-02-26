from svg_constants import DEFAULT_FILL, DEFAULT_STROKE
from svg_parser_utils import *
from render_target import AlphaTexture1D


class SVGStyle(object):

    def __init__(self, inherit_from=None):
        #: The internal color
        self.fill = DEFAULT_FILL

        #: How to determine the "insideness" of a point. Possible values are
        #: "nonzero" and "evenodd". See mozilla documentation for more details:
        #: http://www.w3.org/TR/SVG/painting.html
        self.fill_rule = 'nonzero'

        #: The color of the surrounding outline
        self.stroke = DEFAULT_STROKE

        #: The width of the surrounding outline
        self.stroke_width = 1

        #: Overall opacity (multiplied by other elements)
        self.opacity = 1.0

        #: Controls the pattern of dashes and gaps used to stroke path. List
        #: of alternating dashes and gaps.
        self.stroke_dasharray = []

        self.stroke_texture = None

        if inherit_from:
            self.fill = inherit_from.fill
            self.stroke = inherit_from.stroke
            self.fill_rule = inherit_from.fill_rule
            self.stroke_width = inherit_from.stroke_width

    def from_element(self, element):
        """Read relevant attributes off XML element"""
        self.fill = parse_color(element.get('fill'), self.fill)
        self.fill_rule = element.get('fill-rule', self.fill_rule)

        self.stroke = parse_color(element.get('stroke'), self.stroke)
        self.stroke_width = float(element.get('stroke-width', 1.0))

        self.opacity *= float(element.get('opacity', 1))
        self.fill_opacity = float(element.get('fill-opacity', 1))
        self.stroke_opacity = float(element.get('stroke-opacity', 1))

        dash_array = element.get('stroke-dasharray', None)
        if dash_array and dash_array != 'none':
            self.stroke_dasharray = [float(x.strip()) for x in dash_array.split(',')]
            self._init_stroke_texture()

        style = element.get('style')
        if style:
            style_dict = parse_style(style)
            if 'fill' in style_dict:
                self.fill = parse_color(style_dict['fill'])
            if 'fill-opacity' in style_dict:
                self.fill_opacity *= float(style_dict['fill-opacity'])
            if 'stroke' in style_dict:
                self.stroke = parse_color(style_dict['stroke'])
            if 'stroke-opacity' in style_dict:
                self.stroke_opacity *= float(style_dict['stroke-opacity'])
            if 'stroke-width' in style_dict:
                sw = style_dict['stroke-width']
                self.stroke_width = parse_float(sw)
            if 'stroke-dasharray' in style_dict:
                dash_array = style_dict['stroke-dasharray']
                if dash_array != 'none':
                    if dash_array:
                        self.stroke_dasharray = [float(x.strip()) for x in dash_array.split(',')]
                        self._init_stroke_texture()
            if 'opacity' in style_dict:
                self.fill_opacity *= float(style_dict['opacity'])
                self.stroke_opacity *= float(style_dict['opacity'])
            if 'fill-rule' in style_dict:
                self.fill_rule = style_dict['fill-rule']
        if isinstance(self.stroke, list):
            self.stroke[3] = int(self.opacity * self.stroke_opacity * self.stroke[3])
        if isinstance(self.fill, list):
            self.fill[3] = int(self.opacity * self.fill_opacity * self.fill[3])

    def _init_stroke_texture(self):
        bits = [255, 0, 0, 255] + [0, 255, 0, 255]
        self.stroke_texture = AlphaTexture1D(bits * 8, 16)

    def parse_style_attribute(self, attr):
        pass

    def parse_fill_attribute(self, attr):
        pass

    def parse_fillrule(self, attr):
        pass

    def parse_stroke_attribute(self, attr):
        pass

    def parse_stroke_width(self, attr):
        pass

    def parse_stroke_dasharray(self, attr):
        pass