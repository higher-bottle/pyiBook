import glob
import pandas as pd
import os
import sqlite3
from datetime import datetime


def local_ibook_directory(db_path=None):
    """locate the local Ibook directory"""
    path = {"book_path": "", "book_db": "",
            "note_path": "", "note_db": ""}
    if db_path is None:
        home_directory = os.path.expanduser('~')
        db_path = os.path.join(home_directory,
                               'Library',
                               'Containers',
                               'com.apple.iBooksX',
                               'Data',
                               'Documents')

    book_parent_path = os.path.join(db_path, 'BKLibrary')
    notation_parent_path = os.path.join(db_path, 'AEAnnotation')

    if not os.path.exists(db_path):
        # the path doesn't exist
        path['book_path'] = ''
        path['note_path'] = ''
        return path
    else:
        path['book_path'] = book_parent_path
        path['note_path'] = notation_parent_path
        try:
            book_db_path = glob.glob(os.path.join(book_parent_path, 'BKLibrary*.sqlite'))[0]
            path['book_db'] = book_db_path
        except IndexError:
            path['book_db'] = ''
            pass

        try:
            notation_db_path = glob.glob(os.path.join(notation_parent_path, 'AEAnnotation*.sqlite'))[0]
            path['note_db'] = notation_db_path
        except IndexError:
            path['note_db'] = ''
            pass

        return path


#%%

def connect_to_db(book_db_path, notation_db_path):
    """Define the path to the Apple Books SQLite database,
        Connect to the SQLite database"""
    conn_book = sqlite3.connect(book_db_path)
    conn_notation = sqlite3.connect(notation_db_path)

    cursor_book = conn_book.cursor()
    cursor_notation = conn_notation.cursor()

    # select all the books in the local Apple Books Database
    df_book = pd.read_sql_query('''SELECT ZTITLE, ZASSETID, ZAUTHOR, ZCONTENTTYPE 
                                            FROM ZBKLIBRARYASSET ORDER BY ZTITLE;''', conn_book)

    # select all the notes in the local Apple Books Database
    df_notation = pd.read_sql_query('''SELECT ZANNOTATIONSELECTEDTEXT, ZANNOTATIONNOTE, ZANNOTATIONASSETID, 
                                                    ZANNOTATIONSTYLE, ZANNOTATIONMODIFICATIONDATE
                                                    FROM ZAEANNOTATION 
                                                    WHERE ZANNOTATIONDELETED=0 AND ZANNOTATIONSELECTEDTEXT IS NOT NULL 
                                                    ORDER BY ZANNOTATIONMODIFICATIONDATE DESC;''',
                                    conn_notation)
    conn_book.close()
    conn_notation.close()

    df_book.columns = ['BookName', 'ID', 'Author', 'FileType']
    df_book['FileType'] = df_book['FileType'].map({1: 'Book', 3: 'pdf'})
    df_notation.columns = ['HighLights', 'Notes', 'ID', 'Style', 'UpdateTime']
    df_notation['Style'] = df_notation['Style'].map({0: 'Underline',
                                                     1: 'Green',
                                                     2: 'Blue',
                                                     3: 'Yellow',
                                                     4: 'Pink',
                                                     5: 'Purple'})
    datediff = (datetime(2001, 1, 1) - datetime(1970, 1, 1)).days
    df_notation['UpdateTime'] = df_notation['UpdateTime'].apply(
        lambda x: (pd.Timestamp(x, unit='s') + pd.Timedelta(days=datediff, hours=8)).strftime('%Y-%m-%d %H:%M'))

    df_book = df_book.merge(df_notation[['ID','HighLights']], how='left', on='ID').groupby(['BookName', 'ID', 'Author', 'FileType']).size().reset_index(name = '# of Notes')
    df_notation = df_notation.merge(df_book[['ID','BookName']], how='left', on='ID')

    return df_book, df_notation