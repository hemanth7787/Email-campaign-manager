from datetime import datetime
datetime.utcnow().strftime("%d-%b-%Y")




import zipfile

#Create compressed zip archive and add files
z = zipfile.ZipFile("myzip.zip", "w",zipfile.ZIP_DEFLATED)
z.write("file1.ext")
z.write("file2.ext")
z.printdir()
z.close()

#Append files to compressed archive
z = zipfile.ZipFile("myzip.zip", "a",zipfile.ZIP_DEFLATED)
z.write("file3.ext")
z.printdir()
z.close()

#Extract all files in archive
z = zipfile.ZipFile("myzip.zip", "r",zipfile.ZIP_DEFLATED)
z.extractall("mydir")
z.close()