
# Dependencies to make "headless" chrome/selenium work:
sudo apt-get -y install xvfb gtk2-engines-pixbuf
sudo apt-get -y install xfonts-cyrillic xfonts-100dpi xfonts-75dpi xfonts-base xfonts-scalable

# Optional but nifty: For capturing screenshots of Xvfb display:
sudo apt-get -y install imagemagick x11-apps

pip3 install -r ../requirements.txt