#! /usr/bin/env python3

"""Script for calculating dynamic balance of reciprocating and
   rotating masses of internal combustion engines.
   The calculation is valid for single-row engines and V-engines with
   the same number of cylinders in the left and right banks.
"""

import math
import csv
import yaml
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time

def forces(P1, P2):
    """Reciprocating Forces.
       Calculate Primary and Secondary Reciprocating Forces.
    """
    i, p1l, p2l, p1r, p2r = 0, 0, 0, 0, 0
    if Rows == 1:  # number of rows of cylinders = 1
        for i in range(Cyl_in_row):
            p1l += math.cos(math.radians(a + geometry_angles_l[i]))
            p1r = 0
            p2l += math.cos(2 * math.radians(a + geometry_angles_l[i]))
            p2r = 0
    else:  # number of rows of cylinders = 2
        for i in range(Cyl_in_row):
            p1l += math.cos(math.radians(a + geometry_angles_l[i]))
            p1r += math.cos(math.radians(a + geometry_angles_r[i] - Y))
            p2l += math.cos(2 * math.radians(a + geometry_angles_l[i]))
            p2r += math.cos(2 * math.radians(a + geometry_angles_r[i] - Y))
    P1x = mrcp * R * Omega ** 2 * (p1l + math.cos(math.radians(Y)) * p1r)
    P1y = mrcp * R * Omega ** 2 * math.sin(math.radians(Y)) * p1r
    P1 = round(math.sqrt(P1x ** 2 + P1y ** 2), 2)
    P2x = mrcp * R * Omega ** 2 * Q * (p2l + math.cos(math.radians(Y)) * p2r)
    P2y = mrcp * R * Omega ** 2 * Q * math.sin(math.radians(Y)) * p2r
    P2 = round(math.sqrt(P2x ** 2 + P2y ** 2), 2)
    return P1, P2

def moments(M1, M2):
    """Reciprocating Moments.
       Calculate Primary and Secondary Reciprocating Moments.
    """
    i, m1l, m2l, m1r, m2r = 0, 0, 0, 0, 0
    if Rows == 1:  # number of rows of cylinders = 1
        for i in range(Cyl_in_row):
            m1l += (geometry_dists_l[i]) * (math.cos(math.radians(a + geometry_angles_l[i])))
            m1r = 0
            m2l += (geometry_dists_l[i]) * (math.cos(2 * math.radians(a + geometry_angles_l[i])))
            m2r = 0
    else:  # number of rows of cylinders = 2
        for i in range(Cyl_in_row):
            m1l += (geometry_dists_l[i]) * (math.cos(math.radians(a + geometry_angles_l[i])))
            m1r += (geometry_dists_r[i]) * (math.cos(math.radians(a + geometry_angles_r[i] - Y)))
            m2l += (geometry_dists_l[i]) * (math.cos(2 * math.radians(a + geometry_angles_l[i])))
            m2r += (geometry_dists_r[i]) * (math.cos(2 * math.radians(a + geometry_angles_r[i] - Y)))
    M1x = -(mrcp * R * Omega ** 2 * math.sin(math.radians(Y)) * m1r)
    M1y = mrcp * R * Omega ** 2 * (m1l + math.cos(math.radians(Y)) * m1r)
    M1 = round(math.sqrt(M1x ** 2 + M1y ** 2), 2)
    M2x = -(mrcp * R * Omega ** 2 * Q * math.sin(math.radians(Y)) * m2r)
    M2y = mrcp * R * Omega ** 2 * Q * (m2l + math.cos(math.radians(Y)) * m2r)
    M2 = round(math.sqrt(M2x ** 2 + M2y ** 2), 2)
    return M1, M2

