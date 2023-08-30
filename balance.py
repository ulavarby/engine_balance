#! /usr/bin/env python3

# a1 - alpha relise
# 

'''Script for calculation of engine balance.
   The calculation is valid for single-row engines and V-engines with
   the same number of cylinders in the left and right banks.
'''

import math
import csv
import yaml
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time

def forses(P1, P2):
    """Reciprocating Forces.
       Calculate Primary and Secondary Reciprocating Forces.
    """
    i, p1l, p2l, p1r, p2r = 0, 0, 0, 0, 0
    if Rows == 1: # number of rows of cylinders = 1
        for i in range(Cyl_in_row):
            p1l += math.cos(math.radians(a + geometry_angles_l[i]))
            p1r = 0
            p2l += math.cos(2 * math.radians(a + geometry_angles_l[i]))
            p2r = 0
    else: # number of rows of cylinders = 2
        for i in range(Cyl_in_row):
            p1l += math.cos(math.radians(a + geometry_angles_l[i]))
            p1r += math.cos(math.radians(a + geometry_angles_r[i] - Y))
            p2l += math.cos(2 * math.radians(a + geometry_angles_l[i]))
            p2r += math.cos(2 * math.radians(a + geometry_angles_r[i] - Y))
#            print(p1l, p1r, p2l, p2r)
    P1x = mrcp * R * Omega**2 * (p1l + math.cos(math.radians(Y)) * p1r)
    P1y = mrcp * R * Omega**2 * math.sin(math.radians(Y)) * p1r
    P1 = round(math.sqrt(P1x**2 + P1y**2), 2)
    P2x = mrcp * R * Omega**2 * Q * (p2l + math.cos(math.radians(Y)) * p2r)
    P2y = mrcp * R * Omega**2 * Q * math.sin(math.radians(Y)) * p2r
    P2 = round(math.sqrt(P2x**2 + P2y**2), 2)
#    print(str('\n'), 'P1x =', P1x, '  P1y =', P1y, '  P1 =', P1)
#    print(str('\n'), 'P2x =', P2x, '  P2y =', P2y, '  P2 =', P2)
    return P1, P2

def moments(M1, M2):
    """Reciprocating Moments.
       Calculate Primary and Secondary Reciprocating Moments.
    """
    i, m1l, m2l, m1r, m2r = 0, 0, 0, 0, 0
    if Rows == 1: # number of rows of cylinders = 1
        for i in range(Cyl_in_row):
            m1l += (geometry_dists_l[i]) * (math.cos(math.radians(a + geometry_angles_l[i])))
            m1r = 0
            m2l += (geometry_dists_l[i]) * (math.cos(2 * math.radians(a + geometry_angles_l[i])))
            m2r = 0
#            print(m1l, m1r, m2l, m2r)
    else: # number of rows of cylinders = 2
        for i in range(Cyl_in_row):
            m1l += (geometry_dists_l[i]) * (math.cos(math.radians(a + geometry_angles_l[i])))
            m1r += (geometry_dists_r[i]) * (math.cos(math.radians(a + geometry_angles_r[i] - Y)))
            m2l += (geometry_dists_l[i]) * (math.cos(2 * math.radians(a + geometry_angles_l[i])))
            m2r += (geometry_dists_r[i]) * (math.cos(2 * math.radians(a + geometry_angles_r[i] - Y)))
#            print(m1l, m1r, m2l, m2r)
    M1x = -(mrcp * R * Omega**2 * math.sin(math.radians(Y)) * m1r)
    M1y = mrcp * R * Omega**2 * (m1l + math.cos(math.radians(Y)) * m1r)
    M1 = round(math.sqrt(M1x**2 + M1y**2), 2)
    M2x = -(mrcp * R * Omega**2 * Q * math.sin(math.radians(Y)) * m2r)
    M2y = mrcp * R * Omega**2 * Q * (m2l + math.cos(math.radians(Y)) * m2r)
    M2 = round(math.sqrt(M2x**2 + M2y**2), 2)
