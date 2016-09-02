from Quartz import *

import Images
import DataProvidersAndConsumers
import Utilities

import sys

def exportImageWithMaskFromURLWithDestination(context, imageURL, 
        imagewidth, imageheight, bitsPerComponent, 
        theMaskingImageURL, maskwidth, maskheight):

    imageBitsPerPixel = bitsPerComponent * 3
    bytesPerRow = ((imagewidth * imageBitsPerPixel) + 7)/8
    shouldInterpolate = True
    imageDataProvider = CGDataProviderCreateWithURL(imageURL)
    if imageDataProvider is None:
        print >>sys.stderr, "Couldn't create Image Data provider!"
        return

    colorspace = Utilities.getTheCalibratedRGBColorSpace()
    image = CGImageCreate(imagewidth, imageheight, bitsPerComponent,
                        imageBitsPerPixel, bytesPerRow, colorspace,
                        kCGImageAlphaNone, imageDataProvider, 
                        None, shouldInterpolate,
                        kCGRenderingIntentDefault)
    del imageDataProvider
    if image is None:
        print >>sys.stderr, "Couldn't create CGImageRef for this data!"
        return

    imageRect = CGRectMake(0.0,imageheight, imagewidth, imageheight)
    # Draw the image.
    CGContextDrawImage(context, imageRect, image)
	
    # Now the mask.
    maskDataProvider = CGDataProviderCreateWithURL(theMaskingImageURL)
    if maskDataProvider is None:
        print >>sys.stderr, "Couldn't create Image Data provider!"
        return 

    mask = CGImageMaskCreate(maskwidth, maskheight, bitsPerComponent,
                            bitsPerComponent, maskwidth,
                            maskDataProvider, None, shouldInterpolate)
    del maskDataProvider
    if mask is None:
        print >>sys.stderr, "Couldn't create CGImageRef for mask data!"
        return
	
    # Draw the mask below the image.
    maskRect = CGRectMake(0.0, 0.0, maskwidth, maskheight)
    CGContextDrawImage(context, maskRect, mask)
	
    # Create a new CGImage object, the image, masked with mask.
    imageMaskedWithImage = CGImageCreateWithMask(image, mask)
    # Once the new image is created, we can release the image
    # and the mask which make it up. Quartz retains what it needs
    # for the new masked image.
    del image
    del mask

    if imageMaskedWithImage is None:
        print >>sys.stderr, "Couldn't create image masked with mask!"
        return

    imageRect = CGRectMake(imagewidth, imageheight/2, imagewidth, imageheight)
    # Draw the masked image to the right of the image and its mask.
    CGContextDrawImage(context, imageRect, imageMaskedWithImage)

    # Of course this is a total hack.
    outPath = "/tmp/imageout.png"
    exportURL = CFURLCreateFromFileSystemRepresentation(None,
				    outPath, len(outPath), False)
		
    if exportURL is not None:
        Images.exportCGImageToPNGFileWithDestination(imageMaskedWithImage, exportURL)

