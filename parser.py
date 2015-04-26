import sys
import yaml
from pymongo.errors import DuplicateKeyError
from newspaper import Article
from newspaper.article import ArticleException
from rabbit import Listener
from utils import articles_collection


def main():
    try:
        with open('./config.yml') as file:
            config = yaml.safe_load(file)
    except IOError:
        print("No volume mounted with file 'config.yml'")
        sys.exit(1)
    try:
        target_words = set(config['words'])
    except KeyError:
        print("'words' property is missing in 'config.yml'")
        sys.exit(1)
    try:
        rabbit_url = config['rabbit_url']
    except KeyError:
        print("'rabbit_url' property is missing in 'config.yml'")
        sys.exit(1)
    try:
        mongo_url = config['mongo_url']
    except KeyError:
        print("'mongo_url' property is missing in 'config.yml'")
        sys.exit(1)

    collection = articles_collection(mongo_url)

    def save_article(article):
        doc = {
            'url': article.url,
            'title': article.title,
            'keywords': article.keywords,
            'summary': article.summary,
            'images': article.images,
            'movies': article.movies
        }
        try:
            collection.insert(doc)
        except DuplicateKeyError:
            pass

    def action(message):
        article = Article(message['url'])
        article.download()
        try:
            article.parse()
            article.nlp()
        except ArticleException:
            pass
        else:
            if target_words < set(article.keywords):
                save_article(article)

    listener = Listener(rabbit_url=rabbit_url, action=action)
    listener.run()


if __name__ == '__main__':
    main()
