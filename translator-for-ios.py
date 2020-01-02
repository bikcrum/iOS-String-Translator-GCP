import sys

from ResourceTranslator import ResourceTranslator, get_all_langs

DEBUG = False

avail_langs = get_all_langs()
avail_lang_codes = [code[0] for code in avail_langs]

if 'en' in avail_lang_codes:
    avail_lang_codes.remove('en')

if not DEBUG:
    input_file = sys.argv[1]
    if len(sys.argv) == 3:
        lang_codes = sys.argv[2]
        lang_codes = list(set(lang_codes.split(',')) & set(avail_lang_codes))
    else:
        lang_codes = avail_lang_codes
else:
    input_file = 'Localizable.strings'
    lang_codes = avail_langs

rt = ResourceTranslator(input_file)

target_langs = []

for lang in avail_langs:
    if lang[0] in lang_codes:
        target_langs.append(lang)

rt.translate(target_langs, replace=False)
