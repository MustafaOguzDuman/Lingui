import string
import os
import psycopg2
import config

from youtube_transcript_api import YouTubeTranscriptApi


config.set_values()


def connect():
    conn = psycopg2.connect(
        host=os.getenv('URL'),
        database=os.getenv('DATABASE_NAME'),
        user=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD')
    )

    return conn


connection = connect()
cursor = connection.cursor()


def add_word_to_word_id_table(word):
    # search for word in word_to_word_id table
    cursor.execute("SELECT word_id FROM word_to_id WHERE word = %s", (word,))

    # if word is not found in table, insert a new value
    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO word_to_id (word) VALUES (%s)", (word,))
        cursor.execute("SELECT word_id FROM word_to_id WHERE word = %s", (word,))
        connection.commit()

    return cursor.fetchone()[0]


# TODO: check if word can exist but the videos can be null
def add_word_to_word_to_video_table(word, video_id, thumbnail):
    # find the word_id from word_to_word_id table
    word_id = add_word_to_word_id_table(word)
    print("word", word_id)

    # add word to word_to_video table
    cursor.execute("SELECT video_id FROM word_to_video WHERE word_id = %s", (word_id,))
    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO word_to_video (word_id, video_id, thumbnail) VALUES (%s, %s, %s)",
                       (word_id, [video_id], thumbnail))
    else:
        array = cursor.fetchone()[0]
        if video_id not in array:
            array.append(video_id)
        cursor.execute("UPDATE word_to_video SET video_id = %s WHERE word_id = %s", (array, word_id))

    connection.commit()


def add_captions_to_table(video_id, word_array, start_time, duration, content, thumbnail):
    # insert these values into the captions table, if it does not exist

    print("array:", word_array)
    word_id_array = []

    for word in word_array:
        # find word id from word_to_id table
        cursor.execute("SELECT word_id FROM word_to_id WHERE word = %s", (word.lower(),))
        word_id_array.append(cursor.fetchone()[0])

    cursor.execute("SELECT video_id, start_time FROM caption "
                   "WHERE video_id = %s AND start_time = %s", (video_id, start_time))

    # video does not exist in captions table
    if cursor.rowcount == 0:
        print("inserting")
        cursor.execute("INSERT INTO caption (video_id, word_id_array, start_time, duration, content, thumbnail) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (video_id, word_id_array, start_time, duration, content, thumbnail))
    else:
        print("updating")
        cursor.execute("UPDATE caption SET word_id_array = %s, start_time = %s, duration = %s, content = %s, thumbnail = %s "
                       "WHERE video_id = %s", (word_id_array, start_time, duration, content, thumbnail, video_id))

    connection.commit()


def populate_database(video_id, thumbnail):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_manually_created_transcript(['en-GB', 'en', 'en-US']).fetch()

    # remove \xa0 from transcript
    # transcript = transcript.replace('\xa0', ' ')

    # if video id is already in the database, do not add it again
    """
    cursor.execute("SELECT video_id FROM caption WHERE video_id = %s", video_id)

    if cursor.rowcount != 0:
        return
    """

    for caption in transcript:
        caption_text = caption['text'].replace('\n', ' ')
        caption_text = caption_text.replace('\xa0', ' ')

        lower_words = []

        for word in caption_text.split():
            lower_word = word.lower()
            # remove punctuation
            lower_word = lower_word.translate(str.maketrans('', '', string.punctuation))
            lower_words.append(lower_word)

            # add word and newly generated word_id to database
            add_word_to_word_id_table(lower_word)

            # add word and its video, thumbnail to database
            add_word_to_word_to_video_table(word=lower_word, video_id=video_id, thumbnail=thumbnail)

        # add caption to database
        add_captions_to_table(video_id=video_id, word_array=lower_words,
                              start_time=caption['start'], duration=caption['duration'],
                              content=caption_text,
                              thumbnail=thumbnail)


"""
    video retrieverdan bir kelime için video idler ve thumbnail'leri al
    bu video id'lerin her birinin transcript'inde verilen kelime aratılır


    black kelimesinin geçtiği videonun transkripti
    ['black', 'hole', 'star', 'the', 'star', 'that', 'exist']
    
    
    black kelimesinin içinde geçtiği videolar : video5, video10, video15
    hole 
    star
    ...
"""


def main():
    video_ids = ['FFEm7FRMlb4', 'bK6ldnjE3Y0']
    # video_id = 'aeWyp2vXxqA'
    thumbnails = ["English Conversation at Courtroom— English Conversation Practice Video With Subtitles🌍Part 15",
                  "Oppenheimer | Official Trailer"]

    for i in range(len(video_ids)):
        populate_database(video_ids[i], thumbnails[i])



def search_for_word_in_youtube():
    pass


if __name__ == "__main__":
    main()


# TODO: caption = video_id, [word_id], start_time, duration, text
# TODO: word_video = word_id, video_id

