# Forecast-Data-Application---Python
This web-scraping application utilizes selenium, requests, tkinter to create an interactive program that allow users to collect precipitation data from various locations at once.
Video: https://www.youtube.com/watch?v=KQjXdQZ2hEo&t=2s

### Introduction
Welcome to LACO Forecast Application, this program will help you collect weather data
automatically to help with Storm Water Inspection.
- How It Works:
The program navigates to each site’s predefined URL, open that web site and automatically
locates the weather data such as chance of rain, amount of rain, recorded rain fall. It then
calculates and output the desired data that will be Copy and Pasted into Storm Water Excel
Sheet.
There Are Two Types Of URL That The Program Will Need For Each Sites:
1. Forecast URL: contains forecast chance of rain and precipitation. Ex:
https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=39.15028&amp;lon=-
123.20667&amp;table=custom&amp;duration=7&amp;interval=6

The application will collect data in Chance of Precip and Precip rows.

2. Recorded Rain Fall URL: contains recorded rainfall time table. There are 3 types of time
table that each site can fall into:
A. Precip Accumulative (inches): These are sites that contains recorded rain for the
entire year. For these sites, the program will take the first entry subtract by the last
entry to calculate total rain.
B. 1 Hour Precip (inches): These are sites that contains recorded rain fall hourly. For
these sites, the program simply add the entries row by row to calculate total rain
C. 24 Hour Precip (inches): These are sites that contains recorded rain fall in the last 24
hours. For these sites, the program will take the first entry of the table to present
recorded rain fall

The program will automatically detects which type of time table the site fall into and act
accordingly. Ex:
https://www.wrh.noaa.gov/mesowest/timeseries.php?sid=LAYC1&amp;table=1&amp;banner=off

### II. First Time Configuration
For your first time using the application, there are a couple settings you need to configure
1. Open “LACO Forecast Data” folder located somewhere on your terminal server desktop
2. Right-click on “gui.py” located in this folder, select “Edit with Notepad++”, a new window
will pop up
3. Select “Run” on the upper top bar, a drop down menu will appear (red circle below)
4. In that drop down menu, select “Run”, a small pop up window will appear with a text entry

5. Copy and paste the following text into the text entry (blue circle above):
C:\Users\administrator.LACO\AppData\Local\Programs\Python\Python36\Lib\idlelib\idle.bat
&quot;$(FULL_CURRENT_PATH)&quot;
6. Select “Save” to create a shortcut so you don’t have to do it every time the program is used
7. Name the shortcut and choose key combination you prefer. It is recommended to choose
“Ctrl” + “Alt” + “P” for the shortcut. Select “OK” when done

8. The program is now configured!!! Congrats. Now move on to “How To Launch The Program”
Section
### III. How To Launch The Program
1. Open Terminal Server and log in using your LACO account
2. Open “LACO Forecast Data” folder located somewhere on your desktop
3. Right click on “launch_here” file in the folder. Select “Edit with Notepad++”
4. With Notepad++ opened, press “Ctrl” + “Alt” + “P” (or whatever key combination you saved
when first configure Notepad++)
5. A new window will appear, press “F5” to launch the program
### IV. Features

A. Getting weather data
- Getting weather data is easy. Simply select the sites you want to get data for in the
check box and press the “Get Data Now” button (Blue circle)
- Weather data will be returned in the white text box, simply Copy/Paste the data
into your Storm Water Excel Sheet
- Note: Use the “All On” or “All Off” buttons to quickly select many sites at once

