from processor import MailProcessor

if __name__ == "__main__":
    processor = MailProcessor(
        inbox_dir="inbox",
        output_dir="processed"
    )
    processor.process_all()
    processor.print_report()