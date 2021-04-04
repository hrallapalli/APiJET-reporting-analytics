# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
from shutil import copy2, move
import subprocess

VERSION = '0.1.0'


#Make sure when you run the script, it will run on file from the top down, it is a good idea 
#to have a spreadsheet of what run number corresponding to what flight number -- each DAT file has 
#a lot of numbers so make sure that the number you choose is unique for each DAT file 

#for every file, a new folder will be created for each .dat file l
#the way to track what that run corresponding to will be checking a spreadsheet contain the 
#name of the run and the flight it represents 

   
def GetNextOutputPrefix(OutputPrefix, Directory):
    """ Seaches for existing directories with base prefix and returns base + incremented int """
    OutputPrefixNumber = 0
    while os.path.exists(os.path.join(Directory, OutputPrefix + str(OutputPrefixNumber))):
        OutputPrefixNumber += 1
    return OutputPrefix + str(OutputPrefixNumber)


def GetFilenamesWithPrefix(Prefix, Directory):
    """ Returns list of filenames that have prefix in given directory """
    Filenames = []
    for EntryName in os.listdir(Directory):
        IsFile = os.path.isfile(os.path.join(Directory, EntryName))
        if EntryName.startswith(Prefix) and IsFile:
            Filenames.append(EntryName)
    if len(Filenames) == 0:
        print(
            f"No files with prefix \"{Prefix}\" in directory \"{Directory}\".")
    return(Filenames)


def MakeDirectory(NewDirectoryName, ExistingDirectory):
    """ Attempts to create new directory and returns path to directory on success."""
    NewDirectory = os.path.join(ExistingDirectory, NewDirectoryName)
    try:
        os.mkdir(NewDirectory)
    except OSError as error:
        print(error)
        raise
    if os.path.exists(NewDirectory):
        print(f"Created directory \"{NewDirectory}\".")
    return(NewDirectory)


def MoveFilesWithPrefix(Prefix, CurrentDirectory, TargetDirectory):
    """ Searches for filenames with prefix in current directory and moves to target directory"""
    
    # TODO: try/except move -- validate that target directory exists?
    
    Filenames = GetFilenamesWithPrefix(Prefix, CurrentDirectory)
    for Filename in Filenames:
        move(os.path.join(CurrentDirectory, Filename), TargetDirectory)


def main():
    """ This function runs when file is executed as a script. """
    WorkingDirectory = os.getcwd()
    ExecutablePath = os.path.join(WorkingDirectory, "data_translator.exe")
    file_names = os.listdir(WorkingDirectory)
    
    
    ConfigDirectory = WorkingDirectory
    ConfigFileName = "config.cfg"
    BaseOutputPrefix = "Flight_Run_"

    # get next output prefix
   
    
#looping through the directory to find all files with ending ".dat" and run data_translator.exe on them 

   
    for filenames in file_names:
        if filenames.endswith('.dat'):
            InputPath = os.path.join(WorkingDirectory, filenames)
             # run script with incremented output prefix
             
             
            OutputPrefix = GetNextOutputPrefix(
                      BaseOutputPrefix,
                      WorkingDirectory)
            
            print(f"Running script with prefix \"{OutputPrefix}\".")
            DataTranslatorOutput = subprocess.check_output(
                ExecutablePath
                + " " + InputPath
                + " -c " + ConfigDirectory
                + " -cf " + ConfigFileName
                + " -o " + OutputPrefix + "_",
                shell=True
            )
            print(DataTranslatorOutput.decode("ascii"))
            
            # move all files into their own directory
            OutputDirectory = MakeDirectory(
                NewDirectoryName=OutputPrefix,
                ExistingDirectory=WorkingDirectory
            )
            
            MoveFilesWithPrefix(OutputPrefix, WorkingDirectory, OutputDirectory)
            
            # copy config, input into new directory
            copy2(os.path.join(ConfigDirectory, ConfigFileName), OutputDirectory)
            copy2(InputPath, OutputDirectory)

# Start of execution if run as script
if __name__ == "__main__":
#    execute only if run as a script
    main()

# End of file

    
