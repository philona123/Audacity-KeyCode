# importing pycairo
import cairo

length = 916
width = 902
# creating a SVG surface
# here geek95 is file name & 700, 700 is dimension
with cairo.SVGSurface("plane.svg", length, width) as surface:
 
    # creating a cairo context object for SVG surface
    # using Context method
    context = cairo.Context(surface)
 
    # setting color of the context
    context.set_source_rgb(0, 0, 0)
    # creating a rectangle
    context.rectangle(0, 0, length, width)
 
    # Fill the color inside the rectangle
    context.fill()

    # printing message when file is saved
    print("File Saved")