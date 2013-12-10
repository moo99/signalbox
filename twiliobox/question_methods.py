from django.conf import settings
from django.http import HttpResponse

from twiliobox.settings import *


def reply_to_twilio(response):
    """
    Takes a twiliobox response and returns an HttpResponse
    :type response: a
    """
    return HttpResponse(str(response), content_type="text/xml")


def say_extra_text(response, text):
    response.say(text, language=settings.TTS_LANGUAGE, voice=settings.TTS_VOICE)
    return response


def say_or_play(response, question, reply=None):
    if question.audio:
        response.play(question.audio.url)
    else:
        response.say(question.display_text(reply=reply), language=settings.TTS_LANGUAGE, voice=settings.TTS_VOICE)


def uninterruptible_instruction(twimlresponse, question, url, reply=None, *args, **kwargs):
    say_or_play(twimlresponse, question, reply)
    twimlresponse.redirect(url=url, method="POST")
    return twimlresponse


def hangup(twimlresponse, question, url, reply=None, *args, **kwargs):
    say_or_play(twimlresponse, question, reply)
    twimlresponse.hangup()
    return twimlresponse


def instruction(twimlresponse, question, url, reply=None, *args, **kwargs):
    with twimlresponse.gather(numDigits=1, action=url, method="POST", timeout=0) as g:
        say_or_play(g, question, reply)
    twimlresponse.redirect(url=url, method="POST")
    return twimlresponse


def multiple(twimlresponse, question, url, reply=None, *args, **kwargs):
    for i in range(QUESTION_REPEATS):
        with twimlresponse.gather(numDigits=1, action=url, method="POST", timeout=DEFAULT_TIMEOUT) as g:
            say_or_play(g, question, reply)
    twimlresponse.redirect(url=url, method="POST")  # this skips to the next question if the timeout is reached
    return twimlresponse


# needs more testing at some point
def listen(twimlresponse, question, reply=None, *args, **kwargs):
    say_or_play(twimlresponse, question, reply)
    twimlresponse.record()
    return twimlresponse


# needs more testing...
def integer(twimlresponse, question, url, reply=None, *args, **kwargs):
    for i in range(QUESTION_REPEATS):
        with twimlresponse.gather(action=url, method="POST", timeout=DEFAULT_TIMEOUT) as g:
            say_or_play(g, question, reply)
    twimlresponse.redirect(url=url, method="POST")  # this skips to the next question if the timeout is reached
    return twimlresponse
