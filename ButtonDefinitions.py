import os

import matplotlib.pyplot as plt
import numpy as np
import csv
import math
import cv2
import matplotlib.font_manager as fm

#calculating the error of algorithm comparison

def mse(imageA, imageB):
    '''the 'Mean Squared Error' between the two images is the sum of the squared
        difference between the two images; NOTE: the two images must have the
        same dimension'''
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    #return mse, the lower the error, the more similar the images are
    return err

def psnr(imageA, imageB):
    m = mse(imageA, imageB)
    if m == 0:
        return 100

    PIXEL_MAX = 255.0
    return 20*math.log10(PIXEL_MAX / math.sqrt(m))
    

def compare_images(imageA, imageB, stego_type, enc_type):
    # computing mean squared error
    m = mse(imageA, imageB)
#    if stego_type == "DCT":
#        m /= 100
    print("Mean Square Error for", stego_type, enc_type, "is", m)
    
    # computing peak signal to noise ratio
    p = psnr(imageA, imageB)
    print("Peak Signal to Noise Ratio for", stego_type, enc_type, "is", p)
    #update value in csv file for plotting
    flag = 0
    with open("secret/AlgoAnalysis.csv", 'r+') as varfile:
        read_object = csv.reader(varfile)
        titles = next(read_object)
        

        for row in read_object:
            if len(row) > 0:
                print(row)
                if row[0] == stego_type and row[1] == enc_type:
                    print("Entered")
                    row[2] = ((float(row[2]) + m)/2)
                    row[3] = ((float(row[3]) + p)/2)
                    flag = 1

        if flag == 0:
            write_object = csv.writer(varfile)

            write_object.writerow([stego_type, enc_type, m, p])

def analyse_mse():
    x_axis = ['t']
    y_axis = [0]
    #y1_axis = []

    with open("secret/AlgoAnalysis.csv", 'r') as varfile:
        read_object = csv.reader(varfile)
        titles = next(read_object)
        
        i = 0
        left = [0]
        for row in read_object:
            #print(row[0], row[1])
            if len(row) > 0:
                string = row[0] + " &\n" + row[1]
                if string not in x_axis and string != " &\n":
                    x_axis.append(string)
                    y_axis.append(row[2])
                    left.append(i)
                    i += 1
                #y1_axis.append(row[3])

    #x_axis = []
    #y_axis = []
    #j = 0
    #for i in y1_axis:
    #    if i != '':
    #        x_axis.append(x1_axis[j])
    #        y_axis.append(i)
    #        j += 1

    print(x_axis, y_axis)
    plt.xlabel("Technique used", fontsize = 16)
    plt.ylabel("Mean Square Error", fontsize = 16)
    plt.title("Algorithm Comparison using MSE", fontsize = 20)
    plt.xticks(size = 16, rotation = 90)
    plt.yticks(size = 16, rotation = 0)
#    plt.plot(x_axis, y_axis, color='green', linestyle='dashed', linewidth = 3, 
#         marker='o', markerfacecolor='blue', markersize=12)
    plt.bar(left, y_axis, tick_label = x_axis, width = 0.5, color = ['red', 'green',
                                                                     'blue'], )
    plt.ylim(ymin = 0)
    plt.show()

'''
    fig = plt.figure("Algorithm Comparison")
    plt.title("Algorithm Comparison")

    plot1 = fig.add_subplot(1, 2, 1)
    plot1.plot(x_axis, y_axis, color = 'r')
    #plot1.xlabel("Technique used")
    #plot1.ylabel("Average Mean Square Error")
    
    plot1 = fig.add_subplot(1, 2, 2)
    plot1.plot(x_axis, y_axis, color = 'b')
    #plot1.xlabel("Technique used")
    #plot1.ylabel("Average Peak Signal to Noise Ratio")
'''
    


def analyse_psnr():
    x_axis = ['t']
    y_axis = [0]
    
    with open("secret/AlgoAnalysis.csv", 'r') as varfile:
        read_object = csv.reader(varfile)
        titles = next(read_object)
        
        i = 0
        left = [0]
        for row in read_object:
            #print(row[0], row[1])
            if len(row) > 0:
                string = row[0] + " &\n" + row[1]
                if string not in x_axis and string != " &\n":
                    x_axis.append(string)
                    y_axis.append(row[3])
                    left.append(i)
                    i += 1

    #font = fm.FontProperties(size = 20)

    print(x_axis, y_axis)
    plt.xlabel("Technique used", fontsize = 16)
    plt.ylabel("Peak Signal to Noise Ratio", fontsize = 16)
    plt.title("Algorithm Comparison using PSNR", fontsize = 20)
    plt.xticks(size = 16, rotation = 90)
    plt.yticks(size = 16)
    #plt.plot(x_axis, y_axis, color='red', linestyle='dashed', linewidth = 3, 
    #     marker='o', markerfacecolor='blue', markersize=12)
    plt.bar(left, y_axis, tick_label = x_axis, width = 0.5, color = ['red', 'green',
                                                                     'blue'], )
    plt.ylim(ymin = 0)
    plt.show()

def analyse_strings():
    x_axis = ['t']
    y_axis = [0]
    
    with open("secret/StringAnalysis.csv", 'r') as varfile:
        read_object = csv.reader(varfile)
        titles = next(read_object)
        
        i = 0
        left = [0]
        for row in read_object:
            #print(row[0], row[1])
            if len(row) > 0:
                string = row[0] + " &\n" + row[1]
                if string not in x_axis and string != " &\n":
                    x_axis.append(string)
                    y_axis.append(row[2])
                    left.append(i)
                    i += 1

    print(x_axis, y_axis)
    plt.xlabel("Technique used", fontsize = 16)
    plt.ylabel("Original and Derived String Percentage Comparison", fontsize = 16)
    plt.title("Algorithm Comparison using String Comparion", fontsize = 20)
    plt.xticks(size = 16, rotation = 90)
    plt.yticks(size = 16)
    #plt.plot(x_axis, y_axis, color='red', linestyle='dashed', linewidth = 3, 
    #     marker='o', markerfacecolor='blue', markersize=12)
    plt.bar(left, y_axis, tick_label = x_axis, width = 0.5, color = ['red', 'green',
                                                                     'blue'], )
    plt.ylim(ymin = 0)
    plt.show()
