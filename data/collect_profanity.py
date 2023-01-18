import requests
import pandas as pd
from io import StringIO

profanity_words = []

profanity_words += requests.get(
    'https://raw.githubusercontent.com/coffee-and-fun/google-profanity-words/main/data/list.txt'
).text.splitlines()

profanity_words += requests.get(
    'https://raw.githubusercontent.com/rominf/profanity-filter/master/profanity_filter/data/en_profane_words.txt'
).text.splitlines()

profanity_words += requests.get(
    'https://raw.githubusercontent.com/web-mech/badwords/master/lib/lang.json'
).json()['words']

profanity_words += requests.get(
    'https://raw.githubusercontent.com/mapmeld/profanity-pgp/main/profanity.json'
).json()

profanity_words += requests.get(
    'https://raw.githubusercontent.com/zacanger/profane-words/master/words.json'
).json()

profanity_words += pd.read_csv(StringIO(requests.get(
    'https://raw.githubusercontent.com/surge-ai/profanity/main/profanity_en.csv'
).text), sep=',')['text'].tolist()


print('Collect', len(profanity_words))
profanity_words = set(profanity_words)
profanity_words = [i.lower() for i in profanity_words if len(i.split(' ')) == 1]
print('Collect unique', len(profanity_words))
with open('../profanity_check/data/profanity.txt', 'w') as f:
    f.write('\n'.join(profanity_words))

df_profanity = pd.DataFrame([[1, word]for word in profanity_words], columns=['profanity', 'words'])

all_words = set(requests.get(
    'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
).text.splitlines())

print('Collect english words', len(all_words))

clear_df = pd.DataFrame([[0, word]for word in all_words if not word in profanity_words], columns=['profanity', 'words'])

df = pd.concat([df_profanity, clear_df])
print('Collect', len(df))
print('Clear words', len(df[df['profanity']==0]))
print('Profanity words', len(df[df['profanity']==1]))
df.to_csv('data.csv', index=False)

