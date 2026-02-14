#--------------------------------------------------------------------------------------------------#
# get_hapasschart.py                                                                               #
# Developed by Kiyoaki Okudaira * University of Washington / Kyushu University / IAU CPS SatHub    #
#--------------------------------------------------------------------------------------------------#
# Description                                                                                      #
#--------------------------------------------------------------------------------------------------#
# Download satellite's pass chart from heavens-above.com                                           #
#--------------------------------------------------------------------------------------------------#
# History                                                                                          #
#--------------------------------------------------------------------------------------------------#
# coding 2026.02.14: 1st coding                                                                    #
#--------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------#
# Libraries                                                                                        #
#--------------------------------------------------------------------------------------------------#
# from astropy.time import Time
import argparse
from requests import get as requests_get
import re
import html
# from numpy import array
from datetime import datetime,timezone

#--------------------------------------------------------------------------------------------------#
# Main                                                                                             #
#--------------------------------------------------------------------------------------------------#
PASSSUMMARY_URL  = "https://www.heavens-above.com/PassSummary.aspx"
PASSDETAIL_URL   = "https://www.heavens-above.com/passdetails.aspx"
PASSSKYCHART_URL = "https://www.heavens-above.com/PassSkyChart2.ashx"
SKYCHART_URL     = "https://www.heavens-above.com/wholeskychart.ashx"

