The purpose of this application is to perform character replacement on Japanese Characters (kana) and replace
them with their English pronunciations. 

The main reason I made this was to help teach myself hiragana and katakana, particularly while playing through old 
Japanese games with heavily pixelated fonts. The character replacement was mainly put in there for the assingment
requirements, the main feature is the output file with pronunciation + translation. I'd like to create a more 
automated version of this that lets you capture a live window (i.e. a game window or something) and have it 
perform real time translation and pronunciation in another window. This could be pretty cool for learning japanese
and for helping with fan-translations.

To get this to work you will need both the Google Tesseract Python extension installed, with Japanese Character
recognition enabled, and the googletrans google tranlsate API installed. I also couldn't get this program to run 
properly on the lab computers despite supposedly having both extensions installed. 



To run the program, I used Windows with the anaconda python terminal.

Run the terminal and enter the following commands

1) Python jp_text_reader.py

2) Enter the name of the image you want to read, this image should be placed in the "images" folder.
   (note that the file format does matter)

3) An output image will be displayed, as well as output data being fed through the terminal. These outputs will
   all be stored in an output file and output image