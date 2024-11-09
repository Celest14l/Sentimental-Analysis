import googleapiclient.discovery
import pandas as pd
import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import sys

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyCy9wa92QMq_8kjlfSLXmTX3giPDzu_2q0"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

def fetch_all_comments(video_id):
    all_comments = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=1000  # Fetch 1000 comments
    )

    while request is not None:
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            all_comments.append(comment['textOriginal'])

        request = youtube.commentThreads().list_next(request, response)

    return all_comments

# Example usage
video_id = sys.argv[1]
# video_id = "MQ42OodljVM"
all_comments = fetch_all_comments(video_id)

# Save the comments to a text file with UTF-8 encodin    g
with open('./public/read.txt', 'w', encoding='utf-8') as file:
    for comment in all_comments:
        file.write(comment + '\n\n\n')

# Print the contents of the text file
# with open('read.txt', 'r', encoding='utf-8') as file:
#     print(file.read())

# Process comments for sentiment analysis and visualization
text = open('./public/read.txt', encoding='utf-8').read()
lower_case = text.lower()
cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

# Using word_tokenize because it's faster than split()
tokenized_words = word_tokenize(cleaned_text, "english")

# Removing Stop Words
final_words = []
for word in tokenized_words:
    if word not in stopwords.words('english'):
        final_words.append(word)

# Lemmatization - From plural to single + Base form of a word (example better-> good)
lemma_words = []
for word in final_words:
    word = WordNetLemmatizer().lemmatize(word)
    lemma_words.append(word)

emotion_list = []
with open('emotions.txt', 'r') as file:
    for line in file:
        clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
        word, emotion = clear_line.split(':')

        if word in lemma_words:
            emotion_list.append(emotion)

# print(emotion_list)
w = Counter(emotion_list)
# print(w)
# Check the number of comments loaded
num_comments_loaded = len(all_comments)
print("Number of comments loaded:", num_comments_loaded)


POS = 'positive'
NEG = 'negative'
NEUT = 'neutral'

classes = [POS, NEG, NEUT]


def sentiment_analyse(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    if score['neg'] > score['pos']:
        return NEG
    elif score['neg'] < score['pos']:
        return POS
    else:
        return NEUT

final_dic = {}

for c in classes:
    final_dic[c] = 0


# print('W.values are as follows')
# print(list(w.keys()))

for key, value in w.items():
    # print(str(key) + ' and ' + str(value))
    result = sentiment_analyse(key)
    final_dic[result] +=1


print("Final dic is ")
print(final_dic)
    

# sentiment_analyse(cleaned_text)
# print("The cleaned text is as follows:")
# print(cleaned_text)

fig, ax1 = plt.subplots()
ax1.bar(w.keys(), w.values())
fig.autofmt_xdate()
plt.xticks(rotation=90)
plt.savefig('./public/all_emotions.png')
# plt.show()

fig, ax1 = plt.subplots()
ax1.bar(final_dic.keys(), final_dic.values())
fig.autofmt_xdate()
plt.savefig('./public/classified_emotions.png')