_data = ''.join(map(chr, (
	0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
	0xFE, 0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF8, 0x00, 0x03, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0x00, 0x00, 0xF8, 0xE7, 0xFF, 0xFF, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0xE0, 0x00, 0x00, 0x00, 0x40, 0x7F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xC0,
	0x00, 0x00, 0x00, 0x00, 0x7F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xFF, 0xFF, 0xFF,
	0xFF, 0xFF, 0xF8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF8, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0xFF,
	0xFF, 0xFF, 0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0xFF, 0xFF, 0xFF, 0x80, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x0F, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x0F, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xFF, 0xFF,
	0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7F, 0xFF,
	0xFF, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7F, 0xFF, 0xFF, 0xFE, 0x00, 0x00,
	0x00, 0x00, 0x01, 0xC0, 0x00, 0x00, 0x7F, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x0F, 0xF8,
	0x00, 0x00, 0x7F, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x00, 0x0F, 0xFF, 0xF8, 0x00, 0x00, 0x7F, 0xFF,
	0xFF, 0xFE, 0x00, 0x00, 0x00, 0x1F, 0xFF, 0xFC, 0x00, 0x00, 0x7F, 0xFF, 0xFF, 0xFE, 0x00, 0x00,
	0x00, 0x7F, 0xFF, 0xFC, 0x00, 0x00, 0x7F, 0xFF, 0xFF, 0xF8, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFC,
	0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xF8, 0x00, 0x00, 0x03, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF,
	0xFF, 0xF0, 0x00, 0x00, 0x03, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x7F, 0xFF, 0xFF, 0xF8, 0x00, 0x00,
	0x0F, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x7F, 0xFF, 0xFF, 0xF8, 0x00, 0x00, 0x0F, 0xFF, 0xFF, 0xFF,
	0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xF0, 0x00, 0x00, 0x1F, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0xFF, 0xFF,
	0xFF, 0xE0, 0x00, 0x00, 0x3F, 0xFF, 0xFF, 0xFF, 0x80, 0x01, 0xFF, 0xFF, 0xFF, 0xE0, 0x00, 0x00,
	0x7F, 0xFF, 0xFF, 0xFF, 0x80, 0x00, 0x1F, 0xFF, 0xFF, 0xE0, 0x00, 0x00, 0x7F, 0xFF, 0xFF, 0xFF,
	0x80, 0x00, 0x1F, 0xFF, 0xFF, 0xE0, 0x00, 0x00, 0x3F, 0xFF, 0xFF, 0xFF, 0xC0, 0x00, 0x1F, 0xFF,
	0xFF, 0xF8, 0x00, 0x00, 0x3F, 0xFF, 0xFF, 0xFF, 0xE0, 0x00, 0x1F, 0xFF, 0xFF, 0xF8, 0x00, 0x00,
	0x7F, 0xFF, 0xFF, 0xFF, 0xC0, 0x00, 0x1F, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x7F, 0xFF, 0xFF, 0xFE,
	0x40, 0x00, 0x0F, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x1F, 0xFF,
	0xFF, 0xFC, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xC0, 0x00, 0x00, 0x1F, 0xFF, 0xFF, 0xFC, 0x00, 0x01,
	0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0xFF, 0xFC, 0x00, 0x05, 0xEF, 0xFF, 0xFE, 0x00,
	0x00, 0x00, 0x3F, 0xFF, 0xFF, 0xF0, 0x00, 0x3F, 0x00, 0x03, 0xFC, 0x00, 0x00, 0x00, 0x3F, 0xFF,
	0xFF, 0xE0, 0x00, 0x7C, 0x00, 0x00, 0x78, 0x1F, 0x00, 0x00, 0x7F, 0xFF, 0xFF, 0xC0, 0x00, 0x38,
	0x00, 0x00, 0x78, 0x3C, 0x00, 0x01, 0xFF, 0xFF, 0xFF, 0xC0, 0x00, 0x78, 0x00, 0x00, 0x70, 0x18,
	0x00, 0x01, 0xFF, 0xFF, 0xFF, 0xF0, 0x00, 0x78, 0x1F, 0x00, 0x30, 0x00, 0x00, 0x01, 0xFF, 0xFF,
	0xFF, 0xFE, 0x00, 0x7C, 0x3F, 0x00, 0x18, 0x00, 0x00, 0x01, 0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00,
	0x00, 0x00, 0x38, 0x00, 0x00, 0x03, 0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x80, 0x00, 0x3C, 0x00,
	0x0C, 0x03, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x3C, 0x20, 0x1C, 0x03, 0xFF, 0xFF,
	0xFF, 0xFF, 0x00, 0x00, 0x04, 0x00, 0x3C, 0x00, 0x3C, 0x03, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x70,
	0xBF, 0x86, 0x3C, 0x1F, 0xFC, 0x0B, 0xFF, 0xFF, 0xFF, 0xFF, 0xA0, 0x11, 0xF0, 0x0E, 0x3C, 0x1F,
	0xFE, 0x8B, 0xFF, 0xFF, 0xFF, 0xFF, 0xA0, 0x19, 0xF0, 0x0C, 0x3C, 0x0F, 0xFF, 0x0B, 0xFF, 0xFF,
	0xFF, 0xFF, 0xB0, 0x1D, 0xFE, 0x1C, 0x7E, 0x0F, 0xFF, 0x03, 0xFF, 0xFF, 0xFF, 0xFF, 0xB8, 0x1C,
	0xFF, 0x3C, 0xFE, 0x03, 0xFE, 0x03, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x1E, 0x7F, 0xF8, 0xDE, 0x00,
	0x7C, 0x03, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x1E, 0x7F, 0xF1, 0xDF, 0x30, 0x03, 0x83, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFE, 0x1F, 0x3F, 0xE3, 0x9F, 0x10, 0x3F, 0x83, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x0F,
	0xFF, 0x83, 0xDF, 0x80, 0x1F, 0x83, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x03, 0xFC, 0x03, 0xDF, 0x81,
	0x8F, 0x83, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x07, 0xFE, 0x1F, 0x8F, 0x00, 0x07, 0x83, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0x07, 0xFE, 0x3C, 0x06, 0x00, 0x01, 0x83, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x03,
	0xFC, 0x7C, 0x00, 0x00, 0x01, 0x83, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x01, 0xF8, 0x7F, 0x00, 0x00,
	0x01, 0x83, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x01, 0xF8, 0xFF, 0xE0, 0x30, 0x01, 0x83, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0x00, 0xF1, 0xEF, 0xF9, 0xE0, 0x03, 0x83, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x80,
	0xF1, 0xFF, 0xFF, 0x80, 0x0F, 0x83, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x03, 0xE2, 0xFF, 0xFE, 0x00,
	0x1F, 0x87, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x83, 0xF0, 0x00, 0x00, 0x1C, 0x3F, 0x87, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0xC3, 0xF0, 0x00, 0x01, 0xF8, 0x0F, 0x87, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xC3,
	0xF0, 0x03, 0xFF, 0xF0, 0x5F, 0x07, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xC1, 0xFF, 0xC7, 0xFF, 0xE0,
	0x7F, 0x0F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xE1, 0xFF, 0xF1, 0xFF, 0x80, 0x2F, 0x0F, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0xE1, 0xFF, 0xF8, 0x0F, 0xC0, 0x06, 0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF4,
	0xFF, 0xFE, 0x0F, 0xF8, 0x44, 0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF4, 0xFF, 0xFF, 0xFF, 0xF8,
	0x64, 0x3F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF9, 0xFF, 0xFF, 0xFF, 0x3C, 0xE4, 0x7F, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0xFD, 0x9F, 0xFF, 0xFC, 0x1F, 0xC0, 0x7F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFD,
	0x1F, 0xFF, 0xFC, 0x03, 0xC0, 0x7F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x01, 0xFF, 0xFF, 0xFF,
	0xC0, 0x7F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0xFF, 0xFF, 0xFF, 0x00, 0x7F, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0xFF, 0xFF, 0xFF, 0x00, 0x7F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE,
	0x80, 0x7F, 0xFF, 0xFF, 0x00, 0x3F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x80, 0x1F, 0xFF, 0xFF,
	0x00, 0x3F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0xC0, 0x0F, 0xFF, 0xFF, 0x00, 0x1F, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0xFF, 0xE0, 0x07, 0xFF, 0xFF, 0x00, 0x0F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
	0xF0, 0x03, 0xFF, 0xFF, 0x00, 0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x70, 0x01, 0xFF, 0xFC,
	0x00, 0x17, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x78, 0x00, 0x7F, 0xF0, 0x00, 0x07, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0xF0, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x07, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x03,
	0xFE, 0x00, 0x00, 0x00, 0x00, 0x07, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x1F, 0xFF, 0x80, 0x00, 0x00,
	0x00, 0x07, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x7F, 0x7F, 0xC0, 0x00, 0x00, 0x00, 0x07, 0xFF, 0xFF
    )))

