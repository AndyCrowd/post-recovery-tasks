#
# NOT FINISHED YET
#

#!/bin/python3

import magic
from PIL import Image
import glob, os
import sys
import shutil
import hashlib
import time
from stat import * 
from collections import defaultdict
#import argparse
import sys

#######
#
# CMD line check
# 

# -h - show help
# -fl <file name> - file list to check
## --stdout - out data to stdout
## --fc <file to create>  - save data in a file
# -p - path to scan
# -t - show time when scan started and ended
###
# Output Options
###
# -S - separator, default '|' e.g. -S'|'
# -A - show even duplicate file names
#
# --out='md5,sizeB' 
# mime - show mime type
# md5 - show md5 sum
# size - file size
# resltn - show resolution
# fname - file name with path to it
# dupes - amount of duplicate resolutions
# clones - amount of duplicate files 
#
# -D - description infront, e.g.  Clone: | md5: |
#
# default output example:
# |Path:|./Afname.thumbnail|DupeRes:| 9|Clones:| 11|Size:| 12.3 KB |
###

#parser = argparse.ArgumentParser(description='XXXXXXXX')
#parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                   help='an integer for the accumulator')

#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                   const=sum, default=max,
#                   help='sum the integers (default: find the max)')

#args = parser.parse_args()
ARGS_LEN=len(sys.argv) 
ARGS_CMD = sys.argv
#print(ARGS_CMD[1])
s_HELP=False
s_PATH='./'
s_SEP='|'
s_DESC=False
s_ALLf=False
s_MIME=False
s_OUT=[ ]
s_OUT_line=[ ]

s_OUT_dup=False
s_ALLf_dup=False
out_dup=defaultdict(lambda: 0)

#T=" "
#print(ARGS_CMD[1].rfind("--"))
#quit()

for i in range(ARGS_LEN):
 if ARGS_CMD[i] == '-h':
  s_HELP=True
  break
 if ARGS_CMD[i] == '-p': 
  if ARGS_LEN > i+1:
   if os.path.exists(ARGS_CMD[i+1]):
    if os.path.isdir(ARGS_CMD[i+1]):
     s_PATH=ARGS_CMD[i+1] 
     i+=i
     print('XXXXXXXXXXXXX') 
    else:
     print('Is not a path to folder! ERROR, dosnt showing this message')       
    quit()
  else:
   print('Error: "-p" - path it empty')
   quit()
 if ARGS_LEN > i+1:
  if ARGS_CMD[i] == '-S': 
   s_SEP=ARGS_CMD[i+1]
   i+=i
   print(s_SEP) 
 if ARGS_LEN >= i+1:
  if ARGS_CMD[i] == '-D':
   s_DESC=True 
 if ARGS_LEN >= i+1: 
  if ARGS_CMD[i] == '-A':
   s_ALLf=True
   if s_ALLf_dup == True:
    print('Error: Multiple -A=')
    quit()   
   else:
    s_ALLf_dup=True
 if ARGS_LEN >= i+1:
  if ARGS_CMD[i].rfind("--out=") == 0 :
   if s_OUT_dup == True:
    print('Error: Multiple --out=')
    quit()
   s_OUT_dup = True
   s_OUT_line=ARGS_CMD[i].split("--out=")
   s_OUT=s_OUT_line[1].split(",")
   s_OUT_len=len(s_OUT)
   s_OUT_ok=False
   ZZZ=0
   for i_out in range(s_OUT_len):    
    print('s_OUT: ', s_OUT[i_out],s_OUT_len)
    if s_OUT[i_out] == 'md5' :
     s_OUT_ok = True
     ZZZ=int(out_dup[i_out])
     out_dup[i_out]=ZZZ+1
    elif s_OUT[i_out] == 'hash' :
     s_OUT_ok = True
     out_dup[i_out]+=1
    elif s_OUT[i_out]== 'dupes' :
     s_OUT_ok = True
     out_dup[i_out]+=1
    elif s_OUT[i_out] == 'clones' :
     s_OUT_ok = True
     out_dup[i_out]+=1
    elif s_OUT[i_out] == 'path' :
     s_OUT_ok = True
     out_dup[i_out]+=1
    elif s_OUT[i_out] == 'mime' :
     s_OUT_ok = True
     out_dup[i_out]+=1
    elif s_OUT[i_out] == 'size' :
     s_OUT_ok = True
     out_dup[i_out]+=1
    elif s_OUT[i_out] == 'res' :
     s_OUT_ok = True
     out_dup[i_out]+=1
    else:
     print('Bad parameter in --out=',s_OUT[i_out])
     quit()    
   for i_out in range(s_OUT_len):
    print(s_OUT_len,' ',out_dup[i_out],' :: ',i_out)