#    print(str('\n'), 'M1x =', M1x, '  M1y =', M1y, '  M1 =', M1)
#    print(str('\n'), 'M2x =', M2x, '  M2y =', M2y, '  M2 =', M2)
    return M1, M2

def rots(Krot,Mrot):
    """Centrifugal Forces and Moments.
       Calculate Centrifugal Forces and Moments.
    """
    i, kx, ky, mx, my = 0, 0, 0, 0, 0
    if Rows == 1 or geometry_angles_l == geometry_angles_r: # one crank for one (1 row) or two (2 row) ciliders
        for i in range(Cyl_in_row):
            kx += math.cos(math.radians(a + geometry_angles_l[i]))
            ky += math.sin(math.radians(a + geometry_angles_l[i]))
            mx += (geometry_dists_l[i]) * (math.sin(math.radians(a + geometry_angles_l[i])))
            my += (geometry_dists_l[i]) * (math.cos(math.radians(a + geometry_angles_l[i])))
    elif Rows == 2 and geometry_angles_l != geometry_angles_r: # own crank for each cylinder
        for i in range(Cyl_in_row):
            kx += (math.cos(math.radians(a + geometry_angles_l[i])) + math.cos(math.radians(a + geometry_angles_r[i])))
            ky += (math.sin(math.radians(a + geometry_angles_l[i])) + math.sin(math.radians(a + geometry_angles_r[i])))
            mx += (geometry_dists_l[i]) * (math.sin(math.radians(a + geometry_angles_l[i]))) + (geometry_dists_r[i]) * (math.sin(math.radians(a + geometry_angles_r[i])))
            my += (geometry_dists_l[i]) * (math.cos(math.radians(a + geometry_angles_l[i]))) + (geometry_dists_r[i]) * (math.cos(math.radians(a + geometry_angles_r[i])))
#    print(a, kx, ky)
    Kx = mrot * R * Omega**2 * kx
    Ky = mrot * R * Omega**2 * ky
    Krot = round(math.sqrt(Kx**2 + Ky**2), 2)
    Mx = -(mrot * R * Omega**2 * mx)
    My = mrot * R * Omega**2 * my
    Mrot = round(math.sqrt(Mx**2 + My**2), 2)
    return Krot,Mrot

