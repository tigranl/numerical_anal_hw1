import math
import matplotlib.pyplot as plt
import numpy as np
#


def func_test(x, y):
    # return ((-3 / 2) * y)
    return (-2.5) * y

def func_1(x, y):
    f = math.log1p(x) / (x ** 2 + 1)
    return f * y ** 2 + y - y ** 3 * math.sin(10 * x)


def f_1(x, u_1, u_2, k, f, m):
    return u_2


def f_2(x, u_1, u_2, k, f, m):
    # mu'' + ku = F = fmg
    g = 980.665
    return (1 / m) * (f * m * g  - k * u_1)
 

def rk4_s(x_0, u1_0, u2_0, f_1, f_2, k, f, m, h, v_max):
    u1 = u1_0
    u2 = u2_0
    k_1 = np.longdouble(h * f_1(x_0, u1_0, u2_0, k, f, m))
    if abs(k_1) > v_max:
        return v_max, v_max
    l_1 = np.longdouble(h * f_2(x_0, u1_0, u2_0, k, f, m))
    if abs(l_1) > v_max:
        return v_max, v_max
    k_2 = np.longdouble(h * f_1(x_0 + h / 2, u1_0 + k_1 / 2, u2_0 + l_1 / 2, k, f, m))
    if abs(k_2) > v_max:
        return v_max, v_max
    l_2 = np.longdouble(h * f_2(x_0 + h / 2, u1_0 + k_1 / 2, u2_0 + l_1 / 2, k, f, m))
    if abs(l_2) > v_max:
        return v_max, v_max
    k_3 = np.longdouble(h * f_1(x_0 + h / 2, u1_0 + k_2 / 2, u2_0 + l_2 / 2, k, f, m))
    if abs(k_3) > v_max:
        return v_max, v_max
    l_3 = np.longdouble(h * f_2(x_0 + h / 2, u1_0 + k_2 / 2, u2_0 + l_2 / 2, k, f, m))
    if abs(l_3) > v_max:
        return v_max, v_max
    k_4 = np.longdouble(h * f_1(x_0 + h, u1_0 + k_3, u2_0 + l_3, k, f, m))
    if abs(k_4) > v_max:
        return v_max, v_max
    l_4 = np.longdouble(h * f_2(x_0 + h, u1_0 + k_3, u2_0 + l_3, k, f, m))
    if abs(l_4) > v_max:
        return v_max, v_max
    u1 += np.longdouble(1 / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4))
    if abs(u1) > v_max:
        return v_max, v_max
    u2 += np.longdouble(1 / 6 * (l_1 + 2 * l_2 + 2 * l_3 + l_4))
    if abs(u2) > v_max:
        return v_max, v_max
    return u1, u2


def num_sol_3_task(k, f, m, N_max, f_1, f_2, x_0, u1_0, u2_0, x_end, h, e, error_control):
    v_max = 10e30
    c1 = 0
    c2 = 0
    u1_ds = u1_0
    u2_ds = u2_0
    S_nor = 0
    counter = 1

    C1 = [c1]
    C2 = [c2]
    U1 = [u1_0]
    U1_ds = [u1_0]
    U1_U1ds = [0]
    U2 = [u2_0]
    U2_ds = [u2_0]
    U2_U2ds = [0]
    H = [h]
    error_arr = [0]
    X = [x_0]

    while x_0 <= x_end - h:
        temp_1, temp_2 = rk4_s(x_0, u1_0, u2_0, f_1, f_2, k, f, m, h, v_max)
        temp1_ds, temp2_ds = rk4_s(x_0, u1_0, u2_0, f_1, f_2, k, f, m, h / 2, v_max)
        temp1_ds, temp2_ds = rk4_s(x_0 + h / 2, temp1_ds, temp2_ds, f_1, f_2, k, f, m, h / 2, v_max)

        if v_max in [temp_1, temp_2, temp1_ds]:
            break

        S_nor = abs(((temp_1 - temp1_ds) ** 2 + (temp_2 - temp2_ds) ** 2) ** 0.5)
        if error_control and S_nor > e:
            h /= 2
            c1 += 1
        else:
            x_0 += h
            H.append(h)
            U1_ds.append(temp1_ds)
            U2_ds.append(temp2_ds)
            U1.append(temp_1)
            U2.append(temp_2)
            U1_U1ds.append(u1_0 - u1_ds)
            U1_U1ds.append(u2_0 - u2_ds)
            X.append(x_0)
            error_arr.append(S_nor / 15)
            if error_control:
                if S_nor < e / 32:
                    h *= 2
                    c2 += 1
            C2.append(c2)
            C1.append(c1)
        if error_control:
            if counter >= N_max:
                break
        counter += 1

    return X, U1, U1_ds, error_arr, H, C1, C2, U2, U2_ds


def RK4(x_i, y_i, h, func, v_max):
    y = np.longdouble(y_i)
    k1 = np.longdouble(h * func(x_i, y))
    if abs(k1) > v_max:
        return v_max
    k2 = np.longdouble(h * func(x_i + h / 2, y + k1 / 2))
    if abs(k2) > v_max:
        return v_max
    k3 = np.longdouble(h * func(x_i + h / 2, y + k2 / 2))
    if abs(k3) > v_max:
        return v_max
    k4 = np.longdouble(h * func(x_i + h, y + k3))
    if abs(k4) > v_max:
        return v_max
    y += np.longdouble((1 / 6) * (k1 + 2 * k2 + 2 * k3 + k4))
    return y
