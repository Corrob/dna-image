# dna-image
A simple Python script for converting 23andme raw DNA data into an image for viewing the full genome in one image.

How to run?

1. Clone the repo with `git clone https://github.com/Corrob/dna-image`
2. Make sure you have Python3 installed `python --version` or `python3 --version`. If not, check out https://www.python.org/downloads/.
3. Make sure you have numpy and pillow installed. `pip3 install numpy` and `pip3 install pillow`. You may need `pip` instead of `pip3`.
4. Download the Raw DNA text file from 23andme: https://customercare.23andme.com/hc/en-us/articles/212196868-Accessing-Your-Raw-Genetic-Data
5. Put the text file in the repo you downloaded above and run `python3 dna_image.py <name of 23andme textfile>`.
6. You should see an image pop up with your DNA data and it will also be saved in the directory as `dna.png`.
7. Be careful where you send this image as it contains all the DNA information encoded in an image. Your genetic code could be extracted from this image and analyed in various ways.

Why look at the image of my DNA?

First, it's quite interesting to see all the genetic information that codes your body from birth to death in one place. I also believe this is helpful for the brain to get an overview of what DNA is producing the body it is in, even if it can't process all the data consciously.
