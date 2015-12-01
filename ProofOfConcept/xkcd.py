_author_ = 'luke'

def xkcdify(plt):
    ax = plt.gca()
    ax.spines['bottom'].set_color('#91A2C4')
    ax.spines['top'].set_color('#91A2C4')
    ax.spines['left'].set_color('#91A2C4')
    ax.spines['right'].set_color('#91A2C4')
    ax.tick_params(axis='both', colors='#91A2C4')
    ax.xaxis.label.set_color('#91A2C4')
    ax.yaxis.label.set_color('#91A2C4')