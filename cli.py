import argparse

from core.analyzer import generate_summary, rewrite_content
from core.extractor import extract_text


def main():
    parser = argparse.ArgumentParser(
        description="Document Analysis and Rewriting CLI"
    )

    parser.add_argument(
        "action",
        choices=["summarize", "rewrite"],
        help="Action to perform",
    )

    parser.add_argument(
        "--file-path",
        help="Path to the document file",
    )

    parser.add_argument(
        "--text",
        help="Direct text input (overrides file input)",
    )

    parser.add_argument(
        "--model",
        default="llama3.1:8b",
        help="Model to use (default: llama3.1:8b)",
    )

    parser.add_argument(
        "--length",
        default="medium",
        choices=["short", "medium", "long"],
        help="Summary length",
    )

    parser.add_argument(
        "--tone",
        default="Professional",
        choices=[
            "Professional",
            "Formal",
            "Casual",
            "Executive",
            "Technical",
            "Academic",
            "Marketing",
            "Simple English",
        ],
        help="Rewrite tone",
    )

    parser.add_argument(
        "--target",
        default="Full Document",
        choices=["Summary", "Full Document"],
        help="Rewrite the summary or the full document",
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Temperature (0.0 - 1.0)",
    )

    args = parser.parse_args()

    try:
        # Read input
        if args.text:
            document_text = args.text

        elif args.file_path:
            with open(args.file_path, "rb") as uploaded_file:
                document_text = extract_text(uploaded_file, args.file_path)

        else:
            raise ValueError(
                "Please provide either --text or --file-path."
            )

        # -------------------- Summarize --------------------
        if args.action == "summarize":

            summary = generate_summary(
                document_text,
                args.length,
                args.model,
            )

            print("\n========== SUMMARY ==========\n")
            print(summary)

        # -------------------- Rewrite --------------------
        elif args.action == "rewrite":

            # Generate summary first
            summary = generate_summary(
                document_text,
                args.length,
                args.model,
            )

            rewritten_content = rewrite_content(
                document_text,
                summary,
                args.tone,
                args.temperature,
                args.target,
                args.model,
            )

            print("\n========== REWRITTEN CONTENT ==========\n")
            print(rewritten_content)

    except Exception as e:
        print(f"Error processing the document: {e}")


if __name__ == "__main__":
    main()