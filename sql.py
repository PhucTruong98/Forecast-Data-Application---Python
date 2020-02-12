import sqlite3
conn = sqlite3.connect("sitesSantaRosa.db")


cur = conn.cursor()
#cur.execute('DROP TABLE SiteURL')
#cur.execute('CREATE TABLE SiteURL (id INTEGER AUTOINCREAMENT, site varchar(255) PRIMARY KEY, fcurl varchar(300), rpurl varchar(300), node varchar(255), projectNumber DECIMAL(10,2))')
#cur.execute('INSERT INTO SiteURL (site,fcurl, rpurl, node, projectNumber) VALUES ("Westport Sink", "https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=39.635706&lon=-123.783069", "https://www.wrh.noaa.gov/mesowest/timeseries.php?sid=MCGC1&num=168&banner=NONE" , "" , 6843.29 ), ("Rhys Vineyards","https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=39.15028&lon=-123.20667&table=custom&duration=7&interval=6", "https://www.wrh.noaa.gov/mesowest/getobext.php?wfo=eka&sid=KUKI&num=168&raw=0&dbn=m", "56", 7655.03), ("Ford Road","https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=39.1712668746177&lon=-123.20371629600122&table=custom&duration=7&interval=6", "https://www.wrh.noaa.gov/mesowest/getobext.php?wfo=eka&sid=KUKI&num=168&raw=0&dbn=m", "56", 7760.06), ("Pt. Arena", "https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=38.91140&lon=-123.69070&table=custom&duration=7&interval=6" , "https://www.wrh.noaa.gov/mesowest/getobext.php?wfo=eka&sid=BNVC1&num=72&raw=0" , "", 8229.00), ("Black Mountain", "https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=38.72182&lon=-122.86813&table=custom&duration=7&interval=6", "https://www.wrh.noaa.gov/mesowest/timeseries.php?sid=HWKC1&table=1&banner=off", "", 8545.11), ("Big Daddy", "https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=39.15028&lon=-123.20667&table=custom&duration=7&interval=6", "https://www.wrh.noaa.gov/mesowest/getobext.php?wfo=eka&sid=KUKI&num=168&raw=0&dbn=m", "56", 8592.01), ("Frey Winery","https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=39.30737937171981&lon=-123.22170257917755&table=custom&duration=7&interval=6","https://www.wrh.noaa.gov/mesowest/getobext.php?wfo=eka&sid=KUKI&num=168&raw=0&dbn=m","56", 8761.00), ("Payne","https://www.wrh.noaa.gov/forecast/wxtables/index.php?lat=39.415030211800094&lon=-123.34657907803542&table=custom&duration=7&interval=6","https://www.wrh.noaa.gov/mesowest/timeseries.php?sid=LAYC1&table=1&banner=off","", 9192.01)')

#cur.execute('SELECT * FROM SiteURL')

#cur.execute("CREATE TABLE currentTime (lastTime VARCHAR(255))")
cur.execute('INSERT INTO currentTime (lastTime) VALUES ("5:56:15")')
conn.commit()
fetch = cur.fetchall()
print(fetch)

