# TextTasks

Yet another task management bundle for TextMate. This one is heavily inspired by [Tasks.tmbundle][1] by Henrik Nyh.

## Why don't I just use Tasks? 

In my perpetual search for the perfect editor, the turn has come to TextMate and I wanted to dive under the skin to become fluent with TextMate. What better way to get into the details than writing a bundle of my own. This is my ongoing learning experience.

## Quick start

Help is available from the TextTasks Bundle menu

Open the settings file (Settings… from the TextTasks Bundle menu) and edit to your liking (or use the default settings). If you use Dropbox, consider creating a Lists folder in your Dropbox folder and add that folder to the `PROJECT_DIRS` list. 

## Supporting acts

Install script
: This is run when the settings file (Settings… from the TextTasks Bundle menu) is saved. It will set up the following helpers: 

inbox.tasks
: A dedicated _inbox_ file  
  This file is transient, and should not have sections like `archived:` etc.  
  Will show up as the first entry in projects pop-up list 

inbox
: A shell script that accepts a task and adds it to the dedicated _inbox_ file  
  Usage: FIXME 
  Resides in the TextTasks Bundle and the installer will append the path to your system PATH environment variable.
   
inbox.app
: An application that allows quick entering of task to the dedicated _inbox_ file  
  It accepts dropped files and will ask for a task for each dropped file if more than one
  Resides in the TextTasks Bundle and the installer script will put an alias in the Dock
  
mail rules
: FIXME  

## Configuration

The main config file (defaulting to ~/.texttask_settings) can be edited from TextTasks Bundle menu. Available options and their defaults are:

    # Paths to directories where TextTasks should look for task files
    PROJECT_DIRS = ['${HOME}']
    # A list of the extension recognized by TextTasks
    FILE_EXTS = ['.todo', '.tasks']
    
Environment variables such as HOME, etc. are allowed in paths, but relative paths are not allowed.

Location of inbox shell script can be communicated to inbox.app using `defaults write inbox.app.plist inbox_cmd /path/to/inbox`

Environment variables: FIXME location of the dedicated _inbox_ file

[1]: https://github.com/henrik/tasks.tmbundle   