#    if out_dup[i_out] > 1:
#    print('Duplicates found in --out=')
#    print('AAA: ',out_dup[i_out] )
#    quit()
         
if ARGS_LEN == 1 or s_HELP == True:
 print('-h - show help \n\
-fl <file name> - file list to check \n\
--stdout - out data to stdout \n\
-p - path to scan \n\
-t - show time when scan started and ended \n\
\n\
Output_options - something \n\
-S - separator, default "|" e.g. -S"|" \n\
-A - show even duplicate file names \n\
--out="md5,sizeB" \n\
md5 - show md5 sum \n\
size - file size \n\
resltn - show resolution \n\
fname - file name with path to it \n\
dupes - amount of duplicate resolutions \n\
clones - amount of duplicate files \n\
mime - mime type \n\
-D - description infront, e.g.  Clone: | md5: | \n\n\
default output example: \n\
|Path:|./Afname.thumbnail|DupeRes:| 9|Clones:| 11|Size:| 12.3 KB | ')
 quit()

#print(args.accumulate(args.integers))
quit()
#
#
######
#UserInfoEnabled = "False"
try:
 import pwd
except ImportError:
 UserInfoEnabled = "False"
 print("Failed to import 'pwd'")
 exit()
else:
 UserInfoEnabled = "True"
 

##########
#from optparse import OptionParser
#parser = OptionParser()
#(options, args) = parser.parse_args()
#PathToFile = "".join(args)
##########

## ARRAYS !!!!


ArrayOfFiles = []
ArrayOfRes = []
ArrayOfFSubTypes = []
FileHashArray = []
count_FileHash_dupes={}
Width = {}
Height = {}
DupeRes = defaultdict(lambda: 0)
SkipClone = {}

####
## Start Variables !!!!
####

sys.stdout.write('.')
CountAll = 0
TMPstr=""

###
## ModifAble variables !!!!
###

HashType = "md5"
MchkEnable = "True"
YouNeedFileSize = "True"
OrderYouNeed = ["Path","DupeRes","Clones","Size"]
ShowClones = "True"

#############

def size4human(this_size):
    for SizeForMe in ['bytes','KB','MB','GB','TB']:
        if this_size < 1024.0:
            return "%3.1f %s" % (this_size, SizeForMe)
        this_size /= 1024.0

##########
#
# The FileHashsum function
#
##########


def GetFileHashofAfile(MDTR,var):
 FN = MDTR
 if MchkEnable == "True":
  FN = ArrayOfFiles[var]
  FileName = open(FN,'rb')
  FileData = FileName.read()
  FileName.close()
  if HashType == "md5":
   FileHash = hashlib.md5()
  elif HashType == "sha1":
   FileHash = hashlib.sha1()
  elif HashType == "sha224":
   FileHash = hashlib.sha224()
  elif HashType == "sha256":
   FileHash = hashlib.sha256()
  elif HashType == "sha384":
   FileHash = hashlib.sha384()
  elif HashType == "sha512":
   FileHash = hashlib.sha512()
  else:
   print("Error in HashType")
   exit()
  FileHash.update(FileData)
  FileHashsum = FileHash.hexdigest()
#  FileHashArray.append(FileHashsum) 
#  MDA = FileHashArray[var]
#  cFileHashdupes=count_FileHash_dupes.get(MDA, 0)
#  count_FileHash_dupes[MDA]=cFileHashdupes+1
  var=var+1
  return FileHashsum
 else:
  return "Skipped"

  
