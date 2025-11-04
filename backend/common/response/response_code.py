import dataclasses

from enum import Enum

from backend.common.i18n import t


class CustomCodeBase(Enum):
    """Custom status code base class"""

    @property
    def code(self) -> int:
        """Get status code"""
        return self.value[0]

    @property
    def msg(self) -> str:
        """Get status code message"""
        message = self.value[1]
        return t(message)


class CustomResponseCode(CustomCodeBase):
    """Custom response status code"""

    HTTP_200 = (200, 'response.success')
    HTTP_400 = (400, 'response.error')
    HTTP_500 = (500, 'Internal Server Error')


class CustomErrorCode(CustomCodeBase):
    """Custom error status code"""

    CAPTCHA_ERROR = (40001, 'error.captcha.error')


@dataclasses.dataclass
class CustomResponse:
    """
    Provides open-ended response status codes instead of enums, which can be useful if you want to customize response messages
    """

    code: int
    msg: str


class StandardResponseCode:
    """Standard response status code"""

    """
    HTTP codes
    See HTTP Status Code Registry:
    https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml

    And RFC 2324 - https://tools.ietf.org/html/rfc2324
    """
    HTTP_100 = 100  # CONTINUE: Continue
    HTTP_101 = 101  # SWITCHING_PROTOCOLS: Switching Protocols
    HTTP_102 = 102  # PROCESSING: Processing
    HTTP_103 = 103  # EARLY_HINTS: Early Hints
    HTTP_200 = 200  # OK: OK
    HTTP_201 = 201  # CREATED: Created
    HTTP_202 = 202  # ACCEPTED: Accepted
    HTTP_203 = 203  # NON_AUTHORITATIVE_INFORMATION: Non-Authoritative Information
    HTTP_204 = 204  # NO_CONTENT: No Content
    HTTP_205 = 205  # RESET_CONTENT: Reset Content
    HTTP_206 = 206  # PARTIAL_CONTENT: Partial Content
    HTTP_207 = 207  # MULTI_STATUS: Multi-Status
    HTTP_208 = 208  # ALREADY_REPORTED: Already Reported
    HTTP_226 = 226  # IM_USED: IM Used
    HTTP_300 = 300  # MULTIPLE_CHOICES: Multiple Choices
    HTTP_301 = 301  # MOVED_PERMANENTLY: Moved Permanently
    HTTP_302 = 302  # FOUND: Found
    HTTP_303 = 303  # SEE_OTHER: See Other
    HTTP_304 = 304  # NOT_MODIFIED: Not Modified
    HTTP_305 = 305  # USE_PROXY: Use Proxy
    HTTP_307 = 307  # TEMPORARY_REDIRECT: Temporary Redirect
    HTTP_308 = 308  # PERMANENT_REDIRECT: Permanent Redirect
    HTTP_400 = 400  # BAD_REQUEST: Bad Request
    HTTP_401 = 401  # UNAUTHORIZED: Unauthorized
    HTTP_402 = 402  # PAYMENT_REQUIRED: Payment Required
    HTTP_403 = 403  # FORBIDDEN: Forbidden
    HTTP_404 = 404  # NOT_FOUND: Not Found
    HTTP_405 = 405  # METHOD_NOT_ALLOWED: Method Not Allowed
    HTTP_406 = 406  # NOT_ACCEPTABLE: Not Acceptable
    HTTP_407 = 407  # PROXY_AUTHENTICATION_REQUIRED: Proxy Authentication Required
    HTTP_408 = 408  # REQUEST_TIMEOUT: Request Timeout
    HTTP_409 = 409  # CONFLICT: Conflict
    HTTP_410 = 410  # GONE: Gone
    HTTP_411 = 411  # LENGTH_REQUIRED: Length Required
    HTTP_412 = 412  # PRECONDITION_FAILED: Precondition Failed
    HTTP_413 = 413  # REQUEST_ENTITY_TOO_LARGE: Request Entity Too Large
    HTTP_414 = 414  # REQUEST_URI_TOO_LONG: Request-URI Too Long
    HTTP_415 = 415  # UNSUPPORTED_MEDIA_TYPE: Unsupported Media Type
    HTTP_416 = 416  # REQUESTED_RANGE_NOT_SATISFIABLE: Requested Range Not Satisfiable
    HTTP_417 = 417  # EXPECTATION_FAILED: Expectation Failed
    HTTP_418 = 418  # UNUSED: Unused
    HTTP_421 = 421  # MISDIRECTED_REQUEST: Misdirected Request
    HTTP_422 = 422  # UNPROCESSABLE_CONTENT: Unprocessable Content
    HTTP_423 = 423  # LOCKED: Locked
    HTTP_424 = 424  # FAILED_DEPENDENCY: Failed Dependency
    HTTP_425 = 425  # TOO_EARLY: Too Early
    HTTP_426 = 426  # UPGRADE_REQUIRED: Upgrade Required
    HTTP_427 = 427  # UNASSIGNED: Unassigned
    HTTP_428 = 428  # PRECONDITION_REQUIRED: Precondition Required
    HTTP_429 = 429  # TOO_MANY_REQUESTS: Too Many Requests
    HTTP_430 = 430  # Unassigned: Unassigned
    HTTP_431 = 431  # REQUEST_HEADER_FIELDS_TOO_LARGE: Request Header Fields Too Large
    HTTP_451 = 451  # UNAVAILABLE_FOR_LEGAL_REASONS: Unavailable For Legal Reasons
    HTTP_500 = 500  # INTERNAL_SERVER_ERROR: Internal Server Error
    HTTP_501 = 501  # NOT_IMPLEMENTED: Not Implemented
    HTTP_502 = 502  # BAD_GATEWAY: Bad Gateway
    HTTP_503 = 503  # SERVICE_UNAVAILABLE: Service Unavailable
    HTTP_504 = 504  # GATEWAY_TIMEOUT: Gateway Timeout
    HTTP_505 = 505  # HTTP_VERSION_NOT_SUPPORTED: HTTP Version Not Supported
    HTTP_506 = 506  # VARIANT_ALSO_NEGOTIATES: Variant Also Negotiates
    HTTP_507 = 507  # INSUFFICIENT_STORAGE: Insufficient Storage
    HTTP_508 = 508  # LOOP_DETECTED: Loop Detected
    HTTP_509 = 509  # UNASSIGNED: Unassigned
    HTTP_510 = 510  # NOT_EXTENDED: Not Extended
    HTTP_511 = 511  # NETWORK_AUTHENTICATION_REQUIRED: Network Authentication Required

    """
    WebSocket codes
    https://www.iana.org/assignments/websocket/websocket.xml#close-code-number
    https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent
    """
    WS_1000 = 1000  # NORMAL_CLOSURE: Normal Closure
    WS_1001 = 1001  # GOING_AWAY: Going Away
    WS_1002 = 1002  # PROTOCOL_ERROR: Protocol Error
    WS_1003 = 1003  # UNSUPPORTED_DATA: Unsupported Data
    WS_1005 = 1005  # NO_STATUS_RCVD: No Status Received
    WS_1006 = 1006  # ABNORMAL_CLOSURE: Abnormal Closure
    WS_1007 = 1007  # INVALID_FRAME_PAYLOAD_DATA: Invalid Frame Payload Data
    WS_1008 = 1008  # POLICY_VIOLATION: Policy Violation
    WS_1009 = 1009  # MESSAGE_TOO_BIG: Message Too Big
    WS_1010 = 1010  # MANDATORY_EXT: Mandatory Extension
    WS_1011 = 1011  # INTERNAL_ERROR: Internal Error
    WS_1012 = 1012  # SERVICE_RESTART: Service Restart
    WS_1013 = 1013  # TRY_AGAIN_LATER: Try Again Later
    WS_1014 = 1014  # BAD_GATEWAY: Bad Gateway
    WS_1015 = 1015  # TLS_HANDSHAKE: TLS Handshake Error
    WS_3000 = 3000  # UNAUTHORIZED: Unauthorized
    WS_3003 = 3003  # FORBIDDEN: Forbidden