class heavens_above:
    def get_pass_summary(
            norad_id: int | str,
            obs_gd_lon_deg: float,
            obs_gd_lat_deg: float,
            obs_gd_height: float,
            ha_timezone: str ="UCT"
            ):
        """
        Get satellite pass summary from heavens-above.com

        Parameters
        ----------
        norad_id: `int` or `str`
            NORAD catalog number
        obs_gd_lon_deg: `float`
            Geodetic longitude [deg]
        obs_gd_lat_deg: `float`
            Geodetic latitude [deg]
        obs_gd_height: `float`
            Geodetic height [km]
        ha_timezone: `str`
            Pass Chart display timezone. Default is "UCT"

        Returns
        -------
        query_result: `str`
            Satellite pass summary (HTML format)

        Notes
        -----
            (c) 2026 Kiyoaki Okudaira - University of Washington / IAU CPS SatHub
        """
        query_params = {
            "satid" : f"{norad_id:.0f}",
            "lat"   : f"{obs_gd_lat_deg:.6f}",
            "lng"   : f"{obs_gd_lon_deg:.6f}",
            "loc"   : "Unspecified",
            "alt"   : f"{obs_gd_height*1000:.0f}",
            "tz"    : f"{ha_timezone}"
            }

        r = requests_get(PASSSUMMARY_URL, params=query_params)
        r.raise_for_status()
        query_result = r.text

        return query_result

    def parse_summary2mjd(
            query_result: str
            ):
        """
        Parse satellite pass summary to pass MJD list

        Parameters
        ----------
        query_result: `str`
            Satellite pass summary (HTML format)

        Returns
        -------
        mjds: `np.ndarray`
            Satellite pass MJD list

        Notes
        -----
            (c) 2026 Kiyoaki Okudaira - University of Washington / IAU CPS SatHub
        """
        s = html.unescape(query_result)
        mjd_strs = re.findall(r'passdetails\.aspx\?[^"\']*?\bmjd=([0-9.]+)\b', s)
        mjds = [float(x) for x in mjd_strs]
        mjds = list(dict.fromkeys(mjds))

        return mjds

    def get_pass_detail(
            norad_id: int | str,
            obs_gd_lon_deg: float,
            obs_gd_lat_deg: float,
            obs_gd_height: float,
            ha_mjd: float,
            ha_timezone: str = "UCT"
            ):
        """
        Get satellite pass detail from heavens-above.com

        Parameters
        ----------
        norad_id: `int` or `str`
            NORAD catalog number
        obs_gd_lon_deg: `float`
            Geodetic longitude [deg]
        obs_gd_lat_deg: `float`
            Geodetic latitude [deg]
        obs_gd_height: `float`
            Geodetic height [km]
        ha_mjd: `float`
            MJD at start of satellite pass
        ha_timezone: `str`
            Pass Chart display timezone. Default is "UCT"

        Returns
        -------
        query_result: `str`
            Satellite pass detail (HTML format)

        Notes
        -----
            (c) 2026 Kiyoaki Okudaira - University of Washington / IAU CPS SatHub
        """
        query_params = {
            "lat"   : f"{obs_gd_lat_deg:.6f}",
            "lng"   : f"{obs_gd_lon_deg:.6f}",
            "loc"   : "Unspecified",
            "alt"   : f"{obs_gd_height*1000:.0f}",
            "tz"    : f"{ha_timezone}",
            "satid" : f"{norad_id:.0f}",
            "mjd"   : f"{ha_mjd}",
            "type"  : "V"
            }

        r = requests_get(PASSDETAIL_URL, params=query_params)
        r.raise_for_status()
        query_result = r.text

        return query_result

    def parse_detail2passid(
            query_result: str
            ):
        """
        Parse satellite pass summary to satellite pass ID for PassSkyChart query

        Parameters
        ----------
        query_result: `str`
            Satellite pass detail (HTML format)

        Returns
        -------
        pass_id: `str`
            Satellite pass ID for PassSkyChart query

        Notes
        -----
            (c) 2026 Kiyoaki Okudaira - University of Washington / IAU CPS SatHub
        """
        m = re.search(r'PassSkyChart2\.ashx\?[^"\']*\bpassID=(\d+)\b', query_result)
        if not m:
            raise ValueError("Error : Pass SKY Chart not found")
        pass_id = m.group(1)

        return pass_id

    def get_pass_chart(
            pass_id: int | str,
            obs_gd_lon_deg: float,
            obs_gd_lat_deg: float,
            obs_gd_height: float,
            ha_timezone: str = "UCT",
            ha_imgsize: int = 800
            ):
        """
        Get satellite pass detail from heavens-above.com

        Parameters
        ----------
        pass_id: `str`
            Satellite pass ID for PassSkyChart query
        obs_gd_lon_deg: `float`
            Geodetic longitude [deg]
        obs_gd_lat_deg: `float`
            Geodetic latitude [deg]
        obs_gd_height: `float`
            Geodetic height [km]
        ha_timezone: `str`
            Pass Chart display timezone. Default is "UCT"
        ha_timezone: `int`
            Pass Chart image size [pix]. Default is 800

        Returns
        -------
        query_result: `bytes`
            Satellite pass chart image

        Notes
        -----
            (c) 2026 Kiyoaki Okudaira - University of Washington / IAU CPS SatHub
        """
        query_params = {
            "passID"    : f"{pass_id}",
            "size"      : f"{ha_imgsize:.0f}",
            "lat"       : f"{obs_gd_lat_deg:.6f}",
            "lng"       : f"{obs_gd_lon_deg:.6f}",
            "loc"       : "Unspecified",
            "alt"       : f"{obs_gd_height*1000:.0f}",
            "tz"        : f"{ha_timezone}",
            "showUnlit" : "false"
            }

        r = requests_get(PASSSKYCHART_URL, params=query_params)
        r.raise_for_status()
        query_result = r.content

        return query_result

    def get_wholeskychart(
            obs_gd_lon_deg: float,
            obs_gd_lat_deg: float,
            obs_gd_height: float,
            ha_mjd: float,
            ha_timezone: str = "UCT",
            ha_imgsize: int = 800
            ):
        """
        Get satellite pass detail from heavens-above.com

        Parameters
        ----------
        obs_gd_lon_deg: `float`
            Geodetic longitude [deg]
        obs_gd_lat_deg: `float`
            Geodetic latitude [deg]
        obs_gd_height: `float`
            Geodetic height [km]
        ha_mjd: `float`
            MJD
        ha_timezone: `str`
            Pass Chart display timezone. Default is "UCT"
        ha_timezone: `int`
            Pass Chart image size [pix]. Default is 800

        Returns
        -------
        query_result: `bytes`
            Satellite pass chart image

        Notes
        -----
            (c) 2026 Kiyoaki Okudaira - University of Washington / IAU CPS SatHub
        """
        "lat=0&lng=0&loc=Unspecified&alt=0&tz=UCT&size=800  SL=1&SN=1&BW=1&time=61085.28472&ecl=0&cb=0"
        query_params = {
            "lat"       : f"{obs_gd_lat_deg:.6f}",
            "lng"       : f"{obs_gd_lon_deg:.6f}",
            "loc"       : "Unspecified",
            "alt"       : f"{obs_gd_height*1000:.0f}",
            "tz"        : f"{ha_timezone}",
            "size"      : f"{ha_imgsize:.0f}",
            "SL"        : "1",
            "SN"        : "1",
            "BW"        : "1",
            "time"      : f"{ha_mjd}",
            "ecl"       : "0",
            "cb"        : "0"
            }

        r = requests_get(SKYCHART_URL, params=query_params)
        r.raise_for_status()
        query_result = r.content

        return query_result

