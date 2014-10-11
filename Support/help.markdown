# Intro

Light-weight task/project tracking using plain text files.

# Features

## Return key behaviour 

The return key behaves differently depending on the caret position. There are five cases:

1. in leading whitespace before task => insert new task before line
2. at end of task => insert new task on new line 
3. inside task => split task at caret and insert new task on new line 
4. at end after empty task => clear empty task and align caret with leading space 
5. outside a task behave as usual

## Tags

### Special tags

* @project(<name>)
  When going revising lists you can tag a task with @project(<name>) and when done, selecting "Move Tagged" will move tasks to the project corresponding to <name>.

* @remind(<date>)
  Add the task to Reminders app, changes the tag to @reminded.
  You can set the target Reminders account and list in the settings if you have many accounts and/or lists.

* @mit
  *Most Important Things*, @mit, is a tag that is used by the List MITs command to list all tasks, regardless of project, in the HTML view. 

### Configuration

Confinguration is done via the bundle settings, TextMate -> Bundles -> Edit Bundles…, select Settings.

