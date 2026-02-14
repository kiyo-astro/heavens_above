# Heavens-Above Program Package
Python-based executable file set that shamefully scrap [Heavens-Above](https://heavens-above.com) web service

## Install
**For Apple silicon Mac**<br>
Download ./dist/ folder and you can use executable files as they are.<br>
OR you can execute python files directory<br>
<br>
**For environments other than Apple silicon Mac**<br>
Use PyInstaller to make python files executable.<br>
OR you can execute python files directory<br>
<br>
**If you want to use in raw Python-coding**<br>
Use [satphotometry library heavens_above.py](https://github.com/kiyo-astro/satphotometry/blob/main/heavens_above.py)

## Usage
### get_hapasschart
**usage** :<br>
`get_hapasschart [-h] -n NORAD_ID -t DATE -l LON -b LAT -z HEIGHT [-Z TZ] [-R IMGSIZE] output_PATH`<br>
<br>
Retrieve pass chart from [Heavens-Above](https://heavens-above.com)<br>
<br>
**positional arguments** :<br>
  output_PATH           Output image file path<br>
<br>
**options** :<br>
```TSV
  `-h`, `--help`               show help message and exit
  `-n`, `--norad`  `NORAD_ID`  NORAD catalog number
  `-t`, `--date`   `DATE`      Date and time (UTC) when satellite pass begins [YYYY-MM-DDThh:mm:ss])
  `-l`, `--lon`    `LON`       Observer geodetic longitude [deg]
  `-b`, `--lat`    `LAT`       Observer geodetic latitude [deg]
  `-z`, `--height` `HEIGHT`    Observer geodetic height [km]
  `-Z`, `--tz`     `TZ`        PassChart display timezone (default: "UCT")
  `-R`, `--size`   `IMGSIZE`   Output PassChart image size [pix] (default: 800)
```

## Author
(c) 2026 **Kiyoaki Okudaira**<br>
Kyushu University Hanada Lab (SSDL)
