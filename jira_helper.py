#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, getopt
from jira import JIRA

########################## CONFIGURATION ##########################

SERVER =        '' # https://jira.ru
CURRENT_USER =  ''
TARGET_USER =   ''
PASSWORD =      ''

##################### DON'T CHANGE CODE BELOW #####################

def getVersionAndBuild(raw_args):
    version = ''
    build = ''

    try:
        opts, args = getopt.getopt(raw_args,"v:b:",["version=","build="])
    except getopt.GetoptError:
        print 'jira_script.py -v <version> -b <build>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'jira_script.py -v <version> -b <build>'
            sys.exit()
        elif opt in ("-v", "--version"):
            version = arg
        elif opt in ("-b", "--build"):
            build = arg

    if not version or not build:
        raise Exception('You need to run script with version (-v) and build (-b)')

    print 'DEBUG -> version: {0}, build: {1}'.format(version, build)

    return (version, build)


def moveTasksToTest(version, build):
    fixedInBuild = 'build: {0}'.format(build)

    options = { 'server': SERVER }
    jira = JIRA(options, basic_auth=(CURRENT_USER, PASSWORD)) # a username/password tuple
    print(jira)

    assignee = 'assignee={0}'.format(CURRENT_USER) #на ком таска
    issues = jira.search_issues(assignee)

    for issue in issues:
        if issue.fields.status.name in(u'READY TO MERGE'):
            print(issue.key.encode("utf-8"), issue.fields.summary.encode("utf-8"), issue.fields.status.encode("utf-8"))
            fixedInMsg = 'fixed in ' + version + ' ' + fixedInBuild
            comment = jira.add_comment(issue.key, fixedInMsg)
            jira.transition_issue(issue, transition='Ready for test')
            jira.assign_issue(issue, TARGET_USER)


version, build = getVersionAndBuild(sys.argv[1:])
moveTasksToTest(version, build)
