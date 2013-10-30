"""
Misc. support methods for interacting with the database.
Assumes db connection already established. 
"""

from dbSetup import *

# Retrieve tagID from lastfm_taglist. If not present, generate new tagID (via table auto_increment)
# Since the prepAnnoTable/prepScrobbleTable scripts handles the tag names with a dictionary, we want to be able to save time by not searching through the non-indexed tag_names (hence the "check" variable)

def tagIDfromName(tag,check=True):
    if check:
        cursor=db.cursor()
        cursor.execute("select tag_id from lastfm_taglist where tag_name=%s",(tag))
        result = cursor.fetchone()
        closeDBConnection(cursor)
        if result:
            return result[0]

    cursor=db.cursor()
    cursor.execute("insert into lastfm_taglist (tag_name) values (%s)",(tag))
    cursor.execute("select last_insert_id();")
    tid = cursor.fetchone()[0]
    closeDBConnection(cursor)
    return tid

# Retrieve item ID from lastfm_itemlist. If not present, generate new item ID (via table auto_increment)
# Since the prepAnnoTable/prepScrobbleTable scripts handles the item names with a dictionary, we want to be able to save time by not searching through the non-indexed tag_names (hence the "check" variable)

# ASSUME THINGS ARE ALREADY SPLIT

def itemIDfromURL(item,check=True):
    if check:
        cursor=db.cursor()
        #cursor.execute("select item_id from lastfm_itemlist where item_url=%s",(item))
        cursor.execute("select item_id from lastfm_itemlist where item_url=%s",(item))
        result = cursor.fetchone()
        closeDBConnection(cursor)
        if result:
            return result[0]

    # This block determines the item type (based on URL format, e.g. "artist/album/songName"), and stores item data as appropriate.
    spl = item.split('/') # this was previously "spl = item.replace('_','').split('/')" - don't know why I was doing the replace...

    artist = spl[0]
    
    if len(spl)==1:
        itemType = 'artist'
        album = None
        song = None
    elif len(spl)==2:
        itemType = 'album'
        album = spl[1]
        song = None
    elif len(spl)==3:
        itemType='song'
        if len(spl[1])>0:
            album = spl[1]
        else:
            album=None
        song = spl[2]
    else:
        print item,spl
        raise()
    
    cursor=db.cursor()
    cursor.execute("insert into lastfm_itemlist (item_type,artist,album,song,item_url) values (%s,%s,%s,%s,%s);",(itemType,artist,album,song,item))
    cursor.execute("select last_insert_id();")
    iid = cursor.fetchone()[0]
    closeDBConnection(cursor)
    return iid


# Retrieve tagName from lastfm_taglist. 
def tagNamefromID(ID):
    cursor=db.cursor()
    cursor.execute("select tag_name from lastfm_taglist where tag_id=%s",(ID))
    result = cursor.fetchone()
    closeDBConnection(cursor)
    return result[0]
        