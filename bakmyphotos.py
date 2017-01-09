#by cst 20170106
#this script is to backup all the files in a directory ,including the files in subdirectories.
#firstly,you should assign a start directory by modify the variable root, the program will handl all the files automatically.
#secondly, you should tell the program to which you want to bakcup the files by modify the bakDevice.
#thirdly you can also optionally choose some directories which you don't want to scan, e.g.: avoiding waste time on a system directory.
#fourthly, md5List should be read from the device you choose already, if it doesn't exist, as you use this program for the firs time,
#this program is supposed to create a md5list for future use.
#this program can deal with main stream photograph files, by its extension name.
#this program can avoid duplicated files to be bakcuped twice or more.
#Now it only support my 1T mobile disk and linux like system.
import os,sys,time,hashlib

root= '/Users/chenshaoting/Pictures/金山安全/'                            #root is the start directory of the scan , '/Users/chenshaoting/Pictures'
bakDevice='/Volumes/1T'                        #here you should assign a device to store ALL your photos, mine is 1T.
exceptDir=[]                          #exceptDir is the directories which you don't want to scan
#recordList=[]                          #recordList=['/Users/chenshaoting/Pictures/金山安全/营业执照2015.jpg1922690', '/Users/chenshaoting/Pictures/金山安全/营业执照2015－盖章.jpg1137577']
                                    #recordlist is the already backed file list, which should not be backuped again.  compared by filename and file size exactly.
filesFoundThisTime=0
backupFilesTotalSize=0

toBeCopiedMd5List=[]
tempList=[]
md5List=[]


def startup():
    global root
    if findBakDevice():
        loadMd5List()
        handleDirs(root)                        #start to scan .
    else:
        print('Backup Device is not mounted yet, please mount 1T first.')
        endup()
        sys.exit(0)
    return


def loadMd5List():
    global md5List
    if os.path.exists('/Volumes/1T/MYAUTOBAK/md5List.txt'):
        f=open('/Volumes/1T/MYAUTOBAK/md5List.txt','r')
        for line in f.readlines():
            md5List.append(line.strip('\n'))
        f.close()

    else:
        print ('md5List NOT found')
    return

def copyFiles(string):
    global backupFilesTotalSize,tempList,toBeCopiedMd5List
    filename=os.path.split(string)[1]
    filename2='/Volumes/1T/MYAUTOBAK/'+filename
    os.system ("cp %s %s" % (string, filename2))
    if os.path.exists(filename2):

        print (string,'copied')
    else:
        print('DOES NOT COPIED')
        tempList.remove(string)
        toBeCopiedMd5List.remove(md5EnList(string))
        backupFilesTotalSize=backupFilesTotalSize-1
    return




def handleFiles( str):              #if scanned a file ,it will be handled here. but it's olny a controller, actions will be done in another module.
                global filesFoundThisTime
                if '.'== (os.path.split(str)[1])[0]:                        # . hidden files will be omitted.
                    filesFoundThisTime=filesFoundThisTime+1
                    return
                fileExtName=os.path.splitext(str)[1]

                filesFoundThisTime=filesFoundThisTime+1
                if '.arw' in fileExtName or  '.ARW' in fileExtName:
                                backupTo1T(str)
                                                                         #print (str,  "is a Sony raw Photo file!")
                elif '.cr2' in fileExtName or  '.CR2' in fileExtName:
                                backupTo1T(str)
                                                                        #print (str, " is a CANON RAW file!")
                elif '.dng' in fileExtName or  '.DNG' in fileExtName:
                                backupTo1T(str)
                                                                        #print (str, " is an ADOBE RAW file!")
                elif '.nef' in fileExtName or  '.NEF' in fileExtName:
                                backupTo1T(str)
                                                                        #print (str, " is a NIKKON RAW file!")
                elif '.jpg' in fileExtName or  '.JPG' in fileExtName:
                                backupTo1T(str)
                                                                         #print (str, " is a JPEG file!")
                elif '.jpeg' in fileExtName or  '.JPEG' in fileExtName:
                                backupTo1T(str)
                                                                              #print (str, " is a JPEG file!")
                elif '.png' in fileExtName or  '.PNG' in fileExtName:
                                backupTo1T(str)
                                                                               #print (str, " is a PNG file!")
                elif '.tif' in fileExtName or  '.TIF' in fileExtName:
                                backupTo1T(str)
                                                                             #print (str, " is a TIFF file!")
                else:
                                print (str, 'is an unknown file which wont\'t be backup')
                return 

