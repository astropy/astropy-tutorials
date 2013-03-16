from astropy.io import ascii 
#import ascii subpackage from io subpackage of astropy
import matplotlib.pyplot as plt
#import pyplot subpackage from matplotlib and names it 'plt' (per Python convention)


input_file = 'Young-Objects-Compilation.csv'

data = ascii.read(input_file, header_start=1, data_start=2)
#data_start = 2 is needed so that the default reader uses that line to guess the data types. 
#should not be necessary...data_start should by defalut be header_start + 1 if header_start is specified.

#plot J vs. J-K
JK_color = data['Jmag'] - data['Kmag']

plt.scatter(JK_color, data['Jmag'])
plt.ylim(plt.ylim()[::-1])
plt.ylabel('$J$ mag')
plt.xlabel('$J-K_S$')
#plt.show() #show the figure if needed

