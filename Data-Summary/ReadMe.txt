There are 2 folders (bugs and fixes) and 3 excel files (bug.xlsx, fix.xlsx, and project.xlsx)

project.xlsx lists all the information about studied projects.
for each project, we measured:
#file: the number of files 
#loc: lines of code
#Bugs: the number of studied bugs
#ArchBugs: the number of bugs containing architectural changes
#ArchBugs/Bugs: the ratio of ArchBugs in bugs
#Fixes: the number of studied bug fixes
#ArchFixes:  the number of fixes containing architectural changes
#ArchFixes/Fixes:  the ratio of ArchFixes in fixes


bug.xlsx lists all the information about studied bugs.
for each bug, we measured:
#BugID: the label of bug
#isArch: whether a bug is a arch bug
#Priority: the priority assigned for this bug
#Churn: the fixing lines of code
#Time(s): the total fixing time (seconds).  
#Time: the abstraction of fixing time. XX days XX hours XX minutes XX seconds
#Reopen: the reopen times
#Induce: whether this bug induce the presence of new bug

the bug of each project in contained in folder: bugs


fix.xlsx list all the information about fixes of studied bugs.
for each bug fix, we measured
#commitID: the hash of this fix
#type1: whether this fix contain type1 arch changes
#type2: whether this fix contian type2 arch changes
#type3: whether this fix contain both type1 and type2 arch changes.
#bugID: the bugs patched in this fix 