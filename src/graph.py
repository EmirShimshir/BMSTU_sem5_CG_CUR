import matplotlib.pyplot as plt

x = [8, 32, 72, 128, 200, 288, 392, 512, 648, 800, 968, 1152, 1352, 1568]
y_guro = [134711, 158717, 184150, 206442, 250857, 300670, 369820, 440931, 523032, 604238, 704506, 812945, 935350,
          1054775]

y_fong = [920098, 963961, 1011580, 1072216, 1135146, 1245661, 1356393, 1477853, 1574341, 1722877, 1871794, 2009417,
          2162179, 2308075]

y_wave = [213, 785, 1753, 3112, 4843, 6988, 9506, 12387, 15489, 18840, 22818, 26544, 30861, 35217]


def wave():
    plt.plot(x, y_wave, 'r', marker='.')

    plt.xlabel('Количество полигонов на поверхности жидкости, штук')
    plt.ylabel('Время, мс')

    plt.legend()
    plt.grid(True)

    plt.savefig(f'./wave.pdf')


def draw():
    plt.plot(x, y_guro, 'r', label="Гуро", marker='.')
    plt.plot(x, y_fong, 'b', label="Фонг", marker='+')

    plt.xlabel('Количество полигонов на поверхности жидкости, штук')
    plt.ylabel('Время, мс')

    plt.legend()
    plt.grid(True)

    plt.savefig(f'./draw.pdf')


if __name__ == "__main__":
    # wave()
    draw()