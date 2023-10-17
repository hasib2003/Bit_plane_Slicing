import cv2 as cv;
import numpy as np;
class BitPlaneSlicing:
    def simulateBitPlanes(self,Img):
        """ regenrating the image using only one plane at time, 
        images will be shown as black and white because one plane means 
        we have only information in powers of 2 i.e, 1,2,4,8,...
        so to make the information more visible we scale up the information
        to 255 making it look like an black and white image
        """
        for i in range(8):
            bitplane = Img & (1<<i);
            bitplane =(bitplane * (255/(2**i))).astype(np.uint8)
            self.show(f"regenrated from bitplane level {i} ",bitplane)

    def show(self,prompt,img):
        cv.namedWindow(prompt, cv.WINDOW_NORMAL)
        cv.imshow(prompt, img)
        cv.waitKey(0) 
        # cv.destroyAllWindows()

    def mergeImages(self,img1,img2,bits1=4,inGray=False):
        """
        This function takes in two images and stores the second image into the first image,
        and returns the firstImage (having the second image embedded in it).

        Args:
        img1: The image in which the second image is to hide.
        img2: The image that is to hide.
        bits1: Number of bits of img1 to be preserved; the bits for the second image are calculated automatically since bits1 + bits2 = 8.
        inGray: Specifies whether the images must be converted to grayscale or used as provided.

        Returns:
        The merged image.
        """



        arr1 = np.array(img1)
        arr2 = np.array(img2)

        rows = min(arr1.shape[0] , arr2.shape[0])
        cols = min(arr1.shape[1] , arr2.shape[1])

        arr1 = cv.resize(arr1,(cols,rows))
        arr2 = cv.resize(arr2,(cols,rows))


        if(inGray):
            arr1 = cv.cvtColor(arr1,cv.COLOR_RGB2GRAY)
            arr2 = cv.cvtColor(arr2,cv.COLOR_RGB2GRAY)

        mask1 = 0;
        mask2 = 0;
        for i in range(bits1):
            mask1 += 2**(7-i);
        for i in range(8-bits1):
            mask2 += 2**(7-i);
        
        arr1 = arr1 & (mask1);

        arr1 = arr1.astype(np.uint8);

        arr2 = arr2 & (mask2)

        arr2 = arr2.astype(np.uint8);

        self.show(f"regenrated from {bits1} MS bitplane levels of first image ",arr1)
        self.show(f"regenrated from {8-bits1} MS bitplane levels of second image ",arr2)
        arr2 = (arr2 >> (bits1));


        arr1 = arr1 | arr2;

        self.show(f"merged Images ",arr1)
        return arr1

    def extractImage(self,img1,bitsUsed):
        mask = 0;
        for i in range(8-bitsUsed):
            mask += 2**i;
        extractedImage = np.array(img1); 
        extractedImage = img1 & (mask);
        extractedImage = extractedImage << bitsUsed;
        self.show("extracted Image  ",extractedImage)
        return extractedImage;




Wasam = cv.imread("./img1.jpg");
AbdulRehman = cv.imread("./img2.jpg")

bitPlaneGenerator = BitPlaneSlicing();

merged = bitPlaneGenerator.mergeImages(Wasam,AbdulRehman,bits1=6,inGray=True)


extracted = bitPlaneGenerator.extractImage(merged,6)

print(extracted)
