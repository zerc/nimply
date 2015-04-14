# coding: utf-8
import os
import json
from datetime import datetime
from collections import OrderedDict

from dateutil.parser import parse
from comments.app import app


class MongoCommentsWrapper(object):
    """ Store comments into MongoDB.
    """
    def __init__(self, db, filename):
        self.filename = filename
        self.collection = db.comments

    def add_comment(self, line, author, message):
        comment = self.pre_save_comment(line, author, message)
        self.collection.insert(comment)
        return self.post_save_comment(comment)

    def pre_save_comment(self, line, author, message):
        comment = {
            'filename': self.filename,
            'line': [line],
            'author': author,
            'message': message,
            'date': datetime.now(),
        }
        return comment

    def post_save_comment(self, comment):
        comment.pop('_id')
        comment['date'] = comment['date'].strftime('%d-%m-%Y %H:%M')
        return comment

    def get_for_line(self, line):
        comments = self.collection.find({'line': str(line),
                                         'filename': self.filename})
        return [self.post_save_comment(comment) for comment in comments]

    def all(self):
        comments = self.collection.find({'filename': self.filename})
        return [self.post_save_comment(comment) for comment in comments]


class FormatWrapper(object):
    """
    Are wrapper for doing some things with `format_file`.
    """
    def __init__(self, source_filename):
        """
        :`source_filename`: are reviewed file
        """
        self.filename = get_format_filename(source_filename)

        # TODO: add exception handling
        if not os.path.exists(self.filename):
            self._raw_data = {'format': '0.1', 'comments': {}}
        else:
            with open(self.filename, 'r') as f:
                self._raw_data = json.loads(f.read())

        # special dict for getting comments for line
        self._dict_for_get = OrderedDict()
        for line_code, comments in self._raw_data['comments'].items():
            key = int(line_code.split('-')[-1])
            self._dict_for_get.setdefault(key, []).extend(
                [self.prepare_comment(c) for c in comments])

    def all(self):
        return self._dict_for_get

    def prepare_comment(self, raw_comment):
        raw_comment['date'] = \
            parse(raw_comment['date']).strftime('%d-%m-%Y %H:%M')
        return raw_comment

    @property
    def affected_lines(self):
        """
        Return list of lines numbers who have comments.
        """
        # TODO: cached_property?
        result = []
        for l in self._raw_data['comments'].keys():
            result.extend(self._unwrap_line(l))
        return result

    def get_for_line(self, line):
        """
        Return formatted string of comments for given `line` num.
        """
        comments = self._dict_for_get.get(line, None)
        return comments

    def add_comment(self, line, author, message):
        """
        Add comment by `author` to selected `line`.
        """
        self._raw_data['comments'].setdefault(line, []).append(
            {
                'date': str(datetime.now()),
                'author': author,
                'message': message
            }
        )
        return self._raw_data['comments'][line][-1]

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(json.dumps(self._raw_data))

    def _unwrap_line(self, line_str):
        """
        Unwrap line code like `1-4` to truly list of int's.
        """
        chunks = map(int, line_str.split('-'))
        if len(chunks) == 2:
            return list(range(chunks[0], chunks[1]+1))
        return chunks


def get_format_filename(original_filename):
    """
    Get filename based on given `original_filename`.
    """
    return original_filename.split('.')[0] + '.format'