def rots(Krot, Mrot):
    """Centrifugal Forces and Moments.
       Calculate Centrifugal Forces and Moments.
    """
    i, kx, ky, mx, my = 0, 0, 0, 0, 0
    if Rows == 1 or geometry_angles_l == geometry_angles_r:  # one crank for one (1 row) or two (2 row) cylinders
        for i in range(Cyl_in_row):
            kx += math.cos(math.radians(a + geometry_angles_l[i]))
            ky += math.sin(math.radians(a + geometry_angles_l[i]))
            mx += (geometry_dists_l[i]) * (math.sin(math.radians(a + geometry_angles_l[i])))
            my += (geometry_dists_l[i]) * (math.cos(math.radians(a + geometry_angles_l[i])))
    elif Rows == 2 and geometry_angles_l != geometry_angles_r:  # own crank for each cylinder
        for i in range(Cyl_in_row):
            kx += (math.cos(math.radians(a + geometry_angles_l[i])) + math.cos(math.radians(a + geometry_angles_r[i])))
            ky += (math.sin(math.radians(a + geometry_angles_l[i])) + math.sin(math.radians(a + geometry_angles_r[i])))
            mx += (geometry_dists_l[i]) * (math.sin(math.radians(a + geometry_angles_l[i]))) + (geometry_dists_r[i]) * (
                math.sin(math.radians(a + geometry_angles_r[i])))
            my += (geometry_dists_l[i]) * (math.cos(math.radians(a + geometry_angles_l[i]))) + (geometry_dists_r[i]) * (
                math.cos(math.radians(a + geometry_angles_r[i])))
    Kx = mrot * R * Omega ** 2 * kx
    Ky = mrot * R * Omega ** 2 * ky
    Krot = round(math.sqrt(Kx ** 2 + Ky ** 2), 2)
    Mx = -(mrot * R * Omega ** 2 * mx)
    My = mrot * R * Omega ** 2 * my
    Mrot = round(math.sqrt(Mx ** 2 + My ** 2), 2)
    return Krot, Mrot

def aggregation_to_csv():
    """ Results aggregation
    """
    results = list(zip(A_values, P1_values, P2_values, Krot_values, M1_values, M2_values, Mrot_values))

    with open(config + '/' + config + '.v' + str(j) + '.csv', 'a', newline='') as result_file:
        resultwriter = csv.writer(result_file)

        for item in results:
            resultwriter.writerow(item)

    print ('\n' + '\033[1m' + 'All results saved to files:  '\
           + '\033[1;36m' +  config + '.v' + str(j) + '.csv,  '\
           + config + '.v' + str(j) + '.png' + '\033[0m')

def max_values():
    """Maximum values of Forces and Moments.
    """
    P1_max_value = max(P1_values, key=abs)
    P2_max_value = max(P2_values, key=abs)
    Krot_max_value = max(Krot_values, key=abs)
    M1_max_value = max(M1_values, key=abs)
    M2_max_value = max(M2_values, key=abs)
    Mrot_max_value = max(Mrot_values, key=abs)
    return P1_max_value, P2_max_value, Krot_max_value, M1_max_value, M2_max_value, Mrot_max_value

