"""
Unit tests for BFA Wire Protocol, Encoders, and Decoders.
"""

import pytest
from bfa.protocol.decoder import JSONDecoder
from bfa.protocol.encoder import JSONEncoder


def test_json_encoder_encodes_dict_to_bytes():
    encoder = JSONEncoder()
    data = {"status": "SUCCESS", "data": {"id": 1, "username": "huy"}, "error": None}

    encoded_bytes = encoder.encode(data)
    assert isinstance(encoded_bytes, bytes)
    assert b'"status": "SUCCESS"' in encoded_bytes
    assert b'"username": "huy"' in encoded_bytes


def test_json_decoder_decodes_bytes_to_dict():
    decoder = JSONDecoder()
    raw_bytes = b'{"username": "huy", "age": 20}'

    decoded = decoder.decode(raw_bytes)
    assert isinstance(decoded, dict)
    assert decoded["username"] == "huy"
    assert decoded["age"] == 20


def test_json_decoder_empty_bytes():
    decoder = JSONDecoder()
    assert decoder.decode(b"") == {}
    assert decoder.decode(b"   ") == {}


def test_json_decoder_invalid_json():
    decoder = JSONDecoder()
    with pytest.raises(ValueError, match="Invalid JSON format"):
        decoder.decode(b"invalid-json-content")


def test_json_decoder_non_dict_json():
    decoder = JSONDecoder()
    with pytest.raises(ValueError, match="must be a JSON object/dict"):
        decoder.decode(b'["item1", "item2"]')
