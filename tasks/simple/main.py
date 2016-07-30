def is_prime(n):
    if n > 2:
        for i in range(2, n):
            if n % i == 0:
                return False
    return True


def print_prime():
    for i in range(1, 1000):
        if is_prime(i):
            print(i)


def bank(n, years, percent=10):
    for _ in range(years):
        n += round(n * percent / 100, 2)
    return n


def print_bank():
    n = 1000000
    years = (1, 5, 10, 25, 39)
    for y in years:
        print(n, y, bank(n, y))


def season(month):
    seasons = {
        (12, 1, 2): 'winter',
        (3, 4, 5): 'spring',
        (6, 7, 8): 'summer',
        (9, 10, 11): 'autemn',
    }
    for months, s in seasons.items():
        if month in months:
            return s
    return None


def print_seasons():
    for i in range(12):
        i += 1
        print(i, season(i))


def main():
    print_prime()
    print_bank()
    print_seasons()


if __name__ == '__main__':
    main()