def aggregation():
    """ Results aggregation
    """
    A_values = []
    P1_values = []
    P2_values = []
    Krot_values = []
    M1_values = []
    M2_values = []
    Mrot_values = []

    with open(config + '/' + config + '.v' +  str(j)  + '.csv','r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        next(lines, None)  # skip the headers
        for row in lines:
            A_values.append(int(row[0]))
            P1_values.append(float(row[1]))
            P2_values.append(float(row[2]))
            Krot_values.append(float(row[3]))
            M1_values.append(float(row[4]))
            M2_values.append(float(row[5]))
            Mrot_values.append(float(row[6]))
    return A_values,P1_values,P2_values,Krot_values,M1_values,M2_values,Mrot_values

def max_values():
    """Maximum values of Forces and Moments.
    """
    P1_max_value = max(P1_values, key=abs)
    P2_max_value = max(P2_values, key=abs)
    Krot_max_value = max(Krot_values, key=abs)
    M1_max_value = max(M1_values, key=abs)
    M2_max_value = max(M2_values, key=abs)
    Mrot_max_value = max(Mrot_values, key=abs)
    return P1_max_value,P2_max_value,Krot_max_value,M1_max_value,M2_max_value,Mrot_max_value

def visualization():
    """Results visualization.
    """
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3, figsize=(15, 8))
    
    ax1.plot(A_values, P1_values, color='indigo', linestyle='-', marker='.', markevery=30)
    ax1.set_xlim(0,360)
    ax1.set_xlabel('crank rotation angle, [°]')
    ax1.set_ylabel('P1, [N]')
    ax1.set_title('1st order forse')
    ax1.grid(True)
    plt.text(0.1, 0.93, 'max P1 value = ' + str(P1_max_value),\
             transform=ax1.transAxes, fontsize=8, va='bottom')
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(90))
    
    ax2.plot(A_values, P2_values, color='darkblue', linestyle='-', marker='.', markevery=30)
    ax2.set_xlim(0,360)
    ax2.set_xlabel('crank rotation angle, [°]')
    ax2.set_ylabel('P2, [N]')
    ax2.set_title('2nd order forse', color='k')
    ax2.grid(True)
    plt.text(0.1, 0.93, 'max P2 value = ' + str(P2_max_value),\
             transform=ax2.transAxes, fontsize=8, va='bottom')
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(90))
    
    ax3.plot(A_values, Krot_values, color='lime', linestyle='-', marker='.', markevery=30)
    ax3.set_xlim(0,360)
    ax3.set_xlabel('crank rotation angle, [°]')
    ax3.set_ylabel('Krot, [N]')
    ax3.set_title('centrifugal force')
    ax3.grid(True)
    plt.text(0.1, 0.93, 'max Krot value = ' + str(Krot_max_value),\
             transform=ax3.transAxes, fontsize=8, va='bottom')
    ax3.xaxis.set_major_locator(ticker.MultipleLocator(90))
    
    ax4.plot(A_values, M1_values, color='red', linestyle='-', marker='.', markevery=30)
    ax4.set_xlim(0,360)
    ax4.set_xlabel('crank rotation angle, [°]')
    ax4.set_ylabel('M1, [Nm]')
    ax4.set_title('1st order moment')
    ax4.grid(True)
    plt.text(0.1, 0.93, 'max M1 value = ' + str(M1_max_value),\
             transform=ax4.transAxes, fontsize=8, va='bottom')
    ax4.xaxis.set_major_locator(ticker.MultipleLocator(90))
    
    ax5.plot(A_values, M2_values, color='maroon', linestyle='-', marker='.', markevery=30)
    ax5.set_xlim(0,360)
    ax5.set_xlabel('crank rotation angle, [°]')
    ax5.set_ylabel('M2, [Nm]')
    ax5.set_title('2nd order moment')
    ax5.grid(True)
    plt.text(0.1, 0.93, 'max M2 value = ' + str(M2_max_value),\
             transform=ax5.transAxes, fontsize=8, va='bottom')
    ax5.xaxis.set_major_locator(ticker.MultipleLocator(90))
    #plt.legend ()
    
    ax6.plot(A_values, Mrot_values, color='darkgreen', linestyle='-', marker='.', markevery=30)
    ax6.set_xlim(0,360)
    ax6.set_xlabel('crank rotation angle, [°]')
    ax6.set_ylabel('Mrot, [Nm]')
    ax6.set_title('centrifugal moment')
    ax6.grid(True)
    plt.text(0.1, 0.93, 'max Mrot value = ' + str(Mrot_max_value),\
             transform=ax6.transAxes, fontsize=8, va='bottom')
    ax6.xaxis.set_major_locator(ticker.MultipleLocator(90))

    fig.tight_layout(pad=3.0)
    fig.suptitle('Forses, Moments', fontsize='large') 
    fig.savefig(config + '/' + config  + '.v' + str(j) + '.png')
#    plt.show()

# start program

# read engine configuration from config file
config = input('Enter the name of the config with the data from\
 "mechanics.config.yaml" file \n for the calculation:\n')

with open('mechanics.config.yaml', 'r') as yamlfile:
    allnames = yaml.safe_load(yamlfile)

    while (True):
        if config in allnames:
            break
        else:
            print ('\nGiven config name \"' + '\033[1;31m'\
                           + config + '\033[0m' +'\" not exist in file'\
                           ' \"mechanics.config.yaml\".\nAllowed names: ', *allnames.keys())
            config = input('Enter the allowed name :\n')

# mesure time for test only
start_time = time.time()
        
if not os.path.isdir(config):
    os.makedirs(config)
    print("\nDirectory '%s' created" %config)
    