def visualization():
    """Results visualization.
    """
    fig1, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3, figsize=(15, 8))

    fig1.tight_layout(pad=4.0)
    fig1.suptitle('Forces, Moments', fontsize='x-large', weight='heavy')

    ax1.plot(A_values, P1_values, color='blue', linestyle='-', marker='.', markevery=30)
    ax1.set_xlim(0, 360)
    ax1.set_xlabel('crank rotation angle, [°]')
    ax1.set_ylabel('P1, [N]')
    ax1.set_title('1st order reciprocating force')
    ax1.grid(True, which='minor')
    plt.text(0.1, 0.93, 'max P1 value = ' + str(P1_max_value),
             transform=ax1.transAxes, fontsize=8, va='bottom')
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(90))
    ax1.xaxis.set_minor_locator(ticker.MultipleLocator(30))

    ax2.plot(A_values, P2_values, color='indigo', linestyle='-', marker='.', markevery=30)
    ax2.set_xlim(0, 360)
    ax2.set_xlabel('crank rotation angle, [°]')
    ax2.set_ylabel('P2, [N]')
    ax2.set_title('2nd order reciprocating force')
    ax2.grid(True, which='minor')
    plt.text(0.1, 0.93, 'max P2 value = ' + str(P2_max_value),
             transform=ax2.transAxes, fontsize=8, va='bottom')
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(90))
    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(30))

    ax3.plot(A_values, Krot_values, color='darkblue', linestyle='-', marker='.', markevery=30)
    ax3.set_xlim(0, 360)
    ax3.set_xlabel('crank rotation angle, [°]')
    ax3.set_ylabel('Krot, [N]')
    ax3.set_title('centrifugal force')
    ax3.grid(True, which='minor')
    plt.text(0.1, 0.93, 'max Krot value = ' + str(Krot_max_value),
             transform=ax3.transAxes, fontsize=8, va='bottom')
    ax3.xaxis.set_major_locator(ticker.MultipleLocator(90))
    ax3.xaxis.set_minor_locator(ticker.MultipleLocator(30))

    ax4.plot(A_values, M1_values, color='red', linestyle='-', marker='.', markevery=30)
    ax4.set_xlim(0, 360)
    ax4.set_xlabel('crank rotation angle, [°]')
    ax4.set_ylabel('M1, [Nm]')
    ax4.set_title('1st order reciprocating moment')
    ax4.grid(True, which='minor')
    plt.text(0.1, 0.93, 'max M1 value = ' + str(M1_max_value),
             transform=ax4.transAxes, fontsize=8, va='bottom')
    ax4.xaxis.set_major_locator(ticker.MultipleLocator(90))
    ax4.xaxis.set_minor_locator(ticker.MultipleLocator(30))

    ax5.plot(A_values, M2_values, color='crimson', linestyle='-', marker='.', markevery=30)
    ax5.set_xlim(0, 360)
    ax5.set_xlabel('crank rotation angle, [°]')
    ax5.set_ylabel('M2, [Nm]')
    ax5.set_title('2nd order reciprocating moment')
    ax5.grid(True, which='minor')
    plt.text(0.1, 0.93, 'max M2 value = ' + str(M2_max_value),
             transform=ax5.transAxes, fontsize=8, va='bottom')
    ax5.xaxis.set_major_locator(ticker.MultipleLocator(90))
    ax5.xaxis.set_minor_locator(ticker.MultipleLocator(30))

    ax6.plot(A_values, Mrot_values, color='darkred', linestyle='-', marker='.', markevery=30)
    ax6.set_xlim(0, 360)
    ax6.set_xlabel('crank rotation angle, [°]')
    ax6.set_ylabel('Mrot, [Nm]')
    ax6.set_title('centrifugal moment')
    ax6.grid(True, which='minor')
    plt.text(0.1, 0.93, 'max Mrot value = ' + str(Mrot_max_value),
             transform=ax6.transAxes, fontsize=8, va='bottom')
    ax6.xaxis.set_major_locator(ticker.MultipleLocator(90))
    ax6.xaxis.set_minor_locator(ticker.MultipleLocator(30))

    fig1.savefig(config + '/' + config  + '.v' + str(j) + '.png')
    plt.close(fig1)
#    plt.show()

def visualization_max():
    """Visualization of max values in journals
    """
    fig2, [[ax1, ax2, ax3], [ax4, ax5, ax6]] = plt.subplots(nrows=2, ncols=3, figsize=(15, 8), sharey='row')

    fig2.tight_layout(pad=4.0)
    fig2.suptitle('Maximum Values of Forces, Moments', fontsize='x-large', weight='heavy')

    bark1 = ax1.bar(J_max_values, P1_max_values, width=0.6, align='center', color='blue')
    ax1.set_xticks(range(len(J_max_values)))
    ax1.set_xlabel('Journal Number')
    ax1.set_ylabel('P1, [N]')
    ax1.set_title('max of 1st order recipr. forces')

    bark2 = ax2.bar(J_max_values, P2_max_values, width=0.6, align='center', color='indigo')
    ax2.set_xticks(range(len(J_max_values)))
    ax2.set_xlabel('Journal Number')
    ax2.set_ylabel('P2, [N]')
    ax2.set_title('max of 2nd order recipr. forces')

    bark3 = ax3.bar(J_max_values, Krot_max_values, width=0.6, align='center', color='darkblue')
    ax3.set_xticks(range(len(J_max_values)))
    ax3.set_xlabel('Journal Number')
    ax3.set_ylabel('Krot, [N]')
    ax3.set_title('max of centrifugal force')

    bark4 = ax4.bar(J_max_values, M1_max_values, width=0.6, align='center', color='red')
    ax4.set_xticks(range(len(J_max_values)))
    ax4.set_xlabel('Journal Number')
    ax4.set_ylabel('M1, [Nm]')
    ax4.set_title('max of 1st order recipr. moments')

    bark5 = ax5.bar(J_max_values, M2_max_values, width=0.6, align='center', color='crimson')
    ax5.set_xticks(range(len(J_max_values)))
    ax5.set_xlabel('Journal Number')
    ax5.set_ylabel('M2, [Nm]')
    ax5.set_title('max of 2nd order recipr. moments')

    bark6 = ax6.bar(J_max_values, Mrot_max_values, width=0.6, align='center', color='darkred')
    ax6.set_xticks(range(len(J_max_values)))
    ax6.set_xlabel('Journal Number')
    ax6.set_ylabel('Mrot, [Nm]')
    ax6.set_title('max of centrifugal moment')

    for k in range(1, 7):

        bark = locals()['bark' + str(k)]
        axk = locals()['ax' + str(k)]
        for bar in bark:
            height = bar.get_height()
            axk.annotate(round(height), xy=(bar.get_x() + bar.get_width() / 2,
                                            height), xytext=(0, 0),
                                            textcoords='offset points', ha='center',
                                            va='bottom', fontsize=8)

    fig2.savefig(config + '/' + config  + '.maximums' + '.png')
    plt.show()

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
                           ' \"mechanics.config.yaml\".\nAllowed names: ', ' | '.join(sorted(allnames.keys())))
            config = input('Enter the allowed name :\n')

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

