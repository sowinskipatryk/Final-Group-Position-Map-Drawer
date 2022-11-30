import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
# from matplotlib.colors import LinearSegmentedColormap

class Team:
    def __init__(self, name, mp, w, d, l, gs, gc, p):
        self.name = name
        self.mp = mp
        self.w = w
        self.d = d
        self.l = l
        self.gs = gs
        self.gc = gc
        self.p = p


class Match:
    def __init__(self, team1, team2):
        self.home = team1
        self.away = team2

    def add_result(self, score1, score2):
        self.home.gs += score1
        self.home.gc += score2
        self.away.gc += score1
        self.away.gs += score2

        if score1 > score2:
            self.home.w += 1
            self.away.l += 1
            self.home.p += 3
        elif score1 < score2:
            self.home.l += 1
            self.away.w += 1
            self.away.p += 3
        else:
            self.home.d += 1
            self.away.d += 1
            self.home.p += 1
            self.away.p += 1


class Table:
    def __init__(self, t1, t2, t3, t4):
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4

    def sort_teams(self):
        self.t1, self.t2, self.t3, self.t4 = sorted(
            [self.t1, self.t2, self.t3, self.t4],
            key=lambda t: (-t.p, -(t.gs - t.gc), -t.gs))

    def show_stats(self):
        for team in [self.t1, self.t2, self.t3, self.t4]:
            print(team.name, team.mp, team.w, team.d, team.l, team.gs, team.gc,
                  team.p)

    def show_advance(self):
        print(self.t1.name, self.t2.name)


class Simulation:
    def __init__(self):
        self.t1 = Team('POL', 1, 1, 1, 0, 2, 0, 4)
        self.t2 = Team('KSA', 1, 1, 0, 1, 2, 3, 3)
        self.t3 = Team('ARG', 1, 1, 0, 1, 3, 2, 3)
        self.t4 = Team('MEX', 1, 0, 1, 1, 0, 2, 1)
        self.table = Table(self.t1, self.t2, self.t3, self.t4)
        self.m1 = Match(self.t1, self.t3)
        self.m2 = Match(self.t2, self.t4)

    def simulate(self, r1, r2):
        h1, a1 = r1
        h2, a2 = r2
        self.m1.add_result(h1, a1)
        self.m2.add_result(h2, a2)
        self.table.sort_teams()
        # self.table.show_stats()
        # self.table.show_advance()

def get_position(obj):
    if obj.table.t1.name == 'POL':
        return 1
    if obj.table.t2.name == 'POL':
        return 2
    if obj.table.t3.name == 'POL':
        return 3
    if obj.table.t4.name == 'POL':
        return 4
    raise ValueError('This should not happen')

results = []
for i in range(5):
    for j in range(5):
        for k in range(5):
            for l in range(5):
                s = Simulation()
                # print(f'POL {i}:{j} ARG')
                # print(f'KSA {k}:{l} MEX')
                s.simulate((i, j), (k, l))
                results.append((f'{i}:{j}', f'{k}:{l}', get_position(s)))

df = pd.DataFrame(results)
df = pd.get_dummies(df.set_index([0, 1])).unstack()
df.columns = df.columns.droplevel(0)

# print(df)

cmap = sns.diverging_palette(130, 10, as_cmap=True)

# myColors = ((0.22, 0.52, 0.25, 1.0), (0.69, 0.80, 0.70, 1.0), (0.86, 0.3, 0.34, 1.0))
# cmap = LinearSegmentedColormap.from_list('Custom', myColors, len(myColors))

with sns.axes_style("white"):
    ax = sns.heatmap(df, annot=True, cmap=cmap, vmin=1, vmax=4, center=2.5,
                square=True, linewidths=.5, annot_kws={"size": 12})

plt.title("Poland's final Group C position")
plt.xlabel('KSA - MEX')
plt.ylabel('POL - ARG')
plt.show()
