#Find duplicate music track in Itunes playlist and plot various statistics

import plistlib
import re, argparse
import sys
import numpy as np
from matplotlib import pyplot
from unittest import expectedFailure


def findDuplicates(fileName):
    print('Finding duplicate tracks in %s..' % fileName)
    #read in a playlist
    with open(fileName, 'rb') as fp:
        plist = plistlib.loads(fp.read())

    #get the tracks from the Tracks dictionary
    tracks = plist['Tracks']

    #create a track name dictionary
    trackNames = {}

    #iterate through tracks
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            # look for existing entries
            if name in trackNames:
                #if a name and duration match, increment the count
                #round the track length to nearest second
                if duration //1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration,count+1)
            else:
                #add dictionary entry as a tuple (duratrion, count)
                trackNames[name] = (duration,1)
        except:
            #ignore 
            pass

    #EXTRACTING DUPLICATES
    
    #store duplicates as (name, count) tuples
    dups = []
    for k,v in trackNames.items():
        if v[1]  > 1:
            dups.append((v[1],k))
        
    #save duplicare to file 
    if len(dups) > 0 :
        print("Found duplicates will be printed to dups.txt file")
        f = open("dups.txt","w")
        for val in dups:
            f.write("[%d] %s\n" % (val[0],val[1]))
        f.close()
    else: 
        print("No duplicates found") 

#Find Trackd Common Across Multiple Playlist
def findCommonTracks(fileNames):
        #a list of sets of track names
        trackNameSets = []
        for fileName in fileNames:
            #create a new set
            trackNames = set()
            #read in playlist
            with open(fileName, 'rb') as fp:
                plist = plistlib.loads(fp.read())
            #get the tracks
            tracks = plist['Tracks']
            #iterate through tracks
            for trackID, track in tracks.items():
                try:
                    #add the track name to a set
                    trackNames.add(track['Name'])
                except:
                    #ignore
                    pass
            #add to list
            trackNameSets.append(trackNames)
        #get the set of common tracks
        commonTracks = set.intersection(*trackNameSets)
        #write to file
        if len(commonTracks) > 0 :
            f = open("common.txt", 'wb')
            for val in commonTracks:
                s = "%s\n" % val
                f.write(s.encode("UTF-8"))
            f.close()
            print("%d common tracks found. Track names writen to common.txt" % len(commonTracks))

        else:
            print("No common tracks!")

def plotStats(fileName):
        #read in a playlist
        with open(fileName, 'rb') as fp:
            plist = plistlib.loads(fp.read())
        # get tracks from playlist
        tracks = plist['Tracks']
        #create list of song ratings and track duration
        ratings = []
        durations = []
        
        for trackId, track in tracks.items():
            try: 
                ratings.append(track['Album Rating'])
                durations.append(track['Total Time'])
            except: 
                #ignore 
                pass

        if ratings == [] or durations == []:
            print("No valid Album Rating/ Total time data in %s." % fileName)
            return


    #Plottng your data
        #scatter plot 
        x = np.array(durations,np.int32)
        #convert to minutes
        x = x/60000.0
        y = np.array(ratings,np.int32)
        pyplot.subplot(2,1,1)
        pyplot.plot(x,y,'o')
        pyplot.axis([0,1.05*np.max(x), -1,110])
        pyplot.xlabel('Track duration')
        pyplot.ylabel('Track rating')

        #plot histogram
        pyplot.subplot(2,1,2)
        pyplot.hist(x,bins=20)
        pyplot.ylabel('Track duration')
        pyplot.xlabel('Count')

        #show plot
        pyplot.show()


def main():
        #create parser
        descStr= ""
        parser = argparse.ArgumentParser(description=descStr)
        #add a mutually exclusive group of arg
        group = parser.add_mutually_exclusive_group()

        #add expected arguments
        group.add_argument('--common', nargs='*',dest='plFiles', required=False)
        group.add_argument('--stats', dest='plFile', required=False)
        group.add_argument('--dup', dest='plFileD', required=False)

        #parse args
        args = parser.parse_args()

        if args.plFiles:
            #find common tracks
            findCommonTracks(args.plFiles)
        elif args.plFile:
            #plot stats
            plotStats(args.plFile)
        elif args.plFileD:
            #find duplicate tracks
            findDuplicates(args.plFileD)
        else:
            print("These are not the tracks you are looking for")

if __name__ == '__main__':
        main()