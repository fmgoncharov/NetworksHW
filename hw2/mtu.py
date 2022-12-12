import subprocess
import sys


def check(mtu, host):
    result = subprocess.run(
        ['ping', '-c', '5', '-M', 'do', '-s', str(mtu), host],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    return result.returncode


def main():
    # Обработка исключения
    if len(sys.argv) != 2:
        raise RuntimeError('Wrong amount of arguments in main')
    # Достаём хост из аргументов main
    hostname = sys.argv[1]
    # Проверяем доступность адреса назначения
    if check(0, hostname) != 0:
        raise RuntimeError('Destination not available')
    # Задаём пороговые значения
    mtu_L, mtu_R = 0, 2000
    # Запускаем бинарный поиск по ответу на максимальный mtu
    while mtu_R - mtu_L > 1:
        mtu_M = (mtu_L + mtu_R) // 2
        print("Check:", mtu_M)
        # Пробуем пинг с заданным mtu
        code = check(mtu_M, hostname)
        if code == 0:
            mtu_L = mtu_M
        elif code == 1:
            mtu_R = mtu_M
        else:
            # Обработка исключения
            raise RuntimeError('Error on ping')
    # Печатаем максимальный подошедший mtu с учётом размера хэдера IP и ICMP
    print('Max MTU found:', mtu_L + 28)


if __name__ == "__main__":
    main()
