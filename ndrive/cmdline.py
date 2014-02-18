"""
USAGE:
    ndrive [action] [option]

ACTIONS:
    login   123
    upload  123

OPTIONS:
    -l --login <id>     
    
"""

from __future__ import print_function

try:
    input = __builtins__['raw_input']
except (AttributeError, KeyError):
    pass

from 

actions = {
    'authorize' : DoNothingAction,
    'follow'    : FollowAction,
    'friends'   : FriendsAction,
    'list'      : ListsAction,
    'mylist'    : MyListsAction,
    'help'      : HelpAction,
    'leave'     : LeaveAction,
    'public'    : PublicAction,
    'pyprompt'  : PythonPromptAction,
    'replies'   : RepliesAction,
    'search'    : SearchAction,
    'set'       : SetStatusAction,
    'shell'     : TwitterShell,
}