B. Setting Offset Number
- This program allows you to select the time interval for recorded precipitation. For
example, you may choose to collect the total recorded precipitation from 37 hours
ago to your current time.
- Adjust the offset number in the black circle using the spin box. This number dictates
how far back rain records will be collected when “Get Data Now” button is pressed.
- You may choose the offset number to be any number between 1 and 48.
- Note: For sites that only have “24 hours Precip Accumulative” in their time table
(which are few and rare), any offset number that isn’t 24 will not be allowed to
collect rain data for that site.
C. Saving The Time Last Used
- For the sake of your convenience, the program allows you to save the time when
data was last entered in the Excel sheet. This will help determine how much offset
time you should need.
- Simply press the yellow button “Update Time” in red circle, the program will save
the current time and display it in “Time last used”
D. Adding New Site
As future projects develop, adding new sites to the program will be inevitable, the
instructions to do that is as followed:
1. Click on the “Modify Data” tab located on the upper left corner, this will change the
layout to this:

2. In the “Add New Site” region, enter information of the new site to be added in this
order:
- Project Number: ex 6374.73 (Note: make sure the number entered is formatted like
a number with 2 decimal digits, otherwise it will not work, ex: 47g35.d6j3 or
7345.7255 will not work)
- Project Site Name: ex Rhys vineyard, Big Daddy, Payne
- Forecast URL Address: Enter the URL for forecast chance of rain and precipitation of
the site to be added, this can be found on the Storm Water Excel Sheet
- Recorded URL Address: Enter the URL for recorded precipitation of the site to be
added, this can also be found on the Storm Water Excel Sheet
- Node Number: Some locations can have more complex time table, for example,
Ukiah sites have hourly recorded precipitation at random times. For the program to
be able to accurately compile precipitation data, you need to give it a node number
which is the minute that’s always guarantee to have rain data. For example, Ukiah
sites always have hourly rain data at 56 minute mark. Simply enter 56 for this field.
If the site you’re about to add does not need a node, leave this field empty
3. With all the information entered correctly, press the “Add Now” button, if you have
done everything correctly, the new site should pop up in the checkboxes
NOTE: Sites are organized by the order of their project number
E. Delete Existing Site
1. Click on the “Modify Data” tab located on the upper left corner
2. In the Delete Unwanted Site Here region, select the site you want to delete using
check boxes
3. Press “Delete Chosen Site” button. Warning: once deleted, the site is gone with the
wind unless you re-add it again
F. Detailed Report For Each Site
You can also see a more detailed report for each sites. Look for Python Shell window, it
should look like this after you collect rain data. This report can give you information
such as Forecast URL, Recorded Rain URL, what type of time table does a site have
(Precip Accumulative, 1 Hour Precip, 24 Hour Precip), and how did the program
calculate rain data.

### V. Trouble Shooting
A. The Program Doesn’t Return All Site Data
Sometimes the web server of NOAA fails to deliver the whole html file which can cause
the program to be interrupted. Simply wait a couple minutes and try again. If the
problem persists, check “Detail Report For Each Site” to see at what site did the
program stop at, go to that site’s URLs to make sure everything looks fine. Delete and
Re-add the site with new and updated URL if needed.
It should be noted that forecast URL such as
https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=39.15028&amp;lon=-
123.20667 can sometimes result in incomplete html display. If you click on “Reload
table” (red circle below), the browser will give you a new URL that looks like this:
https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=39.15028&amp;lon=-
123.20667&amp;table=custom&amp;duration=7&amp;interval=6 which is more guarantee to have
accurate html result. When adding new site in the future, it is recommended to acquire
URLs like the latter to avoid crashes.

B. The Program Outputs “#.##” For Recorded Precipitation Data
If the returned data looks like “#.##”, it is because the site of that data has 24 Hour
Precipitation time table and the Offset Number is not 24 (Read Setting Offset Number
for more details).

To fix this, turn Offset Number to 24. If that’s not possible, simply collect rain data for
that site by hand.
C. Important Notes
- Always make sure you are running launch_here.py, make sure the tab that’s opened
in Notepad++ is launch_here.py
- Please do not make any changes to the code and save it. It will stop the program
from working properly

### VI. Contact Info
Cell: (707)-391-3992
Email: phucthanhtruong0405@gmail.com
