from scipy import misc      # Import misc 
import matplotlib.pyplot as plt

def main():
    #         Get the filename as string
    fn = str(raw_input("File : "))

    #         Read file it np array
    im = misc.imread(fn) 
   
    #         Display with grayscale colour map 
    plt.imshow(im,cmap=plt.cm.gray)

    #         Show the image
    plt.show()

main()
