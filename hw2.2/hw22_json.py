import codecs
import json

with codecs.open('newsfr.json', encoding="iso8859_5") as news:
    js = json.load(news)
    [print(i) for i in js.keys()]
    [print(i) for i in js['rss'].keys()]
    print(type(js['rss']['channel']))
    for key, value in js['rss']['channel'].items():
        if isinstance(value, dict):
            for k, v in value.items():
                print(v)
        elif isinstance(value, str):
            print(value)
        else:
            print(type(value))
            print(key)
            print(value)
            break
