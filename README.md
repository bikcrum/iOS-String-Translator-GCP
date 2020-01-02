# Translator for iOS string resource


### How to bulk translate?

#### Prerequisites

1. Must have python version 3
2. Must have billing enabled in Google Cloud Platform (GCP)
3. Install the google client translation library `pip install --upgrade google-cloud-translate`
4. Create service account in GCP 

#### Steps:

1. Clone and go to the project directory
2. Paste above service account and rename to `project-service-account.json`
3. Use this command ``python translator-for-ios.py <source-string-file> <languages list>``
4. Example ``python translator-for-ios.py Localizable.strings fr`` or  ``python translator-for-ios.py Localizable.strings fr,de,nl``
5. To translate to all available languages just provide source string in the command
6. After above operation you will get new translated file(s) in current directory