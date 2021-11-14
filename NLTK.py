from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import wordnet
nltk.download('punkt')
nltk.download('wordnet')


ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

example_text = "award awarding accolade honor honour laurels prize present grant"
words = word_tokenize(example_text)

# Stemming
for i in words:
    print(ps.stem(i))
    if ps.stem(i) == "spam":
        print("ACTION")
# Lemmatization
for i in words:
    print(lemmatizer.lemmatize(i))

# Synonyms
synonyms = []
for syn in wordnet.synsets('prize'):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())
print(synonyms)
