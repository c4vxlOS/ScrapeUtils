# !/bin/bash
sudo sh /usr/bin/scraper/sh/uninstall.sh

sudo mkdir -p /usr/bin/scraper/sh

sudo cp -R bulkdownload.py /usr/bin/scraper/
sudo cp -R base64convert.py /usr/bin/scraper/
sudo cp -R scrape.py /usr/bin/scraper/
sudo cp -R scrapeUtils.py /usr/bin/scraper/

cd /usr/bin/scraper/sh/

sudo tee bulkdownload.sh <<EOF
# !/bin/bash
python3 /usr/bin/scraper/bulkdownload.py "\$@"
EOF

sudo tee scrape.sh <<EOF
# !/bin/bash
python3 /usr/bin/scraper/scrape.py "\$@"
EOF

sudo tee base64convert.sh <<EOF
# !/bin/bash
python3 /usr/bin/scraper/base64convert.py "\$@"
EOF

sudo tee uninstall.sh <<EOF
# !/bin/bash
sudo rm /usr/bin/bulkdownload
sudo rm /usr/bin/scrape
sudo rm /usr/bin/base64convert
sudo rm -R /usr/bin/scraper/
EOF

sudo chmod 777 -R ../sh/

sudo ln -s /usr/bin/scraper/sh/bulkdownload.sh /usr/bin/bulkdownload
sudo ln -s /usr/bin/scraper/sh/scrape.sh /usr/bin/scrape
sudo ln -s /usr/bin/scraper/sh/base64convert.sh /usr/bin/base64convert