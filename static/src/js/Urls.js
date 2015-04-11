var URLS = {};

/* List & upload files */
URLS.FILES_BASE = '/api/files/';

/* Get file`s detail url */
URLS.file_detail = function (fname) {
    return URLS.FILES_BASE + fname;
};

URLS.COMMENTS_BASE = '/api/comments/';

URLS.comments_add = function (fname) {
    return URLS.COMMENTS_BASE + fname;
}

module.exports = URLS;
