Last Updated: 14.01.2021

A fun little family tree generator that is extremly barebones at the moment, but it can generate families with more than 5000 total members.



DEPENDECIES:
    Python 3.6 or higher (https://www.python.org/)
    MESA (https://github.com/projectmesa/mesa)
    
Suggestions:
    Any program that can read .ged files(for example Ahnentafel or an online .ged reader)

How it works:
    First you open Settings.txt then you can change the numbers in the first three lines, DON'T ADD LETTERS IN THOSE LINES
    	The first line is the size of the starting population, any whole number that is equell to or greater than 1 will work
    	IMPORTANT! Any population below 10 will likely go extinct in the first one or two generations, 20 is a safe starting size at the moment
    	The second line changes the start year, any number from 0 to n will work, currently doesn't support negative dates
    	The last line is the end year, any number larger than the start year will work
    Next go into the Family Tree Generator Folder and open run.py in python, then simply run that file
    The code will then generate a family tree, this may or may not take a few minutes depending on the time span you chose
    Once the code is finished it will generate a .ged and eventlog.txt file in the Output folder
    
    You can also add/change the names used by changing the content of the namelist files in Family Tree Generator, MAINTAIN THE FORMAT ONE NAME FOR EVERY LINE

Changelog:

    0.0.0001
    -Created Project
    
    0.1.0000
    -Created first very useless version
    
    0.1.0012
    -Fixed problems from previous version
    -Other minor stuff
    
    0.2.0002
    -Added culling system to counter overpopulation
    -Added child limit for females, no more 12+ children from ONE woman, woman now want 1 to ~6 children
    
    0.2.0003
    -Added prototype .ged exporter, still needs proper fixing
    -Other minor stuff
    
    0.2.0004
    -Fixed bug with .ged generation
    -Added eventlog
    
    0.2.0005
    -Fixed bug with minors marring adults
    -Added Output folder
    -Auto-cleanup, NO MORE LEFT OVER FILES!
    
TODO:
    -Add adultry/wedlock + bastards
    -Add child mortality
    -Add ranks -> Lord/Lady; Patrician/Patricia; Burgher; Peasant or King/Queen; Lord/Lady; Lowborn
    	-Add ability to rise and fall in rank
    -Add population effecting events like:
    	-Famins
    	-Plague
    	-War
    -Improve Performance
