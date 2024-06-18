from math import *

"""
-----------------------------------
Reference functions to use in hs-logger
JLS 7/07/2021
 READY TO RUN IN PYCHARM
-----------------------------------
"""
# from GTC import *  # when in lib
# import implicit as im


def vp(ts, df):
    """
    6/8/2021
     returns vapour pressure calculated over ice (df=0 and ts<0.01) or liquid water df=1 (may be supercooled)
    WATER: Wagner W, Saul A and Pruss A, "International equations for the pressure along the melting
    'and along the sublimation curve of ordinary water",
    'J. Phys. Chem. Ref. Data, 23,3,515-525, 1994
    ICE: Revised IAPWS Sept 2008 for t<0.01
    IAPWS Sept 2008 "Revised Release on the Pressure along the
    'Melting and Sublimation Curves of Ordinary Water Substance"
    # Note, supercooled dew below -50 C is likely to be unphysical so
    (ts<-50 and df=1), while not prevented, should not be used.

    :param ts: the temperature at saturation in deg C.
    :param df: indicates phase df=1 for dew, df=0  for frost
    :return: vapour pressure of phase given by df
    """
    if ts > 0.01 or df == 1:  # Use Wagner and Pruss (1993)
        a1 = -7.85951783
        a2 = 1.84408259
        a3 = -11.7866497
        a4 = 22.6807411
        a5 = -15.9618719
        a6 = 1.80122502
        pc = 22064000
        tc = 647.096
        torr = 1 - (ts + 273.15) / tc
        return pc * exp(tc / (ts + 273.15) * (a1 * torr + a2 * torr ** 1.5 + a3 * torr ** 3 + a4 *
                                              torr ** 3.5 + a5 * torr ** 4 + a6 * torr ** 7.5))
    else:
        # 'IAPWS Sept 2008 "Revised Release on the Pressure along the Melting and Sublimation Curves of Ordinary
        # Water Substance" checked 23/03/2010: error in a1 picked up: should be  -21.2144006, not  -21.21446 as was
        # transcribed!
        theta = (ts + 273.15) / 273.16
        pt = 611.657  # WTP pressure in Pa
        a1 = -21.2144006
        a2 = 27.3203819
        a3 = -6.1059813
        b1 = 0.00333333333
        b2 = 1.20666667
        b3 = 1.70333333
        return pt * exp(1 / theta * (a1 * theta ** b1 + a2 * theta ** b2 + a3 * theta ** b3))


def ef(ts, p, df):
    """
    calculates Water Vapour Enhancement Factor based on Greenspan 1976
    Greenspan L 1976 Journal of Research of the National Bureau of Standards, 80A, 41-44

    :param ts: temperature in C: -100C < t < 200C
    :param p: pressure in Pa
    :param df: calculate over dew(1)  or frost (0)
    :return: water vapour enhancement factor (unitless)
    """

    if df == 0 and ts < 0:    # frost
        a1 = 0.000364449
        a2 = 0.0000293631
        a3 = 0.000000488635
        a4 = 0.00000000436543
        b1 = -10.7271
        b2 = 0.0761989
        b3 = -0.000174771
        b4 = 0.00000246721

    elif df == 1 and ts < 0:  # supercooled dew
        a1 = 0.000362183
        a2 = 0.0000260553
        a3 = 0.000000386501
        a4 = 0.00000000382449
        b1 = -10.7604
        b2 = 0.0639725
        b3 = -0.000263416
        b4 = 0.00000167254
    else:  # dew
        a1 = 0.000353624
        a2 = 0.0000293228
        a3 = 0.000000261474
        a4 = 0.00000000857538
        b1 = -10.7588
        b2 = 0.0632529
        b3 = -0.000253591
        b4 = 0.000000633784
    alpha = a1 + a2 * ts + a3 * ts ** 2 + a4 * ts ** 3
    beta = exp(b1 + b2 * ts + b3 * ts ** 2 + b4 * ts ** 3)
    svp = vp(ts, df)

    if ts < -100:
        temp = "Error: Temperature < -100C"
    elif ts > 200:
        temp = "Error: Temperature > 200C"
    elif svp >= p:
        temp = 1.0  # note ef= 1 if svp=P'
    else:
        temp = exp(alpha * (1 - svp / p) + beta * (p / svp - 1))
    return temp


