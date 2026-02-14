# Heavens-Above Program Package
Python-based executable file set that shamefully scrap Heavens-Above.com web service

## Install
**For Apple silicon Mac**<br>
Download ./dist/ folder and you can use executable files as they are.<br>
OR you can execute python files directory<br>
<br>
**For environments other than Apple silicon Mac**<br>
Use PyInstaller to make python files executable.<br>
OR you can execute python files directory

## Usage
### get_hapasschart
**usage** : `get_hapasschart [-h] -n NORAD_ID -t DATE -l LON -b LAT -z HEIGHT [-Z TZ] [-R IMGSIZE] output_PATH`<br>
<br>
Retrieve pass chart from heavens-above.com<br>
<br>
**positional arguments** :<br>
  output_PATH           Output image file path<br>
<br>
**options** :<br>
  -h, --help            show this help message and exit<br>
  -n, --norad NORAD_ID  NORAD catalog number<br>
  -t, --date DATE       Date and time (UTC) when satellite pass begins [YYYY-MM-DDThh:mm:ss])<br>
  -l, --lon LON         Observer geodetic longitude [deg]<br>
  -b, --lat LAT         Observer geodetic latitude [deg]<br>
  -z, --height HEIGHT   Observer geodetic height [km]<br>
  -Z, --tz TZ           PassChart display timezone (default: "UCT")<br>
  -R, --size IMGSIZE    Output PassChart image size [pix] (default: 800)<br>

## Author
(c) 2026 **Kiyoaki Okudaira**<br>
Kyushu University Hanada Lab (SSDL) / University of Washington / IAU CPS SatHub