###########
# Going through folders
###########
rootdir = "."
for root, subFolders, files in os.walk(rootdir):
 for FLS in files: 
   PathToFile = "{0}/{1}".format(root,FLS)
     #for PathToFile in glob.glob("*"):
   mimeTypeIs = magic.open(magic.MAGIC_MIME_TYPE)
   mimeE = magic.open(magic.MAGIC_MIME_ENCODING)
   mimeTypeIs.load()
   mimeE.load()
   mtype = mimeTypeIs.file(PathToFile)
   mimeEnc = mimeE.file(PathToFile)
   FType = mtype.split('/')[0]
   FSubTypes = mtype.split('/')[1]
   if "image" in FType:
       file, ext = os.path.splitext(PathToFile)
       IfImage = Image.open(PathToFile)
       G = str(IfImage.size).replace(')',"").replace('(','').replace(' ','')
       IfImage.close()
       s = G
       W = s.split(',')[0]
       H = s.split(',')[1]
       try:
         myimg = Image.open(PathToFile,"r")
       except IOError:
         print("Cannot open the «",PathToFile,"» file!")
       else:
        try:
          TestLoadImgData = list(myimg.getdata())
        except IOError:
          print("An error was found in a «",PathToFile,"» file!")
          myimg.close()
        else:
          myimg.close()
          ArrayOfFiles.append(PathToFile)
          Mfilename = GetFileHashofAfile(PathToFile,CountAll)
          FileHashArray.append(Mfilename)
          if Mfilename == "Skipped":
           count_FileHash_dupes[CountAll] = ""
           FileHashArray[CountAll] = "0"
          else:
           MDA = FileHashArray[CountAll]
           cF = count_FileHash_dupes.get(MDA, 0)
           count_FileHash_dupes[MDA] = cF + 1
################################################################
          if count_FileHash_dupes[MDA] > 1:
           SkipClone[CountAll] = 1
          else:
           SkipClone[CountAll] = 0         
          if ShowClones == "True":
           SkipClone[CountAll] = 0
          ArrayOfFiles.append(PathToFile)
          ResAll = "{0}x{1}".format(W,H)
          Width[CountAll] = W
          Height[CountAll] = H
          DupeRes[W,H] += 1
#          Mfilename = GetFileHashofAfile(PathToFile,CountAll)
          FileHashArray.append(Mfilename)
          ArrayOfRes.append(ResAll)
          ArrayOfFSubTypes.append(FSubTypes)
#          if Mfilename == "Skipped":
#           count_FileHash_dupes[CountAll] = ""
#           FileHashArray[CountAll] = "0"        
#          else:
#            MDA = FileHashArray[CountAll]             
#            cF = count_FileHash_dupes.get(MDA, 0) 
#            count_FileHash_dupes[MDA] = cF + 1            
#          ArrayOfFiles.append(PathToFile)
          CountAll = CountAll + 1
#####
I = 0
#OrderYouNeed = ["P","R","H","D","S","U","I"]
#OrderYouNeed = ["Path","Res","Hash","Clones","Size","UserPerm","DupeRes"]
while I < CountAll:
 WforDup = Width[I]
 HforDup = Height[I]
 for ToShowInOrder in OrderYouNeed:
   if ToShowInOrder == "Path":
#    print("|Path:| ", ArrayOfFiles[I],"",end="")
    TMPstr+="|Path:|"+ArrayOfFiles[I]
   elif ToShowInOrder == "Res":
#    print("|Res:| ", ArrayOfRes[I],"",end="")
    TMPstr+="|Res:|"+ArrayOfRes[I]
   elif  ToShowInOrder == "Hash":
#    print("|Hash:| ", FileHashArray[I],"",end="")
    TMPstr+="|Hash:| "+FileHashArray[I]
   elif  ToShowInOrder == "Clones":
    GetHFA =  FileHashArray[I]
#    print("|Dupes:| ", count_FileHash_dupes[GetHFA],"",end="")
#     print(count_FileHash_dupes[GetHFA])
    TMPstr+="|Clones:| "+str(count_FileHash_dupes[GetHFA])
   elif ToShowInOrder == "Size":
    FSize4Print = os.path.getsize(ArrayOfFiles[I])
#    print("|Size:| ", size4human(FSize4Print),"",end="")
    TMPstr+="|Size:| "+size4human(FSize4Print)
   elif ToShowInOrder == "UserPerm":
    st = os.stat(ArrayOfFiles[I])
#    print("|",pwd.getpwuid(st[ST_UID]),end="")
    TMPstr+="|",pwd.getpwuid(st[ST_UID])
   elif ToShowInOrder == "DupeRes":
#    print("|DupeRes:| ",DupeRes[WforDup,HforDup],end="")
     TMPstr+="|DupeRes:| "+str(DupeRes[WforDup,HforDup])
   else:
    print("ERROR in Order type")
    exit()
 if SkipClone[I] ==  0 :
  print(TMPstr,"|")
 TMPstr=""
# print("|")
 I = I + 1

#################### WHILE MOVE ####################
