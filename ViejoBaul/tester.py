import matplotlib.pyplot as plt
import scipy
import numpy as np

#x = [0.0, 2.4343476531707129, 3.606959459205791, 3.9619355597454664, 4.3503348239356558, 4.6651002761894667, 4.9360228447915109, 5.1839565805565826, 5.5418099660513596, 5.7321342976055165,5.9841050994671106, 6.0478709402949216, 6.3525180590674513, 6.5181245134579893, 6.6627517592933767, 6.9217136972938444,7.103121623408132, 7.2477706136047413, 7.4502723880766748, 7.6174503055171137, 7.7451599936721376, 7.9813193157205191, 8.115292520850506,8.3312689109403202, 8.5648187916197998, 8.6728478860287623, 8.9629327234023926, 8.9974662723308612, 9.1532523634107257, 9.369326186780814, 9.5143785756455479, 9.5732694726297893, 9.8274813411538613, 10.088572892445802, 10.097305715988142, 10.229215999264703, 10.408589988296546, 10.525354763219688, 10.574678982757082, 10.885039893236041, 11.076574204171795, 11.091570626351352, 11.223859812944436, 11.391634940142225, 11.747328449715521, 11.799186895037078, 11.947711314893802, 12.240901223703657, 12.50151825769724, 12.811712563174883, 13.153496854155087, 13.978408296586579, 17.0, 25.0]
#y = [0.0, 4.0, 6.0, 18.0, 30.0, 42.0, 54.0, 66.0, 78.0, 90.0, 102.0, 114.0, 126.0, 138.0, 150.0, 162.0, 174.0, 186.0, 198.0, 210.0, 222.0, 234.0, 246.0, 258.0, 270.0, 282.0, 294.0, 306.0, 318.0, 330.0, 342.0, 354.0, 366.0, 378.0, 390.0, 402.0, 414.0, 426.0, 438.0, 450.0, 462.0, 474.0, 486.0, 498.0, 510.0, 522.0, 534.0, 546.0, 558.0, 570.0, 582.0, 594.0, 600.0, 600.0]
#y2 = [0.0, 4.0, 6.0, 18.0, 30.0, 42.0, 54.0, 66.0, 78.0, 90.0, 102.0, 114.0, 126.0, 138.0, 150.0, 162.0, 174.0, 186.0, 198.0, 210.0, 222.0, 234.0, 246.0, 258.0, 270.0, 282.0, 294.0, 306.0, 318.0, 330.0, 342.0, 354.0, 366.0, 378.0, 390.0, 402.0, 414.0, 426.0, 438.0, 450.0, 462.0, 474.0, 486.0, 498.0, 510.0, 522.0, 534.0, 546.0, 558.0, 570.0, 582.0, 594.0, 600.0, 600.0]
#y3 = [0.0, 4.0, 6.0, 18.0, 30.0, 42.0, 54.0, 66.0, 78.0, 90.0, 102.0, 114.0, 126.0, 138.0, 150.0, 162.0, 174.0, 186.0, 198.0, 210.0, 222.0, 234.0, 246.0, 258.0, 270.0, 282.0, 294.0, 306.0, 318.0, 330.0, 342.0, 354.0, 366.0, 378.0, 390.0, 402.0, 414.0, 426.0, 438.0, 450.0, 462.0, 474.0, 486.0, 498.0, 510.0, 522.0, 534.0, 546.0, 558.0, 570.0, 582.0, 594.0, 600.0, 600.0]

'''def test_sg_filter_basic():
	# Some basic test cases for savgol_filter().
	x = np.array([1.0, 2.0, 1.0])
	y = scipy.signal.savgol_filter(x, 3, 1, mode='constant')
   # np.testing.assert_allclose(y, [1.0, 4.0 / 3, 1.0])

	y2 = scipy.signal.savgol_filter(x, 3, 1, mode='mirror')
	#np.testing.assert_allclose(y, [5.0 / 3, 4.0 / 3, 5.0 / 3])

	y3 = scipy.signal.savgol_filter(x, 3, 1, mode='wrap')
	#np.testing.assert_allclose(y, [4.0 / 3, 4.0 / 3, 4.0 / 3])
#Smoothing here

test_sg_filter_basic()

fig, ax = plt.subplots(figsize=(8, 6))
#ax.plot(x, y, color='red', label= 'Unsmoothed curve')
#ax.plot(x_int, y_int, color="blue", label= "Interpolated curve")

ax.plot(x, y, color="blue", label= "Interpolated curve")
fig.show()

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y2, color="red", label= "Interpolated curve")
fig.show()

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y3, color="yellow", label= "Interpolated curve")
fig.show()'''
x = []
y= []

def test_sg_filter_trivial():

	print("hello")
	""" Test some trivial edge cases for savgol_filter()."""
	x = np.array([1.0])
	y = scipy.signal.savgol_filter(x, 1, 0)
	np.testing.assert_equal(y, [1.0])

	# Input is a single value.  With a window length of 3 and polyorder 1,
	# the value in y is from the straight-line fit of (-1,0), (0,3) and
	# (1, 0) at 0. This is just the average of the three values, hence 1.0.
	x = np.array([3.0])
	y = scipy.signal.savgol_filter(x, 3, 1, mode='constant')
	np.testing.assert_almost_equal(y, [1.0], decimal=15)

	x = np.array([3.0])
	y = scipy.signal.savgol_filter(x, 3, 1, mode='nearest')
	np.testing.assert_almost_equal(y, [3.0], decimal=15)

	x = np.array([1.0] * 3)
	y = scipy.signal.savgol_filter(x, 3, 1, mode='wrap')
	np.testing.assert_almost_equal(y, [1.0, 1.0, 1.0], decimal=15)

	print("hchao")

test_sg_filter_trivial()

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y, color="yellow", label= "Interpolated curve")
fig.show()