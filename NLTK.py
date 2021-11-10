from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer

ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

example_text = "This is a secret prizes"
words = word_tokenize(example_text)

for i in words:
    print(ps.stem(i))
    if ps.stem(i) == "spam":
        print("ACTION")

for i in words:
   print(lemmatizer.lemmatize(i))