def getMaskData1():
    return _data

_data2 = ''.join(map(chr, (
	0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
	0xFF, 0xFF, 0x03, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x00, 0x1F, 
	0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xE0, 0x00, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 
	0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x80, 0x00, 0x00, 0x3F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
	0xFF, 0x00, 0x00, 0x00, 0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 
	0x07, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF8, 0x00, 0x00, 0x00, 0x03, 0xFF, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0x00, 0x00, 0x00, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
	0xE0, 0x00, 0x00, 0x00, 0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xC0, 0x00, 0x00, 0x00, 
	0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x80, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 
	0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x3F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0xF8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF8, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x0F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0x00, 0x00, 0x00, 0x01, 
	0x80, 0x07, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0x00, 0x00, 0x00, 0x03, 0xC0, 0x07, 0xFF, 0xFF, 
	0xFF, 0xFF, 0xFF, 0xF0, 0x00, 0x00, 0x00, 0x0B, 0xE0, 0x07, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xE0, 
	0x00, 0x00, 0x00, 0x07, 0xF0, 0x03, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xE0, 0x00, 0x00, 0x00, 0x1F, 
	0xF4, 0x83, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xC0, 0x00, 0x00, 0x00, 0x3F, 0xE4, 0x03, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFF, 0xC0, 0x00, 0x00, 0x00, 0x3F, 0xE4, 0x43, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x80, 
	0x00, 0x00, 0x00, 0x3F, 0xE4, 0x4B, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x80, 0x00, 0x00, 0x02, 0xFF,
	0xE4, 0x5B, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x02, 0xFF, 0xE0, 0x5B, 0xFF, 0xFF, 
	0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x07, 0xC1, 0xFF, 0xE0, 0x59, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x18,
	0x00, 0x7F, 0xF0, 0xFE, 0x00, 0x79, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x18, 0x00, 0x78, 0x0F, 0xFE, 
	0x04, 0xE1, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x18, 0x00, 0xB0, 0x47, 0xFF, 0xFF, 0xE1, 0xFF, 0xFF,
	0xFF, 0xFF, 0xFE, 0x10, 0x00, 0xC4, 0x69, 0xFF, 0xFF, 0xC3, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE, 0x10, 
	0x01, 0xFF, 0xE1, 0xFC, 0x07, 0xC1, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x00, 0x01, 0xFF, 0xF8, 0x78,
	0x01, 0xC5, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x04, 0x01, 0xFF, 0xF0, 0x78, 0x01, 0xC5, 0xFF, 0xFF, 
	0xFF, 0xFF, 0xFC, 0x0C, 0x00, 0xFF, 0xF8, 0x7E, 0x3F, 0xC1, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x0C,
	0x00, 0x7F, 0xF0, 0x18, 0xFF, 0xC3, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x07, 0x00, 0x7F, 0xF4, 0x1F, 
	0xFF, 0xE3, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0x23, 0x00, 0x7F, 0xE0, 0x3E, 0xFF, 0xE3, 0xFF, 0xFF,
	0xFF, 0xFF, 0xF8, 0x11, 0x00, 0x7F, 0xEC, 0x5F, 0xBF, 0xE3, 0xFF, 0xFF, 0xFF, 0xFF, 0xF8, 0x01, 
	0x00, 0x3F, 0xCE, 0x7E, 0x3F, 0xE3, 0xFF, 0xFF, 0xFF, 0xFF, 0xF8, 0x08, 0x00, 0x7F, 0x80, 0x2E,
	0x3F, 0xE3, 0xFF, 0xFF, 0xFF, 0xFF, 0xF8, 0x06, 0x00, 0x7F, 0x00, 0x6E, 0x3F, 0xEB, 0xFF, 0xFF, 
	0xFF, 0xFF, 0xF0, 0x00, 0x00, 0x7E, 0x0D, 0xFE, 0xFF, 0xEB, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0x00,
	0x00, 0x3C, 0x00, 0xFE, 0x3F, 0xEB, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0x00, 0x00, 0x50, 0x00, 0xFE, 
	0x3F, 0xCB, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0x00, 0x00, 0x01, 0x98, 0xFF, 0x3F, 0xCB, 0xFF, 0xFF,
	0xFF, 0xFF, 0xF0, 0x00, 0x00, 0xC7, 0xE1, 0xFF, 0x3F, 0x8B, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0x00, 
	0x00, 0x40, 0xFF, 0xFF, 0xBF, 0x8B, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0x00, 0x00, 0xE0, 0x1F, 0xFF,
	0xDF, 0x0B, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0x00, 0x00, 0xE8, 0x63, 0xFF, 0xDF, 0x0F, 0xFF, 0xFF, 
	0xFF, 0xFF, 0xF0, 0x00, 0x02, 0xFC, 0xF9, 0xFF, 0xEF, 0x0F, 0xFF, 0xFF, 0xFF, 0xFF, 0xF0, 0x00,
	0x03, 0xFE, 0x7F, 0xF8, 0x1E, 0x0F, 0xFF, 0xFF, 0xFF, 0xFF, 0xE0, 0x00, 0x03, 0x7E, 0x0F, 0xF9, 
	0xBE, 0x05, 0xFF, 0xFF, 0xFF, 0xFF, 0xE0, 0x00, 0x01, 0x7F, 0xC1, 0xF3, 0xFC, 0x05, 0xFF, 0xFF,
	0xFF, 0xFF, 0xE0, 0x00, 0x01, 0x3D, 0xF8, 0x0F, 0x7C, 0x05, 0xFF, 0xFF, 0xFF, 0xFF, 0xE0, 0x00, 
	0x01, 0xBC, 0x7F, 0xFF, 0xF8, 0x02, 0xFF, 0xFF, 0xFF, 0xFF, 0xE0, 0x00, 0x00, 0xBE, 0xFF, 0xFF,
	0xF8, 0x02, 0xFF, 0xFF, 0xFF, 0xFF, 0xC0, 0x00, 0x00, 0x1D, 0xFF, 0xFF, 0xF0, 0x00, 0xFF, 0xFF, 
	0xFF, 0xFF, 0xC0, 0x00, 0x00, 0x0F, 0xF7, 0xFF, 0xE0, 0x00, 0x7F, 0xFF, 0xFF, 0xFF, 0xC0, 0x00,
	0x00, 0x0F, 0xF3, 0xFF, 0xE0, 0x00, 0x7F, 0xFF, 0xFF, 0xFF, 0x80, 0x00, 0x00, 0x03, 0xF3, 0xFF, 
	0xC0, 0x00, 0x7F, 0xFF, 0xFF, 0xFF, 0x80, 0x00, 0x00, 0x01, 0xF7, 0xFF, 0x80, 0x00, 0x3F, 0xFF,
	0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xFF, 0x00, 0x00, 0x3F, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 
	0x00, 0x00, 0x1F, 0xFF, 0x00, 0x20, 0x3F, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x1F, 0xFF,
	0x00, 0x10, 0x3F, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x1F, 0xFF, 0x00, 0x10, 0x3F, 0xFF, 
	0xFF, 0xFC, 0x00, 0x00, 0x02, 0x00, 0x0F, 0xFF, 0x00, 0x00, 0x1F, 0xFF, 0xFF, 0xFC, 0x00, 0x00,
	0x04, 0x00, 0x1F, 0xFE, 0x00, 0x00, 0x1F, 0xFF, 0xFF, 0xF8, 0x00, 0x00, 0x07, 0x81, 0x7F, 0xFE, 
	0x00, 0x00, 0x1F, 0xFF, 0xFF, 0xF8, 0x00, 0x00, 0x03, 0xDF, 0xFF, 0xFE, 0x00, 0x00, 0x1F, 0xFF,
	0xFF, 0xF8, 0x00, 0x00, 0x07, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x1F, 0xFF, 0xFF, 0xF0, 0x00, 0x00, 
	0x07, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x1F, 0xFF, 0xFF, 0xF0, 0x00, 0x40, 0x07, 0xFF, 0xFF, 0xFE,
	0x00, 0x00, 0x0F, 0xFF, 0xFF, 0xF0, 0x00, 0xC0, 0x03, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x0F, 0xFF, 
	0xFF, 0xE0, 0x00, 0xE0, 0x07, 0xFF, 0xFF, 0xFE, 0x81, 0x00, 0x07, 0xFF, 0xFF, 0xC0, 0x01, 0xE0,
	0x07, 0xFF, 0xFF, 0xFE, 0x01, 0x00, 0x07, 0xFF, 0xFF, 0x80, 0x0F, 0xF0, 0x03, 0xFF, 0xFF, 0xFE, 
	0x83, 0x80, 0x03, 0xFF, 0xFF, 0x00, 0x1F, 0xF0, 0x13, 0xFF, 0xFF, 0xFE, 0x03, 0xE0, 0x01, 0xFF,
	0xFC, 0x03, 0x3F, 0xF0, 0x21, 0xFF, 0xFF, 0xFE, 0x03, 0xFC, 0x00, 0x3F, 0xF0, 0x3F, 0x3F, 0xF8, 
	0x3B, 0xFF, 0xFF, 0xFE, 0x03, 0xFE, 0xC0, 0x0F, 0xE3, 0xFB, 0x7F, 0xF8, 0x3B, 0xFF, 0xFF, 0xFF, 
	0x07, 0xFF, 0xFF, 0x07, 0x9F, 0xFB, 0x7F, 0xFC, 0x79, 0xFF, 0xFF, 0xFF, 0x07, 0xFF, 0xFF, 0xFF, 
	0xFF, 0xFF, 0x7F, 0xFC, 0x39, 0xFF, 0xFF, 0xFF, 0x07, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F, 0xFE,
	0x3F, 0xFF, 0xFF, 0xFE, 0x07, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F, 0xFE, 0x1F, 0xFF, 0xFF, 0xFE, 
	0x0F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F, 0xFE, 0x1F, 0x7F, 0xFF, 0xFE, 0x0F, 0xFF, 0xFF, 0xFF, 
	0xFF, 0xFF, 0x7F, 0xFF, 0x1F, 0xFE, 0xFF, 0xFC, 0x0F, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
	0x0F, 0xFF, 0xFF, 0xFF, 0x1F, 0xFF, 0xEF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x87, 0xFF, 0xFF, 0xFE, 
	0x1F, 0xFF, 0xEF, 0xFF, 0xFF, 0xFF, 0xBF, 0xFF, 0x82, 0xFF, 0xFF, 0xFC, 0x3F, 0xFF, 0xFF, 0xFF, 
	0xFF, 0xFF, 0xBF, 0xFF, 0x83, 0xFF, 0xFF, 0xFC, 0x3F, 0xFF, 0xBF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
	0xC1, 0xFF, 0xFF, 0xF8, 0x7F, 0xFF, 0xBF, 0xFF, 0xFF, 0xFF, 0xBF, 0xFF, 0xE0, 0xFF, 0xFF, 0xF0, 
	0xFF, 0xFF, 0xBF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF
    )))
