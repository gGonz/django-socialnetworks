import requests

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.simple_tag(takes_context=True)
def linkedin_login(context, label=None, css_class=None):
    """
    Renders a 'Sign in with LinkedIn' button.

    """
    context['label'] = label or _('Sign in with LinkedIn')
    context['css_class'] = css_class
    context['action'] = reverse('socialnetworks:linkedin:login')

    return template.loader.render_to_string('login_button.html', context)


@register.simple_tag(takes_context=True)
def linkedin_share(context, label=None, css_class=None, **kwargs):
    """
    Renders a 'Tweet' button to share content on LinkedIn.

    Parameters:
        - label: the text to show inside the button, default 'Tweet'
        - css_class: the class to apply to the button

    Keyword arguments:
        - hashtags: Comma separated hashtags appended to tweet text.
        - related: Related accounts.
        - text: Default Tweet text.
        - url: URL of the page to share.
        - via: Screen name of the user to attribute the Tweet to.

    Please visit https://dev.linkedin.com/docs/tweet-button for a detailed
    reference of the arguments supported by LinkedIn.

    """
#    # Base javascript for the button.
#    base_script = (
#        "javascript:(function(){window.twttr=window.twttr||{};var D=550,"
#        "A=450,C=screen.height,B=screen.width,H=Math.round((B/2)-(D/2)),"
#        "G=0,F=document,E;if(C>A){G=Math.round((C/2)-(A/2))}"
#        "window.twttr.shareWin=window.open('%(__URL__)s','','left='+H+',"
#        "top='+G+',width='+D+',height='+A+',personalbar=0,toolbar=0,"
#        "scrollbars=1,resizable=1');E=F.createElement('script');"
#        "E.src=('https:'==document.location.protocol?'https://':'http://')+"
#        "'platform.linkedin.com/widgets.js';"
#        "F.getElementsByTagName('head')[0].appendChild(E)}());"
#    )

    __URL__ = "http://www.linkedin.com/shareArticle?mini=false&url=YourURL&title=TheTitleOfYourWebPageGoesHere&summary=TheSummaryOfYourWebPageGoesHere&source=TheNameOfYourSiteGoesHere"

    base_script = (
        "javascript:(function(){var D=620,"
        "A=350,C=screen.height,B=screen.width,H=Math.round((B/2)-(D/2)),"
        "G=0,F=document,E;if(C>A){G=Math.round((C/2)-(A/2))}"
        "window.open('%(__URL__)s','','left='+H+',"
        "top='+G+',width='+D+',height='+A+',personalbar=0,toolbar=0,"
        "scrollbars=1,resizable=1');"
        ""
        ""
        "}());"
    )


    # Preparing the url with the encoded parameters.
#    r = requests.Request(url='https://linkedin.com/share',
#        params=kwargs).prepare()

    context['label'] = label or _('Share')
    context['css_class'] = css_class
    context['script'] = base_script % {'__URL__': __URL__}

    return template.loader.render_to_string('share_button.html', context)


"""
<a href="http://www.linkedin.com/shareArticle?mini=true&url=YourURL&title=TheTitleOfYourWebPageGoesHere&summary=TheSummaryOfYourWebPageGoesHere&source=TheNameOfYourSiteGoesHere" rel="nofollow" onclick="NewWindow(this.href,'template_window','550','400','yes','center');return false" onfocus="this.blur()"> <img src="LinkedInShareButton.jpg" title="Share on LinkedIn" alt="Share on LinkedIn" width="100" height="100" border="0" /> </a>
"""