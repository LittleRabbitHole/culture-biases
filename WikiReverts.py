#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 16:05:37 2018
some reading to understand revert: https://meta.wikimedia.org/wiki/Research:Revert

use of revert library
http://paws-public.wmflabs.org/paws-public/User:EpochFail/editquality/ipython/reverted_detection_demo.ipynb

@author: angli
"""

###collecting whether the revision is reverted ########

import mwapi, mwreverts.api

# Gather a page's revisions from the API
session = mwapi.Session("https://en.wikipedia.org", user_agent="mwreverts basic usage script")


#An edit can reverting other edits, it can be reverted, or it can be reverted_to by another edit.
def print_revert_status(rev_id, reverting, reverted, reverted_to):
    """Prints a nice, pretty version of a revert status."""
    print(str(rev_id) + ":")
    if reverting is not None:
        print(" - reverting {0} other edits".format(len(reverting.reverteds)))
    if reverted is not None:
        print(" - reverted in {revid} by {user}".format(**reverted.reverting))
    if reverted_to is not None:
        print(" - reverted_to in {revid} by {user}".format(**reverted_to.reverting))

reverting, reverted, reverted_to = mwreverts.api.check(session, rev_id=423282501, page_id=31445634, radius=20, rvprop={'user','userid'})

print_revert_status(423282501, reverting, reverted, reverted_to)

reverted.reverting


#whether reverted, 1=yes
def revert_status(rev_id, reverted):
    reverting, reverted, reverted_to = mwreverts.api.check(session, rev_id, rvprop={'user'})
    if reverted is not None: 
        return 1
    else: 
        return 0


