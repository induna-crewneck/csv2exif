"""
CSV2EXIF    v1.5    (2023-09-21)
https://github.com/induna-crewneck/csv2exif
Requirements:
    python3     v3+         https://www.python.org/downloads/
    pip         v19.3+      https://pip.pypa.io/en/stable/installation/
    pandas      v.2.1.0+    https://pandas.pydata.org/docs/getting_started/install.html

Current Errors:
    "Malformed UTF-8" for example in Comment of imgID33 (internal note)     Severity: low

To Do:
    -
"""
import os
from os import walk
import re
import pandas as pd
import sys
from sys import platform
import subprocess

DEBUG = 1 # Default=0, Some Info=1, Extensive Info for debugging=2


print("###################################################################github.com/induna-crewneck\n################################ EXIF Metadata from CSV Tool ################################\n#############################################################################################\n")

#Checking if exiftool is installed and callable directly
try:
    exifinstalled = subprocess.check_output("exiftool");
    if DEBUG >= 1: print("exiftool installed and callable")
    exiftoolpath = "exiftool"
    exifinstalled = True
except Exception as e:
    testmsg = str(e)
    exifinstalled = False
    if "Errno 2" in str(e) or "WinError 2" in str(e):
        if DEBUG >= 1: print("exiftool not installed or callable [Error 2]")
    elif DEBUG >= 1: print("exiftool Error:",e)
#Trying to locate exiftool in working directory
if exifinstalled == False:
    scriptpath = os.path.join(os.path.dirname(__file__).strip().replace("\\","/"))
    for root, dirs, files in os.walk(scriptpath):
        for file1 in files:
            if re.match('(.*)(^|\/)exiftool($|.exe$)', file1):    # Finds "exiftool.exe" (Windows) and "exiftool" (mac) in directory and subdirectory of script location
                exiftoolpath = os.path.join(root, file1).strip().replace("\\","/")
                if DEBUG >= 1: print("    found "+exiftoolpath+"\n")
            else:

                try: exiftoolpath
                except: exiftoolpath = ""
    if os.path.isfile(exiftoolpath): exiftoolpath = exiftoolpath
    else:

        print(exiftoolpath)
        print("exiftool not found in current directory or subdirectories.")
        exiftoolpath = input("Please specify exiftool path:    ").strip().replace("\\","/")
        if os.path.isfile(exiftoolpath) == False:
            print("The specified file could not be found")
            exit()
        try:
            exifdefined = subprocess.check_output(exiftoolpath);
            exifinstalled = True
        except Exception as e:
            print("exiftool Error: ",e)
            exit()

configpath = os.path.join(os.path.dirname(__file__).replace("\\","/")+"/csv2exif.exiftoolconfig")
photopath = input("Photo folder:"+" "*(15-13)).strip()
if re.match ("(.*)\\$",photopath): photopath = re.sub("\\$",photopath)
csvpath = input("CSV path:"+" "*(15-9)).strip()
if os.path.isfile(configpath): configpath = configpath
else:
    print("csv2exif.exiftoolconfig not found in current directory. Please ensure this script, exiftool.exe and csv2exif.exiftoolconfig are in the same directory.")
    configpath = input("Alternatively drag&drop csv2exif.exiftoolconfig here now ").strip()
    if os.path.isfile(configpath) == False: exit()

keeporiginalq = input("Do you wish to create backups of the files? (Y/N):    ").strip()
if keeporiginalq == "Y" or keeporiginalq == "y":    keeporiginal = True
else: keeporiginal = False

photopath = photopath.replace("\\","/")
csvpath = csvpath.replace("\\","/")
exiftoolpath = exiftoolpath.replace("\\","/")
configpath = configpath.replace("\\","/")
w = walk(photopath)
variables = {}
linelength = 30