def handleDirs(str):        # this is the main module to scan files.

                try:                                     #to avoid file system error cause break before we go further
                                items=os.listdir(str)    # store all the directories or files found in current directory into the list-- items
                except:
                                tp,val,tb = sys.exc_info()
                                print ('Error Type:',tp)
                                print('Error Value:',val)
                                print ('Trace Back:',tb)
                                return
                 

                
                for i in range (0, len(items)):
                                global exceptDir
                                item=os.path.join(str,items[i])     #make a real path from every item we found in the directory
                                if len(exceptDir)>0 :
                                    for j in range (0,len(exceptDir)):     #if the directory is not you want scan further, it will be skipped and turn to the next.

                                                  if exceptDir[j] in item:

                                                                                # you can add codes to handle exceptions here
                                                      return
                                                
                                if os.path.exists(item) :                       #to avoid an non-existed file or directory
                                                
                                                if os.path.isfile(item) :
                                                                handleFiles(item)       # if it's a file , switch to the action module
                                                elif os.path.isdir(item) :
                                                                handleDirs(item)        # if it's a directory, we will go further in to it and scan it, this is an instance of recursion here.
                                                else :
                                                                print('Neither file or dir!') # oops! we found an Alien, which is neither a file nor a directory, here.
                                else:
                                                print(item, ' does not exist!')          # if it doen'st exist.
                                                
                return

def backupTo1T(string):             #we will actually handle a file here

    global backupFilesTotalSize,md5List,toBeCopiedList,tempList

    if isDup(string):                                  #if it had been backuped already, we won't do anything...
        print('Duplicated --',string)                  #,isDup(string))            #only tell you the fact.
        return

    else:

        if findBakDevice():                 # what you really want to do to the files.


            md5List.append(md5EnList(string))

            tempList.append(string)
            toBeCopiedMd5List.append(md5EnList(string))

            copyFiles(string)
    return

def isDup(string):                          #judge if the file had been backuped already.



    for i in range(0, len(md5List)):
        if md5List[i] == md5EnList(string):                 #compare md5.
            return True
    return False

def md5EnList(filePathString):

    md5=filePathString+str(os.path.getsize(filePathString))  #FAKE MD5
    #md5file=open(filePathString,'rb')
    #md5=hashlib.md5(md5file.read()).hexdigest()
    #md5file.close()
    return md5



def findBakDevice():
    global bakDevice
    if os.path.ismount(bakDevice):
        #print ('1T is mounted already')
        return True
    #print('1T NOT mounted.')
    return False





def endup():
    global  backupFilesTotalSize,backupFilesTotalSize,toBeCopiedMd5List
    f=open('/Volumes/1T/MYAUTOBAK/recordList.txt','a')
    for i in tempList:
        if os.path.exists(i) :
            copyFiles(i)
        else:
            tempList.remove(i)
            print(string,' does not exist.')


    for l in tempList:
        f.writelines(l+'\n')
    now=str(time.localtime())
    f.writelines('------updated in %s\n'%now)
    f.close()

    f=open('/Volumes/1T/MYAUTOBAK/md5List.txt','a')
    for l in toBeCopiedMd5List:
        f.writelines(l+'\n')
    now=str(time.localtime())
    f.writelines('------updated in %s\n'%now)
    f.close()


    print ('%d files  has been found this time' %filesFoundThisTime)            #congratulations, it's done here.
    print ('%d bytes backkuped this time---------All Done! ' %backupFilesTotalSize)
    print (toBeCopiedMd5List,tempList)



startup()
endup()

#some comments here.
