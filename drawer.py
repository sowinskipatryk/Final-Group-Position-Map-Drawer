import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def get_position(obj, teamname):
    if obj.table.t1.name == teamname:
        return 1
    if obj.table.t2.name == teamname:
        return 2
    if obj.table.t3.name == teamname:
        return 3
    if obj.table.t4.name == teamname:
        return 4
    raise ValueError('This should not happen')


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
        self.init_values = (mp, w, d, l, gs, gc, p)

    def __str__(self):
        return self.name

    def reset_score(self):
        self.mp, self.w, self.d, self.l, self.gs, self.gc, self.p = self.init_values


class Match:
    def __init__(self, team1, team2):
        self.home = team1
        self.away = team2

    def __str__(self):
        return f"{self.home} - {self.away}"

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
    def __init__(self, tm1, tm2, tm3, tm4):
        self.t1 = tm1
        self.t2 = tm2
        self.t3 = tm3
        self.t4 = tm4
        self.table = Table(self.t1, self.t2, self.t3, self.t4)
        self.m1 = Match(self.t1, self.t2)
        self.m2 = Match(self.t3, self.t4)

    def simulate(self, r1, r2):
        h1, a1 = r1
        h2, a2 = r2
        self.m1.add_result(h1, a1)
        self.m2.add_result(h2, a2)
        self.table.sort_teams()
        # self.table.show_stats()
        # self.table.show_advance()

def create_colormap(teams, group, title='', team='POL', max_goals=4):
    a, b, c, d = teams
    results = []
    for i in range(max_goals+1):
        for j in range(max_goals+1):
            for k in range(max_goals+1):
                for l in range(max_goals+1):
                    s = Simulation(a, b, c, d)
                    # print(f'{a} {i}:{j} {b}')
                    # print(f'{c} {k}:{l} {d}')
                    s.simulate((i, j), (k, l))
                    results.append((f'{i}:{j}', f'{k}:{l}', get_position(s, team)))
                    a.reset_score()
                    b.reset_score()
                    c.reset_score()
                    d.reset_score()

    df = pd.DataFrame(results)
    df = pd.get_dummies(df.set_index([0, 1])).unstack()
    df.columns = df.columns.droplevel(0)

    cmap = sns.diverging_palette(130, 10, as_cmap=True)

    with sns.axes_style("white"):
        ax = sns.heatmap(df, annot=True, cmap=cmap, vmin=1, vmax=4, center=2.5,
                    square=True, linewidths=.5, annot_kws={"size": 12})

    if title:
        plt.title(title)
    else:
        plt.title(f"{team}'s Final Group {group} Position")
    plt.xlabel(f'{c.name} - {d.name}')
    plt.ylabel(f'{a.name} - {b.name}')
    plt.show()


t1 = Team('Poland', 1, 1, 1, 0, 2, 0, 4)
t2 = Team('Saudi Arabia', 1, 1, 0, 1, 2, 3, 3)
t3 = Team('Argentina', 1, 1, 0, 1, 3, 2, 3)
t4 = Team('Mexico', 1, 0, 1, 1, 0, 2, 1)

create_colormap((t1,t3,t2,t4), 'C', team='Poland')
