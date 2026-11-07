
import requests
import os

# Folder to save downloaded documents
RAW_FOLDER = os.path.join("Day-03", "data", "raw")

os.makedirs(RAW_FOLDER, exist_ok=True)

# Official Ministry of Labour documents
documents = {
    "labour_faqs_2025.pdf":
        "https://labour.gov.in/static/uploads/2026/01/de4758d5bfeffc456d7de97a801891b0.pdf",

    "additional_faqs_2026.pdf":
        "https://www.labour.gov.in/static/uploads/2026/03/a4ccf4c6d97c4f1f36a6d83f8c64213d.pdf",

    "social_security_code.pdf":
    "https://labour.maharashtra.gov.in/sites/default/files/2026-04/the-code-on-social-security-2020-no-36-of-2020.pdf"
}


def download_documents():

    for filename, url in documents.items():

        file_path = os.path.join(RAW_FOLDER, filename)

        try:
            print("\nDownloading:", filename)

            response = requests.get(
                url,
                timeout=30
            )

            response.raise_for_status()

            with open(file_path, "wb") as file:
                file.write(response.content)

            print("Download successful!")

        except requests.exceptions.Timeout:
            print("Error: Download timed out.")

        except requests.exceptions.RequestException as error:
            print("Download failed:", error)

        except OSError as error:
            print("File saving error:", error)


if __name__ == "__main__":
    download_documents()
