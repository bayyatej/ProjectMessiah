#--------------------------------------------------------------|
#    T.Bayya          wallpaperMessiah.py           5/12/2016  |
#--------------------------------------------------------------|
#  Saves current desktop wallpaper. (Windows Only)             |                                                
#--------------------------------------------------------------|

import tkFileDialog, os, subprocess, tkMessageBox
from Tkinter import *
from ttk import *
from shutil import *

class wallpaperMessiah(Frame):

    global wallPath     
    global destPath
    global fileName
    global GUID
    global possGUID
    global newFileName
    global currSettings
    global currAC
    global currDC
    
    wallPath = ("C:\Users\ ").replace(" ", "") + os.environ.get( "USERNAME" ) + "\AppData\Roaming\Microsoft\Windows\Themes\CachedFiles";
    destPath = "";
    fileName = (os.listdir(wallPath))[0];
    GUID = subprocess.check_output("powercfg /GETACTIVESCHEME");
    possGUID = ["381b4222-f694-41f0-9685-ff5bb260df2e", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c", "a1841308-3541-4fab-bc81-f71556f20b4a"];
    newFileName = "";
    currSettings = subprocess.check_output("powercfg -q").split("\r\n\r\n");

    #following code used to get current AC/DC wallpaper slideshow settings
    for i in range(len(currSettings)):
        if "309dce9b-bef4-4119-9921-a851fb12f0f4" in currSettings[i]:
            currSettings = currSettings[i];
            break;
    currSettings = currSettings.split("\r\n");
    currAC = currSettings[-2][-1];
    currDC = currSettings[-1][-1];

    def __init__(self, master):
        self.pauseSlideshow();
        Frame.__init__(self, master);
        self.grid();
        self.create_widgets();

    def create_widgets(self):
        self.destLbl = Label(self, text = "1. Choose a destination to save your wallpaper to: ");
        self.destLbl.grid(row = 1, column = 0, sticky = W);

        self.selectDir = Button(self, text = "Choose Destination", command = self.selDir);
        self.selectDir.grid(row = 1, column = 1);

        self.saveLbl = Label(self, text = "2. Click /'Save Wallpaper/' to save your wallpaper to the destination: ");
        self.saveLbl.grid(row = 2, column = 0, sticky = W);
        
        self.save = Button(self, text =  "Save Wallpaper", command = self.saveWall);
        self.save.grid(row = 2, column = 1);

        self.doneLbl = Label(self, text =  "3. Click 'Done' to finish! ");
        self.doneLbl.grid(row = 3, column = 0, sticky = W);

        self.done = Button(self, text = "Done!", command = self.onClose);
        self.done.grid(row = 3, column = 1);

    def selDir(self):
        global wallPath;
        global destPath;
        self.fileOpts = options = {};
        options["parent"] = root;
        options["title"] = "Save Location";
        options["mustexist"] = False;        
        destPath = tkFileDialog.askdirectory(**self.fileOpts);

    def saveWall(self):
        global wallPath;
        global destPath;
        global newFileName;
        newFileName = tkFileDialog.asksaveasfilename(filetypes = [("JPEG" ,".jpg")], initialdir = destPath, parent = root, title = "Save As");
        copy2((wallPath+"\\"+fileName), newFileName+".jpg");
        tkMessageBox.showinfo("Saved!", "Wallpaper saved at: "  + newFileName);

    def onClose(self):
        global newFileName;
        if tkMessageBox.askyesno("Quit?", "Do you want to quit?"):
            self.resetSlideshow();
            root.destroy();

    def pauseSlideshow(self):
        global GUID;
        global possGUID;
        for ID in possGUID:
            if ID in GUID:
                GUID = ID;
                break;
        #Uses GUIDs to pause slideshow
        subprocess.call("powercfg -setacvalueindex " + GUID + " 0d7dbae2-4294-402a-ba8e-26777e8488cd 309dce9b-bef4-4119-9921-a851fb12f0f4 1");
        subprocess.call("powercfg -setdcvalueindex " + GUID + " 0d7dbae2-4294-402a-ba8e-26777e8488cd 309dce9b-bef4-4119-9921-a851fb12f0f4 1");

    def resetSlideshow(self):
        global currAC
        global currDC
        #Restores slideshow settings to settings before program run
        subprocess.call("powercfg -setacvalueindex " + GUID + " 0d7dbae2-4294-402a-ba8e-26777e8488cd 309dce9b-bef4-4119-9921-a851fb12f0f4 " + currAC);
        subprocess.call("powercfg -setdcvalueindex " + GUID + " 0d7dbae2-4294-402a-ba8e-26777e8488cd 309dce9b-bef4-4119-9921-a851fb12f0f4 " + currDC);
        
root = Tk();
root.title("WallpaperMessiah");
root.geometry("485x200");

messiah = wallpaperMessiah(root);
root.mainloop();