def getMaskData2():
    return _data2


def doOneBitMaskImages(context):
    bitsPerComponent = 1
    bitsPerPixel = 1
    width = 96
    height = 96
    bytesPerRow = 12

    imageDataSize = bytesPerRow*height
    shouldInterpolate = True
    lightBlue = [0.482, 0.62, 0.871, 1.0]
    black = [0.0, 0.0, 0.0, 1.0]
    darkRed = [0.663, 0., 0.031, 1.0]
    darkGreen = [0.404, 0.808, 0.239, 1.0]
    darkBlue = [0.11, 0.208, 0.451, 1.0]
    purple = [0.69, 0.486, 0.722, 1.0]
    darkOrange = [0.965, 0.584, 0.059, 1.0]

    # A decode array contains two elements for each component. In this
    # case, an image mask has one component so the array consists of
    # two values. When using this decode array, a sample value of 0
    # is mapped into the value 1, and the maximum sample value is
    # mapped into the value 0. This inverts the sense of the mask data.
    decode = (1 , 0)
	
    # Create a Quartz data provider for the image data. Because this 
    # data is static data, we don't need to release it so the data 
    # release function is None.
    data = getMaskData1()
    dataProvider = CGDataProviderCreateWithData(None, data, imageDataSize, None)
    if dataProvider is None:
        print >>sys.stderr, "Couldn't create Mask1 Data provider!"
        return
	
    # Create a mask from the data.
    mask1 = CGImageMaskCreate(width, height, bitsPerComponent,
                                    bitsPerPixel, bytesPerRow, dataProvider, 
                                    None, shouldInterpolate)
    # Create the same mask but with a decode array that 
    # inverts the sense of the mask.
    invertedmask1 = CGImageMaskCreate(width, height, 
                                    bitsPerComponent, bitsPerPixel, bytesPerRow, 
                                    dataProvider, decode, shouldInterpolate)
    # Release the data provider now that this code no longer needs it.
    del dataProvider

    if mask1 is None or invertedmask1 is None:
        if mask1 is None:
            print >>sys.stderr, "Couldn't create CGImageRef for the mask data 1!"

        if invertedmask1 is None:
            print >>sys.stderr, "Couldn't create CGImageRef for the inverted mask data 1!"
        return

    # Get the pointer to the data for the second mask.
    data = getMaskData2()
    dataProvider = CGDataProviderCreateWithData(None, data, imageDataSize, None)
    if dataProvider is None:
        print >>sys.stderr, "Couldn't create Mask2 Data provider!"
        return
    
    mask2 = CGImageMaskCreate(width, height, bitsPerComponent,
                                bitsPerPixel, bytesPerRow, dataProvider, 
                                None, shouldInterpolate)
    # Create the same mask but with a decode array that 
    # inverts the sense of the mask.
    invertedmask2 = CGImageMaskCreate(width, height, 
                                    bitsPerComponent, bitsPerPixel, bytesPerRow, 
                                    dataProvider, decode, shouldInterpolate)
    # Release the data provider now that this code no longer needs it.
    del dataProvider
    if mask2 is None or invertedmask2 is None:
        if mask2 is None:
            print >>sys.stderr, "Couldn't create CGImageRef for the mask data 2!"

        if invertedmask2 is None:
            print >>sys.stderr, "Couldn't create CGImageRef for the inverted mask data 2!"

        return
    
    CGContextScaleCTM(context, 1.5, 1.5)
    colorSpace = Utilities.getTheCalibratedRGBColorSpace()
    CGContextSetFillColorSpace(context, colorSpace);	
    
    # Set the fill color to a light blue.
    CGContextSetFillColor(context, lightBlue)
    # Paint part of the background.
    backRect = CGRectMake(width/2, height/2, width*3, height)
    CGContextFillRect(context, backRect)
    
    imageRect = CGRectMake(0., height, width, height)
    CGContextSaveGState(context)
    # Set the fill color to opaque black.
    CGContextSetFillColor(context, black)
    # Mask 1.
    CGContextDrawImage(context, imageRect, mask1)
    
    CGContextTranslateCTM(context, width, 0)
    # Set the fill color to opaque red.
    CGContextSetFillColor(context, darkRed);			
    # Mask 2.
    CGContextDrawImage(context, imageRect, mask2)
    CGContextTranslateCTM(context, width, 0)
    # Set the fill color to dark orange.
    CGContextSetFillColor(context, darkOrange)
    # Mask 3.
    CGContextDrawImage(context, imageRect, mask1)

    CGContextTranslateCTM(context, width, 0)
    # Make the orange 50% transparent.
    darkOrange[3] = 0.5
    CGContextSetFillColor(context, darkOrange)
    # Mask 4.
    CGContextDrawImage(context, imageRect, mask2)
    CGContextRestoreGState(context)
    
    # Translate down the page. The cast is necessary
    # since height is typed as size_t which is unsigned.
    CGContextTranslateCTM(context, 0, -height)
    
    # Set the fill color to an opaque green.
    CGContextSetFillColor(context, darkGreen)
    # Mask 5.
    CGContextDrawImage(context, imageRect, invertedmask2)
    
    CGContextTranslateCTM(context, width, 0)
    # Set the fill color to a dark blue.
    CGContextSetFillColor(context, darkBlue)
    # Mask 6.
    CGContextDrawImage(context, imageRect, invertedmask1)
    CGContextTranslateCTM(context, width, 0)
    # Set the fill color to purple.
    CGContextSetFillColor(context, purple)
    # Mask 7.
    CGContextDrawImage(context, imageRect, invertedmask2)
    CGContextTranslateCTM(context, width, 0)
    
    # Make the purple 50% transparent.
    purple[3] = 0.5
    CGContextSetFillColor(context, purple)
    # Mask 8.
    CGContextDrawImage(context, imageRect, invertedmask1)

