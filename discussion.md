# Discussion

## [Bootstrap][BoSt] data

![N|Solid](https://github.com/vahagnh/tud18/blob/master/numberofbugs.png)

## [Pygame][PyGa] data

![N|Solid](numberofbugspygame.png)

## Analysis

| METRIC | CORRELATION Bootstrap | CORRELATION Pygame | MSE TRAIN Bootstrap | MSE TRAIN Pygame | MSE TEST Bootstrap | MSE TEST Pygame |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| BASE | 0.0012477272592731348 | 0.00010730238773770662 | 0.9459564104641988 | 0.02364395405456605 | 1.006673606471882 | 0.007832580253627765 |
| BASE + TOTAL | 0.02234222849032297 | 0.0005386617115646919 | 0.9259770029477598 | 0.023633753920033678 | 1.025374430912147 | 0.007879658530511842 |
| BASE + MINOR | 0.01937877224415474 | 0.0013935621067346915 | 0.9287838055050149 | 0.02361353852520891 | 1.2079000085464167 | 0.007183619186462648 |
| BASE + MINOR + MAJOR | 0.22584710883972514 | 0.0013935621067346915 | 0.733229760832356 | 0.02361353852520891 | 1.0510042954307408 | 0.007183619186462648 |
| BASE + MINOR + MAJOR + OWNERSHIP | 0.25218226758090667 | 0.0016777322605541212 | 0.7082867264966736 | 0.0236068188981163 | 1.0435597763348212 | 0.0072510773054636135 |

Correlation factors are pretty low. Usually we need values greater than 60% to conclude that there is a correlation.
We think that the quality of our data is not good enough :
* Pygame repo: not enough errors detected (bad time window, not many line deletions) and not so many contributors for the same file
* Bootstrap repo: many errors detected but not so sure about the quality of the detection

[BoSt]: <https://github.com/twbs/bootstrap>
[PyGa]: <https://github.com/pygame/>
