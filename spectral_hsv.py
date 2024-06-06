from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import hsv_to_rgb

def hue_to_wavelength(hue):
    #a function to convert wavelength to hue. This was made using a rough by eye comparison to some wavelength to colour plots
    wavelength_tmp=None
    if hue>340:
        hue=hue-360.0
    if hue>290:
        wavelength_tmp=None
    elif hue<0:
        wavelength_tmp=610-6.0*hue
    elif hue<260:
        wavelength_tmp=450.0-160.0*(hue-260)/260.0
    elif hue>=260:
        wavelength_tmp=390.0-2.0*(hue-290)
    return wavelength_tmp

def wavelength_to_hue(wavelength_tmp):
    #the inverse of the above function
    if wavelength_tmp>610:
        hue=360+((610-wavelength_tmp)/6.0)
    elif wavelength_tmp>450:
        hue=((450-wavelength_tmp)*(260.0/160.0))+260.0
    elif wavelength_tmp>390:
        hue=0.5*(390.0-wavelength_tmp)+290
    else:
        hue=None
    return hue

lambda_min=390
lambda_max=701

#open the input image and define the output file
img_tmp=Image.open('/Users/deacon/temp/SDSS_temp/hsv_images/Flag_of_Germany.svg.png')
outfile='/Users/deacon/temp/SDSS_temp/hsv_images/Flag_of_Germany_plot.png'
#convert image from RGB to HSV
hsv_image=img_tmp.convert('HSV')
width, height = hsv_image.size
n_pixels=width*height
pixel_map = hsv_image.load()
#define numpy arrays for wavelength and the total intensity
wavelengths=np.arange(395.0,715.0,10)
intensities=np.zeros(wavelengths.shape)
for i0 in range(0,width):
    for i1 in range(0,height):
        hsv=pixel_map[i0,i1]
        hue=360.0*hsv[0]/255.0
        saturation=100*hsv[1]/255.0
        value=100*hsv[2]/255.0
        #define numpy arrays for colour and a flat white spectrum
        colour_array=np.zeros(wavelengths.shape)
        white_array=np.ones(wavelengths.shape)*3.0/len(wavelengths) #this is normalised so that the amount of white light integrated over all wavelengths is the same as the amount coloured light at one wavelength (see below). In a later part we will mix the coloured and white light. Note I am multiplying by 3 here to take account the fact that an RGB green with 0% saturation will have a white/grey component that has a value of 1 in all three colours (i.e. sum this up and you get 3). This means that if you summed all of the white light it would have an intensity of 3.
        #find the wavelength for the hue of this pixel and set the colour array for that wavelength to one
        wavelength_tmp=hue_to_wavelength(hue)
        if wavelength_tmp:
            index_tmp = np.abs(wavelengths-wavelength_tmp).argmin()
            colour_array[index_tmp]=1.0
        else:
            continue
        #combine the colour and white arrays based on the value of saturation
        intensities_tmp=(saturation*colour_array+(100.0-saturation)*white_array)/100.0
        #normalise the pixel so total value is one and then multiply by value to set the lightness of the pixel
        intensities_norm=sum(intensities_tmp)
        if intensities_norm==0:
            intensities_norm=1
        intensities=intensities+value*intensities_tmp/(100.0*intensities_norm)

#create a colour rainbow for the plot
x=[]
y=[]
colors=[]
y_max=max(intensities/n_pixels)
for i0 in range(lambda_min,lambda_max):
    hue_tmp=wavelength_to_hue(i0)
    if hue_tmp:
        rgb_tmp=hsv_to_rgb((hue_tmp/360.0,1.0,1.0))
        x.append(i0)
        y.append(1.2* y_max)
        colors.append(tuple(rgb_tmp))

#plot the spectrum along with the colour rainbow
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
lc = LineCollection(segments,colors=colors, linewidths=40)
lc.set_array(x)
lc.set_linewidth(30)

plt.rcParams['figure.figsize']= 16,9
plt.rcParams.update({'font.size': 30})
plt.figure()

fig, ax = plt.subplots(1, 1)
ax.plot(wavelengths,intensities/n_pixels,linewidth=5.0,color='k')
line = ax.add_collection(lc)
plt.ylim(0.0,1.3*y_max)
plt.xlabel('wavelength(nm)')
plt.ylabel('Intensity')
plt.savefig(outfile)

