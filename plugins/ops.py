"""
Written by @waltz.
"""

from util import hook

def db_init(db):
    """Checks to see if our database has the 'ops' table and create it if not."""
    db.execute("create table if not exists ops(nick, primary key(nick), unique(nick))")
    db.commit()
    return db
               
@hook.command
def ops(input, nick=None, conn=None, chan=None):
    # """Grants operator priveleges to the requesting user."""
    db_init(db).execute("insert or replace into ops(nick) values (?)", nick.lower())
    conn.cmd('MODE', [ chan, '+o', nick ])

@hook.command
def ops_list(input, nick=None, conn=None, chan=None, db=None):
    # """Returns a list of people who will get auto-op'd."""
    db = db_init(db)
    nicks = db.execute("select nick from ops").fetchall()
    db.commit()
    
    message = ""
    for nick in nicks:
        message = message + " " + nick[0]

    return message

@hook.event('NICK')
@hook.event('JOIN')
def give_ops(input, nick=None, conn=None, db=None, bot=None):
    # """Gives certain user's operator priveleges when they show up."""
    nick = nick.lower()
    db = db_init(db)
    result = db.execute("select nick from ops where nick='?'", nick).fetchall()
    
    if result:
        conn.cmd('MODE', [ chan, '+o', nick ])
