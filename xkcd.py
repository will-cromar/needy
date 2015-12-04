XCKD_COLOR = '#91A2C4'

def xkcdify(plt):
    """
    Makes the given graph literally one XKCD
    :param plt: plot to xkcdify
    :return: None
    """
    ax = plt.gca()
    ax.spines['bottom'].set_color(XCKD_COLOR)
    ax.spines['top'].set_color(XCKD_COLOR)
    ax.spines['left'].set_color(XCKD_COLOR)
    ax.spines['right'].set_color(XCKD_COLOR)
    ax.tick_params(axis='both', colors=XCKD_COLOR)
    ax.xaxis.label.set_color(XCKD_COLOR)
    ax.yaxis.label.set_color(XCKD_COLOR)