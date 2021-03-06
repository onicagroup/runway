"""
This type stub file was generated by pyright.
"""

import logging

logger = logging.getLogger(__name__)

def register_retry_handler(client): ...

class ClientRateLimiter(object):
    _MAX_RATE_ADJUST_SCALE = ...
    def __init__(
        self, rate_adjustor, rate_clocker, token_bucket, throttling_detector, clock
    ) -> None: ...
    def on_sending_request(self, request, **kwargs): ...
    def on_receiving_response(self, **kwargs): ...

class RateClocker(object):
    """Tracks the rate at which a client is sending a request."""

    _DEFAULT_SMOOTHING = ...
    _TIME_BUCKET_RANGE = ...
    def __init__(self, clock, smoothing=..., time_bucket_range=...) -> None: ...
    def record(self, amount=...): ...
    @property
    def measured_rate(self): ...
