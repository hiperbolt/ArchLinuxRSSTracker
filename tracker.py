# hiperbolt 2019 (tomasimoes03@gmail.)
# script to check for an rss update to arch linux's rss feed, used to integrate with tint2
# shouldn't be too hard to adapt for another use, feedparser is a funny api

#################################################################################################################

import feedparser
import sys
import datetime
import os

#RSSFeedLinks
NewsFeed = feedparser.parse('https://www.archlinux.org/feeds/news/')
NewsFeedHuman = ('https://www.archlinux.org/news/')

nmrpubs = len(NewsFeed.entries)
dates = []
datesdict = {}
candidatesdict = {}
args = sys.argv

if args[1] == "help" or args[1] == "--help":
    print(" archrssparser [query] [track / specify] \n archrssparser [ignore]")

elif args[1] == "query":
    for i in range(0, nmrpubs):
        for i in NewsFeed.entries[i].published_parsed:
            dates.append(i)

    for i in range(0, nmrpubs):
        datesdict["entry{0}".format(i)] = dates[:9]
        del dates[:9]

    for i in range(0, nmrpubs):
        if datesdict["entry{0}".format(i)][0] == 2018:#int(datetime.datetime.now().year):
            if datesdict["entry{0}".format(i)][1] == int(datetime.datetime.now().month) or datesdict["entry{0}".format(i)][1] == int(datetime.datetime.now().month)-1:
                candidatesdict["entry{0}".format(i)] = datesdict["entry{0}".format(i)]

    try:
        #f = open('~/.config/archrssparser/archrssparserrc')
        with open(os.path.expanduser("~/.config/archrssparser/archrssparserrc"), "r") as f:
            for entry in candidatesdict:
                if str(candidatesdict["{0}".format(entry)]) not in f.read():
                    if args[2] == "specify":
                        print("Incoming RSS Broadcast: ", NewsFeed.entries[int(entry[-1:])].title, " \n NewsFeed: %s" % NewsFeedHuman)
                    if args[2] == "track":
                        print("WARNING!")
                        break
                    else:
                        print("Wrong arguments!")
    except IOError:
        os.system("mkdir ~/.config/archrssparser")
        os.system("touch ~/.config/archrssparser/archrssparserrc")

elif args[1] == "ignore":
    print("Choose a broadcast to ignore warnings on: ")
    for i in range(0, nmrpubs):
        for date in NewsFeed.entries[i].published_parsed:
            dates.append(date)

    for i in range(0, nmrpubs):
        datesdict["entry{0}".format(i)] = dates[:9]
        del dates[:9]

    for i in range(0, nmrpubs):
        if datesdict["entry{0}".format(i)][0] == 2018:#int(datetime.datetime.now().year):
            if datesdict["entry{0}".format(i)][1] == int(datetime.datetime.now().month) or datesdict["entry{0}".format(i)][1] == int(datetime.datetime.now().month)-1:
                candidatesdict["entry{0}".format(i)] = datesdict["entry{0}".format(i)]

    with open(os.path.expanduser("~/.config/archrssparser/archrssparserrc"), "r") as f:
        for entry in candidatesdict:
            if str(candidatesdict["{0}".format(entry)]) not in f.read():
                print("(", entry[-1:], ") ", NewsFeed.entries[int(entry[-1:])].title)
            else:
                print("Nothing to ignore.")
                exit()

        userint = input(": ")

        for entry in candidatesdict:
            try:
                if int(userint) == int(entry[-1:]):
                    f.close()
                    with open(os.path.expanduser("~/.config/archrssparser/archrssparserrc"), "a") as f:
                        f.write(str(candidatesdict["{0}".format("entry" + userint)]))
                        f.close()
                else:
                    print("Please insert a valid broadcast as option.")
            except:
                print("Please insert a valid broadcast as option.")

else:
    print("Wrong arguments!")