def doMaskImageWithMaskFromURL(context, imageURL, 
        imagewidth, imageheight, bitsPerComponent, 
        theMaskingImageURL, maskwidth, maskheight):

    imageBitsPerPixel = bitsPerComponent * 3
    bytesPerRow = ((imagewidth * imageBitsPerPixel) + 7)/8
    shouldInterpolate = True
    imageDataProvider = CGDataProviderCreateWithURL(imageURL)
    if imageDataProvider is None:
        print >>sys.stderr,  "Couldn't create Image Data provider!"
        return

    colorspace = Utilities.getTheCalibratedRGBColorSpace()
    image = CGImageCreate(imagewidth, imageheight, bitsPerComponent,
                            imageBitsPerPixel, bytesPerRow, colorspace,
                            kCGImageAlphaNone, imageDataProvider, 
                            None, shouldInterpolate,
                            kCGRenderingIntentDefault)
    del imageDataProvider
    if image is None:
        print >>sys.stderr, "Couldn't create CGImageRef for this data!"
        return
    
    imageRect = CGRectMake(0.0,imageheight, imagewidth, imageheight)
    # Draw the image.
    CGContextDrawImage(context, imageRect, image)
    
    # Now the mask.
    maskDataProvider = CGDataProviderCreateWithURL(theMaskingImageURL)
    if maskDataProvider is None:
        print >>sys.stderr, "Couldn't create Image Data provider!"
        return
    
    mask = CGImageMaskCreate(maskwidth, maskheight, bitsPerComponent,
                            bitsPerComponent, maskwidth,
                            maskDataProvider, None, shouldInterpolate)
    del maskDataProvider
    if mask is None:
        print >>sys.stderr, "Couldn't create CGImageRef for mask data!"
        return
    
    # Draw the mask below the image. The current fill color (black)
    # is painted through the mask.
    maskRect = CGRectMake(0.0, 0.0, maskwidth, maskheight)
    CGContextDrawImage(context, maskRect, mask)
    
    # Create a new CGImage object, the image, masked with mask.
    imageMaskedWithImage = CGImageCreateWithMask(image, mask)
    # Once the new image is created, the code can release the image
    # and the mask which make it up. Quartz retains what it needs
    # for the new masked image 'imageMaskedWithImage'.
    del image
    del mask
    if imageMaskedWithImage is None:
        print >>sys.stderr, "Couldn't create image masked with mask!"
        return
    
    imageRect = CGRectMake(imagewidth + 10, imageheight/2, imagewidth, imageheight)
    # Draw the masked image to the right of the image and its mask.
    CGContextDrawImage(context, imageRect, imageMaskedWithImage)