ImgFormatList = ["jpg","jpeg","jpeg2000","jpejif","jfif","jfi","png","gif","webp","tiff","raw","bmp","indd"]
EXIFtags =  ["Make","Model","Lens","ISO","Flash","Orientation","UserComment","Copyright"]
XMPtags = ["Event","PersonInImage","Subject","LocationShownCountryName","LocationShownProvinceState","LocationShownCity","LocationShownSublocation"]
FlashValues = ["0","1","5","7","8","9","d","f","10","14","18","19","1d","1f","20","30","41","45","47","49","4d","4f","50","58","59","5d","5f"]
FlashWordList = ["No Flash", "Fired", "Fired, Return not detected", "Fired, Return detected", "On, Did not fire", "On, Fired", "On, Return not detected", "On, Return detected", "Off, Did not fire", "Off, Did not fire, Return not detected", "Auto, Did not fire", "Auto, Fired", "Auto, Fired, Return not detected", "Auto, Fired, Return detected", "No flash function", "Off, No flash function", "Fired, Red-eye reduction", "Fired, Red-eye reduction, Return not detected", "Fired, Red-eye reduction, Return detected", "On, Red-eye reduction", "On, Red-eye reduction, Return not detected", "On, Red-eye reduction, Return detected", "Off, Red-eye reduction", "Auto, Did not fire, Red-eye reduction", "Auto, Fired, Red-eye reduction", "Auto, Fired, Red-eye reduction, Return not detected", "Auto, Fired, Red-eye reduction, Return detected"]
OrientationValues = ["1","2","3","4","5","6","7","8"]
OrientationWorldList = ["Horizontal (normal)","Mirror horizontal","Rotate 180","Mirror vertical","Mirror horizontal and rotate 270 CW","Rotate 90 CW","Mirror horizontal and rotate 90 CW","Rotate 270 CW"]
lookupdata = [["Flash","0","No Flash"],["Flash","1","Fired"],["Flash","5","Fired, Return not detected"],["Flash","7","Fired, Return detected"],["Flash","8","On, Did not fire"],["Flash","9","On, Fired"],["Flash","d","On, Return not detected"],["Flash","f","On, Return detected"],["Flash","10","Off, Did not fire"],["Flash","14","Off, Did not fire, Return not detected"],["Flash","18","Auto, Did not fire"],["Flash","19","Auto, Fired"],["Flash","1d","Auto, Fired, Return not detected"],["Flash","1f","Auto, Fired, Return detected"],["Flash","20","No flash function"],["Flash","30","Off, No flash function"],["Flash","41","Fired, Red-eye reduction"],["Flash","45","Fired, Red-eye reduction, Return not detected"],["Flash","47","Fired, Red-eye reduction, Return detected"],["Flash","49","On, Red-eye reduction"],["Flash","4d","On, Red-eye reduction, Return not detected"],["Flash","4f","On, Red-eye reduction, Return detected"],["Flash","50","Off, Red-eye reduction"],["Flash","58","Auto, Did not fire, Red-eye reduction"],["Flash","59","Auto, Fired, Red-eye reduction"],["Flash","5d","Auto, Fired, Red-eye reduction, Return not detected"],["Flash","5f","Auto, Fired, Red-eye reduction, Return detected"],["Orientation","1","Horizontal (normal)"],["Orientation","2","Mirror horizontal"],["Orientation","3","Rotate 180"],["Orientation","4","Mirror vertical"],["Orientation","5","Mirror horizontal and rotate 270 CW"],["Orientation","6","Rotate 90 CW"],["Orientation","7","Mirror horizontal and rotate 90 CW"],["Orientation","8","Rotate 270 CW"]]
lookupdf = pd.DataFrame(lookupdata, columns=["Category","In","Out"])
"""
Info on Tags:
https://exiftool.org/TagNames/EXIF.html
https://exiftool.org/TagNames/XMP.html
"""

def removeSpecialChars(inString):
    try: outString = inString.replace("ß","ss").replace("ü","ue").replace("ä","ae").replace("ü","ue").replace("ö","oe").replace("é","e").replace("è","e").replace("á","a").replace("à","a").replace("ó","o").replace("ò","o").replace("æ","ae").replace("ø","o").replace("å","a").replace("\\r\\n",". ").replace("\\n",". ")
    except Exception as e:
        if DEBUG >= 1: print("Error while processing string containing weird symbols",e)
        outString = ""
    return outString

try:
    pd.set_option("display.max_colwidth", 10000)
    df = pd.read_csv(csvpath, sep = ";", encoding='utf8')        #encoding='utf8'
except Exception as e:
    if "can't decode" in str(e): print("CSV Error. Please make sure the CSV uses ; as separator, the contents are UTF-8 and don't contain special characters")
    else: print("CSV Error")
    if DEBUG >= 1: print("      ",e)
    exit()

