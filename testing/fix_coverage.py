import sqlite3

QUERY_SITE_PACKAGES = '''\
SELECT id FROM file WHERE path LIKE '%site-packages/future_annotations.py'
'''
QUERY_NOT_SITE_PACKAGES = '''\
SELECT id FROM file
WHERE (
    path LIKE '%/future_annotations.py' AND
    path NOT LIKE '%site-packages/future_annotations.py'
)
'''
QUERY_TEST = '''\
SELECT id FROM file WHERE path LIKE '%/future_annotations_test.py'
'''
MERGE_FILE_IN_ARC = 'UPDATE arc SET file_id = ? WHERE file_id = ?'
DELETE_FROM_ARC = 'DELETE FROM arc WHERE file_id NOT IN (?, ?)'
DELETE_FROM_FILE = 'DELETE FROM file WHERE id NOT IN (?, ?)'


def main() -> int:
    with sqlite3.connect('.coverage') as db:
        (site_packages,) = db.execute(QUERY_SITE_PACKAGES).fetchone()
        (src,) = db.execute(QUERY_NOT_SITE_PACKAGES).fetchone()
        (test,) = db.execute(QUERY_TEST).fetchone()
        db.execute(MERGE_FILE_IN_ARC, (src, site_packages))
        db.execute(DELETE_FROM_ARC, (src, test))
        db.execute(DELETE_FROM_FILE, (src, test))
        return 0


if __name__ == '__main__':
    exit(main())
