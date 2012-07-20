from django import template
from django.template.defaultfilters import stringfilter
from oembed.core import replace

register = template.Library()


@register.filter(name='oembed', is_safe=True)
@stringfilter
def oembed(input, args=''):
    '''
    args - optional oembed max size argument
    args="640x480" - max_width = 640, max_height = 480
    args="!640x..." - max_width = width = 640
    args="...x!480" - max_height = height = 480
    '''
    if args:
        max_width, max_height = args.lower().split('x')
        if not (max_width and max_height):
            raise template.TemplateSyntaxError("Oembed's optional WIDTHxHEIGHT argument requires WIDTH and HEIGHT to be positive integers.")
        if max_width[0] == '!':
            max_width = max_width[1:]
            fixed_width = True
        else:
            fixed_width = False
        if max_height[0] == '!':
            max_height = max_height[1:]
            fixed_height = True
        else:
            fixed_height = False
    else:
        max_width, max_height = None, None
        fixed_width, fixed_height = False, False

    return replace(input, max_width=max_width, max_height=max_height, fixed_width=fixed_width, fixed_height=fixed_height)


@register.tag(name='oembed')
def do_oembed(parser, token):
    """
    A node which parses everything between its two nodes, and replaces any links
    with OEmbed-provided objects, if possible.

    Supports one optional argument, which is the maximum width and height,
    specified like so:

        {% oembed 640x480 %}http://www.viddler.com/explore/SYSTM/videos/49/{% endoembed %}

    You also can specify fixed width or height (but not all oEmbed services handles it):

        {% oembed !640x!480 %}http://www.viddler.com/explore/SYSTM/videos/49/{% endoembed %}
    """
    args = token.contents.split()
    if len(args) > 2:
        raise template.TemplateSyntaxError("Oembed tag takes only one (optional) argument: WIDTHxHEIGHT, where WIDTH and HEIGHT are positive integers.")
    if len(args) == 2:
        max_width, max_height = args[1].lower().split('x')
        if not (max_width and max_height):
            raise template.TemplateSyntaxError("Oembed's optional WIDTHxHEIGHT argument requires WIDTH and HEIGHT to be positive integers.")
        if max_width[0] == '!':
            max_width = max_width[1:]
            fixed_width = True
        else:
            fixed_width = False

        if max_height[0] == '!':
            max_height = max_height[1:]
            fixed_height = True
        else:
            fixed_height = False

    else:
        max_width, max_height = None, None
        fixed_width, fixed_height = False, False

    nodelist = parser.parse(('endoembed',))
    parser.delete_first_token()
    return OEmbedNode(nodelist, max_width, max_height, fixed_width, fixed_height)


class OEmbedNode(template.Node):
    def __init__(self, nodelist, max_width, max_height, fixed_width, fixed_height):
        self.nodelist = nodelist
        self.max_width = max_width
        self.max_height = max_height
        self.fixed_width = fixed_width
        self.fixed_height = fixed_height

    def render(self, context):
        kwargs = {}
        if self.max_width and self.max_height:
            kwargs['max_width'] = self.max_width
            kwargs['max_height'] = self.max_height

        kwargs['fixed_width'] = self.fixed_width
        kwargs['fixed_height'] = self.fixed_height

        return replace(self.nodelist.render(context), **kwargs)