def inversemagnus(vp, df):
    """
    Calculate starting value for dew point using the inverse magnus equation
    :param vp:  known vapour pressure in Pa
    :param df:  calculate over dew(1)  or frost (0)
    :return: approximate dew/frost point deg C
    """
    a0 = 611.2
    if vp < 611.2 and df == 1:
        a1 = 22.46
        a2 = 272.46
    else:
        a1 = 17.62
        a2 = 243.12
    return a2 * log(vp / a0) / (a1 - log(vp / a0))


def td_ex_vp(vp1, df):
    """
    Finds dew point from pure phase water vapour pressure using  Inversemagnus() function
    to give a first approximation and then uses an iterative method to find the inverse of the Vapour pressure equation
    :param vp1:  known vapour pressure in Pa
    :param df:  calculate over dew(1)  or frost (0)
    :returns: dew/frost point deg C
    """
    tdi = inversemagnus(vp1, df)
    tol = 10E-15
    ct = 0
    del_vp = 1
    while abs(del_vp) > tol and ct < 10:
        ct = ct+1
        vpi = vp(tdi, df)
        del_vp = vp1 - vpi
        tdi = del_vp / dedt(tdi, df) + tdi
    return tdi


def td_ex_pv(pvo, po, df):
    """
    calculate dewpoint from partial pressure Pv and total pressure Po
    :param pvo: partial pressure (Pa)
    :param po: total pressure Po
    :param df: calculate over dew(1)  or frost (0)
    :return: dew/frost poin (deg C)
    """

    tdi = td_ex_vp(pvo/1.004, df)  # first guess
    diff = 11
    tol = 1E-10
    ct = 0
    while abs(diff) > tol and ct < 20:
        ct = ct+1
        edi = pvo/ef(tdi, po, df)  # recalculate ed from Pv and new fd
        td = td_ex_vp(edi, df)  # recalculate td from new ed
        pvi = ef(td, po, df) * vp(td, df)
        diff = pvi - pvo
        tdi = td
    return tdi


def dedt(ts, df):
    """
    calculates the derivative of the saturation vapour pressure based on IAPWS2008 equation* (ice below 0C) and
    Wagner Pruss equation* (supercooled dew (t<0 C) and dew.
    WATER: Wagner W, Saul A and Pruss A, "International equations for the pressure along the melting
    'and along the sublimation curve of ordinary water",
    'J. Phys. Chem. Ref. Data, 23,3,515-525, 1994
    ICE: Revised IAPWS Sept 2008 for t<0.01
    IAPWS Sept 2008 "Revised Release on the Pressure along the
    'Melting and Sublimation Curves of Ordinary Water Substance"
    # Note, supercooled dew below -50 C is likely to be unphysical so
    (ts<-50 and df=1), while not prevented, should not be used.
    :param ts: saturation temperature
    :param df: calculate over dew(1)  or frost (0)
    :return: first derivative of the vapour pressure wrt temperature
    """

    t = 273.15 + ts
    if df == 0 and ts < 0:  # If frost desired ok only if ts<0
        theta = (ts + 273.15) / 273.16
        pt = 611.657  # Pa
        a1 = -21.2144006
        a2 = 27.3203819
        a3 = -6.1059813
        b1 = 0.00333333333
        b2 = 1.20666667
        b3 = 1.70333333
        dvpdt = vp(ts, df) * ((b1 - 1) * a1 * theta ** (b1 - 2) + (b2 - 1) * a2 * theta ** (b2 - 2) +
                              (b3 - 1) * a3 * theta ** (b3 - 2)) / 273.16
    else:  # use derivative of Wagner Pruss
        a1 = -7.85951783
        a2 = 1.84408259
        a3 = -11.7866497
        a4 = 22.6807411
        a5 = -15.9618719
        a6 = 1.80122502
        pc = 22064000
        tc = 647.096
        torr = 1 - (ts + 273.15) / tc
        y = 1 / (1 - torr)
        z = (a1 * torr + a2 * torr ** 1.5 + a3 * torr ** 3 + a4 * torr ** 3.5 + a5 * torr ** 4 + a6 * torr ** 7.5)
        x = y * z
        vp1 = pc * exp(x)
        dtorrdt = -1 / tc
        dydtorr = y ** 2
        dzdtorr = (a1 + (1.5 * a2 * torr ** 0.5) + (3 * a3 * torr ** 2) +
                   (3.5 * a4 * torr ** 2.5) + (4 * a5 * torr ** 3) + (7.5 * a6 * torr ** 6.5))
        dxdtorr = z * dydtorr + y * dzdtorr
        dvpdx = vp1
        dvpdt = dvpdx * dxdtorr * dtorrdt
    return dvpdt


