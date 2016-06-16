# coding=utf8
def solve(n, c, w, i, V):
    save = [([0] * (V + 1)) for i in range(i + 1)]
    for i in range(1, i + 1):
        for v in range(1, V + 1):
            max_result = save[i - 1][v]
            for k in range(1, n[i - 1] + 1):
                if v - k * c[i - 1] >= 0:
                    max_result = max(max_result, save[i - 1][v - k * c[i - 1]] + k * w[i - 1])
            save[i][v] = max_result
    return save


def parse(save, c, w):
    i = len(save) - 1
    V = len(save[0]) - 1
    result = [0] * i
    while save[i][V] != 0:
        if save[i][V] != save[i - 1][V]:  # 进解析
            count = 1
            temp = V
            while temp >= c[i - 1] and save[i][temp - c[i - 1]] != save[i - 1][temp - c[i - 1]]:
                count += 1
                temp -= c[i - 1]
            result[i - 1] = count
            V -= c[i - 1] * count
            i -= 1
        else:
            i -= 1
    return result