counter = len(mech['journals'])

J_max_values = []
P1_max_values = []
P2_max_values = []
Krot_max_values = []
M1_max_values = []
M2_max_values = []
Mrot_max_values = []

for j in range(0, counter, 1):

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
    geometry_angles_l = list(map(float, mech['journals']['journal'+str(j)]
                                            ['geometry_angles_l'].split(',')))

    # angles between the first and subsequent crankpins of the right row
    geometry_angles_r = list(map(float, mech['journals']['journal'+str(j)]
                                            ['geometry_angles_r'].split(',')))

    # distances between the first connecting rod and subsequent ones
    # on the crankshaft journals of the left row
    geometry_dists_l = list(map(float, mech['journals']['journal'+str(j)]
                                           ['geometry_dists_l'].split(',')))

    # distances between the first connecting rod and subsequent ones
    # on the crankshaft journals of the right row
    geometry_dists_r = list(map(float, mech['journals']['journal'+str(j)]
                                           ['geometry_dists_r'].split(',')))

    # number of cylinders in a row
    Cyl_in_row = len(geometry_angles_l)

    # total number of cyliders
    N = int(Cyl_in_row * Rows)

    # coefficient lambda
    Q = R / L
    
    A_values = []
    P1_values = []
    P2_values = []
    Krot_values = []
    M1_values = []
    M2_values = []
    Mrot_values = []

    for a in range(0, 360, 1): # angle of crank rotation
        P1,P2 = forces(0, 0)
        M1, M2 = moments(0, 0)
        Krot, Mrot = rots(0, 0)

        A_values.append(a)
        P1_values.append(P1)
        P2_values.append(P2)
        Krot_values.append(Krot)
        M1_values.append(M1)
        M2_values.append(M2)
        Mrot_values.append(Mrot)
        
    aggregation_to_csv()

    P1_max_value,P2_max_value,Krot_max_value,M1_max_value,M2_max_value,Mrot_max_value = max_values()

    J_max_values.append(int(j))
    P1_max_values.append(float(P1_max_value))
    P2_max_values.append(float(P2_max_value))
    Krot_max_values.append(float(Krot_max_value))
    M1_max_values.append(float(M1_max_value))
    M2_max_values.append(float(M2_max_value))
    Mrot_max_values.append(float(Mrot_max_value))

    with open(config + '/' + config + '.maximums' + '.txt', 'a+') as max_file:
        max_file.write("{: >7} | {: >9.2f} | {: >9.2f} | {: >9.2f} | {: >9.2f} | {: >9.2f} | {: >9.2f}\n".format(j, P1_max_value, P2_max_value, Krot_max_value,\
                        M1_max_value, M2_max_value, Mrot_max_value))

    visualization()

if counter > 1:

    visualization_max()

print ('\n\n' + '\033[1m' + 'All of maximum values of calculated '\
               'results for each variant saved to files:  \n' + '\033[1;36m' + config\
               + '.maximums.txt' + ', ' + config  + '.maximums' + '.png' + '\033[0m')

def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