def doMaskImageWithGrayImageFromURL(context, imageURL, imagewidth, imageheight, bitsPerComponent, 
        theMaskingImageURL, maskwidth, maskheight):

    imageBitsPerPixel = bitsPerComponent * 3
    bytesPerRow = ( (imagewidth * imageBitsPerPixel) + 7)/8
    shouldInterpolate = True

    imageDataProvider = CGDataProviderCreateWithURL(imageURL)
    if imageDataProvider is None:
        print >>sys.stderr, "Couldn't create Image Data provider!"
        return

    colorspace = Utilities.getTheCalibratedRGBColorSpace()
    image = CGImageCreate(imagewidth, imageheight, bitsPerComponent,
                            imageBitsPerPixel, bytesPerRow, colorspace,
                            kCGImageAlphaNone, imageDataProvider, 
                            None, shouldInterpolate,
                            kCGRenderingIntentDefault)
    del imageDataProvider
    if image is None:
        print >>sys.stderr, "Couldn't create CGImageRef for this data!"
        return

    imageRect = CGRectMake(0.,imageheight, imagewidth, imageheight)
    # Draw the image.
    CGContextDrawImage(context, imageRect, image)
	
    # Now the mask.
    maskDataProvider = CGDataProviderCreateWithURL(theMaskingImageURL)
    if maskDataProvider is None:
        print >>sys.stderr, "Couldn't create Image Data provider!"
        return

    # The color space for the image MUST be DeviceGray for it to   
    # be used as a masking image with CGImageCreateWithMask.
    deviceGraySpace = CGColorSpaceCreateDeviceGray();   
    mask = CGImageCreate(maskwidth, maskheight, bitsPerComponent, 
                            bitsPerComponent, maskwidth, 
                            deviceGraySpace, 
                            kCGImageAlphaNone, maskDataProvider, 
                            None, shouldInterpolate, 
                            kCGRenderingIntentDefault)
    # Release the color space since it is no longer needed.
    del deviceGraySpace
    del maskDataProvider

    if mask is None:
        print >>sys.stderr, "Couldn't create CGImageRef for gray image data!"
        return
	
    # Draw the mask below the image. The current fill color (black)
    # is painted through the mask.
    maskRect = CGRectMake(0., 0., maskwidth, maskheight)
    CGContextDrawImage(context, maskRect, mask)
	
    # Create a new CGImage object, the image, masked with mask.
    imageMaskedWithImage = CGImageCreateWithMask(image, mask)
	
    # Once the new image is created, the code can release the image
    # and the mask which make it up. Quartz retains what it needs
    # for the new masked image 'imageMaskedWithImage'.
    del image
    del mask

    if imageMaskedWithImage is None:
        print >>sys.stderr, "Couldn't create image masked with mask!"
        return

    imageRect = CGRectMake(imagewidth + 10, imageheight/2, 
                                                    imagewidth, imageheight)
    # Draw the masked image to the right of the image and its mask.
    CGContextDrawImage(context, imageRect, imageMaskedWithImage)
    # Be sure and release the masked image.
    del imageMaskedWithImage

