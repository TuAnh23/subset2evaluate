# %%

import matplotlib.pyplot as plt
import utils_fig
import numpy as np

utils_fig.matplotlib_default()


def pred_irt(theta, item):
    return item["feas"] / (1 + np.exp(-item["disc"] * (theta - item["diff"])))


points_x = np.linspace(-3, 5.0, 100)
models = [-1, 4]

fig, axs = plt.subplots(4, 1, figsize=(3.5, 5), sharex=True)


def plot_item(ax, item, models=models):
    ax.plot(
        points_x,
        [pred_irt(theta, item) for theta in points_x],
        color="black",
        linewidth=2.5,
    )
    ax.scatter(
        models,
        [pred_irt(theta, item) for theta in models],
        color=utils_fig.COLORS[0],
        zorder=10,
    )
    ax.text(
        -2.7, 0.42,
        f"$b_x = {item['diff']:.1f}$\n$a_x = {item['disc']:.1f}$\n$c_x = {item['feas']:.1f}$",
        bbox=dict(facecolor='#ddd', edgecolor="white", pad=2),
    )


item = {"diff": 0.0, "disc": 1.0, "feas": 1.0}
plot_item(axs[0], item)
axs[0].annotate(
    "IRT predicts low\nscore for a model\nwith low ability",
    xy=(models[0], pred_irt(models[0], item)),
    xytext=(1.3, 0.4),
    arrowprops=dict(arrowstyle="->", color=utils_fig.COLORS[0]),
    fontstyle="italic",
    va="center",
)

item = {"diff": 3.0, "disc": 1.0, "feas": 1.0}
plot_item(axs[1], item)
axs[1].annotate(
    "Difficult ($b_x$) items,\nneed high $\\theta$s to      \npredict success     ",
    xy=(models[1], pred_irt(models[1], item)),
    xytext=(3, 0.7),
    arrowprops=dict(arrowstyle="->", color=utils_fig.COLORS[0]),
    fontstyle="italic",
    va="center",
    ha="right"
)


item = {"diff": 0.0, "disc": 9.0, "feas": 1.0}
plot_item(axs[2], item, models=[-0.2, 0.5])
axs[2].annotate(
    "Discriminative ($a_x$)\nitems distinguish\nbetween models of\nclose abilities ($\\theta$)",
    xy=(-0.2, pred_irt(-0.2, item)),
    xytext=(1.3, 0.4),
    arrowprops=dict(arrowstyle="->", color=utils_fig.COLORS[0]),
    fontstyle="italic",
    va="center",
    ha="left"
)
axs[2].annotate(
    "",
    xy=(0.5, pred_irt(0.5, item)),
    xytext=(1.2, 0.22),
    arrowprops=dict(arrowstyle="->", color=utils_fig.COLORS[0]),
)


item = {"diff": 0.0, "disc": 1.0, "feas": 0.8}
plot_item(axs[3], item)
axs[3].annotate(
    "Low feasibility ($c_x$)\nprevents any model from\never getting the full score.",
    xy=(models[1], pred_irt(models[1], item)),
    xytext=(5, 0.25),
    arrowprops=dict(arrowstyle="->", color=utils_fig.COLORS[0]),
    fontstyle="italic",
    va="center",
    ha="right"
)

for ax in axs.flatten():
    ax.set_xlim(-3, 5)
    ax.set_ylim(-0.1, 1.1)
    ax.set_ylabel("Success", labelpad=-2)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_yticklabels(['0%', '25%', '50%', '75%', '100%'])
    ax.spines[["top", "right"]].set_visible(False)

axs[3].set_xlabel("Model ability $\\theta$", labelpad=-1)

plt.tight_layout(pad=0.1, h_pad=0, w_pad=0.5)
plt.savefig("../figures_pdf/40-mock_irt.pdf")
plt.savefig("../figures_svg/40-mock_irt.svg")
plt.show()
