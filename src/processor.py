import os
import shutil
import logging

from email_model import Email
from classifier import Classifier


class MailProcessor:
    def __init__(self, inbox_dir="inbox", output_dir="processed"):
        self.inbox_dir = inbox_dir
        self.output_dir = output_dir
        self.classifier = Classifier()
        self.emails = []

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("processing.log", encoding="utf-8"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def process_all(self):
        self.logger.info(f"Начало обработки: {self.inbox_dir}")

        try:
            filenames = os.listdir(self.inbox_dir)
        except FileNotFoundError:
            self.logger.error(f"Папка не найдена: {self.inbox_dir}")
            return

        for filename in filenames:
            if filename.startswith("."):
                continue
            filepath = os.path.join(self.inbox_dir, filename)
            self._process_one(filepath)

        self.logger.info(f"Готово. Обработано писем: {len(self.emails)}")

    def _process_one(self, filepath):
        email = Email(filepath)
        success = email.read()

        if not success:
            self.logger.warning(f"{email.filename}: не прочитано ({email.error})")

        self.classifier.classify(email)
        self._move_email(email)
        self.emails.append(email)
        self.logger.info(f"{email.filename} -> {email.category}")

    def _move_email(self, email):
        dest_dir = os.path.join(self.output_dir, email.category)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(email.filepath, os.path.join(dest_dir, email.filename))

    def print_report(self):
        stats = {}
        for email in self.emails:
            stats[email.category] = stats.get(email.category, 0) + 1

        print("\nРЕЗУЛЬТАТЫ ОБРАБОТКИ:")
        print("------")
        for cat, count in sorted(stats.items()):
            print(f"{cat}: {count} писем")
        print("------")
        print(f"Всего: {len(self.emails)} писем")
