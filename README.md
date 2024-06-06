# Introduction
This is some code (spectral_hsv.py) that was used to create an Astronomy on Tap game at the 2024 SDSS collaboration meeting. The idea of this is to get people thinking about spectra by making approximate spectra of images and then asking the audience to guess which image this comes from. These aren't scientifically accurate spectra, you can use this as a way to discuss how a real spectrum might bt a bit different.

# What does this code do?
Many people will be familiar with RGB images, where colour information is stored as three values, red, green and blue. However there are other ways of storing colour information. Here I'm using <a href="https://en.wikipedia.org/wiki/HSL_and_HSV">Hue, Saturation and Value</a>. Here the hue is the dominant colour in a pixel. This is essentially a colour wheel with red=0, green=120 and blue=240. I convert this to wavelength and treat the dominant colour of each pixel as a delta function at the wavelength of the dominant colour. Purple is obviously a little hard so I set this to have some of the reddest purple be at the red end of the spectrum and then have the rest of the purples at the violet end of the spectrum.

The saturation is basically how washed-out a colour looks. To represent this I use a grey spectrum across all wavelengths in visible light. I then add this grey spectrum to the colour delta function with a factor dependent on the saturation in the pixel we are dealing with. So for a totally saturated colour the colour delta function will dominate, for a totally unsaturated colour (black, grey, white) the grey spectrum will dominate.

The resulting spectrum is then normalised and multiplied by the value (the third part of HSV). A bright pixel will have a high value, a black pixel will have a value of zero.

The code loops over all pixels in the image and builts up a "spectrum" by summing the "spectra" of every pixel.

This total spectrum is then plotted along with a colour bar to show what colour is what wavelength.

# Caveats
Obviously this is not a scientifically accurate spectrum of the image. It is intended to get people thinking spectrally, how colours might appear on a spectrum, how much a grey continuum dominates compared to a strong colour. Obviously this should never be used for scientific purposes.

# Licences
I've included the code here, it's under an MIT license. I've put a few example images in the images folder. These are under difference licenses, see the credits and licenses document in the image folder
