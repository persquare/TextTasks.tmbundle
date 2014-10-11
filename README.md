# TextTasks

Yet another task management bundle for TextMate. This one is heavily inspired by [Tasks.tmbundle][1] by Henrik Nyh.

## Why don't I just use Tasks? 

In my perpetual search for the perfect editor, the turn has come to TextMate and I wanted to dive under the skin to become fluent with TextMate. What better way to get into the details than writing a bundle of my own. This is my ongoing learning experience.

## Quick start

Help is available from the TextTasks Bundle menu

Open the settings and edit to your liking (or use the default settings). If you use Dropbox, consider creating a Lists folder in your Dropbox folder and add that folder to the `TT_PROJECT_DIRS` list. 

## Supporting acts

Reminders
: Inspired by nvRemind
  TBW

## Configuration

TextTask setting are edited from Edit bundle -> TextTasks -> Settings menu. Available options and their defaults are:

    # A Colon separated list of paths to directories where TextTasks should look for task files
    TT_PROJECT_DIRS = '${HOME}'
    # A comma separated list of the file extension recognized by TextTasks
    FILE_EXTS = '.todo'
    
Environment variables such as `HOME`, etc. are allowed in paths, but relative paths are not allowed.


[1]: https://github.com/henrik/tasks.tmbundle   
