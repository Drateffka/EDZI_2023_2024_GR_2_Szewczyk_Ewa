import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(context="notebook", style="darkgrid")


def skills_counter(skills_series: pd.Series) -> pd.DataFrame:
    skills_count = {}

    for skills in skills_series:
        for skill in skills:
            skills_count[skill] = (
                skills_count[skill] + 1 if skill in skills_count.keys() else 1
            )

    return pd.DataFrame({"skill": skills_count.keys(), "count": skills_count.values()})


def positions_counter(df: pd.DataFrame) -> pd.DataFrame:
    levels = ["Junior ", "", "Senior "]
    positions = [
        "Data Analyst",
        "Data Scientist",
        "Data Engineer",
        "Data Architect",
    ]

    whole = []
    for position in positions:
        for level in levels:
            pos = level + position
            whole.append(pos)

    df_trimmed = df[df.position.isin(whole)]
    means = (df_trimmed.min_wage + df_trimmed.max_wage) / 2
    df_trimmed = df_trimmed.assign(mean_wage=means)
    grouped = df_trimmed.groupby("position")[
        ["min_wage", "max_wage", "mean_wage", "source"]
    ].aggregate(
        {
            "source": np.count_nonzero,
            "min_wage": "min",
            "max_wage": "max",
            "mean_wage": "mean",
        }
    )

    result = grouped.reset_index().rename(columns={"source": "count"})

    return result


def save_results_one_json(df1, df2):
    file1 = "results/analysis.json"
    file2 = "results/temp.json"

    df1.to_json(file1, orient="records")
    df2.to_json(file2, orient="records")

    with open(file1, "r") as f1:
        data1 = json.load(f1)

    with open(file2, "r") as f2:
        data2 = json.load(f2)

    data1.extend(data2)

    with open(file1, "w") as f:
        json.dump(data1, f, indent=4)

    os.remove(file2)


def skills_plotter(skills: pd.DataFrame):
    skills_10 = skills.sort_values("count", ascending=False)[:10]

    fig = plt.figure("Umiejętności", figsize=[10, 7])
    ax = sns.barplot(skills_10, x="skill", y="count", palette="blend:#7AB,#EDA")
    ax.set(
        title="10 najbardziej pożądanych umiejętności/technologii",
        xlabel="Umiejętność/technologia",
        ylabel="Ilość wystąpień",
    )
    ax.bar_label(ax.containers[0], fontsize=10)

    # plt.show() (not needed in project 2)

    fig.savefig("results/skills.jpg")


def positions_plotter(positions: pd.DataFrame):

    mins = positions["min_wage"]
    maxs = positions["max_wage"]
    pos = positions["position"]

    fig = plt.figure(
        "Stanowiska",
        figsize=[10, 7],
    )
    ax = plt.axes()

    ax.set(
        title="Najważniejsze stanowiska i ich wynagrodzenia",
        xlabel="Stanowisko",
        ylabel="Wynagrodzenie [PLN]",
        ylim=[0, 50000],
    )

    for i in range(len(mins)):
        plt.axvline(
            x=pos[i],
            ymin=mins[i] / 50000,
            ymax=maxs[i] / 50000,
            color="#EDA",
        )

    plt.axvline(x="Data Analyst", ymin=0, ymax=0, color="#EDA", label="Zakres min-max")

    sns.scatterplot(
        positions,
        x="position",
        y="mean_wage",
        label="Średnia",
        s=100,
        ax=ax,
        color="#7AB",
    )

    plt.xticks(rotation=-10)
    plt.legend(title="Legenda", facecolor="white")
    # plt.show() (not needed in project 2)

    fig.savefig("results/stanowiska.jpg")
