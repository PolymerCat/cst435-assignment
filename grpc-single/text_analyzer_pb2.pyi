from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AnalysisRequest(_message.Message):
    __slots__ = ("text_content",)
    TEXT_CONTENT_FIELD_NUMBER: _ClassVar[int]
    text_content: str
    def __init__(self, text_content: _Optional[str] = ...) -> None: ...

class AnalysisResponse(_message.Message):
    __slots__ = ("word_count", "sentence_count", "longest_word", "shortest_word", "server_processing_time")
    WORD_COUNT_FIELD_NUMBER: _ClassVar[int]
    SENTENCE_COUNT_FIELD_NUMBER: _ClassVar[int]
    LONGEST_WORD_FIELD_NUMBER: _ClassVar[int]
    SHORTEST_WORD_FIELD_NUMBER: _ClassVar[int]
    SERVER_PROCESSING_TIME_FIELD_NUMBER: _ClassVar[int]
    word_count: int
    sentence_count: int
    longest_word: str
    shortest_word: str
    server_processing_time: float
    def __init__(self, word_count: _Optional[int] = ..., sentence_count: _Optional[int] = ..., longest_word: _Optional[str] = ..., shortest_word: _Optional[str] = ..., server_processing_time: _Optional[float] = ...) -> None: ...
