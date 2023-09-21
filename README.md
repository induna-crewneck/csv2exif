# csv2exif

### What does it do?
It takes data from a csv file and runs it through exiftool to apply exif and xmp tags to a set of photos.

### Requirements
- [python v3+](https://www.python.org/downloads/)
- [pip v19.3+](https://pip.pypa.io/en/stable/installation/)
- [pandas v.2.1.0+](https://pandas.pydata.org/docs/getting_started/install.html)
- [exiftool](https://exiftool.org/)

### Setup
For ease of use, you should create a folder with the following contents:
- csv2exif.py
- csv2exif.exiftoolconfig
- exiftool (either just the exe on Windows or the folder containing the program on Mac)
- the csv containing your data (see below)
- a folder containing your photos (this isn't really necessary, but saves you a few clicks and can function as a safety procaution not to directly write to your original files)

### Usage
1. Open your CMD (Windows) or Terminal (Mac) and run the script like this `python path/to/your/script/csv2exif.py`
2. The script will scan the folder for exiftool. If you have followed my advice above, it should find it. If not, it will ask you to pinpoint the location of exiftool.
3. Next it will ask for the location of your photos. So enter for example `path/to/your/script/photos`
4. Next it will ask you to pinpoint your csv file. Example: `path/to/your/script/filminfo.csv`
5. Finally it will ask you wether you want to keep the original files as backup. Just answer with Y,y,N or n
6. Now wait for it to process. Depending on wether or not you've changed the DEBUG flag in the code, you will see more or less info about what's going on. But you don't have to do anything else.

### Preparing the CSV
The data used is taken from a csv file. The easiest way to do this is to download my template and fill in your data. You could also try to create your own or add tags in the header row, but it may not work with the script. The template is made in conjunction with the script and should work without issues. In the template I have included some samples of valid foromatting for the specific columns. Make sure to save as "CSV UTF-8" or equivalent.

#### CSV Values
Most of the template is straight forward and looking at my examples, you should know what to fill and what not to fill. There are a few exeptions which I've listed below:

ID: The ID is the number of your photo on the roll. If you only have 24 images or you have shot on the 0 or 00, just fill the corresponding rows. Rows can be left empty as needed.

FilmID: If you're cataloguing your films, you can use this. As with all the values, you can leave it empty if not needed.

| Flash | Meaning                                             |
| ----- | --------------------------------------------------- |
| 0     | No Flash                                            |
| 1     | Fired                                               |
| 5     | Fired, Return not detected                          |
| 7     | Fired, Return detected                              |
| 8     | On, Did not fire                                    |
| 9     | On, Fired                                           |
| d     | On, Return not detected                             |
| f     | On, Return detected                                 |
| 10    | Off, Did not fire                                   |
| 14    | Off, Did not fire, Return not detected              |
| 18    | Auto, Did not fire                                  |
| 19    | Auto, Fired                                         |
| 1d    | Auto, Fired, Return not detected                    |
| 1f    | Auto, Fired, Return detected                        |
| 20    | No flash function                                   |
| 30    | Off, No flash function                              |
| 41    | Fired, Red-eye reduction                            |
| 45    | Fired, Red-eye reduction, Return not detected       |
| 47    | Fired, Red-eye reduction, Return detected           |
| 49    | On, Red-eye reduction                               |
| 4d    | On, Red-eye reduction, Return not detected          |
| 4f    | On, Red-eye reduction, Return detected              |
| 50    | Off, Red-eye reduction                              |
| 58    | Auto, Did not fire, Red-eye reduction               |
| 59    | Auto, Fired, Red-eye reduction                      |
| 5d    | Auto, Fired, Red-eye reduction, Return not detected |
| 5f    | Auto, Fired, Red-eye reduction, Return detected     |

| ExposureMode | Meaning      |
| ------------ | ------------ |
|              |              |
| 0            | Auto         |
| 1            | Manual       |
| 2            | Auto bracket |