def doMaskImageWithColorFromURL(context, url,
        width, height, isColor):

    # This routine treats color images as RGB.
    bitsPerComponent = 8
    if isColor:
        bitsPerPixel = bitsPerComponent * 3
    else:
        bitsPerPixel = bitsPerComponent

    bytesPerRow = ( (width * bitsPerPixel) + 7)/8
    shouldInterpolate = True

    # This is a range of dark gray to black colors for an 8 bit per component
    # image in a gray or RGB color space. The entries are image sample 
    # values of 0-0x1F for the first color component, 0-0x1F for the 
    # second color component, and so on. For image sample values where 
    # all components fall within the ranges in maskingColors, the sample 
    # value is masked and therefore unpainted.
    maskingColors = (0x00, 0x1F, 0x00, 0x1F, 0x00, 0x1F)
    backColor = (1., 0., 0., 1.) # Opaque red.

    # Create a Quartz data provider from the supplied URL.	 
    dataProvider = CGDataProviderCreateWithURL(url)
    if dataProvider is None:
        print >>sys.stderr, "Couldn't create Image data provider!"
        return

    # Create an image of the specified width, height and bits per pixel
    # from the URL.
    if isColor:
        colorspace = Utilities.getTheCalibratedRGBColorSpace()
    else:
        colorspace = Utilities.getTheCalibratedGrayColorSpace()

    image = CGImageCreate(width, height, bitsPerComponent, bitsPerPixel,
                                    bytesPerRow, colorspace, kCGImageAlphaNone,
                                    dataProvider, None, shouldInterpolate, 
                                    kCGRenderingIntentDefault)
    del dataProvider
    if image is None:
        print >>sys.stderr, "Couldn't create CGImageRef for this data!"
        return
	
    imageRect = CGRectMake(10., 10., width, height)
    #CGContextScaleCTM(context, 0.33, 0.33)
    # Set the color space and the color, then 
    # paint a red rectangle behind the image.
    CGContextSetFillColorSpace(context, colorspace)
    CGContextSetFillColor(context, backColor)
    CGContextFillRect(context, imageRect)
    # Draw the image into the rectangle.
    CGContextDrawImage(context, imageRect, image)
    # Create a new image from the original one, masking out a range
    # of the blackest sample values.
    imageMaskedWithColor = CGImageCreateWithMaskingColors(image, maskingColors)
    # Release the original image; it is no longer needed.
    del image
    if imageMaskedWithColor is None:
        print >>sys.stderr, "Couldn't create CGImageRef for masking color!"
        return
	
    # Paint the rectangle behind the next image with red.
    imageRect = CGRectMake(30. + width, 10., width, height)
    CGContextFillRect(context, imageRect)
    # Draw the image. Image sample values in the range of
    # the masking color are unpainted, allowing the background
    # to show through.
    CGContextDrawImage(context, imageRect, imageMaskedWithColor)
	

