# Intro

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
  Intended for use with an "Inbox" project

### Configuration
