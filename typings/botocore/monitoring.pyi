"""
This type stub file was generated by pyright.
"""

import logging

logger = logging.getLogger(__name__)

class Monitor(object):
    _EVENTS_TO_REGISTER = ...
    def __init__(self, adapter, publisher) -> None:
        """Abstraction for monitoring clients API calls

        :param adapter: An adapter that takes event emitter events
            and produces monitor events

        :param publisher: A publisher for generated monitor events
        """
        ...
    def register(self, event_emitter):
        """Register an event emitter to the monitor"""
        ...
    def capture(self, event_name, **payload):
        """Captures an incoming event from the event emitter

        It will feed an event emitter event to the monitor's adaptor to create
        a monitor event and then publish that event to the monitor's publisher.
        """
        ...

class MonitorEventAdapter(object):
    def __init__(self, time=...) -> None:
        """Adapts event emitter events to produce monitor events

        :type time: callable
        :param time: A callable that produces the current time
        """
        ...
    def feed(self, emitter_event_name, emitter_payload):
        """Feed an event emitter event to generate a monitor event

        :type emitter_event_name: str
        :param emitter_event_name: The name of the event emitted

        :type emitter_payload: dict
        :param emitter_payload: The payload to associated to the event
            emitted

        :rtype: BaseMonitorEvent
        :returns: A monitor event based on the event emitter events
            fired
        """
        ...

class BaseMonitorEvent(object):
    def __init__(self, service, operation, timestamp) -> None:
        """Base monitor event

        :type service: str
        :param service: A string identifying the service associated to
            the event

        :type operation: str
        :param operation: A string identifying the operation of service
            associated to the event

        :type timestamp: int
        :param timestamp: Epoch time in milliseconds from when the event began
        """
        ...
    def __repr__(self): ...
    def __eq__(self, other) -> bool: ...

class APICallEvent(BaseMonitorEvent):
    def __init__(
        self,
        service,
        operation,
        timestamp,
        latency=...,
        attempts=...,
        retries_exceeded=...,
    ) -> None:
        """Monitor event for a single API call

        This event corresponds to a single client method call, which includes
        every HTTP requests attempt made in order to complete the client call

        :type service: str
        :param service: A string identifying the service associated to
            the event

        :type operation: str
        :param operation: A string identifying the operation of service
            associated to the event

        :type timestamp: int
        :param timestamp: Epoch time in milliseconds from when the event began

        :type latency: int
        :param latency: The time in milliseconds to complete the client call

        :type attempts: list
        :param attempts: The list of APICallAttempts associated to the
            APICall

        :type retries_exceeded: bool
        :param retries_exceeded: True if API call exceeded retries. False
            otherwise
        """
        ...
    def new_api_call_attempt(self, timestamp):
        """Instantiates APICallAttemptEvent associated to the APICallEvent

        :type timestamp: int
        :param timestamp: Epoch time in milliseconds to associate to the
            APICallAttemptEvent
        """
        ...

class APICallAttemptEvent(BaseMonitorEvent):
    def __init__(
        self,
        service,
        operation,
        timestamp,
        latency=...,
        url=...,
        http_status_code=...,
        request_headers=...,
        response_headers=...,
        parsed_error=...,
        wire_exception=...,
    ) -> None:
        """Monitor event for a single API call attempt

        This event corresponds to a single HTTP request attempt in completing
        the entire client method call.

        :type service: str
        :param service: A string identifying the service associated to
            the event

        :type operation: str
        :param operation: A string identifying the operation of service
            associated to the event

        :type timestamp: int
        :param timestamp: Epoch time in milliseconds from when the HTTP request
            started

        :type latency: int
        :param latency: The time in milliseconds to complete the HTTP request
            whether it succeeded or failed

        :type url: str
        :param url: The URL the attempt was sent to

        :type http_status_code: int
        :param http_status_code: The HTTP status code of the HTTP response
            if there was a response

        :type request_headers: dict
        :param request_headers: The HTTP headers sent in making the HTTP
            request

        :type response_headers: dict
        :param response_headers: The HTTP headers returned in the HTTP response
            if there was a response

        :type parsed_error: dict
        :param parsed_error: The error parsed if the service returned an
            error back

        :type wire_exception: Exception
        :param wire_exception: The exception raised in sending the HTTP
            request (i.e. ConnectionError)
        """
        ...

class CSMSerializer(object):
    _MAX_CLIENT_ID_LENGTH = ...
    _MAX_EXCEPTION_CLASS_LENGTH = ...
    _MAX_ERROR_CODE_LENGTH = ...
    _MAX_USER_AGENT_LENGTH = ...
    _MAX_MESSAGE_LENGTH = ...
    _RESPONSE_HEADERS_TO_EVENT_ENTRIES = ...
    _AUTH_REGEXS = ...
    _SERIALIZEABLE_EVENT_PROPERTIES = ...
    def __init__(self, csm_client_id) -> None:
        """Serializes monitor events to CSM (Client Side Monitoring) format

        :type csm_client_id: str
        :param csm_client_id: The application identifier to associate
            to the serialized events
        """
        ...
    def serialize(self, event):
        """Serializes a monitor event to the CSM format

        :type event: BaseMonitorEvent
        :param event: The event to serialize to bytes

        :rtype: bytes
        :returns: The CSM serialized form of the event
        """
        ...

class SocketPublisher(object):
    _MAX_MONITOR_EVENT_LENGTH = ...
    def __init__(self, socket, host, port, serializer) -> None:
        """Publishes monitor events to a socket

        :type socket: socket.socket
        :param socket: The socket object to use to publish events

        :type host: string
        :param host: The host to send events to

        :type port: integer
        :param port: The port on the host to send events to

        :param serializer: The serializer to use to serialize the event
            to a form that can be published to the socket. This must
            have a `serialize()` method that accepts a monitor event
            and return bytes
        """
        ...
    def publish(self, event):
        """Publishes a specified monitor event

        :type event: BaseMonitorEvent
        :param event: The monitor event to be sent
            over the publisher's socket to the desired address.
        """
        ...