if 1:	# Set to 1 for code in the book.

    def drawWithClippingMask(context, theMaskingImageURL, imagewidth, imageheight):
        # An array of CGColor objects.
        colors = ( Utilities.getRGBOpaqueDarkGreenColor(), Utilities.getRGBOpaqueDarkBlueColor(),  
                Utilities.getRGBOpaqueBlueColor(), Utilities.getRGBOpaqueRedColor() )

        imageBitsPerComponent = 8
        bytesPerRow = imagewidth
        shouldInterpolate = True
        decode = (1, 0)
        
        # Create the data.
        dataProvider =  CGDataProviderCreateWithURL(theMaskingImageURL)
        if dataProvider is None:
            print >>sys.stderr, "Couldn't create Image data provider!"
            return

        cs = CGColorSpaceCreateDeviceGray()
        image = CGImageCreate(imagewidth, imageheight, 
                        imageBitsPerComponent, imageBitsPerComponent, 
                        bytesPerRow, cs, kCGImageAlphaNone, dataProvider, decode, 
                        shouldInterpolate, kCGRenderingIntentDefault)
        del cs
        del dataProvider

        if image is None:
            print >>sys.stderr, "Couldn't create Image!"
            return
        
        imageRect = CGRectMake(0, 0, imagewidth*2/3, imageheight*2/3)

        # Position for drawing the image at the left side of the figure.
        CGContextTranslateCTM(context, 50, 50 )

        # Draw the image.
        CGContextDrawImage(context, imageRect, image)

        # Position to the right of the image just painted.
        CGContextTranslateCTM(context, CGRectGetWidth(imageRect) + 25,  0)

        # Clip to the image.
        CGContextClipToMask(context, imageRect, image)
        # Release the image since this code no longer needs it.
        del image

        # Make a rect that has a width and height 1/3 that of the image.
        rect = CGRectMake(0, 0, CGRectGetWidth(imageRect)/3, CGRectGetHeight(imageRect)/3)

        CGContextTranslateCTM(context, 0, 2*CGRectGetHeight(rect))
        
        # Draw a 3 x 3 grid of rectangles, setting the color for each rectangle
        # by cycling through the array of CGColor objects in the 'colors' array.
        for j in range(3):
            CGContextSaveGState(context)
            for i in range(3):
                # Draw a row of rectangles.
                # Set the fill color using one of the CGColor objects in the 
                # colors array.	    
                CGContextSetFillColorWithColor(context, colors[(i+j) % 4])
                CGContextFillRect(context, rect)
                CGContextTranslateCTM(context, CGRectGetWidth(rect), 0)

            CGContextRestoreGState(context)
            # Position to draw the next row.
            CGContextTranslateCTM(context, 0, -CGRectGetHeight(rect))

else:
    # This code works just fine to screen but when drawing to a PDF 
    # or printing context the masked drawing is completely masked out 
    # due to a bug in Quartz prior to Tiger 10.4.3.
    def drawWithClippingMask(context, theMaskingImageURL, maskwidth, maskheight):
        # An array of CGColor objects.
        colors = (
                Utilities.getRGBOpaqueDarkGreenColor(), 
                Utilities.getRGBOpaqueDarkBlueColor(),  
                Utilities.getRGBOpaqueBlueColor(), 
		Utilities.getRGBOpaqueRedColor())
        maskBitsPerComponent = 8
        bytesPerRow = ( (maskwidth * maskBitsPerComponent) + 7)/8
        shouldInterpolate = True
        maskDataProvider = CGDataProviderCreateWithURL(theMaskingImageURL)
    
        if maskDataProvider is None:
            print >>sys.stderr, "Couldn't create Image Mask provider!"
	    return
        mask = CGImageMaskCreate(maskwidth, maskheight, maskBitsPerComponent,
                                        maskBitsPerComponent, maskwidth,
                                        maskDataProvider, None, shouldInterpolate)
        del maskDataProvider

        if mask is None:
            print >>sys.stderr, "Couldn't create Image Mask!"
            return

        maskRect = CGRectMake(0, 0, maskwidth/3, maskheight/3)

        # Position for drawing the mask at the left side of the figure.
        CGContextTranslateCTM(context, 50, 50 )
        # Set the context fill color to a CGColor object that is black.
        CGContextSetFillColorWithColor(context, getRGBOpaqueBlackColor())
        # Draw the mask. It is painted with with the black fill color.
        CGContextDrawImage(context, maskRect, mask)

        # Position to the right of the mask just painted.
        CGContextTranslateCTM(context, CGRectGetWidth(maskRect) + 25,  0)

        # Clip to the mask.
        CGContextClipToMask(context, maskRect, mask)
        # Release the mask since this code no longer needs it.
        del mask

        # Make a rect that has a width and height 1/3 that of the image mask.
        rect = CGRectMake(0, 0, CGRectGetWidth(maskRect)/3, CGRectGetHeight(maskRect)/3)

        CGContextTranslateCTM(context, 0, 2*CGRectGetHeight(rect))
        
        # Draw a 3 x 3 grid of rectangles, setting the color for each rectangle
        # by cycling through the array of CGColor objects in the 'colors' array.
        for j in range(3):
            CGContextSaveGState(context)
            for i in range(3):
                # Draw a row of rectangles.
                # Set the fill color using one of the CGColor objects in the 
                # colors array.	    
                CGContextSetFillColorWithColor(context, colors[(i+j) % 4])
                CGContextFillRect(context, rect)
                CGContextTranslateCTM(context, CGRectGetWidth(rect), 0)
            CGContextRestoreGState(context)
            # Position to draw the next row.
            CGContextTranslateCTM(context, 0, -CGRectGetHeight(rect))
