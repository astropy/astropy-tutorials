from astropy.io import ascii
#import ascii subpackage from io subpackage of astropy
import matplotlib.pyplot as plt
#import pyplot subpackage from matplotlib and names it 'plt' (per Python convention)
import astropy.units as u
import astropy.coordinates as coord


#simple table example
input_file1 = 'simple_table.csv'
data = ascii.read(input_file1)

#display first RA in degrees
#support for arrays coming in astropy version 0.3
print 'First RA in degrees:', coord.RA(data['ra'][0],unit=u.hour).degrees
#unit for RA is either u.hour (0-24), u.degree (0-365), or u.radian(0-2pi)
#the ".degrees" is the bit that does the conversion

#more complex table example
input_file2 = 'Young-Objects-Compilation.csv'

data = ascii.read(input_file2, header_start=1, data_start=2)
#data_start = 2 is needed so that the default reader uses that line to guess the data types.
#should not be necessary...data_start should by defalut be header_start + 1 if header_start is specified.

#plot J vs. J-K
JK_color = data['Jmag'] - data['Kmag']

plt.figure() #initializes blank figure
plt.scatter(JK_color, data['Jmag'])
plt.ylim(reversed(plt.ylim()))
plt.ylabel('$J$ mag')
plt.xlabel('$J-K_S$')
plt.show() #show the figure if needed

#plot Ra/Dec on sky projection

#convert RA and Dec to radians for matplotlib projection. which wants radians, but shows degrees
ra_radians = [coord.Angle(val, unit=u.degree, bounds=(-180,180)).radians
                for val in data['RA'] if val !='']
#converts RA from degrees to radians, ranging from -pi to pi cause that's what matplotlib wants.
#Use coord.Angle class because it takes 'bounds' argument
#and only do it if RA is not blank.

dec_radians = [coord.Dec(val,unit=u.degree).radians for val in data['Dec']
                if val !='']

fig = plt.figure() #initializes 2nd figure object and calls it fig
ax1 = fig.add_subplot(111, projection="mollweide") #creates 1 x 1 grid of subplots and add's axes to first plot and calls it ax1
ax1.scatter(ra_radians, dec_radians) #adds scatter plot to ax1
ax1.set_xticklabels(['14h','16h','18h','20h','22h','0h','2h','4h','6h','8h','10h'])
ax1.grid(True)
fig.savefig('map.pdf')