#Checking if folder contains only photos:
counter = 0
filelist = []
invalidfiles = []
for (dirname, dirnames, filenames) in w:
    for filename in filenames:
        try:
            extension=filename.replace(re.match("(.*)\.[a-zA-Z0-9]*$",filename).group(1),"").replace(".","")
            if extension not in ImgFormatList: print("Wrong file format: ",filename)
            else: filelist.append(filename)
        except Exception as e:
            invalidfiles.append(filename) #expected, therefore no error output
    photocounter = len(filelist)
    if DEBUG >= 1 and len(invalidfiles)>0: print("\nIgnoring files: "+", ".join(invalidfiles)+"\n")
    if DEBUG >= 1: print(photocounter,"Photos found:\n"+", ".join(filelist)+"\n")
    else: print(photocounter,"Photos found\n")
    photocounter = len(filelist)
    
#Main Processing:
    print("\nProcessing photos ###########################################################################\n")
    counter = 0
    for filename in filelist:
        if DEBUG >= 1: print("File name:"+" "*(linelength-10)+filename) #25 characters
        #Get Photo ID:
        try:
            regextract1 = re.match("[a-zA-Z0-9]*\.[0-9]*.[a-zA-Z]*$",filename).group(0)
            regextract2 = re.match("(.*)\.[a-zA-Z]*$",regextract1).group(1)
            IDstr = re.match("(.*)\.(.*)",regextract2).group(2)
            ID = int(IDstr)
            if DEBUG >= 1: print("Photo ID:"+" "*(linelength-9)+IDstr)
        except Exception as e:
            print("Error during image ID parsing of "+filename+":\n  ",e)
            exit()

        #Find corresponding Row in CSV based on PhotoID:
        data = df[df["ID"] == ID]   #Outputs

        # Matching EXIFtags to CSV Columns:
        exiftoolcommandargs = [exiftoolpath+' -config "'+configpath+'" -exif:ImageNumber='+str(int(ID))]
        if keeporiginal == False: exiftoolcommandargs.append('-overwrite_original')

        # Setting DateTime
        try:
            date = data["Date"].to_string(index=False, header=False)
            time = data["Time"].to_string(index=False, header=False)
            if re.match("\d\d\.\d\d\.\d\d\d\d",date) or re.match("\d\d\/\d\d\/\d\d\d\d",date): date = date[6:10]+date[3:5]+date[0:2]
            elif re.match("\d\d\d\d\-\d\d\-\d\d",date): date = date[0:4]+date[5:7]+date[8:10]
            elif re.match("\d{8}",date): date = date
            else:
                print("Please use one of these date formats:\nYYYYMMDD, DD.MM.YYYY, DD/MM/YYYY")
                continueq = input("Press Enter to coninue")
            DateTimeOriginal = date[0:4]+":"+date[4:6]+":"+date[6:8]+" "+time+":00"
            exiftoolcommandargs.append('-exif:DateTimeOriginal="'+DateTimeOriginal+'" -exif:CreateDate="'+DateTimeOriginal+'" -XMP-microsoft:DateAcquired="'+DateTimeOriginal+'"')
            if DEBUG >= 1: print("DateTime:"+" "*(linelength-9)+DateTimeOriginal)
        except Exception as e:
            print("Error during DateTime processing:\n  ",e)

        # Setting FocalLength:
        if "FocalLength" in data:
            try:
                FocalLength = data["FocalLength"].to_string(index=False, header=False)
                if "mm" in FocalLength: FocalLength = FocalLength.replace("mm","").strip()
                elif "NaN" in FocalLength: FocalLength = ""
                elif FocalLength == "?": FocalLength = ""
                # Check if Variable is set
                try: FocalLength
                except NameError: FocalLength = ""
                if len(FocalLength)>0:
                    exiftoolcommandargs.append('-exif:FocalLength="'+FocalLength+'" -ExifIFD:FocalLengthIn35mmFormat="'+FocalLength+'" -xmp-exif:FocalLength="'+FocalLength+'" -xmp-exif:FocalLengthIn35mmFormat="'+FocalLength+'"')
                    if DEBUG >= 1: print("Focal Length:"+" "*(linelength-13)+FocalLength+" mm")
                elif DEBUG > 1: print("FocalLength not found in CSV")
            except Exception as e:
                if DEBUG >= 1: print("Error during FocalLength processing:\n    ",e)

        # Setting Aperture:
        if "FNumber" in data: FNumber = data["FNumber"].to_string(index=False, header=False)
        elif "Aperture" in data: FNumber = data["Aperture"].to_string(index=False, header=False)
        elif DEBUG >= 1: print("Error during Aperture(FNumber) processing:\n    ",e)
        # Check if Variable is set
        try: FNumber
        except NameError: FNumber = ""
        try:
            if FNumber == "?": FNumber = ""
            elif "NaN" in FNumber and len(FNumber)>0: FNumber = ""
            elif "f/" in FNumber and len(FNumber)>0: FNumber = str(float(FNumber.replace("f/","").strip()))
            if re.match('^(\d|\.)*$',FNumber) and len(FNumber)>0: FNumber = str(float(FNumber))
            if len(FNumber)>0:
                exiftoolcommandargs.append('-exif:FNumber="'+FNumber+'" -ApertureValue="'+FNumber+'" -xmp-exif:FNumber="'+FNumber+'"')
                if DEBUG >= 1: print("Aperture:"+" "*(linelength-9)+"f/"+FNumber)
            elif DEBUG > 1: print("FNumber/Aperture not found in CSV")
        except Exception as e:
            if DEBUG >= 1: print("Error during FNumber processing:\n    ",e)
            if DEBUG >= 1: print("FNumber: ",FNumber)

        # Setting Artist:
        try:
            Artist = data["Artist"].to_string(index=False, header=False)
            #exiftoolcommandargs.append('-exif:Artist="'+Artist+'" -exif:OwnerName="'+Artist+'" -exif:Photographer="'+Artist+'" -xmp-dc:Creator="'+Artist+'"')
            exiftoolcommandargs.append('-exif:Artist="'+Artist+'" -exif:OwnerName="'+Artist+'" -xmp-dc:Creator="'+Artist+'" -IFD0:XPAuthor="'+Artist+'"')
            if DEBUG >= 1: print("Artist:"+" "*(linelength-7)+Artist)
        except Exception as e:
            if DEBUG >= 1: print("Error during Artist processing:\n    ",e)

        # Setting ExposureTime:
        try:
            if "ExposureTime" in data: ExposureTime = data["ExposureTime"].to_string(index=False, header=False)
            elif "ShutterSpeedValue" in data: ExposureTime = data["ShutterSpeedValue"].to_string(index=False, header=False)
            elif "Shutter" in data: ExposureTime = data["Shutter"].to_string(index=False, header=False)
            else: ExposureTime = ""
            # Check if Variable is set
            try: ExposureTime
            except NameError: ExposureTime = ""
            if ExposureTime == "?": ExposureTime = ""
            elif "NaN" in ExposureTime: ExposureTime = ""
            elif "Jan" in ExposureTime:
                # Automatic formatting sometimes formats values like 1/30 to 1-Jan
                try: ExposureTime = "1/"+str(re.search('(\d*)(.*)',ExposureTime,re.IGNORECASE).group(1)).strip()
                except Exception as e:
                    if DEBUG >= 1: print("Error during ExposureTime processing: "+ExposureTime+"\n    ",e)
            if len(ExposureTime)>0:
                ExposureTime = ExposureTime.replace("(ca)","").replace("ca","").strip()
                if re.match('^(\d|\.)*$',ExposureTime):    ExposureTime = str(float(ExposureTime))
                exiftoolcommandargs.append('-exif:ExposureTime="'+ExposureTime+'" -ShutterSpeedValue="'+ExposureTime+'" -IFD0:BaselineExposure="'+ExposureTime+'" -ExifIFD:ExposureTime="'+ExposureTime+'"')
                if DEBUG >= 1: print("Exposure:"+" "*(linelength-9)+ExposureTime," s")
            elif DEBUG > 1: print("ExposureTime not found in CSV")
        except Exception as e:
            ERROR = e
            if DEBUG >= 1: print("Error during ExposureTime processing:\n    ",e)

        # Setting Film Info
        try:
            if "Film" in data:
                Film = data["Film"].to_string(index=False, header=False)
                if len(Film)>0:
                    exiftoolcommandargs.append('-xmp-xmp:film="'+Film+'"')
                    if DEBUG >= 1: print("Film:"+" "*(linelength-5)+Film)
                else:
                    Film =""
                    if DEBUG > 1: print("Film not found in CSV")
                try:
                    FilmMaker = data["FilmMaker"].to_string(index=False, header=False)
                    if len(FilmMaker)>0:
                        exiftoolcommandargs.append('-xmp-xmp:film="'+FilmMaker+'"')
                        if DEBUG >= 1: print("FilmMaker:"+" "*(linelength-10)+FilmMaker)
                    else:
                        FilmMaker =""
                except:
                    if DEBUG >= 1: print("FilmMaker not found in CSV")
                try:
                    FilmType = data["FilmType"].to_string(index=False, header=False)
                    if len(FilmType)>0:
                        exiftoolcommandargs.append('-xmp-xmp:film="'+FilmType+'"')
                        if DEBUG >= 1: print("FilmType:"+" "*(linelength-9)+FilmType)
                    else:
                        FilmType =""
                except:
                    if DEBUG > 1: print("FilmType not found in CSV")
                try:
                    FilmID = data["FilmID"].to_string(index=False, header=False)
                    if len(FilmID)>0:
                        exiftoolcommandargs.append('-xmp-xmp:film="'+FilmID+'"')
                        if DEBUG >= 1: print("FilmID:"+" "*(linelength-7)+FilmID)
                    else:
                        FilmID =""
                except:
                    if DEBUG > 1: print("FilmID not found in CSV")
            elif DEBUG > 1: print("Film Info not found in CSV")
        except Exception as e:
            ERROR = e
            if DEBUG >= 1:
                print("Error during Film Info processing:")
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print("    ",exc_type, os.path.split(exc_tb.tb_frame.f_code.co_filename)[1], exc_tb.tb_lineno)

        # Setting other Tags from lists:
        for exif in EXIFtags:
            #variables[exif] = exif  would make a variable with the exiftag name containing the exiftag
            #to list variables: for exif in EXIFtags: print(variables[exif])
            try:
                variables[exif] = data[exif].to_string(index=False, header=False)
                if "NaN" in variables[exif]:
                    variables[exif] = ""
                    if DEBUG > 1: print(exif,"found in CSV but empty")
                elif exif == "UserComment":
                    Comment = str(variables[exif]).replace("\\r\\n",". ").replace("\\n",". ")
                    CommentConv = removeSpecialChars(Comment)
                    exiftoolcommandargs.append('-exif:UserComment="'+Comment+'" -IFD0:XPComment="'+CommentConv+'"')
                    if DEBUG >= 1: print("Comment:"+" "*(linelength-8)+Comment)
                elif exif == "Make": CamMake = str(variables[exif])
                elif exif == "Model": CamModel = str(variables[exif])
                elif exif == "LensModel" or exif == "Lens":
                    Lens = str(variables[exif])
                    exiftoolcommandargs.append('-xmp:Lens="'+Lens+'" -xmp-aux:Lens="'+Lens+'" -ExifIFD:Lens="'+Lens+'"')
                    try:
                        LensMake = re.search('^(\w*) (.*)',Lens).group(1).strip()
                        LensModel = Lens.replace(LensMake,"").strip()
                        exiftoolcommandargs.append('-xmp-exifex:LensMake="'+LensMake+'" -ExifIFD:LensMake="'+LensMake+'" -xmp-exifex:LensModel="'+LensModel+'" -ExifIFD:LensModel="'+LensModel+'"')
                    except Exception as e:
                        LensModel = ""
                        if DEBUG >= 1: print("Error while processing LensMake and LensModel")
                        if DEBUG > 1: print(e)
                    if len(Lens)>0 and DEBUG >= 1: print("Lens:"+" "*(linelength-5)+Lens)
                else:
                    if exif == "Flash":
                        if str(variables[exif]).replace(".0","") in FlashValues:
                            #Lookup Conditions:
                            FlashListFiltered = lookupdf.loc[(lookupdf["Category"] == "Flash")&(lookupdf["In"] == str(variables[exif]).replace(".0",""))]
                            #Getting Target Value:
                            FlashConv = FlashListFiltered["Out"].to_string(index=False, header=False)
                            variables[exif] = FlashConv
                        elif str(variables[exif]) not in FlashWordList: variables[exif] = ""
                        elif DEBUG >= 1: print("Exception when processing Flash value")
                    if exif == "Orientation":
                        if str(variables[exif]).replace(".0","") in FlashValues:
                            #Lookup Conditions:
                            OrientationListFiltered = lookupdf.loc[(lookupdf["Category"] == "Orientation")&(lookupdf["In"] == str(variables[exif]).replace(".0",""))]
                            #Getting Target Value:
                            OrientationConv = OrientationListFiltered["Out"].to_string(index=False, header=False)
                            variables[exif] = OrientationConv
                        elif str(variables[exif]) not in OrientationWordList: variables[exif] = ""
                        elif DEBUG >= 1: print("Exception when processing Orientation value")
                    exiftoolcommandargs.append('-exif:'+exif+'="'+str(variables[exif])+'"')
                    if DEBUG >= 1:
                        print(exif+":"+" "*(linelength-len(exif)-1)+str(variables[exif]))
            except Exception as e:
                if DEBUG > 1: print(exif+" not found in CSV")
        for xmp in XMPtags:
            try:
                variables[xmp] = data[xmp].to_string(index=False, header=False)
                if "NaN" in variables[xmp]:
                    variables[xmp] = ""
                    if DEBUG > 1: print(xmp,"found in CSV but empty")
                else:
                    if xmp == "Event": exiftoolcommandargs.append('-xmp-iptcExt:Event="'+str(variables[xmp])+'"')
                    elif xmp == "Subject":
                        Subject = str(variables[xmp])
                        Subjectconv = removeSpecialChars(Subject)
                        exiftoolcommandargs.append('-xmp-dc:Subject="'+Subject+'" -IFD0:ImageDescription="'+Subject+'" -IFD0:XPSubject="'+Subjectconv+'"')
                    else: exiftoolcommandargs.append('-xmp:'+xmp+'="'+str(variables[xmp])+'"')
                    if xmp == "LocationShownSublocation": LocationShownSublocation = str(variables[xmp])
                    elif xmp == "LocationShownCity": LocationShownCity = str(variables[xmp])
                    elif xmp == "LocationShownProvinceState": LocationShownProvinceState = str(variables[xmp])
                    elif xmp == "LocationShownCountryName": LocationShownCountryName = str(variables[xmp])
                    if DEBUG >= 1:
                        print(xmp+":"+" "*(linelength-len(xmp)-1)+str(variables[xmp]))
            except Exception as e:
                ERROR = exif+" not found in CSV"
                if DEBUG > 1: print(ERROR,"\n",e)

        #Applying set Variables to additional tags:
        try:
            if len(CamMake)+len(CamModel)>0:
                CameraLabel = CamMake+" "+CamModel
                if DEBUG >= 1: print("CameraLabel:"+" "*(linelength-12)+CameraLabel)
                exiftoolcommandargs.append('-IFD0:CameraLabel="'+CameraLabel+'" -XMP-xmpDM:CameraModel="'+CameraLabel+'" -XMP-getty:CameraMakeModel="'+CameraLabel+'"')
                try: exiftoolcommandargs.append("-XMP-Device:Camera:VendorInfo=\"{Manufacturer='"+CamMake+"',Model='"+CamModel+"'}\"")
                except: error=true #just to do something
            elif DEBUG >1: print("Make and Model could not be found to create CameraLabel")
        except Exception as e:
            if DEBUG >= 1: print("Exception while processing CameraLabel")
            if DEBUG >1: print(e)

        filepath = photopath+"/"+filename
        exiftoolcommandargs.append('-exif:Software="github.com/induna-crewneck/csv2exif" "'+filepath+'"')
        if DEBUG > 1: print("\nArgument list:\n",exiftoolcommandargs,"\n")
        exiftoolcommand = ' '.join(exiftoolcommandargs)
        if DEBUG > 1: print("Commandline:\n"+exiftoolcommand+"\n")
        try:
            if DEBUG > 1:
                f=open(photopath+"/"+filename+"_exiftoolcommand.txt", "w")
                f.write(exiftoolcommand)
                f.close()
            if DEBUG == 0:
                try:print("Processing "+filename+", "+str(counter+1)+"/"+str(photocounter)+" ("+str(round(counter/photocounter*100,2))+"%)")
                except:error=true
            os.system(exiftoolcommand)
            counter = counter+1
        except Exception as e:
            if DEBUG >= 1: print("\nError during exiftool execution:\n",e)
        if DEBUG != 0: print("#############################################################################################\n")
if counter == 1:print("    "+str(counter)+" image file updated\n")
elif counter > 1:print("    "+str(counter)+" image files updated\n")
