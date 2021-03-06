import math
import matplotlib.pyplot as plt
import numpy as np
def fitfunction_root(x, par):
    # source: https://github.com/root-project/root/blob/master/roofit/roofit/src/RooBukinPdf.cxx
    Xp = par[0]
    sigp = par[1]
    xi = par[2]
    rho1 = par[3]
    rho2 = par[4]
    ap = par[5]
    consts = 2*math.sqrt(2*math.log(2.0))
    r1=0
    r2=0
    r3=0
    r4=0
    r5=0
    hp=0
    x1 = 0
    x2 = 0
    fit_result = 0

    hp=sigp*consts
    r3=math.log(2.)
    r4=math.sqrt(xi*xi+1)
    r1=xi/r4

    if abs(xi) > math.exp(-6.):
        r5=xi/math.log(r4+xi)
    else:
        r5=1

    x1 = Xp + (hp / 2) * (r1-1)
    x2 = Xp + (hp / 2) * (r1+1)

    #--- Left Side
    if x < x1:
        r2=rho1*(x-x1)*(x-x1)/(Xp-x1)/(Xp-x1)-r3 + 4 * r3 * (x-x1)/hp * r5 * r4/(r4-xi)/(r4-xi)
    #--- Center
    elif x < x2:
        if abs(xi) > math.exp(-6.):
            r2=math.log(1 + 4 * xi * r4 * (x-Xp)/hp)/math.log(1+2*xi*(xi-r4));
            r2=-r3*r2*r2
        else:
            r2=-4*r3*(x-Xp)*(x-Xp)/hp/hp
    #--- Right Side
    else:
        r2=rho2*(x-x2)*(x-x2)/(Xp-x2)/(Xp-x2)-r3 - 4 * r3 * (x-x2)/hp * r5 * r4/(r4+xi)/(r4+xi)

    if abs(r2) > 100:
        fit_result = 0
    else:
        #---- Normalize the result
        fit_result = math.exp(r2)

    return fit_result *ap

plotx = []
ploty = []
parameters = [10, 50, -0.2, -0.5, 0.1, 1]
for each in np.linspace(-200, 200, 100):
    plotx.append(each)
    ploty.append(fitfunction_root(each, parameters))
plt.plot(plotx, ploty)
plt.show()
