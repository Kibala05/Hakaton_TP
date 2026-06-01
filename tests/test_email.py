import pytest
from email_model import Email


def test_normal_email_reads_correctly(tmp_path):
    filepath = tmp_path / "mail.txt"
    filepath.write_text("Subject: Тест\nFrom: user@test.ru\n\nТело письма", encoding="utf-8")
    email = Email(str(filepath))
    result = email.read()
    assert result == True
    assert email.subject == "Тест"
    assert email.sender == "user@test.ru"
    assert "Тело письма" in email.body


def test_empty_file_returns_false(tmp_path):
    filepath = tmp_path / "empty.txt"
    filepath.write_text("", encoding="utf-8")
    email = Email(str(filepath))
    result = email.read()
    assert result == False
    assert email.error == "empty_file"


def test_binary_file_returns_false(tmp_path):
    filepath = tmp_path / "bad.bin"
    filepath.write_bytes(b"\xff\xfe\x00\x01\x02\x03")
    email = Email(str(filepath))
    result = email.read()
    assert result == False
    assert email.error == "binary_file"


def test_email_without_subject_does_not_crash(tmp_path):
    filepath = tmp_path / "mail.txt"
    filepath.write_text("From: user@test.ru\n\nТекст без темы", encoding="utf-8")
    email = Email(str(filepath))
    email.read()
    assert email.subject == ""
    assert email.body != ""


def test_email_without_body_does_not_crash(tmp_path):
    filepath = tmp_path / "mail.txt"
    filepath.write_text("Subject: Тест\nFrom: user@test.ru\n", encoding="utf-8")
    email = Email(str(filepath))
    email.read()
    assert email.subject == "Тест"
    assert email.body == ""