def pv(td1, p1, df1):
    """
    returns the vapour partial pressure for given dew-frost point at pressure
    :param td1: known dew-frost point
    :param p1: known total pressure
    :param df1: calculate over dew(1)  or frost (0)
    :return: vapour partial pressure (Pa)
    """
    return vp(td1, df1)*ef(td1, p1, df1)


# transformations
def td2_ex_td1(td1, p1, p2, df1, df2):
    """
    returns the dew or frost point temperature under condition 2,
    from the dew/frost point under condition 2 assuming
    assuming there has been no condensation or evaporation
    :param td1: known dew/frost point (deg C) under condition 1
    :param p1:  pressure (Pa) under condition 1
    :param p2:  pressure (Pa) under condition 2
    :param df1: phase of dew/frost point under condition 1
    :param df2: phase of desired dew/frost point under condition 2
    :return: dew/frost point under condition 2
    """
    return td_ex_pv(pv(td1, p1, df1)*p2/p1, p2, df2)


def h2_ex_td1(td1, p1, p2, t2, df1, df2):  # df2 determines whether satVP calc over ice or water
    """
    returns the relative humidity under condition 2, from the dew/frost point under condition 1
    assuming there has been noo condensation or evaporation
    Note: RH=x/xos=pv1/P1*P2/pv2=pv1/pv2*P2/P1 *100%
    :param td1: known dew/frost point (deg C) under condition 1
    :param p1:  pressure (Pa) under condition 1
    :param p2:  pressure (Pa) under condition 2
    :param t2:  temperature (deg C) under condition 2
    :param df1: phase of dew/frost point under condition 1
    :param df2: phase of reference saturation vapour pressure under condition 2
    :return: h2, the relative humidity (%rh) under condition 2 calc wrt dew/frost (df2=1/0)
    """
    return pv(td1, p1, df1)/pv(t2, p2, df2)*p2/p1*100


def td2_ex_h1(h1, p1, p2, t1, df1, df2):
    """
    returns the dew/frost point under condition 2, from RH under condition 1
    assuming there has been noo condensation r evaporation
    :param h1: known relative humidity that is calculated wrt dew/frost (df1=1/0)
    :param p1:  pressure (Pa) under condition 1
    :param p2:  pressure (Pa) under condition 2
    :param t1:  temperature (deg C) under condition 1
    :param df1: phase of reference SVP under condition 1
    :param df2: phase of dew/frost point under condition 2
    :return: dew/frost point under condition 2
    """
    return td_ex_pv(h1/100*pv(t1, p1, df1), p2, df2)


def h2_ex_h1(h1, p1, p2, t1, t2, df1, df2):
    """
    returns RH under condition 2, from RH under condition 1
    assuming there has been noo condensation r evaporation
   :param h1: known relative humidity that is calculated wrt dew/frost (df1=1/0)
    :param p1:  pressure (Pa) under condition 1
    :param p2:  pressure (Pa) under condition 2
    :param t1:  temperature (deg C) under condition 1
    :param t2:  temperature (deg C) under condition 2
    :param df1: phase of dew/frost point under condition 1
    :param df2: phase of reference saturation vapour pressure under condition 2
    :return:h2 RH (%rh) under condition 2 calc from RH under condition 1
    """
    return h1/100*pv(t1, p1, df1)/pv(t2, p2, df2)*p2/p1*100


# testing
def main():
    df1 = 0
    df2 = 0
    td1 = -30
    pd1 = 1e5
    pd2 = 1e5
    p1 = 1e5
    p2 = 1e5
    t1 = -10
    t2 = -20
    h1 = 20
    print("df1={} df2={} td1={} pd1={} pd2={} p1={} p2={} t1={} t2={} h1={}".format(
        df1, df2, td1, pd1, pd2, p1, p2, t1, t2, h1))

    print("td2_ex_td1 = ", td2_ex_td1(td1, pd1, pd2, df1, df2), " C")
    print("h2_ex_td1 = ", h2_ex_td1(td1, pd1, pd2, t2, df1, df2), " %rh")

    print("td2_ex_h1 = ", td2_ex_h1(h1, p1, pd2, t1, df1, df2), " C")
    print("h2_ex_h1 = ", h2_ex_h1(h1, p1, p2, t1, t2, df1, df2), " %rh")


if __name__ == '__main__':
    main()
