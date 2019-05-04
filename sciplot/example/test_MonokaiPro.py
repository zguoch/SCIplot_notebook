
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


def test_Lines():
    x = np.linspace(-2*np.pi, 2*np.pi, 100)
    y = np.sin(x)
    # mpl.rcParams["ytick.color"] = "red"
    plt.style.use(['MonokaiPro', 'keynote'])
    plt.figure()
    for i in range(0, 5):
        plt.plot(x+i*np.pi/4, y, label=str(i))
    plt.xlabel('Distance')
    plt.ylabel('Depth')
    plt.title('MonokaiPro')
    plt.text(0, 0.5, 'Point', va='center', ha='center')
    plt.savefig('test_MonokaiPro.pdf')
    plt.legend()
    plt.show()


# run test function
test_Lines()
