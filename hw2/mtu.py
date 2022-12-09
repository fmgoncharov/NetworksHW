import subprocess
import sys


def main():
    # Обработка исключения
    if len(sys.argv) != 2:
        raise RuntimeError('Wrong amount of arguments in main')
    # Достаём хост из аргументов main
    hostname = sys.argv[1]
    # Задаём пороговые значения
    mtu_L, mtu_R = 10, 2000
    # Запускаем бинарный поиск по ответу на максимальный mtu
    while mtu_R - mtu_L > 1:
        mtu_M = (mtu_L + mtu_R) // 2
        print("Check:", mtu_M)
        # Пробуем пинг с заданным mtu
        result = subprocess.run(
            ['ping', hostname, '-M', 'do', '-s', str(mtu_M), '-c', '1'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode == 0:
            mtu_L = mtu_M
        elif result.returncode == 1:
            mtu_R = mtu_M
        else:
            # Обработка исключения
            raise RuntimeError('Error on ping')
    # Печатаем максимальный подошедший mtu
    print('Max MTU found:', mtu_L)


if __name__ == "__main__":
    main()
