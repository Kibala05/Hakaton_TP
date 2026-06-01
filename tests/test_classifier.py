import pytest
from email_model import Email
from classifier import Classifier


@pytest.fixture
def classifier():
    return Classifier()


@pytest.fixture
def make_email(tmp_path):
    def _make(text, filename="test.txt"):
        filepath = tmp_path / filename
        filepath.write_text(text, encoding="utf-8")
        email = Email(str(filepath))
        email.read()
        return email
    return _make


@pytest.mark.parametrize("subject,body,expected", [
    ("Критический инцидент", "работа полностью остановлена", "urgent"),
    ("Сервер упал", "ошибка 500 уже час", "urgent"),
    ("Проблема с ноутбуком", "ноутбук не включается", "respond_today"),
    ("", "гарнитура не определяется системой", "respond_today"),
    ("Запрос доступа к GitLab", "прошу выдать доступ", "respond_soon"),
    ("Больничный", "направляю больничный лист нетрудоспособности", "respond_soon"),
    ("Дайджест", "корпоративный дайджест в этом выпуске", "no_action"),
    ("Демо", "приглашение на демо новой системы", "no_action"),
    ("Розыгрыш!", "победителем розыгрыша введите данные банковской карты", "spam"),
    ("", "totally-not-spam приз для вас", "spam"),
    ("Привет", "как дела", "unknown"),
    ("", "", "unknown"),
])
def test_classify_parametrized(classifier, make_email, subject, body, expected):
    text = f"Subject: {subject}\nFrom: test@test.ru\n\n{body}"
    email = make_email(text)
    result = classifier.classify(email)
    assert result == expected


def test_error_email_is_unknown(classifier, tmp_path):
    filepath = tmp_path / "bad.bin"
    filepath.write_bytes(b"\xff\xfe\x00")
    email = Email(str(filepath))
    email.read()
    result = classifier.classify(email)
    assert result == "unknown"


def test_classify_by_body_when_no_subject(classifier, make_email):
    email = make_email("From: x@x.ru\n\nработа полностью остановлена просим срочно проверить")
    result = classifier.classify(email)
    assert result == "urgent"

