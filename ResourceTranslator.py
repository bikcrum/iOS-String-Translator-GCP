import json
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

CREDENTIAL_FILE = 'project-service-account.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIAL_FILE

from google.cloud import translate_v3beta1 as translate

client = translate.TranslationServiceClient()

project_id = json.load(open(CREDENTIAL_FILE))['project_id']
location = 'global'

parent = client.location_path(project_id, location)


def get_all_langs():
    lang = []
    response = client.get_supported_languages(parent=parent, display_language_code='en')
    for language in response.languages:
        lang.append((language.language_code, language.display_name))

    return lang


def is_directory(path):
    return os.path.exists(path) and not os.path.isfile(path)


class ResourceTranslator:
    def __init__(self, file_name):
        file = open(file_name, 'r')
        self.keys = []
        self.values = []
        for line in file.readlines():
            if line is not None and "=" in line:
                key, value = line.split("=")
                self.keys.append(key)
                self.values.append(value)
            else:
                self.keys.append(line)
                self.values.append(' ')

    @staticmethod
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def translate(self, langs, replace=False):
        for lang in langs:
            if not os.path.exists('translated') or os.path.isfile('translated'):
                os.mkdir('translated')

            dir = 'translated/%s-%s' % (lang[1], lang[0])
            if os.path.exists(dir):
                if os.path.isfile(dir):
                    os.mkdir(dir)
                else:
                    print("File already exist for translation %s (%s)" % (lang[1], lang[0]))
                    continue
            else:
                os.mkdir(dir)

            out_file = dir + '/' + 'Localizable.strings'

            texts_list = self.chunks(self.values, 128)
            new_values = []

            for texts in texts_list:
                translations = client.translate_text(
                    parent=parent,
                    contents=texts,
                    mime_type='text/plain',  # mime types: text/plain, text/html
                    source_language_code='en-US',
                    target_language_code=lang[0])

                for translation in translations.translations:
                    new_values.append(translation.translated_text)

            print("Translated %d in %s (%s)" % (len(new_values), lang[1], lang[0]))

            f = open(out_file, "w")

            out = ''
            for i in range(len(self.keys)):
                if not new_values[i] or len(new_values[i].strip()) == 0:
                    out += self.keys[i]
                else:
                   out += '%s = %s' % (self.keys[i], new_values[i])

            f.write(out)
            f.close()
