# Computer Vision Pong

This was used as a learning project to determine the best methods and possible image processing algorithms that could be used in the game of Atari Pong (1972).

## Python
The Python scripts were made first. OpenCV was used as the benchmark for the algorithms detection capability and speed. After which, all of the algorithms were implemented from first principles. The image processing pipeline was as follows. 

| Detection | OpenCV    | First Principles  |   Reason for use |     
| :----:       |    :----:    |    :----:   |   :----: |
| ball + Paddles | Gray scaling | Gray scaling | Reduce RGB to grayscale |
| Ball + Paddles | Gaussian Blur | Gaussian Blur with 2D Convolution | Reduce noise in the image |
| Ball + Paddles | Hough Circles (Gradient Method) | Hough Circle Gradient Method (Sobel, Canny, Tangential) | Determine the centre of the ball |
| Paddles | Thresholding (binary) | Binary Thresholding |  Image preparation for Suzuki85 |
| Paddles | findContours | Suzuki85 Algorithm  | Contour following and label the contours in the image |
| Paddles | arcLength | N/A | Input parameter for RDP |
| Paddles | approxPolyDP | Ramer-Douglas-Peuker Algorithm | Used to reduce the number of points of the contours |
| Paddles | moments | Moments | Find the centroid of the detected contours in the image

### Explanation
The images required some preparation for them to be passed into the Hough Circles Algorithm. The first operation that had to be performed was the Gray scaling operation in which the image would be converted from RGB to Grayscale. This was done according to the layer weightings according to [[1]](#1) used by OpenCV. 
<!-- Add grayscale image -->

The image now only has one layer, which can be convolved with a Gaussian Kernel. Two methods of convolution were implemented, although they produce the same result the one attempts to pad the 2D Matrix before convolving while the other ignores the values that would be in the padded position [[2]](#2). The Gaussian kernel was generated according to the getGaussianKernel() [[3]](#3) method, which means that it is not limited to a 3x3 matrix as in its current implementation. 
<!-- Add gaussian blur image -->

The noise in the image has been suppressed, so now the Hough Circles algorithm [[4]](#4) can be applied to the image. The OpenCV implementation uses the "HOUGH_GRADIENT" implementation to speed up detection [[5]](#5). The Hough Circles algorithm works by first performing Sobel Edge Detection [[6]](#6). The result is then used to get information about the gradient and magnitude of the image. This information can then be used to perform Canny Edge detection [[7]](#7) on the image. The result is a single-pixel trace of the edges in the image. The actual part of the Hough Circle algorithm can now take that information and draw normal lines to tangent lines on those single-pixel edges on an accumulator space, and this is using the case of the tangential method. The point in the image where the highest frequency of point accumulated is where the circle's centre will be. 
<!-- Add the accumulator -->

The first principles implementation was extremely slow in Python, so a solution to that problem was decreasing the area that was analysed for the ball. This was done by creating a windowing method that would first perform the Hough Circles algorithm on the entire picture and determine where the ball is in the playing field. Then a much smaller window would be scanned for the ball, creating a window that would essentially follow the ball. This method did reduce the time it took for the algorithm to be completed, but it does assume that the ball will not be moving fast enough to escape the window.
<!-- Add images of the window -->

The paddle detection was performed by performing Binary Thresholding on the image as preparation for the Suzuki85 Algorithm [[8]](#8). The Suzuki85 Algorithm would then be used to detect the contours. The contours usually contain many points, the number of points can be reduced by using the Ramer-Douglas-Peuker Algorithm [[9]](#9). The contours can then be analysed by the moments [[10]](#10) algorithm to detect the shape's centroid. This process can also be used to determine the centre of the paddle. However, this method assumes that only the two paddles and the ball are in the image.

Connected-Component Labelling [[11]](#11) could be used to determine the contours. The contours could then be passed to the moments algorithm to determine the paddle and the ball's centre demonstrated in CCLOpenCV.py.




### Discoveries

The approxPoly2D would have been sufficient to detect all objects moving around in the field.

Connected Component Labelling was also tested. The implementation in OpenCV was slow. However, certain YACCLAB [[12]](#12) algorithms and other similar implementations of the algorithm show promise regarding their processing time. 

Note: None of the first principles implementations was optimised.


## C++




## References 

<a id="1">[1]</a> 
“OpenCV: Color conversions.” https://docs.opencv.org/3.4/de/d25/imgproc_color_conversions.html

<a id="2">[2]</a>
“linear algebra - What does it mean to convolve a matrix with a kernel?,” Mathematics Stack Exchange. https://math.stackexchange.com/questions/241041/what-does-it-mean-to-convolve-a-matrix-with-a-kernel

<a id="3">[3]</a>
“OpenCV: Image Filtering.” https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gac05a120c1ae92a6060dd0db190a61afa 

<a id="4">[4]</a>
“OpenCV: Feature Detection.” https://docs.opencv.org/3.4/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d 

<a id="5">[5]</a>
W. Yi and S. Marshall, “Circle detection using Fast Finding and Fitting (FFF) algorithm,” Geo-spatial Information Science, vol. 3, no. 1, pp. 74–78, Jan. 2000, doi: 10.1007/BF02826812.

<a id="6">[6]</a>
Y. Hang and Institute of Electrical and Electronics Engineers, Eds., 2010 3rd IEEE International Conference on Computer Science and Information Technology: (ICCSIT 2010) ; Chengdu, China, 9 - 11 July 2010. Piscataway, NJ: IEEE, 2010.

<a id="7">[7]</a>
J. Canny, “A Computational Approach to Edge Detection,” IEEE Trans. Pattern Anal. Mach. Intell., vol. PAMI-8, no. 6, pp. 679–698, Nov. 1986, doi: 10.1109/TPAMI.1986.4767851.


<a id="8">[8]</a>
S. Suzuki and K. be, “Topological structural analysis of digitized binary images by border following,” Computer Vision, Graphics, and Image Processing, vol. 30, no. 1, pp. 32–46, Apr. 1985, doi: 10.1016/0734-189X(85)90016-7.

<a id="9">[9]</a>
“Ramer–Douglas–Peucker algorithm,” Wikipedia. [Online]. Available: https://en.wikipedia.org/w/index.php?title=Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm&oldid=1063755023

<a id="10">[10]</a>
U. Sinha, “Image Moments - AI Shack.” https://aishack.in/tutorials/image-moments/.

<a id="11">[11]</a>
“OpenCV Connected Component Labeling and Analysis,” PyImageSearch, Feb. 22, 2021. https://www.pyimagesearch.com/2021/02/22/opencv-connected-component-labeling-and-analysis/.

<a id="12">[12]</a>
C. Grana, F. Bolelli, L. Baraldi, and R. Vezzani, “YACCLAB - Yet Another Connected Components Labeling Benchmark,” in 2016 23rd International Conference on Pattern Recognition (ICPR), Cancun, Dec. 2016, pp. 3109–3114. doi: 10.1109/ICPR.2016.7900112.