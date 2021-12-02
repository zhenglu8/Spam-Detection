from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import wordnet

# May need to download wordnet first
# nltk.download('punkt')
# nltk.download('wordnet')

ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# create banned word list in here
spam_word_list = "cash discount prize free urgent"
words = word_tokenize(spam_word_list)
# print(words)

ban_word = []
# Synonyms
for i in words:
    for syn in wordnet.synsets(ps.stem(i)):
        for lemma in syn.lemmas():
            ban_word.append(lemma.name())

# lowercase word in list
for i in range(len(ban_word)):
    ban_word[i] = ban_word[i].lower()
# print(ban_word)

# remove repeated word from list
ban_word = list(dict.fromkeys(ban_word))
# print(ban_word)


# Stemming banned word list
stemming_list = []
for i in ban_word:
    stemming_list.append(ps.stem(i))
# print(stemming_list)

# Remove punctuation
new_list = []
for char in stemming_list:
    if char.find('_') != -1:
        new_list.append(char.replace('_', ''))
    else:
        new_list.append(char)
print(new_list)
