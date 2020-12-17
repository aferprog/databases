import csv
import json
import codecs
from io import StringIO

def get_categories(path):
    file = codecs.open(path, "r", "utf_8_sig")
    data = json.load(file)['items']
    return [{'id': x['id'], 'name': x['snippet']['title']} for x in data]


def get_videos(path):
    def improve_video(video):
        # print(video)
        data = csv.reader([video['tags']], delimiter='|')
        data = list(data)
        if data:
            tags = data[0]
        else:
            tags = ''
        del video['tags']
        if 'thumbnail_link' in video:
            del video['thumbnail_link']
        return {'video': video, 'tags': tags}

    with (codecs.open(path, "r", "utf_8_sig")) as file:
        data = csv.DictReader(file, delimiter=',')
        return [improve_video(video) for video in data]


def write_videos(path, videos):
    def tags_string(tags):
        with StringIO('') as res:
            writer = csv.writer(res, delimiter='|')
            writer.writerow(tags)
            return res.getvalue()
    with (codecs.open(path, "w", "utf_8_sig")) as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['video_id', 'trending_date', 'title', 'channel_title', 'category_id',
                         'publish_time', 'views', 'likes', 'dislikes', 'comment_count', 'comments_disabled',
                         'ratings_disabled', 'video_error_or_removed', 'description', 'tags'])
        for video in videos:
            video['video'].append(tags_string(video['tags']))
            writer.writerow(video['video'])

