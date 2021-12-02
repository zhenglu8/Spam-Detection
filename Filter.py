# Import packages
import pandas as pd
import re

# Read dataset
sms_spam = pd.read_csv('SMSSpamCollection', sep='\t',
                       header=None, names=['Label', 'SMS'])

# sms_spam.shape
# sms_spam.head()

sms_spam['Label'].value_counts(normalize=True)

# Randomize the dataset
data_randomized = sms_spam.sample(frac=1, random_state=1)

# Calculate index for split
training_test_index = round(len(data_randomized) * 0.8)

# Split into training and test sets
training_set = data_randomized[:training_test_index].reset_index(drop=True)
testing_set = data_randomized[training_test_index:].reset_index(drop=True)

# training_set.shape
# test_set.shape

# Analyze percentage of spam hand ham in training set
training_set['Label'].value_counts(normalize=True)
# Analyze percentage of spam hand ham in testing set
testing_set['Label'].value_counts(normalize=True)

# After cleaning
training_set['SMS'] = training_set['SMS'].str.replace(
    '\W', ' ')  # Removes punctuation
training_set['SMS'] = training_set['SMS'].str.lower()
training_set.head(3)

training_set['SMS'] = training_set['SMS'].str.split()

vocabulary = []
for sms in training_set['SMS']:
    for word in sms:
        vocabulary.append(word)

vocabulary = list(set(vocabulary))
len(vocabulary)

word_counts_per_sms = {unique_word: [
    0] * len(training_set['SMS']) for unique_word in vocabulary}

for index, sms in enumerate(training_set['SMS']):
    for word in sms:
        word_counts_per_sms[word][index] += 1

word_counts = pd.DataFrame(word_counts_per_sms)
print(word_counts.head())

training_set_clean = pd.concat([training_set, word_counts], axis=1)
print(training_set_clean.head())

# Isolating spam and ham messages first
spam_messages = training_set_clean[training_set_clean['Label'] == 'spam']
ham_messages = training_set_clean[training_set_clean['Label'] == 'ham']

# P(Spam) and P(Ham)
p_spam = len(spam_messages) / len(training_set_clean)
p_ham = len(ham_messages) / len(training_set_clean)

# N_Spam
n_words_per_spam_message = spam_messages['SMS'].apply(len)
n_spam = n_words_per_spam_message.sum()

# N_Ham
n_words_per_ham_message = ham_messages['SMS'].apply(len)
n_ham = n_words_per_ham_message.sum()

# N_Vocabulary
n_vocabulary = len(vocabulary)

# Laplace smoothing
alpha = 1

# Initiate parameters
parameters_spam = {unique_word: 0 for unique_word in vocabulary}
parameters_ham = {unique_word: 0 for unique_word in vocabulary}

# Calculate parameters
for word in vocabulary:
    # spam_messages already defined
    n_word_given_spam = spam_messages[word].sum()
    p_word_given_spam = (n_word_given_spam + alpha) / \
        (n_spam + alpha * n_vocabulary)
    parameters_spam[word] = p_word_given_spam

    n_word_given_ham = ham_messages[word].sum()  # ham_messages already defined
    p_word_given_ham = (n_word_given_ham + alpha) / \
        (n_ham + alpha * n_vocabulary)
    parameters_ham[word] = p_word_given_ham


def classify(message):
    message = re.sub('\W', ' ', message)
    message = message.lower().split()

    p_spam_given_message = p_spam
    p_ham_given_message = p_ham

    for word in message:
        if word in parameters_spam:
            p_spam_given_message *= parameters_spam[word]

        if word in parameters_ham:
            p_ham_given_message *= parameters_ham[word]

    # print('P(Spam|message):', p_spam_given_message)
    # print('P(Ham|message):', p_ham_given_message)

    # Return 0 if the message is Ham
    if p_ham_given_message >= p_spam_given_message:
        #print('This message is Ham')
        return 0
    # Return 1 if the message is Spam
    elif p_ham_given_message < p_spam_given_message:
        #print('This message is Spam')
        return 1


"""
# Classify testing
classify('WINNER!! This is the secret code to unlock the money: C3421.')
classify("Sounds good, Tom, then see u there")

classify('NICE! You have won $1000! Click here')
classify("WINNER! Click here to unlock prizes")
classify("You have won $1000! Click here")

# classify("deduct")
# classify("Warning")
#classify('Counter + 1')
"""
"""# Accuracy testing
def classify_testing_set(message):
    message = re.sub('\W', ' ', message)
    message = message.lower().split()

    p_spam_given_message = p_spam
    p_ham_given_message = p_ham

    for word in message:
        if word in parameters_spam:
            p_spam_given_message *= parameters_spam[word]

        if word in parameters_ham:
            p_ham_given_message *= parameters_ham[word]

    if p_ham_given_message > p_spam_given_message:
        return 'ham'
    elif p_spam_given_message > p_ham_given_message:
        return 'spam'
    else:
        return 'needs human classification'


testing_set['predicted'] = testing_set['SMS'].apply(classify_testing_set)
print(testing_set.head())

correct = 0
total = testing_set.shape[0]

for row in testing_set.iterrows():
    row = row[1]
    if row['Label'] == row['predicted']:
        correct += 1

print('Correct:', correct)
print('Incorrect:', total - correct)
print('Accuracy:', correct / total)
"""
