import random
import gradio as gr
import pyshorteners
from pyshorteners.exceptions import (
    BadAPIResponseException,
    BadURLException,
    ExpandingErrorException,
    ShorteningErrorException,
)
import logging


logger = logging.getLogger(__name__)

def get_random_error_message():
    error_messages = [
        "Oops! That link seems to have wandered off the beaten path. Please provide a valid URL to continue.",
        "Hmm, this doesn't look like a proper gateway. Let's ensure you enter a valid link to proceed!",
        "Ahoy! We can't set sail without a proper link. Please drop anchor and provide a valid URL!",
        "Beware of digital detours! Only a valid link can guide you through this checkpoint.",
        "Your journey requires a valid passkey. Please enter a valid URL to unlock the gate!",
        "It looks like we've hit a digital dead-end. Please provide a valid link to find the way forward.",
        "Unlock the power of the web with a valid link! Without it, we're lost in the digital wilderness.",
        "We've encountered a binary puzzle! To proceed, you must supply a valid URL.",
        "Climb the virtual tower with a valid link to reach the enchanted realm of the web.",
        "Only by providing a valid link shall you gain passage through this digital gateway.",
        "Oh no! It seems you've entered an invalid link. Let's try again with a valid URL.",
        "Uh-oh! We're missing a proper link. Please provide a valid URL and try again.",
        "Oops! That link doesn't seem right. Let's try again with a valid URL.",
        "Oh dear! The link you provided isn't valid. Please enter a legitimate URL.",
        "Uh-oh! We've hit a roadblock with that link. Please provide a valid URL to proceed.",
        "Oh my! That link seems invalid. Please enter a proper URL and try again.",
        "Yikes! That doesn't look like a valid link. Please provide a legitimate URL.",
        "Oopsie-daisy! The link you entered isn't valid. Please provide a genuine URL.",
        "Oh dear! The link you provided isn't quite right. Please enter a valid URL.",
        "Oh no, we've encountered an issue with the link you entered. Please double-check and provide a valid URL.",
        "It seems the link you entered isn't valid. Please provide a genuine URL and try again.",
    ]
    return random.choice(error_messages)


random_error = get_random_error_message()


def bitly_shorten(url):
    if not url.startswith("https://") and not url.startswith("http://"):
        url = "https://" + url
    try:
        s = pyshorteners.Shortener(api_key="Enter your own API key")
        shortened_url = s.bitly.short(url)
        return shortened_url
    except (
        BadAPIResponseException,
        BadURLException,
        ExpandingErrorException,
        ShorteningErrorException,
    ) as e:
        logger.error(repr(e))
        return get_random_error_message()


def tinyurl_shorten(url):
    try:
        s = pyshorteners.Shortener()
        shortened_url = s.tinyurl.short(url)
        return shortened_url
    except (
        BadAPIResponseException,
        BadURLException,
        ExpandingErrorException,
        ShorteningErrorException,
    ) as e:
        logger.error(repr(e))
        return get_random_error_message()


def cuttly_shorten(url):
    try:
        s = pyshorteners.Shortener(api_key="Enter your own API key")
        shortened_url = s.cuttly.short(url)
        return shortened_url
    except (
        BadAPIResponseException,
        BadURLException,
        ExpandingErrorException,
        ShorteningErrorException,
    ) as e:
        logger.error(repr(e))
        return get_random_error_message()


"""Services menu"""
services = {
    "Bitly": bitly_shorten,
    "TinyURL": tinyurl_shorten,
    "Cuttly": cuttly_shorten,
}


def shorten_url(url, selected_service):
    shortened_url = services[selected_service](url)
    return shortened_url


"""Gradio UI"""
url_input = gr.Textbox(
    label="Enter the URL to shorten:", placeholder="https://github.com/quangnguyen3499"
)

service_dropdown = gr.Dropdown(
    choices=list(services.keys()),
    label="Select the URL shortening service:",
    value="Please select any",
)

output_text = gr.Textbox(label="Shortened URL:", show_copy_button=True, container=True)

interface = gr.Interface(
    fn=shorten_url,
    inputs=[url_input, service_dropdown],
    outputs=[output_text],
    title="Link Shortener 🔗",
    theme=gr.themes.Soft(),
    allow_flagging="never",
)
interface.launch()
