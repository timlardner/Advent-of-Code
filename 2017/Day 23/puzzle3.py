b = -91900
c = -74900

g = 0
h = 0

# Big bit
while b != c:
    f = 1
    d = 2
    e = 2
    while g != 0:
        while g != 0:
            g = d
            g *= e
            g -= b
            if g == 0:
                f = 0
            e += 1
            g = e
            g -= b
        d += 1
        g -= b
    if f == 0:
        h -= 1
    b += 17

print(h)
