import random
import gradio as gr
import pyshorteners
from pyshorteners.exceptions import (
    BadAPIResponseException,
    BadURLException,
    ExpandingErrorException,
    ShorteningErrorException,
)
import requests
import logging

logger = logging.getLogger(__name__)

def get_random_error_message():
    error_messages = [
        "Oops! That link seems to have wandered off the beaten path. Please provide a valid URL to continue.",
        "Hmm, this doesn't look like a proper gateway. Let's ensure you enter a valid link to proceed!",
        "Ahoy! We can't set sail without a proper link. Please drop anchor and provide a valid URL!",
    ]
    return random.choice(error_messages)

def bitly_shorten(url, api_key):
    if not url.startswith("https://") and not url.startswith("http://"):
        url = "https://" + url
    try:
        s = pyshorteners.Shortener(api_key=api_key)
        shortened_url = s.bitly.short(url)
        return shortened_url
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            logger.error("bitly: API key is not correct")
            return "Bitly: API key is not correct"
    except (
        BadAPIResponseException,
        BadURLException,
        ExpandingErrorException,
        ShorteningErrorException,
    ) as e:
        logger.error(f"bitly: {repr(e)}")
        return f"Bitly: {get_random_error_message()}"

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
        logger.error(f"TinyURL: {repr(e)}")
        return f"TinyURL: {get_random_error_message()}"

def cuttly_shorten(url, api_key):
    try:
        s = pyshorteners.Shortener(api_key=api_key)
        shortened_url = s.cuttly.short(url)
        return shortened_url
    except (
        BadAPIResponseException,
        BadURLException,
        ExpandingErrorException,
        ShorteningErrorException,
    ) as e:
        logger.error(f"Cuttly: {repr(e)}")
        return f"Cuttly: {get_random_error_message()}"

services = {
    "Bitly": bitly_shorten,
    "TinyURL": tinyurl_shorten,
    "Cuttly": cuttly_shorten,
}

def shorten_url(url, selected_service, api_key):
    if selected_service == "Bitly" or selected_service == "Cuttly":
        return services[selected_service](url, api_key)
    else:
        return services[selected_service](url)

def toggle_api_key_visibility(selected_service):
    return gr.update(visible=(selected_service == "Bitly" or selected_service == "Cuttly"))

with gr.Blocks(title="Link Shortener 🔗") as application:
    gr.Markdown("# Link Shortener 🔗")
    
    with gr.Row():
        url_input = gr.Textbox(label="Enter the URL to shorten:", placeholder="https://github.com/")
        service_dropdown = gr.Dropdown(
            choices=list(services.keys()),
            label="Select the URL shortening service:",
            value="Bitly",
        )
    api_key_input = gr.Textbox(label="Enter API Key:", placeholder="API key", visible=True)

    shorten_button = gr.Button("Shorten URL")
    
    with gr.Row():
        gr.Markdown("### Shortened URL:")
        output_text = gr.Textbox(
            label="",
            show_copy_button=True,
            elem_id="shortened-url",  # Assign an ID for custom styling
        )

    # Toggle visibility of API Key input based on selected service
    service_dropdown.change(
        fn=toggle_api_key_visibility,
        inputs=service_dropdown,
        outputs=api_key_input,
    )

    # Handle the shortening process
    shorten_button.click(
        fn=shorten_url,
        inputs=[url_input, service_dropdown, api_key_input],
        outputs=output_text,
    )

    # Inject custom CSS for styling
    gr.HTML(
        """
        <style>
        #shortened-url textarea {
            font-size: 1.25em;
            background-color: #f0f8ff;
            color: #000000; /* Set text color to black */
            border: 2px solid #007acc;
            border-radius: 10px;
            padding: 10px;
        }
        </style>
        """
    )

if __name__ == "__main__":
    application.launch(server_port=8000)
