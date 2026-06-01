import os
import pytest
from processor import MailProcessor


@pytest.fixture
def inbox(tmp_path):
    d = tmp_path / "inbox"
    d.mkdir()
    return d


@pytest.fixture
def output(tmp_path):
    d = tmp_path / "processed"
    d.mkdir()
    return d


def write_mail(directory, filename, content):
    f = directory / filename
    f.write_text(content, encoding="utf-8")
    return f


def test_process_all_creates_category_dirs(inbox, output):
    write_mail(inbox, "urgent.txt", "Subject: Инцидент\nFrom: a@b.ru\n\nработа полностью остановлена")
    write_mail(inbox, "spam.txt", "Subject: Приз\nFrom: x@spam.com\n\nдля получения приза введите данные")

    processor = MailProcessor(str(inbox), str(output))
    processor.process_all()

    assert os.path.isdir(str(output / "urgent"))
    assert os.path.isdir(str(output / "spam"))


def test_email_copied_to_correct_folder(inbox, output):
    write_mail(inbox, "mail.txt", "Subject: Доступ\nFrom: u@c.ru\n\nпрошу выдать доступ к GitLab")

    processor = MailProcessor(str(inbox), str(output))
    processor.process_all()

    assert os.path.isfile(str(output / "respond_soon" / "mail.txt"))


def test_unreadable_email_goes_to_unknown(inbox, output):
    f = inbox / "bad.bin"
    f.write_bytes(b"\xff\xfe\x00\x01\x02")

    processor = MailProcessor(str(inbox), str(output))
    processor.process_all()

    assert os.path.isfile(str(output / "unknown" / "bad.bin"))


def test_empty_email_goes_to_unknown(inbox, output):
    write_mail(inbox, "empty.txt", "")

    processor = MailProcessor(str(inbox), str(output))
    processor.process_all()

    assert os.path.isfile(str(output / "unknown" / "empty.txt"))


def test_missing_inbox_does_not_crash(tmp_path, output):
    processor = MailProcessor(str(tmp_path / "nonexistent"), str(output))
    processor.process_all()
    assert processor.emails == []


def test_process_all_counts_emails(inbox, output):
    for i in range(3):
        write_mail(inbox, f"mail{i}.txt", f"Subject: Тест {i}\nFrom: u@c.ru\n\nтекст {i}")

    processor = MailProcessor(str(inbox), str(output))
    processor.process_all()

    assert len(processor.emails) == 3


def test_hidden_files_are_skipped(inbox, output):
    write_mail(inbox, ".DS_Store", "мусор")
    write_mail(inbox, "real.txt", "Subject: Дайджест\nFrom: n@c.ru\n\nкорпоративный дайджест в этом выпуске")

    processor = MailProcessor(str(inbox), str(output))
    processor.process_all()

    assert len(processor.emails) == 1


def test_print_report_output(inbox, output, capsys):
    write_mail(inbox, "u.txt", "Subject: Инцидент\nFrom: a@b.ru\n\nработа полностью остановлена")
    write_mail(inbox, "s.txt", "Subject: Спам\nFrom: x@x.ru\n\nдля получения приза введите данные")

    processor = MailProcessor(str(inbox), str(output))
    processor.process_all()
    processor.print_report()

    captured = capsys.readouterr()
    assert "urgent" in captured.out
    assert "spam" in captured.out
    assert "Всего" in captured.out
