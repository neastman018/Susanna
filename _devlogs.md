## 7/27/2025
# System Overview:
    Both Push buttons are functional, with hardware methods to interact. 
    However the right button has been observed as activily randomly, although this is infrequent

    Rotary Encoder including button is not functioning at all. Wiring has not been done

    Neo Pixels are working, however they are not running correctly on startup. 
    Think it is a problem with the RaspPi Trying to multitask -- cutting of Neo Pixel Sequence.

    Alarm is going off on time. However I know it will not working for mulitiple days consectrivily as the application only checks the time on start.

    Screen control is fucntioning correctly.

## 12/2/2025
Fixed Calendar Functionality. Was not displaying recurring events so I needed to create RRule dependiecnes to expand recurring events.
Furthermore recurring events were not adjusting to the time zone, therefore had to manually set there time to fix.

On main page.js grid is not laying out properly.

## 12/9/2025
Started Implement SQLite instead of MongoDB. Will play better with Raspiban. Developed some test scripts currently debugging database to be used for the quotes. Issue that it is creating two tables. Need to figure out more where databases are stored when created and how to reference them properly.

Created 2 databases, one in ./ and one on ./backend/

# TODO:
    1. Need to work to get lights functioning with buttons and wake up.
    2. Change the way the application checks for wake up time
    3. Implement a more interrupt based approach?