with open(config + '/' + config + '.maximums.txt', 'w') as max_file:
    max_file.write('Pivot table\n\n')
    max_file.write('Maximum values of calculated results for each variant of\n')
    max_file.write('axial positions of the crankshaft journals.\n')
    max_file.write('Engine configuration: ' + config + '\n\n\n')
    max_file.write("{: >7} | {: >9} | {: >9} | {: >9} | {: >9} | {: >9} | {: >9}\n".format('journal', 'max P1', 'max P2', 'max Krot', 'max M1', 'max M2', 'max Mrot'))
    max_file.write(' ==============================================================================\n')

with open('mechanics.config.yaml', 'r') as f:

    # load of engine configuration
    mech = yaml.safe_load(f)[config]

count1 = len(mech['journals'])

for j in range(0, count1, 1):

    with open(config + '/' + config  + '.v' + str(j) + '.csv', 'w') as result_file:
        headwrite = csv.writer(result_file)
        headwrite.writerow(['a','P1','P2','Krot','M1','M2', 'Mrot'])

    # mass of reciprocating parts
    mrcp = float(mech['mrcp'])

    # mass of rotating parts
    mrot = float(mech['mrot'])

    # connecting rod length
    L = float(mech['L'])

    # crank radius
    R = float(mech['R'])

    # angular velocity
    Omega = float(mech['Omega'])

    # number of rows of cylinders
    Rows = int(mech['Rows'])

    # angle between the two banks of cylinders
    Y = float(mech['Y'])

    # angles between the first and subsequent crankpins of the left row
    geometry_angles_l = list(map(float, mech['journals']['journal'+str(j)]['geometry_angles_l']\
                             .split(',')))

    # angles between the first and subsequent crankpins of the right row
    geometry_angles_r = list(map(float, mech['journals']['journal'+str(j)]['geometry_angles_r']\
                             .split(',')))

    # distances between the first connecting rod and subsequent ones
    # on the crankshaft journals of the left row
    geometry_dists_l = list(map(float, mech['journals']['journal'+str(j)]['geometry_dists_l']\
                            .split(',')))

    # distances between the first connecting rod and subsequent ones
    # on the crankshaft journals of the right row
    geometry_dists_r = list(map(float, mech['journals']['journal'+str(j)]['geometry_dists_r']\
                            .split(',')))

    # number of cylinders in a row
    Cyl_in_row = len(geometry_angles_l)

    # total number of cyliders
    N = int(Cyl_in_row * Rows)

    # coefficient lambda
    Q = R / L 

    for a in range(0, 360, 1): # angle of crank rotation
        P1,P2 = forses(0, 0)
        M1, M2 = moments(0, 0)
        Krot, Mrot = rots(0, 0)

        fomo = [a, P1, P2, Krot, M1, M2, Mrot]
        
        with open(config + '/' + config + '.v' + str(j) + '.csv', 'a', newline='') as result_file:
            resultwrite = csv.writer(result_file)
            resultwrite.writerow(fomo)
    
    print ('\n' + '\033[1m' + 'All results saved to files:  '\
           + '\033[1;36m' +  config + '.v' + str(j) + '.csv,  ' + config + '.v' + str(j) + '.png' + '\033[0m')
    
    A_values,P1_values,P2_values,Krot_values,M1_values,M2_values,Mrot_values = aggregation()
    
    P1_max_value,P2_max_value,Krot_max_value,M1_max_value,M2_max_value,Mrot_max_value = max_values()
    
    with open(config + '/' + config + '.maximums' + '.txt', 'a+') as max_file:
        max_file.write("{: >7} | {: >9.2f} | {: >9.2f} | {: >9.2f} | {: >9.2f} | {: >9.2f} | {: >9.2f}\n".format(j, P1_max_value, P2_max_value, Krot_max_value, M1_max_value, M2_max_value, Mrot_max_value))

    visualization()
    
print ('\n\n' + '\033[1m' + 'All of maximum values of calculated '\
               'results \n for each variant saved to file:  ' + '\033[1;36m' + config\
               + '.maximums.txt' + '\033[0m')

# mesure time for test only
print ('\nTime used: ', round(time.time() - start_time, 2))
