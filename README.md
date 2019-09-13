# NEISS Downloader
[A quick Python script](download.py) to download the data and lookup files from the U.S. Consumer Product Safety Commission's _fabulous_ [National Electronic Injury Surveillance System](https://www.cpsc.gov/Research--Statistics/NEISS-Injury-Data). See also the [coding manual](https://www.cpsc.gov/s3fs-public/2018%20NEISS%20Coding%20Manual.pdf) (PDF).

### Requirements
Python 3 (we're using `urllib.request` and `io.StringIO`)

### Usage
`python3 download.py`

This will download ~1GB of TSV files, broken up by year starting with 1997, into the `./data` directory. It will also create a handful of lookup files (derived from [this duder here](https://www.cpsc.gov/cgibin/NEISSQuery/Data/Info%20Docs/neiss_fmt.txt) and drop them into the `./lookups` directory.

If you want to specify a different range of years to download, change the `FIRST_YEAR` and `LAST_YEAR` variables in the script.

### Combining the files
I used [`csvstack`](https://csvkit.readthedocs.io/en/latest/scripts/csvstack.html), which you would need to install separately: `csvstack -t data/*.tsv > neiss.csv`.
