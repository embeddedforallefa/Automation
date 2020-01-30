import os
import sys
import stat
import shutil
import glob

os.chdir('..')
CURRENT_DIR_PATH = os.getcwd()
print CURRENT_DIR_PATH

print "Cleaning sandbox ..."

if os.path.isdir('.\obj'):
    for root, dirs, files in os.walk('.\obj'):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0xFFF)
        for f in files:
            os.chmod(os.path.join(root, f), 0xFFF)
        
if os.path.isdir('.\src'):
    for root, dirs, files in os.walk('.\src'):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0xFFF)
        for f in files:
            os.chmod(os.path.join(root, f), 0xFFF)

			
os.chdir('..')

print "Removing directories ..."

os.chdir(CURRENT_DIR_PATH)

if os.path.isdir('.\obj'):
    shutil.rmtree('.\obj', False, None)

if os.path.isdir('.\src'):
    shutil.rmtree('.\src', False, None)


print "Sandbox cleaned !"

os.chdir('./source')
print (os.getcwd())

# Checking Current file to find the currnet working variant
try:
    os.chmod("Current", 0xFFF)
    f = open("Current","r") #opens Current file name"
except IOError as e:
    print ("Current file not found! Please cresync from IMS for default varient")
    exit()
    
Current_Varient = f.readline()
f.close()
print(Current_Varient)

if (Current_Varient == '2M'):
    print ("This is 2M variant")
    CURRENT_DERIVATE='2M'
elif (Current_Varient == '6M'):
    print ("This is 6M variant")
    CURRENT_DERIVATE='6M'
elif (Current_Varient == '10M'):
    print ("This is 10M variant")
    CURRENT_DERIVATE='10M'
elif (Current_Varient == 'notest'):
    print ("This is notest variant")
    CURRENT_DERIVATE='notest'
else:
    print ("This is 4M variant")
    CURRENT_DERIVATE='4M'


TARGET_DERIVATE=sys.argv[1]  # Takes target variant from cmd line argv

print "Transitioning from "+CURRENT_DERIVATE+" to "+TARGET_DERIVATE+"..."

os.chdir('..')
os.chdir('..')


if CURRENT_DERIVATE != TARGET_DERIVATE:
    print "Saving "+CURRENT_DERIVATE+" files"
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            try:
                if (file.endswith(str('.'+CURRENT_DERIVATE))):
                    os.chmod(os.path.join(root, file), 0xFFF)
                    os.chmod(os.path.join(root, file.replace(("."+CURRENT_DERIVATE),'')), 0xFFF)
                    shutil.copy(os.path.join(root, file.replace(("."+CURRENT_DERIVATE),'')), os.path.join(root, file.replace(CURRENT_DERIVATE,'')+CURRENT_DERIVATE))
                    print "Saved "+CURRENT_DERIVATE+" file "+file.replace("."+CURRENT_DERIVATE,'')+" as "+file.replace(CURRENT_DERIVATE,'')+CURRENT_DERIVATE
                elif ((CURRENT_DERIVATE == '4M') and (file.endswith(str('.'+TARGET_DERIVATE)))):
                    os.chmod(os.path.join(root, file), 0xFFF)
                    os.chmod(os.path.join(root, file.replace(("."+TARGET_DERIVATE),'')), 0xFFF)
                    shutil.copy(os.path.join(root, file.replace(("."+TARGET_DERIVATE),'')), os.path.join(root, file.replace(TARGET_DERIVATE,'')+CURRENT_DERIVATE))
                    print "Saving "+CURRENT_DERIVATE+" file "+file.replace(("."+TARGET_DERIVATE),'')+" as: "+file.replace(TARGET_DERIVATE,'')+CURRENT_DERIVATE
            except WindowsError as e:
                pass

    for root, dirs, files in os.walk(os.getcwd()):
      for file in files:
                try:
                        if (file.endswith(str('.4M'))):
                                os.chmod(os.path.join(root, file), 0xFFF)
                                os.chmod(os.path.join(root, file.replace(".4M",'')), 0xFFF)
                                print "Restoring 4M default file "+file
                                shutil.copy(os.path.join(root, file), os.path.join(root, file.replace(".4M",'')))     
                except OSError as e:
                        pass

          
    for root, dirs, files in os.walk(os.getcwd()):
      for file in files:
        if (file.endswith(str('.'+TARGET_DERIVATE))):
            try:
                os.chmod(os.path.join(root, file), 0xFFF)
                os.chmod(os.path.join(root, file.replace(("."+TARGET_DERIVATE),'')), 0xFFF)
                print "Setting "+TARGET_DERIVATE+" file:"+file+" to working file "+file.replace(("."+TARGET_DERIVATE),'')
                shutil.copy(os.path.join(root, file), os.path.join(root, file.replace(("."+TARGET_DERIVATE),'')))
            except WindowsError as e:
                pass

    
    os.chdir(CURRENT_DIR_PATH)
    os.chdir('.\source')
    Ideas_update_cmd = "call .\..\etools\TsStarter.cmd update"
    os.system(Ideas_update_cmd)  #on windows to update Ideas
    Cessar_CT_update_cmd = "call .\..\etools\TsStarter.cmd CessarUpdater -pdr"  
    os.system(Cessar_CT_update_cmd)  #on windows to update Cessar CT
	
    f = open("Current","w+")
    f.write(TARGET_DERIVATE)
    f.close()
    print "\nTransition "+TARGET_DERIVATE+" done !"
	
    
else:
    print "Already on "+CURRENT_DERIVATE+", nothing for transition !"