def main():
    parser = argparse.ArgumentParser(
        description="Retrieve pass chart from heavens-above.com | (c) 2026 Kiyoaki Okudaira - Kyushu University"
    )

    # positional
    parser.add_argument(
        "output_PATH",
        type=str,
        help="Output image file path"
    )

    # optional arguments
    parser.add_argument(
        "-n", "--norad",
        dest="norad_id",
        type=int,
        required=True,
        help="NORAD catalog number"
    )
    parser.add_argument(
        "-t", "--date",
        type=str,
        required=True,
        help="Date and time (UTC) when satellite pass begins [YYYY-MM-DDThh:mm:ss])"
    )
    parser.add_argument(
        "-l", "--lon",
        type=float,
        required=True,
        help="Observer geodetic longitude [deg]"
    )
    parser.add_argument(
        "-b", "--lat",
        type=float,
        required=True,
        help="Observer geodetic latitude [deg]"
    )
    parser.add_argument(
        "-z", "--height",
        type=float,
        required=True,
        help="Observer geodetic height [km]"
    )

    # optional arguments
    parser.add_argument(
        "-Z", "--tz",
        dest="tz",
        type=str,
        default="UCT",
        help='PassChart display timezone (default: "UCT")'
    )
    parser.add_argument(
        "-R", "--size",
        dest="imgsize",
        type=int,
        default=800,
        help="Output PassChart image size [pix] (default: 800)"
    )

    args = parser.parse_args()

    # unpack
    output_PATH = args.output_PATH
    norad_id = args.norad_id
    obs_begin = args.date
    obs_gd_lon_deg = args.lon
    obs_gd_lat_deg = args.lat
    obs_gd_height = args.height
    ha_timezone = args.tz
    ha_imgsize = args.imgsize

    obs_begin_mjd = (datetime.fromisoformat(obs_begin).replace(tzinfo=timezone.utc).timestamp() / 86400.0+ 40587.0)

    try:
        query_result = heavens_above.get_pass_summary(norad_id,obs_gd_lon_deg,obs_gd_lat_deg,obs_gd_height,ha_timezone)
        # obs_begin_mjd = Time(obs_begin, format="isot", scale="utc").mjd
        mjds = heavens_above.parse_summary2mjd(query_result)
        mjds_dif = [abs(f-obs_begin_mjd) for f in mjds]
        ha_mjd = mjds[mjds_dif.index(min(mjds_dif))]
        ha_mjd = ha_mjd if abs(ha_mjd - obs_begin_mjd) < 1/48 else None

        query_result = heavens_above.get_pass_detail(norad_id,obs_gd_lon_deg,obs_gd_lat_deg,obs_gd_height,ha_mjd,ha_timezone)
        pass_id = heavens_above.parse_detail2passid(query_result)

        query_result = heavens_above.get_pass_chart(pass_id,obs_gd_lon_deg,obs_gd_lat_deg,obs_gd_height,ha_timezone,ha_imgsize)
        with open(output_PATH, mode='wb') as f:
            f.write(query_result)
    except:
        # obs_begin_mjd = Time(obs_begin, format="isot", scale="utc").mjd
        query_result = heavens_above.get_wholeskychart(obs_gd_lon_deg,obs_gd_lat_deg,obs_gd_height,obs_begin_mjd,ha_timezone,ha_imgsize)
        with open(output_PATH, mode='wb') as f:
            f.write(query_result)

if __name__ == "__main__":
    main()