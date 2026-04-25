from datetime import datetime, timezone, timedelta

import pytest
from jose import jwt

from app.config import settings
from app.utils.auth import create_access_token, hash_password, verify_password


class TestHashPassword:
    def test_returns_string(self):
        result = hash_password("mysecret")
        assert isinstance(result, str)

    def test_hash_is_not_plaintext(self):
        result = hash_password("mysecret")
        assert result != "mysecret"

    def test_different_calls_produce_different_hashes(self):
        # bcrypt uses a random salt — same input should never produce the same hash
        hash1 = hash_password("mysecret")
        hash2 = hash_password("mysecret")
        assert hash1 != hash2


class TestVerifyPassword:
    def test_correct_password_returns_true(self):
        hashed = hash_password("mysecret")
        assert verify_password("mysecret", hashed) is True

    def test_wrong_password_returns_false(self):
        hashed = hash_password("mysecret")
        assert verify_password("wrongpassword", hashed) is False

    def test_empty_password_returns_false(self):
        hashed = hash_password("mysecret")
        assert verify_password("", hashed) is False

    def test_case_sensitive(self):
        hashed = hash_password("mysecret")
        assert verify_password("MySecret", hashed) is False


class TestCreateAccessToken:
    def test_token_is_a_string(self):
        token = create_access_token({"sub": "user@example.com"})
        assert isinstance(token, str)

    def test_token_contains_sub_claim(self):
        token = create_access_token({"sub": "user@example.com"})
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert payload["sub"] == "user@example.com"

    def test_token_contains_exp_claim(self):
        token = create_access_token({"sub": "user@example.com"})
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert "exp" in payload

    def test_token_expiry_is_in_the_future(self):
        token = create_access_token({"sub": "user@example.com"})
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        assert exp > datetime.now(timezone.utc)

    def test_token_expiry_respects_config(self):
        before = datetime.now(timezone.utc)
        token = create_access_token({"sub": "user@example.com"})
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        expected = before + timedelta(minutes=settings.access_token_expire_minutes)
        # allow a 5-second window for test execution time
        assert abs((exp - expected).total_seconds()) < 5

    def test_extra_claims_are_preserved(self):
        token = create_access_token({"sub": "user@example.com", "role": "admin"})
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert payload["role"] == "admin"
