import sublime

from .core import ev_setting
from .logging import log

import certifi

from json import dumps

from os import environ

from threading import Thread

from urllib.error import URLError, HTTPError
from urllib.parse import urlparse, urlunparse
from urllib.request import urlopen, Request


## ----------------------------------------------------------------------------


class EnvaultRequestThread(Thread):
    """
    Make a request to the Envault API using the provided URL and key, in order
    to fetch the associated environment keys that go with the list of request
    keys provided.

    The request will run in a background thread so as to not hang the UI in
    Sublime if the request takes too much time.

    When the request completes (regardless of success or fail), the callback
    is invoked on the main thread with the result of the query. In the case
    of success, this is a dict that contains the keys; for failure, the result
    is None.
    """
    def __init__(self, url, apiKeyName, vars, callback):
        super().__init__()

        self.url = self.update_url(url)
        self.apiKeyName = apiKeyName
        self.vars = vars
        self.callback = callback

    def update_url(self, url):
        """
        Given a URL from an envault configuration file, ensure that it has the
        appropriate endpoint on it to query the keys we need.
        """
        scheme, netloc, path, params, query, fragment = urlparse(url)

        path = f"{path}{'' if path[-1:] == '/' else '/'}load"

        return urlunparse((scheme, netloc, path, params, query, fragment))


    def run(self):
        """
        Make an envault request to the specific url in order to fetch the
        values of the keys provided.

        An api key must be provided, which is the name of an existing
        environment variable that specifies the actual key to use in the
        request.

        The request will be sent with the list of keys, and results in a
        dictionary that represents the various environment variables and the
        values that should be assigned to them. This need not (and likely is
        not) the same as any of the keys provided in the request itself.
        """
        if ev_setting("debug"):
            log(f"Making key request with '{self.apiKeyName}' via '{self.url}'")
            log(f"Keys requested: {', '.join(self.vars)}")

        # Look up the API key to use; the key we get is actually the name of an
        # environment variable that contains the actual API key.
        apikey_value = environ.get(self.apiKeyName, "unknown")

        # Set the headers tp use in the request. Note that when Envault is
        # hosted on Cloudflare Workers, a 403 result with payload "error 1010"
        # will be returned if the user agent is recognized as some sort of bot
        # or scraper (e.g. the standard urllib user agent).
        #
        # Here we are directly outlining who we are; it is possible to go into
        # the Cloudflare Dashboard for the domain, hit Security > Settings and
        # then either turn off the Browser Integrity Check, or set an explicit
        # exemption for this particular user agent
        headers = {
            "api-key": apikey_value,
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": 'Sublime/Envault v0.0.1',
        }

        # Create the payload; it has to be a JSON object that is encoded as
        # bytes.
        data = dumps(self.vars).encode('utf-8')

        env_keys = None
        try:
            req = Request(self.url, data, headers, method="POST")
            with urlopen(req, cafile=certifi.where()) as res:
                body = res.read().decode("utf-8")
                env_keys = sublime.decode_value(body)

        except HTTPError as e:
            log(f"http error: {e.code}")
            log(f"error while fetching the contents of the config", error=True)

            # The error result is sometimes but not always a JSON object, so
            # for the time being just dump it to the console; we can work out
            # how to get a meaningful error message out of it later.
            print(f"{str(e.read().decode('utf-8'))}")

        except URLError as e:
            log(f"url error: {e.reason}")

        sublime.set_timeout(lambda: self.callback(env_keys))


## ----------------------------------------------------------------------------
