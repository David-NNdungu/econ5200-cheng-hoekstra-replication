# AI Appendix — P.R.I.M.E. Review

## Preparation

I used ChatGPT while working through the replication and robustness checks. I focused on understanding the differences between specifications, checking the units and explaining what the results mean. This appendix summarises the questions and checks from that process.

## Request

The main questions I worked through were:

- Why does the coefficient match the paper while the default clustered standard error differs?
- How can I compare TWFE with an approach that does not use already-treated states as controls?
- Does changing the sample, weights or reference year change my conclusion?
- How should I explain a result that keeps the same sign but changes in size or precision?

## Iteration

I kept the original fractional-year treatment variable and population weights. I examined the standard-error correction rather than changing the model just to obtain a closer match. I also kept the comparison between binary and fractional exposure because the group-time calculation changes more than the estimator alone.

I revised my interpretation to separate three points: whether the sign stays positive, how much the magnitude changes, and how certain the estimate is. I kept the less precise specifications in the results instead of reporting only the significant ones.

## Mechanism Checks

I checked the sample size, treatment dates, positive homicide rates and population weights. I compared the first three weighted results with the paper and checked the conversion from log units to percentages.

The code was also checked on synthetic data with a known treatment effect. Selected bootstrap statistics were compared with direct regression calculations. Finally, the project was run in a separate environment after removing saved outputs to check that it could rebuild the results.

## Evaluation

My main conclusion is that the positive pooled result survives the checks I run, but I would be cautious about presenting one exact effect size. A pre-trend test that does not reject zero is not proof of parallel trends, and a positive pooled estimate does not establish a positive effect in every state.

The supporting response and source record follows below. This appendix is a summary of the review process, not a claim that it is an unedited export of the full conversation.


---

# Supporting Response and Source Record

# Supporting Response Record

## Response and resulting files

The response prepared the README, report, notebooks, code and supporting appendix. The material below records the resulting analytical text and source. It is a source-and-response archive, not an unedited transcript of every earlier chat message or tool call.

## Report text

# Castle Doctrine and Homicide: Replication and Reassessment

David Njihia Ndungu · ECON 5200 · Replication Study

## 1. Positioning

I study whether expanding self-defense laws reduces crime or makes confrontations more likely to end in a death. Both outcomes seem possible: the law could discourage an offender, but it could also make someone more willing to use lethal force. My focus is the expansion of self-defense protection outside the home. I also keep the reported homicide rate separate from the question of whether a particular killing was legally justified.

Cheng and Hoekstra (2013) use staggered state adoption to compare changes around policy expansion rather than interpret a cross-state crime correlation as causal. Their positive homicide finding challenges the deterrence account, while their estimates do not establish convincing reductions in burglary, robbery or aggravated assault. An aggregate homicide response does not by itself identify which individual encounters generated it.

I read three related studies to understand how the paper has been received. Miller and Pepper (2020) revisit the same policy setting and replicate related models. They show why the assumptions about what would have happened without the law matter. I take this as a reminder that a precise regression result is only as convincing as its comparison group and identifying assumptions.

Guettabi and Munasib (2018) use synthetic controls to study states separately. Their findings suggest that the effect is not the same everywhere. This made me want to check how much individual states affect the pooled estimate and whether population weights change the answer.

McClellan and Tekin (2017) study related laws using monthly mortality and injury data. Their results also raise doubts about the public-safety argument. However, they use different measures and a different time frequency, so I do not treat their study as an exact replication. These studies help me explain why a positive average effect does not necessarily mean the same effect in every state.

My identifying assumption is that, absent adoption, adopting and comparison states would have experienced comparable homicide changes conditional on the chosen fixed effects and controls. I also need no relevant anticipation or cross-state spillovers and defensible treatment dates. These are assumptions about unobserved outcomes, not consequences of including fixed effects. Modern staggered-adoption work adds a concern about heterogeneous treatment effects in two-way fixed-effects averages (Goodman-Bacon, 2021; Callaway and Sant’Anna, 2021). I use those tools to reassess the claim, while judging the original fairly against its period’s methods.


---

# 2. Direct Replication

I use 50 states over 2000–2010, giving 550 state-year observations: 21 adopters and 29 never-adopters. I retain the supplied fractional-year cdl treatment and average-population analytic weight. There are 21 partially exposed state-years. All homicide rates are positive, so no log-zero adjustment or row deletion is necessary.

My model is log(homicide rate) = state effect + time effect + β × fractional exposure + controls + error. SY uses common year effects; RY uses Census-region-by-year effects; RYX also includes the twelve supplied policing, incarceration, income, unemployment, poverty, spending and demographic controls. Covariance is clustered by state.

| Table 5, Panel A | Paper β | My β | Paper SE | My SE | β gap |
| --- | --- | --- | --- | --- | --- |
| SY | 0.0801 | 0.0801 | 0.0342 | 0.0342 | -0.00003649 |
| RY | 0.0946 | 0.0946 | 0.0279 | 0.0279 | -0.00001226 |
| RYX | 0.0937 | 0.0937 | 0.0290 | 0.0290 | -0.00002482 |

SY, RY and RYX reproduce columns 1, 2 and 3. I read the public author manuscript and cross-check those cells against NBER Working Paper 18134. These cells agree across the two versions; later columns differ, so I do not pool their benchmarks. Source values are transcribed in src/analysis.py.

For SY, β = 0.08006351 corresponds to 8.006 log points or 8.336% using 100 × (exp(β) − 1). Its 95% cluster-t interval in log units is [0.0113, 0.1488]. This is not a change in homicide counts or percentage points.

## Discrepancy log: what I checked

Rounding. The SY coefficient gap is -0.00003649 log units (-0.0456% relative to the printed value). All three coefficients and corrected SEs match at the paper’s displayed precision. I verify the complete panel, outcome definition, exposure coding and weights rather than treating the match as self-validating. The largest relative difference between popwt and mean state population is 5.21e-08, consistent with storage precision.

Software defaults. Default statsmodels state clustering gives the SY SE 0.03590, versus the paper’s 0.0342. My absorbed-effects correction gives 0.03422. The correction is G/(G−1) × (N−1)/(N−K*), with nested state effects excluded from K* except one intercept. For SY, N = 550, G = 50, full rank = 61 and K* = 12. This convention reproduces the three reported SEs. Because the article does not specify every software default, I document the inferred convention rather than claim to have rerun its original Stata command.


---

# 3. Robustness: Clean Comparisons

## Exercise 1 · Unconditional cohort-time DiD

What I did. For each adoption cohort and comparison year, I subtract the control group’s change since the last pre-adoption year from the cohort’s change. Controls are never-treated or not-yet-treated states; already-treated states never serve as controls. I average post-adoption cells with cohort-population weights, so earlier cohorts contribute more observed post years. Uncertainty comes from resampling entire state histories.

| Estimator | β | SE | 95% interval |
| --- | --- | --- | --- |
| TWFE fractional exposure | 0.0801 | 0.0342 | [0.0113, 0.1488] |
| TWFE binary exposure | 0.0594 | 0.0276 | [0.0040, 0.1148] |
| Group-time never | 0.1082 | 0.0247 | [0.0592, 0.1549] |
| Group-time notyet | 0.1095 | 0.0243 | [0.0618, 0.1553] |

TWFE intervals use a state-cluster t reference. Cohort-time intervals are percentile intervals from 999 whole-state bootstrap draws. This is an unconditional two-by-two implementation inspired by the starter and group-time framework, not the full conditional or doubly robust Callaway–Sant’Anna estimator.

What I found. Both clean-comparison averages are positive. Binary exposure also changes the conventional TWFE estimate, providing a bridge between the published dose regression and the group-time comparison. I therefore do not attribute the entire difference between the published estimate and the cohort-time average to forbidden comparisons.

What it implies. I still find a positive effect when already-treated states are not used as controls. I am more cautious about the size of the effect because the exercise also changes the weights, treatment coding and controls. It is therefore not a direct replacement for the fully adjusted regression. The earliest adoption group contains only one state, which also limits what its bootstrap comparison can tell me.

## Treatment timing matters

The adoption-year cohort-time cell includes partial exposure, whereas the original regression coefficient scales a full year of exposure. Redefining treatment as the first full year and then using the partly treated adoption year as a baseline would contaminate that reference. I retain the last fully untreated year and show the first full post-adoption year separately in Exercise 2.


---

# 3. Robustness: Event Time

## Exercise 2 · Balanced cohorts and a different reference year

What I did. I plot relative years −4 through +1 so that every point is supported by the same adoption cohorts. I use never-treated controls, fixed population weights and the last pre-adoption year as the reference. I then re-anchor to two years before adoption to examine whether the final untreated year is unusual.

Figure 1. Pointwise 95% whole-state bootstrap intervals; −1 is normalized. These are not simultaneous bands.

![Figure 1. Pointwise 95% whole-state bootstrap intervals; −1 is normalized. These are not simultaneous bands.](../output/event_study.png)

| Relative year | Estimate | 95% interval |
| --- | --- | --- |
| -4 | 0.0246 | [-0.0555, 0.0988] |
| -3 | 0.0480 | [-0.0134, 0.1073] |
| -2 | 0.0362 | [-0.0174, 0.0904] |
| -1 | 0.0000 | [0.0000, 0.0000] |
| 0 | 0.0537 | [-0.0114, 0.1111] |
| 1 | 0.1358 | [0.0810, 0.1952] |

What I found. A joint pre-adoption Wald statistic is 3.138 on 3 restrictions (p = 0.371), using the bootstrap covariance. The first-full-year estimate is 0.1358; with the earlier reference it is 0.0996.

What it implies. The pre-period estimates are above the final untreated year, and re-anchoring lowers the post-adoption contrast. The sign survives, but the magnitude depends on the reference. Failure to reject the pre-adoption null does not establish parallel trends: the intervals permit important differences, and this short panel has limited power.


---

# 3. Robustness: Specification Curve

## Exercise 3 · Retain every model in a declared grid

What I did. I define all combinations of three samples (all states, no Florida, no South), population or equal state weights, common year or region-by-year effects, and no time-varying controls or the full supplied set. These choices produce 24 models. I retain every estimate and interval. The systematic grid and interactions are the extension; weighting and regional controls alone were already examined by the original authors.

Figure 2. Blue: population weights; amber: equal weights. Dashed: weighted region-year baseline. Intervals are model-specific, not multiplicity-adjusted.

![Figure 2. Blue: population weights; amber: equal weights. Dashed: weighted region-year baseline. Intervals are model-specific, not multiplicity-adjusted.](../output/specification_curve.png)

What I found. Coefficients range from 0.0600 to 0.1639 log units. All 24 of 24 point estimates are positive, but only 8 reject zero at 5% under the stated state-cluster convention.

| Sample | Smallest β in grid | SE |
| --- | --- | --- |
| All states | 0.0600 | 0.0684 |
| No Florida | 0.0602 | 0.0706 |
| No South | 0.0913 | 0.0522 |

What it implies. The positive sign does not depend on just one specification in my grid. The size and precision of the estimate do change. Removing the South changes the states represented, while changing weights gives small and large states different importance. These models therefore do not all estimate exactly the same average effect. I also do not treat the number of significant models as a probability that the paper is correct.


---

# 3. Robustness: State Influence

## Exercise 4 · Delete one complete state at a time

What I did. I rerun the population-weighted region-year model after omitting each state history once. This provides a full influence profile instead of selecting a salient state after seeing its result. Influence does not establish that an observation is erroneous.

Figure 3. Each point is a separate 49-state fit. The complete deletion profile is saved as leave_one_state_out.csv.

![Figure 3. Each point is a separate 49-state fit. The complete deletion profile is saved as leave_one_state_out.csv.](../output/state_influence.png)

| Omitted state | β | Change | 95% interval |
| --- | --- | --- | --- |
| Florida | 0.0832 | -0.0114 | [0.0241, 0.1423] |
| Minnesota | 0.0833 | -0.0113 | [0.0283, 0.1382] |
| Indiana | 0.1046 | +0.0100 | [0.0467, 0.1625] |
| Michigan | 0.1059 | +0.0113 | [0.0470, 0.1648] |

What I found. The all-state region-year estimate is 0.0946. Across state deletions, it ranges from 0.0832 to 0.1059. Omitting Florida gives 0.0832, a change of -0.0114.

What it implies. My positive pooled estimate is not driven by Florida alone. However, this does not show that the law raised homicide in every state. Dropping a state changes both the comparison group and the weights. A factor affecting several adopting states could still explain part of the result.


---

# 3. Robustness: Inference

## Exercise 5 · A null-imposed wild cluster bootstrap

What I did. In the region-year model, I impose a zero treatment effect by fitting the nuisance regressors without cdl. I multiply restricted weighted residuals by one Rademacher sign per state, rebuild outcomes, refit and studentise using the same state-cluster convention. I compare the observed statistic with the simulated absolute statistics, using a plus-one tail correction and a fixed seed.

| Inference method | Result |
| --- | --- |
| State-cluster t p-value | 0.00137 |
| Restricted wild-cluster p-value | 0.00350 |
| Bootstrap draws | 1999 |
| Approximate Monte Carlo SE of bootstrap p | 0.00132 |

What I found. Both p-values fall below 5%. I verify selected vectorised bootstrap t-statistics against direct regressions and sandwich calculations. Resampling changes the reference distribution, not the fitted coefficient or the assumed source of policy variation.

What it implies. The positive region-year estimate is not an artifact of relying only on the asymptotic p-value. This does not repair a violation of parallel trends or account for arbitrary cross-state shocks. Fifty total states do not guarantee ideal inference if identifying variation is concentrated among relatively few adopters.

## Additional falsification diagnostics, not a novel extension

| Log outcome | Region-year FE | β | 95% interval |
| --- | --- | --- | --- |
| l_larceny | False | 0.0030 | [-0.0294, 0.0354] |
| l_larceny | True | -0.0066 | [-0.0361, 0.0229] |
| l_motor | False | 0.0517 | [-0.0614, 0.1647] |
| l_motor | True | -0.0389 | [-0.1290, 0.0513] |

Larceny and motor-vehicle theft follow the paper’s falsification logic, but neither is guaranteed unaffected. Motor theft changes sign when regional time controls enter. I keep that fixed-effect comparison visible and do not read a different estimator’s placebo as though only the treatment-comparison rule changed. A non-rejection is not a validation certificate.


---

# 4. Does the Finding Hold?

My answer is yes on the direction of the pooled result, but I am less certain about its exact size. I reproduce the paper’s weighted coefficients at the reported precision and explain the small numerical differences. My robustness checks also give positive estimates, including when I leave out individual states.

I conclude that these laws are associated with higher reported homicide in this sample, provided the comparison assumptions hold. I cannot say that the effect is the same in every state or that the exact national increase is always eight percent. I also cannot determine whether the additional deaths were legally justified. The specification curve and reference-year exercise show why I would report a range of estimates rather than rely on one number.

Further work would need a longer pre-adoption panel, independently verified legal dates, regional untreated trends without already-treated comparisons, and evidence about concurrent policy changes. Those are next steps, not exercises I claim to have run. The original authors already undertook substantial sensitivity work; the extensions here reassess the result rather than assume that later methods automatically overturn it.

## 5. Peer Audit

I am assigned to audit Roman Carrubba’s replication of Card (1995); Julia Clark is assigned to audit my Cheng–Hoekstra repository. Roman’s repository URL is still needed. The audit issue is due Sunday 22 November at 11:59 pm, while the project deadline remains Thursday 19 November at 11:59 pm. I will test the final version from a clean checkout, file an approximately 300-word GitHub issue on reproducibility, one methodological question and one practice to adopt, and add its URL to my Canvas submission comment. The peer run and issue have not yet been completed.

## 6. Reproducibility

After installing the pinned requirements, python reproduce.py verifies the data checksum, reruns estimation, writes every table and figure, generates this PDF and refreshes the executed notebooks. Data are included with the Mixtape licence notice; download_data.py can recover the same pinned bytes if absent. The README records the measured runtime and project map.

The README describes the reproduction command, runtime, data provenance and project layout. My public repository link must be available to Julia, and the peer audit will be completed once Roman’s final repository URL is available.


---

# References and Source Notes

Cheng, C., and M. Hoekstra (2013). Does Strengthening Self-Defense Law Deter Crime or Escalate Violence? Evidence from Expansions to Castle Doctrine. Journal of Human Resources 48(3): 821–854.

https://doi.org/10.1353/jhr.2013.0023

Cheng, C., and M. Hoekstra (2012). Public working-paper version, NBER Working Paper 18134. Table 5, Panel A, columns 1–3 are the numerical benchmarks, also verified in the later author manuscript.

https://www.nber.org/papers/w18134

Miller, M., and J. Pepper (2020). Assessing the Effect of Firearms Regulations Using Partial Identification Methods: A Case Study of the Impact of Stand Your Ground Laws on Violent Crime. Law and Contemporary Problems 83(3): 213–230.

https://scholarship.law.duke.edu/lcp/vol83/iss3/12/

Guettabi, M., and A. Munasib (2018). Stand Your Ground laws, homicides and gun deaths. Regional Studies 52(9): 1250–1260.

https://doi.org/10.1080/00343404.2017.1371846

McClellan, C., and E. Tekin (2017). Stand Your Ground Laws, Homicides, and Injuries. Journal of Human Resources 52(3): 621–653. Public version: NBER Working Paper 18187.

https://www.nber.org/papers/w18187

Goodman-Bacon, A. (2021). Difference-in-differences with variation in treatment timing. Journal of Econometrics 225(2): 254–277.

https://doi.org/10.1016/j.jeconom.2021.03.014

Callaway, B., and P. H. C. Sant’Anna (2021). Difference-in-Differences with multiple time periods. Journal of Econometrics 225(2): 200–230.

https://doi.org/10.1016/j.jeconom.2020.12.001

Cunningham, S., Mixtape data repository. Public castle.dta and repository licence. The package pins the data revision and verifies SHA-256 before estimation.

https://github.com/scunning1975/mixtape

Ryan Piao, ECON 5200 replication materials. The repository layout and Cheng–Hoekstra starter inform the structure and the unconditional cohort-time comparison. My implementation and additional diagnostics are supplied in this package.

https://github.com/RyanPiao/econ5200-replication-template

## Numerical source map

Headline: output/headline_table.csv. Cohort-time estimates: estimator_comparison.csv and group_time_*.csv. Event study: balanced_event_study.csv and pretrend_test.json. Specifications: specification_curve.csv. Influence: leave_one_state_out.csv. Inference: inference.csv and wild_bootstrap_draws.csv. Placebos: placebo_outcomes.csv. Every empirical report value is constructed by the pipeline.

The numerical benchmarks are Table 5, Panel A, columns 1–3. The public NBER version and later author manuscript agree on these cells. Article PDFs are not redistributed in the code archive; the references supply access paths.


## Source: download_data.py

```python
"""Fetch and verify the public data revision used in the replication."""
from pathlib import Path
import hashlib
import urllib.request
SOURCE = 'https://raw.githubusercontent.com/scunning1975/mixtape/9471dd0c45477386bf208516882895af340f3d33/castle.dta'
SHA256 = '804633c161827b6c0824f86f239046386d1a8266a866f83bf5ddb2aa762a5f29'
def ensure_data(root=None):
    root=Path(__file__).resolve().parent if root is None else Path(root)
    target=root/'data/castle.dta';target.parent.mkdir(exist_ok=True)
    if not target.exists():
        with urllib.request.urlopen(SOURCE,timeout=60) as response:
            content=response.read()
        if hashlib.sha256(content).hexdigest()!=SHA256:
            raise ValueError('Downloaded data do not match the documented checksum.')
        target.write_bytes(content)
    if hashlib.sha256(target.read_bytes()).hexdigest()!=SHA256:
        raise ValueError('Data checksum differs; do not silently substitute another version.')
    return target
if __name__=='__main__':
    print(ensure_data())

```


## Source: reproduce.py

```python
"""Regenerate the analysis, PDF report and executed notebooks with one command."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import json
import time
import pandas as pd
from download_data import ensure_data
from src.analysis import run
from src.report import build_report
from src.notebooks import build_notebooks
def main():
    root=Path(__file__).resolve().parent;start=time.perf_counter()
    ensure_data(root)
    summary=run(root)
    build_report(root,summary)
    build_notebooks(root,summary)
    print('\nHeadline replication (coefficients in log units):')
    print(pd.read_csv(root/'output/headline_table.csv')[['model','paper_beta','replication_beta','paper_se','replication_se','coefficient_gap']].to_string(index=False,float_format='{:.8f}'.format))
    elapsed=time.perf_counter()-start
    (root/'output/run_time.json').write_text(json.dumps({'seconds':elapsed},indent=2))
    print(f'End-to-end runtime: {elapsed:.2f} seconds')
    print('Report: report/Castle_Doctrine_Replication.pdf')
if __name__=='__main__':
    main()

```


## Source: src/analysis.py

```python
"""Castle-doctrine replication and prespecified sensitivity exercises."""
from pathlib import Path
import hashlib
import itertools
import json
import time

import numpy as np
import pandas as pd
import scipy.linalg as la
from scipy.stats import t as student_t, chi2
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_cluster
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

CONTROLS = ['l_police', 'l_income', 'unemployrt', 'poverty', 'l_prisoner',
            'l_lagprisoner', 'l_exp_subsidy', 'l_exp_pubwelfare',
            'blackm_15_24', 'whitem_15_24', 'blackm_25_44', 'whitem_25_44']
PAPER = {'SY': (0.0801, 0.0342), 'RY': (0.0946, 0.0279), 'RYX': (0.0937, 0.0290)}


def design(data, region=False, controls=False, treatment='cdl'):
    """Full-rank design: retain treatment, prune only redundant nuisance indicators."""
    d = data.reset_index(drop=True).copy()
    if 'region' not in d:
        d['region'] = d[['northeast', 'midwest', 'south', 'west']].idxmax(axis=1)
    nuisance = [pd.DataFrame({'const': np.ones(len(d))}),
                pd.get_dummies(d.sid.astype(str), prefix='state', drop_first=True, dtype=float)]
    time_key = d.region.astype(str) + '_' + d.year.astype(str) if region else d.year.astype(str)
    nuisance.append(pd.get_dummies(time_key, prefix='time', drop_first=True, dtype=float))
    if controls:
        nuisance.append(d[CONTROLS].astype(float))
    z = pd.concat(nuisance, axis=1)
    _, r, piv = la.qr(z.to_numpy(), mode='economic', pivoting=True)
    rank = np.linalg.matrix_rank(r)
    z = z.iloc[:, sorted(piv[:rank])]
    X = pd.concat([d[[treatment]].astype(float), z], axis=1)
    if np.linalg.matrix_rank(X.to_numpy()) != X.shape[1]:
        raise ValueError('Treatment is not identified after fixed effects.')
    return d, X


def fit_model(data, region=False, controls=False, weighted=True, outcome='l_homicide', treatment='cdl'):
    d, X = design(data, region, controls, treatment)
    w = d.popwt.to_numpy(dtype=float) if weighted else np.ones(len(d))
    # Normalising analytic weights has no effect on beta or the cluster sandwich.
    w /= w.mean()
    fit = sm.WLS(d[outcome].astype(float), X, weights=w).fit()
    n, rank = X.shape
    groups = d.sid.to_numpy()
    G = d.sid.nunique()
    # State FE are nested in the state clusters. Count the nonabsorbed rank,
    # including one intercept, for the small-sample correction used here.
    k_absorbed = rank - (G - 1)
    correction = G / (G - 1) * (n - 1) / (n - k_absorbed)
    covariance = cov_cluster(fit, groups, use_correction=False) * correction
    j = X.columns.get_loc(treatment)
    beta = float(fit.params.iloc[j])
    se = float(np.sqrt(covariance[j, j]))
    critical = student_t.ppf(.975, G - 1)
    default_se = float(np.sqrt(cov_cluster(fit, groups, use_correction=True)[j, j]))
    result = {'beta': beta, 'se': se, 'lo': beta-critical*se, 'hi': beta+critical*se,
              'p': float(2*student_t.sf(abs(beta/se), G-1)), 'exact_pct': float(100*np.expm1(beta)),
              'n': n, 'clusters': G, 'rank': rank, 'k_absorbed': k_absorbed,
              'default_cluster_se': default_se, 'correction': correction}
    return result, fit, d, X


def arrays(data, outcome='l_homicide', weighted=True):
    states = np.sort(data.sid.unique())
    years = np.sort(data.year.unique())
    panel = data.pivot(index='sid', columns='year', values=outcome).loc[states, years]
    if panel.isna().any().any():
        raise ValueError('Group-time calculations require a complete outcome panel.')
    by_state = data.groupby('sid').first().loc[states]
    return (panel.to_numpy(dtype=float), by_state.effyear.to_numpy(dtype=float),
            by_state.popwt.to_numpy(dtype=float) if weighted else np.ones(len(states)), years)


def group_time(Y, cohort, weights, years, control='never', counts=None, base_offset=-1, balanced=False):
    """Unconditional two-by-two cohort/year DIDs, not conditional/doubly-robust CS."""
    w = weights.copy() if counts is None else weights * counts
    cells = []
    for g in np.sort(np.unique(cohort[np.isfinite(cohort)])):
        treated = cohort == g
        if w[treated].sum() == 0:
            continue
        base = int(g + base_offset)
        if base not in years:
            continue
        b = int(np.flatnonzero(years == base)[0])
        for j, year in enumerate(years):
            e = int(year-g)
            if year == base or (balanced and not -4 <= e <= 1):
                continue
            comparison = np.isnan(cohort) if control == 'never' else (np.isnan(cohort) | (cohort > max(year, base)))
            comparison &= ~treated
            if w[comparison].sum() == 0:
                continue
            delta = Y[:,j] - Y[:,b]
            att = np.average(delta[treated], weights=w[treated]) - np.average(delta[comparison], weights=w[comparison])
            cells.append((int(g), int(year), e, float(att), float(w[treated].sum())))
    frame = pd.DataFrame(cells, columns=['cohort','year','event','att','weight'])
    post = frame[frame.event >= 0]
    overall = np.average(post.att, weights=post.weight)
    events = {int(e): float(np.average(f.att, weights=f.weight)) for e,f in frame.groupby('event')}
    return float(overall), events, frame


def group_bootstrap(Y, cohort, weights, years, reps=999, seed=20261119, **kwargs):
    """Resample whole state histories; retain estimated weights and composition per draw."""
    rng = np.random.default_rng(seed)
    estimates, events = [], []
    for _ in range(reps):
        counts = rng.multinomial(len(cohort), np.repeat(1/len(cohort), len(cohort)))
        estimate, by_e, _ = group_time(Y,cohort,weights,years,counts=counts,**kwargs)
        estimates.append(estimate)
        events.append(by_e)
    return np.asarray(estimates), pd.DataFrame(events)


def wild_bootstrap(data, region=True, reps=1999, seed=20261120):
    result, fit, d, Xframe = fit_model(data, region=region)
    X = fit.model.wexog
    y = fit.model.wendog
    j = Xframe.columns.get_loc('cdl')
    Z = np.delete(X,j,axis=1)
    fitted_null = Z @ np.linalg.lstsq(Z,y,rcond=None)[0]
    residual_null = y-fitted_null
    ids = pd.factorize(d.sid)[0]
    G = len(np.unique(ids))
    rng = np.random.default_rng(seed)
    weights = rng.choice([-1.,1.],size=(reps,G))
    ys = fitted_null[None,:] + residual_null[None,:]*weights[:,ids]
    bread = np.linalg.inv(X.T@X)
    betas = ys@X@bread
    residuals = ys-betas@X.T
    influence = X@bread[:,j]
    scores = np.column_stack([(residuals[:,ids==g]*influence[ids==g]).sum(axis=1) for g in range(G)])
    se_star = np.sqrt(result['correction']*(scores**2).sum(axis=1))
    t_star = betas[:,j]/se_star
    observed = result['beta']/result['se']
    exceed = int((np.abs(t_star) >= abs(observed)).sum())
    p = (exceed+1)/(reps+1)
    # Validate the vectorised sandwich against direct WLS computations.
    for b in [0, reps//2, reps-1]:
        direct = sm.OLS(ys[b],X).fit()
        v = cov_cluster(direct,ids,use_correction=False)*result['correction']
        assert np.isclose(t_star[b],direct.params[j]/np.sqrt(v[j,j]),rtol=1e-7,atol=1e-8)
    return {'beta':result['beta'],'cluster_se':result['se'],'cluster_t_p':result['p'],
            'wild_p':float(p),'wild_mc_se':float(np.sqrt(p*(1-p)/reps)),
            'draws':reps,'exceedances':exceed,'seed':seed}, pd.DataFrame({'t_star':t_star})


def run(root):
    start = time.perf_counter()
    out = Path(root)/'output'
    out.mkdir(exist_ok=True)
    data = pd.read_stata(Path(root)/'data/castle.dta', convert_categoricals=False)
    assert len(data)==550 and data.sid.nunique()==50 and not data.duplicated(['sid','year']).any()
    data['region'] = data[['northeast','midwest','south','west']].idxmax(axis=1)
    rows=[]
    for label,region,controls in [('SY',False,False),('RY',True,False),('RYX',True,True)]:
        r,*_ = fit_model(data,region,controls)
        paper_b,paper_se = PAPER[label]
        rows.append({'model':label,'paper_beta':paper_b,'replication_beta':r['beta'],
                     'coefficient_gap':r['beta']-paper_b,'relative_gap_pct':100*(r['beta']-paper_b)/paper_b,
                     'paper_se':paper_se,'replication_se':r['se'],'se_gap':r['se']-paper_se,**r})
    headline=pd.DataFrame(rows)
    headline.to_csv(out/'headline_table.csv',index=False)
    cohort=data.groupby('sid').effyear.first()
    cohort.value_counts(dropna=False).rename_axis('cohort').reset_index(name='states').to_csv(out/'adoption_counts.csv',index=False)
    characteristics={'n':len(data),'states':int(data.sid.nunique()),'first_year':int(data.year.min()),
      'last_year':int(data.year.max()),'adopters':int(cohort.notna().sum()),'never':int(cohort.isna().sum()),
      'partial_rows':int(((data.cdl>0)&(data.cdl<1)).sum()),'positive_homicide':bool((data.homicide>0).all()),
      'weight_max_relative_diff_from_mean_pop':float(np.max(np.abs(data.groupby('sid').popwt.first()-data.groupby('sid').population.mean())/data.groupby('sid').population.mean()))}
    (out/'data_checks.json').write_text(json.dumps(characteristics,indent=2))
    Y,g,w,years=arrays(data)
    group_rows=[]
    event_outputs={}
    for control in ['never','notyet']:
        att,events,cells=group_time(Y,g,w,years,control=control)
        boot,boot_events=group_bootstrap(Y,g,w,years,control=control)
        group_rows.append({'model':'Group-time '+control,'beta':att,'se':float(boot.std(ddof=1)),
                          'lo':float(np.quantile(boot,.025)),'hi':float(np.quantile(boot,.975)),
                          'exact_pct':float(100*np.expm1(att)),'bootstrap_draws':len(boot)})
        cells.to_csv(out/f'group_time_{control}.csv',index=False)
        pd.DataFrame({'draw':boot}).to_csv(out/f'bootstrap_{control}.csv',index=False)
        event_outputs[control]=(events,boot_events)
    # Binary TWFE isolates treatment-dose coding from the estimator change.
    data['any_exposure']=(data.year>=data.effyear).astype(float)
    r,*_=fit_model(data,treatment='any_exposure')
    group_rows.insert(0,{'model':'TWFE binary exposure',**r})
    r,*_=fit_model(data)
    group_rows.insert(0,{'model':'TWFE fractional exposure',**r})
    gt=pd.DataFrame(group_rows)
    gt.to_csv(out/'estimator_comparison.csv',index=False)
    # Cohort-balanced event window: all five cohorts observed at every plotted e.
    _,bal_events,bal_cells=group_time(Y,g,w,years,balanced=True)
    bal_boot,bal_be=group_bootstrap(Y,g,w,years,balanced=True)
    _,alternate,_=group_time(Y,g,w,years,balanced=True,base_offset=-2)
    es=[]
    for e in range(-4,2):
        if e==-1:
            es.append({'event':e,'beta':0.,'se':0.,'lo':0.,'hi':0.,'alternate_reference':alternate[e]})
            continue
        es.append({'event':e,'beta':bal_events[e],'se':bal_be[e].std(ddof=1),
                   'lo':bal_be[e].quantile(.025),'hi':bal_be[e].quantile(.975),
                   'alternate_reference':alternate.get(e,0.)})
    event=pd.DataFrame(es)
    event.to_csv(out/'balanced_event_study.csv',index=False)
    pre=np.array([bal_events[e] for e in [-4,-3,-2]])
    covariance=bal_be[[-4,-3,-2]].cov().to_numpy()
    pre_wald=float(pre@np.linalg.pinv(covariance)@pre)
    pretest={'wald':pre_wald,'df':3,'p':float(chi2.sf(pre_wald,3)),
             'balanced_e1':float(bal_events[1]),'e1_reference_minus2':float(alternate[1])}
    (out/'pretrend_test.json').write_text(json.dumps(pretest,indent=2))
    specs=[]
    samples={'All states':data,'No Florida':data[data.state!='Florida'],
             'No South':data[data.region!='south']}
    for sample,weighted,region,controls in itertools.product(samples,[True,False],[False,True],[False,True]):
        r,*_=fit_model(samples[sample],region,controls,weighted)
        specs.append({'sample':sample,'weighted':weighted,'region_year':region,'controls':controls,**r})
    curve=pd.DataFrame(specs)
    curve.to_csv(out/'specification_curve.csv',index=False)
    # Use RY for the influence exercise, avoiding nuisance-control misspecification.
    base=fit_model(data,region=True)[0]
    loo=[]
    for state in sorted(data.state.unique()):
        r,*_=fit_model(data[data.state!=state],region=True)
        loo.append({'omitted_state':state,'change':r['beta']-base['beta'],**r})
    loo=pd.DataFrame(loo).sort_values('beta')
    loo.to_csv(out/'leave_one_state_out.csv',index=False)
    inference,draws=wild_bootstrap(data)
    pd.DataFrame([inference]).to_csv(out/'inference.csv',index=False)
    draws.to_csv(out/'wild_bootstrap_draws.csv',index=False)
    # Original-style placebo crime, diagnostic only (not counted as a novel extension).
    placebo=[]
    for outcome in ['l_larceny','l_motor']:
        for region in [False,True]:
            r,*_=fit_model(data,region=region,outcome=outcome)
            placebo.append({'outcome':outcome,'region_year':region,**r})
    pd.DataFrame(placebo).to_csv(out/'placebo_outcomes.csv',index=False)

    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(8,3.8))
    ax.errorbar(event.event,event.beta,yerr=[event.beta-event.lo,event.hi-event.beta],fmt='o-',color='#174C68',capsize=3)
    ax.axhline(0,color='gray',lw=1);ax.axvline(-.5,color='gray',ls='--',lw=1)
    ax.set(xlabel='Years relative to adoption (−1 is the reference)',ylabel='Log homicide rate difference',title='Cohort-balanced group-time event study')
    fig.tight_layout();fig.savefig(out/'event_study.png',dpi=180);plt.close(fig)
    ordered=curve.sort_values('beta').reset_index(drop=True)
    fig,ax=plt.subplots(figsize=(8,3.8))
    colors=np.where(ordered['weighted'],'#174C68','#B97B30')
    for i,row in ordered.iterrows():
        ax.plot([i,i],[row.lo,row.hi],color=colors[i],alpha=.65)
    ax.scatter(ordered.index,ordered.beta,c=colors,s=24)
    ax.axhline(0,color='gray',lw=1);ax.axhline(base['beta'],color='#174C68',ls='--',label='Weighted region-year baseline')
    ax.set(xlabel='Prespecified specification, sorted by coefficient',ylabel='Coefficient on fractional exposure',title='24-model specification curve (95% state-cluster intervals)')
    ax.legend(fontsize=8);fig.tight_layout();fig.savefig(out/'specification_curve.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,3.8))
    ax.plot(np.arange(len(loo)),loo.beta,'o',color='#174C68',ms=4)
    ax.axhline(base['beta'],color='gray',ls='--',label='All states')
    for state in ['Florida','Texas','California']:
        idx=int(np.flatnonzero(loo.omitted_state.to_numpy()==state)[0]);ax.annotate(state,(idx,loo.iloc[idx].beta),xytext=(3,7),textcoords='offset points',fontsize=8)
    ax.set(xlabel='Omitted state, sorted by resulting coefficient',ylabel='Coefficient on fractional exposure',title='Leave-one-state-out sensitivity: region-year model')
    fig.tight_layout();fig.savefig(out/'state_influence.png',dpi=180);plt.close(fig)
    summary={'headline':headline.to_dict('records'),'group':gt.to_dict('records'),'pretrend':pretest,
             'curve_min':float(curve.beta.min()),'curve_max':float(curve.beta.max()),
             'curve_positive':int((curve.beta>0).sum()),'curve_significant':int((curve.p<.05).sum()),
             'loo_min':float(loo.beta.min()),'loo_max':float(loo.beta.max()),
             'no_florida':loo[loo.omitted_state=='Florida'].iloc[0].to_dict(),
             'inference':inference,'data':characteristics,'analysis_seconds':time.perf_counter()-start}
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    return summary

```


## Source: src/report.py

```python
"""Generate the report from analysis outputs rather than hand-entered estimates."""
from pathlib import Path
import html
import pandas as pd
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

REFERENCES=[
('Cheng, C., and M. Hoekstra (2013)', 'Does Strengthening Self-Defense Law Deter Crime or Escalate Violence? Evidence from Expansions to Castle Doctrine. Journal of Human Resources 48(3): 821–854.', 'https://doi.org/10.1353/jhr.2013.0023'),
('Cheng, C., and M. Hoekstra (2012)', 'Public working-paper version, NBER Working Paper 18134. Table 5, Panel A, columns 1–3 are the numerical benchmarks, also verified in the later author manuscript.', 'https://www.nber.org/papers/w18134'),
('Miller, M., and J. Pepper (2020)', 'Assessing the Effect of Firearms Regulations Using Partial Identification Methods: A Case Study of the Impact of Stand Your Ground Laws on Violent Crime. Law and Contemporary Problems 83(3): 213–230.', 'https://scholarship.law.duke.edu/lcp/vol83/iss3/12/'),
('Guettabi, M., and A. Munasib (2018)', 'Stand Your Ground laws, homicides and gun deaths. Regional Studies 52(9): 1250–1260.', 'https://doi.org/10.1080/00343404.2017.1371846'),
('McClellan, C., and E. Tekin (2017)', 'Stand Your Ground Laws, Homicides, and Injuries. Journal of Human Resources 52(3): 621–653. Public version: NBER Working Paper 18187.', 'https://www.nber.org/papers/w18187'),
('Goodman-Bacon, A. (2021)', 'Difference-in-differences with variation in treatment timing. Journal of Econometrics 225(2): 254–277.', 'https://doi.org/10.1016/j.jeconom.2021.03.014'),
('Callaway, B., and P. H. C. Sant’Anna (2021)', 'Difference-in-Differences with multiple time periods. Journal of Econometrics 225(2): 200–230.', 'https://doi.org/10.1016/j.jeconom.2020.12.001'),
('Cunningham, S., Mixtape data repository', 'Public castle.dta and repository licence. The package pins the data revision and verifies SHA-256 before estimation.', 'https://github.com/scunning1975/mixtape'),
('Ryan Piao, ECON 5200 replication materials', 'The repository layout and Cheng–Hoekstra starter inform the structure and the unconditional cohort-time comparison. My implementation and additional diagnostics are supplied in this package.', 'https://github.com/RyanPiao/econ5200-replication-template')]

def build_report(root,s):
    root=Path(root);out=root/'output';dest=root/'report';dest.mkdir(exist_ok=True)
    pdfmetrics.registerFont(TTFont('BodyFont',str(root/'assets/DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('BoldFont',str(root/'assets/DejaVuSans-Bold.ttf')))
    styles=getSampleStyleSheet()
    for name,font,size,leading,after in [('BodyR','BodyFont',9.5,14,8),('HeadR','BoldFont',16,20,13),('SubR','BoldFont',11,15,7),('SmallR','BodyFont',8,11,6)]:
        styles.add(ParagraphStyle(name=name,fontName=font,fontSize=size,leading=leading,spaceAfter=after,textColor=colors.HexColor('#174C68') if name=='HeadR' else colors.black))
    story=[];md=[]
    def p(text,small=False):
        story.append(Paragraph(html.escape(text),styles['SmallR' if small else 'BodyR']));md.append(text+'\n')
    def h(text):
        story.append(Paragraph(html.escape(text),styles['HeadR']));md.append('# '+text+'\n')
    def sub(text):
        story.append(Paragraph(html.escape(text),styles['SubR']));md.append('## '+text+'\n')
    def page():story.append(PageBreak());md.append('\n---\n')
    def table(headers,rows,widths):
        cells=[[Paragraph(html.escape(str(v)),styles['SmallR']) for v in r] for r in [headers]+rows]
        t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E6EFF3')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#174C68')),('BOTTOMPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F5F7F8')])]))
        story.extend([t,Spacer(1,9)])
        md.append('| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(str(v) for v in r)+' |' for r in rows)+'\n')
    def fig(name,caption):
        story.append(Image(str(out/name),width=504,height=239.4));p(caption,True);md.append(f'![{caption}](../output/{name})\n')
    f=lambda x:f'{x:.4f}'
    head=pd.DataFrame(s['headline']).set_index('model');b=head.loc['SY'];ry=head.loc['RY']
    group=pd.read_csv(out/'estimator_comparison.csv');event=pd.read_csv(out/'balanced_event_study.csv')
    curve=pd.read_csv(out/'specification_curve.csv');loo=pd.read_csv(out/'leave_one_state_out.csv')
    h('Castle Doctrine and Homicide: Replication and Reassessment')
    p('David Njihia Ndungu · ECON 5200 · Replication Study',True)
    sub('1. Positioning')
    p('I study whether expanding self-defense laws reduces crime or makes confrontations more likely to end in a death. Both outcomes seem possible: the law could discourage an offender, but it could also make someone more willing to use lethal force. My focus is the expansion of self-defense protection outside the home. I also keep the reported homicide rate separate from the question of whether a particular killing was legally justified.')
    p('Cheng and Hoekstra (2013) use staggered state adoption to compare changes around policy expansion rather than interpret a cross-state crime correlation as causal. Their positive homicide finding challenges the deterrence account, while their estimates do not establish convincing reductions in burglary, robbery or aggravated assault. An aggregate homicide response does not by itself identify which individual encounters generated it.')
    p('I read three related studies to understand how the paper has been received. Miller and Pepper (2020) revisit the same policy setting and replicate related models. They show why the assumptions about what would have happened without the law matter. I take this as a reminder that a precise regression result is only as convincing as its comparison group and identifying assumptions.')
    p('Guettabi and Munasib (2018) use synthetic controls to study states separately. Their findings suggest that the effect is not the same everywhere. This made me want to check how much individual states affect the pooled estimate and whether population weights change the answer.')
    p('McClellan and Tekin (2017) study related laws using monthly mortality and injury data. Their results also raise doubts about the public-safety argument. However, they use different measures and a different time frequency, so I do not treat their study as an exact replication. These studies help me explain why a positive average effect does not necessarily mean the same effect in every state.')
    p('My identifying assumption is that, absent adoption, adopting and comparison states would have experienced comparable homicide changes conditional on the chosen fixed effects and controls. I also need no relevant anticipation or cross-state spillovers and defensible treatment dates. These are assumptions about unobserved outcomes, not consequences of including fixed effects. Modern staggered-adoption work adds a concern about heterogeneous treatment effects in two-way fixed-effects averages (Goodman-Bacon, 2021; Callaway and Sant’Anna, 2021). I use those tools to reassess the claim, while judging the original fairly against its period’s methods.')

    page();h('2. Direct Replication')
    d=s['data']
    p(f"I use {d['states']} states over {d['first_year']}–{d['last_year']}, giving {d['n']} state-year observations: {d['adopters']} adopters and {d['never']} never-adopters. I retain the supplied fractional-year cdl treatment and average-population analytic weight. There are {d['partial_rows']} partially exposed state-years. All homicide rates are positive, so no log-zero adjustment or row deletion is necessary.")
    p('My model is log(homicide rate) = state effect + time effect + β × fractional exposure + controls + error. SY uses common year effects; RY uses Census-region-by-year effects; RYX also includes the twelve supplied policing, incarceration, income, unemployment, poverty, spending and demographic controls. Covariance is clustered by state.')
    table(['Table 5, Panel A','Paper β','My β','Paper SE','My SE','β gap'],[[lab,f(head.loc[lab,'paper_beta']),f(head.loc[lab,'beta']),f(head.loc[lab,'paper_se']),f(head.loc[lab,'se']),f'{head.loc[lab,"coefficient_gap"]:+.8f}'] for lab in ['SY','RY','RYX']],[107,60,60,65,65,147])
    p('SY, RY and RYX reproduce columns 1, 2 and 3. I read the public author manuscript and cross-check those cells against NBER Working Paper 18134. These cells agree across the two versions; later columns differ, so I do not pool their benchmarks. Source values are transcribed in src/analysis.py.',True)
    p(f"For SY, β = {b.beta:.8f} corresponds to {100*b.beta:.3f} log points or {b.exact_pct:.3f}% using 100 × (exp(β) − 1). Its 95% cluster-t interval in log units is [{b.lo:.4f}, {b.hi:.4f}]. This is not a change in homicide counts or percentage points.")
    sub('Discrepancy log: what I checked')
    p(f"Rounding. The SY coefficient gap is {b.coefficient_gap:+.8f} log units ({b.relative_gap_pct:+.4f}% relative to the printed value). All three coefficients and corrected SEs match at the paper’s displayed precision. I verify the complete panel, outcome definition, exposure coding and weights rather than treating the match as self-validating. The largest relative difference between popwt and mean state population is {d['weight_max_relative_diff_from_mean_pop']:.2e}, consistent with storage precision.")
    p(f"Software defaults. Default statsmodels state clustering gives the SY SE {b.default_cluster_se:.5f}, versus the paper’s {b.paper_se:.4f}. My absorbed-effects correction gives {b.se:.5f}. The correction is G/(G−1) × (N−1)/(N−K*), with nested state effects excluded from K* except one intercept. For SY, N = {int(b.n)}, G = {int(b.clusters)}, full rank = {int(b['rank'])} and K* = {int(b.k_absorbed)}. This convention reproduces the three reported SEs. Because the article does not specify every software default, I document the inferred convention rather than claim to have rerun its original Stata command.")

    page();h('3. Robustness: Clean Comparisons')
    sub('Exercise 1 · Unconditional cohort-time DiD')
    p('What I did. For each adoption cohort and comparison year, I subtract the control group’s change since the last pre-adoption year from the cohort’s change. Controls are never-treated or not-yet-treated states; already-treated states never serve as controls. I average post-adoption cells with cohort-population weights, so earlier cohorts contribute more observed post years. Uncertainty comes from resampling entire state histories.')
    table(['Estimator','β','SE','95% interval'],[[r.model,f(r.beta),f(r.se),f'[{r.lo:.4f}, {r.hi:.4f}]'] for r in group.itertuples()],[212,67,67,158])
    p('TWFE intervals use a state-cluster t reference. Cohort-time intervals are percentile intervals from 999 whole-state bootstrap draws. This is an unconditional two-by-two implementation inspired by the starter and group-time framework, not the full conditional or doubly robust Callaway–Sant’Anna estimator.',True)
    p('What I found. Both clean-comparison averages are positive. Binary exposure also changes the conventional TWFE estimate, providing a bridge between the published dose regression and the group-time comparison. I therefore do not attribute the entire difference between the published estimate and the cohort-time average to forbidden comparisons.')
    p('What it implies. I still find a positive effect when already-treated states are not used as controls. I am more cautious about the size of the effect because the exercise also changes the weights, treatment coding and controls. It is therefore not a direct replacement for the fully adjusted regression. The earliest adoption group contains only one state, which also limits what its bootstrap comparison can tell me.')
    sub('Treatment timing matters')
    p('The adoption-year cohort-time cell includes partial exposure, whereas the original regression coefficient scales a full year of exposure. Redefining treatment as the first full year and then using the partly treated adoption year as a baseline would contaminate that reference. I retain the last fully untreated year and show the first full post-adoption year separately in Exercise 2.')

    page();h('3. Robustness: Event Time')
    sub('Exercise 2 · Balanced cohorts and a different reference year')
    p('What I did. I plot relative years −4 through +1 so that every point is supported by the same adoption cohorts. I use never-treated controls, fixed population weights and the last pre-adoption year as the reference. I then re-anchor to two years before adoption to examine whether the final untreated year is unusual.')
    fig('event_study.png','Figure 1. Pointwise 95% whole-state bootstrap intervals; −1 is normalized. These are not simultaneous bands.')
    table(['Relative year','Estimate','95% interval'],[[str(int(r.event)),f(r.beta),f'[{r.lo:.4f}, {r.hi:.4f}]'] for r in event.itertuples()],[137,137,230])
    p(f"What I found. A joint pre-adoption Wald statistic is {s['pretrend']['wald']:.3f} on {s['pretrend']['df']} restrictions (p = {s['pretrend']['p']:.3f}), using the bootstrap covariance. The first-full-year estimate is {s['pretrend']['balanced_e1']:.4f}; with the earlier reference it is {s['pretrend']['e1_reference_minus2']:.4f}.")
    p('What it implies. The pre-period estimates are above the final untreated year, and re-anchoring lowers the post-adoption contrast. The sign survives, but the magnitude depends on the reference. Failure to reject the pre-adoption null does not establish parallel trends: the intervals permit important differences, and this short panel has limited power.')

    page();h('3. Robustness: Specification Curve')
    sub('Exercise 3 · Retain every model in a declared grid')
    p('What I did. I define all combinations of three samples (all states, no Florida, no South), population or equal state weights, common year or region-by-year effects, and no time-varying controls or the full supplied set. These choices produce 24 models. I retain every estimate and interval. The systematic grid and interactions are the extension; weighting and regional controls alone were already examined by the original authors.')
    fig('specification_curve.png','Figure 2. Blue: population weights; amber: equal weights. Dashed: weighted region-year baseline. Intervals are model-specific, not multiplicity-adjusted.')
    p(f"What I found. Coefficients range from {s['curve_min']:.4f} to {s['curve_max']:.4f} log units. All {s['curve_positive']} of 24 point estimates are positive, but only {s['curve_significant']} reject zero at 5% under the stated state-cluster convention.")
    chosen=curve.loc[curve.groupby('sample').beta.idxmin()]
    table(['Sample','Smallest β in grid','SE'],[[r['sample'],f(r.beta),f(r.se)] for _,r in chosen.iterrows()],[220,147,137])
    p('What it implies. The positive sign does not depend on just one specification in my grid. The size and precision of the estimate do change. Removing the South changes the states represented, while changing weights gives small and large states different importance. These models therefore do not all estimate exactly the same average effect. I also do not treat the number of significant models as a probability that the paper is correct.')

    page();h('3. Robustness: State Influence')
    sub('Exercise 4 · Delete one complete state at a time')
    p('What I did. I rerun the population-weighted region-year model after omitting each state history once. This provides a full influence profile instead of selecting a salient state after seeing its result. Influence does not establish that an observation is erroneous.')
    fig('state_influence.png','Figure 3. Each point is a separate 49-state fit. The complete deletion profile is saved as leave_one_state_out.csv.')
    extreme=pd.concat([loo.head(2),loo.tail(2)]).drop_duplicates('omitted_state')
    table(['Omitted state','β','Change','95% interval'],[[r.omitted_state,f(r.beta),f'{r.change:+.4f}',f'[{r.lo:.4f}, {r.hi:.4f}]'] for r in extreme.itertuples()],[140,67,107,190])
    p(f"What I found. The all-state region-year estimate is {ry.beta:.4f}. Across state deletions, it ranges from {s['loo_min']:.4f} to {s['loo_max']:.4f}. Omitting Florida gives {s['no_florida']['beta']:.4f}, a change of {s['no_florida']['change']:+.4f}.")
    p('What it implies. My positive pooled estimate is not driven by Florida alone. However, this does not show that the law raised homicide in every state. Dropping a state changes both the comparison group and the weights. A factor affecting several adopting states could still explain part of the result.')

    page();h('3. Robustness: Inference')
    sub('Exercise 5 · A null-imposed wild cluster bootstrap')
    p('What I did. In the region-year model, I impose a zero treatment effect by fitting the nuisance regressors without cdl. I multiply restricted weighted residuals by one Rademacher sign per state, rebuild outcomes, refit and studentise using the same state-cluster convention. I compare the observed statistic with the simulated absolute statistics, using a plus-one tail correction and a fixed seed.')
    z=s['inference']
    table(['Inference method','Result'],[['State-cluster t p-value',f"{z['cluster_t_p']:.5f}"],['Restricted wild-cluster p-value',f"{z['wild_p']:.5f}"],['Bootstrap draws',str(z['draws'])],['Approximate Monte Carlo SE of bootstrap p',f"{z['wild_mc_se']:.5f}"]],[310,194])
    p('What I found. Both p-values fall below 5%. I verify selected vectorised bootstrap t-statistics against direct regressions and sandwich calculations. Resampling changes the reference distribution, not the fitted coefficient or the assumed source of policy variation.')
    p('What it implies. The positive region-year estimate is not an artifact of relying only on the asymptotic p-value. This does not repair a violation of parallel trends or account for arbitrary cross-state shocks. Fifty total states do not guarantee ideal inference if identifying variation is concentrated among relatively few adopters.')
    sub('Additional falsification diagnostics, not a novel extension')
    placebo=pd.read_csv(out/'placebo_outcomes.csv')
    table(['Log outcome','Region-year FE','β','95% interval'],[[r.outcome,str(r.region_year),f(r.beta),f'[{r.lo:.4f}, {r.hi:.4f}]'] for r in placebo.itertuples()],[143,98,78,185])
    p('Larceny and motor-vehicle theft follow the paper’s falsification logic, but neither is guaranteed unaffected. Motor theft changes sign when regional time controls enter. I keep that fixed-effect comparison visible and do not read a different estimator’s placebo as though only the treatment-comparison rule changed. A non-rejection is not a validation certificate.')

    page();h('4. Does the Finding Hold?')
    p('My answer is yes on the direction of the pooled result, but I am less certain about its exact size. I reproduce the paper’s weighted coefficients at the reported precision and explain the small numerical differences. My robustness checks also give positive estimates, including when I leave out individual states.')
    p('I conclude that these laws are associated with higher reported homicide in this sample, provided the comparison assumptions hold. I cannot say that the effect is the same in every state or that the exact national increase is always eight percent. I also cannot determine whether the additional deaths were legally justified. The specification curve and reference-year exercise show why I would report a range of estimates rather than rely on one number.')
    p('Further work would need a longer pre-adoption panel, independently verified legal dates, regional untreated trends without already-treated comparisons, and evidence about concurrent policy changes. Those are next steps, not exercises I claim to have run. The original authors already undertook substantial sensitivity work; the extensions here reassess the result rather than assume that later methods automatically overturn it.')
    sub('5. Peer Audit')
    p('I am assigned to audit Roman Carrubba’s replication of Card (1995); Julia Clark is assigned to audit my Cheng–Hoekstra repository. Roman’s repository URL is still needed. The audit issue is due Sunday 22 November at 11:59 pm, while the project deadline remains Thursday 19 November at 11:59 pm. I will test the final version from a clean checkout, file an approximately 300-word GitHub issue on reproducibility, one methodological question and one practice to adopt, and add its URL to my Canvas submission comment. The peer run and issue have not yet been completed.')
    sub('6. Reproducibility')
    p('After installing the pinned requirements, python reproduce.py verifies the data checksum, reruns estimation, writes every table and figure, generates this PDF and refreshes the executed notebooks. Data are included with the Mixtape licence notice; download_data.py can recover the same pinned bytes if absent. The README records the measured runtime and project map.')
    p('The README describes the reproduction command, runtime, data provenance and project layout. My public repository link must be available to Julia, and the peer audit will be completed once Roman’s final repository URL is available.')

    page();h('References and Source Notes')
    for author,title,url in REFERENCES:
        p(author+'. '+title,True)
        story.append(Paragraph(f'<link href="{html.escape(url)}" color="#174C68">{html.escape(url)}</link>',styles['SmallR']))
        md.append(url+'\n')
    sub('Numerical source map')
    p('Headline: output/headline_table.csv. Cohort-time estimates: estimator_comparison.csv and group_time_*.csv. Event study: balanced_event_study.csv and pretrend_test.json. Specifications: specification_curve.csv. Influence: leave_one_state_out.csv. Inference: inference.csv and wild_bootstrap_draws.csv. Placebos: placebo_outcomes.csv. Every empirical report value is constructed by the pipeline.',True)
    p('The numerical benchmarks are Table 5, Panel A, columns 1–3. The public NBER version and later author manuscript agree on these cells. Article PDFs are not redistributed in the code archive; the references supply access paths.',True)
    def footer(canvas,doc):
        canvas.saveState();canvas.setFont('BodyFont',8);canvas.setFillColor(colors.HexColor('#647580'))
        canvas.drawString(54,33,'Castle Doctrine · Replication and Reassessment');canvas.drawRightString(558,33,str(doc.page));canvas.restoreState()
    doc=SimpleDocTemplate(str(dest/'Castle_Doctrine_Replication.pdf'),pagesize=(612,792),leftMargin=54,rightMargin=54,topMargin=45,bottomMargin=51)
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    (dest/'report.md').write_text('\n'.join(md))
    (root/'references.md').write_text('# References\n\n'+'\n\n'.join(a+'. '+t+'\n\n'+u for a,t,u in REFERENCES))

```


## Source: src/notebooks.py

```python
"""Create readable notebooks and execute their real code cells in process."""
from pathlib import Path
import os
import nbformat as nb
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output

def build_notebooks(root,summary):
    root=Path(root)
    shell=InteractiveShell.instance()
    setup="""from pathlib import Path
import sys
import json
import pandas as pd
ROOT = Path.cwd()
if not (ROOT / 'reproduce.py').exists():
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))
from download_data import ensure_data
from src.analysis import fit_model, run
ensure_data(ROOT)
if not (ROOT / 'output/summary.json').exists():
    run(ROOT)
castle = pd.read_stata(ROOT / 'data/castle.dta', convert_categoricals=False)
summary = json.loads((ROOT / 'output/summary.json').read_text())
print(f"{len(castle)} state-year observations, {castle.sid.nunique()} states")"""
    first=[
      nb.v4.new_markdown_cell('# Castle Doctrine and Homicide\n\n## Positioning and Direct Replication\n\nI replicate Cheng and Hoekstra (2013), Table 5, Panel A, columns 1–3. The accompanying report states the identification assumptions and discusses Miller and Pepper (2020), Guettabi and Munasib (2018), and McClellan and Tekin (2017).\n\nOpen this notebook from the extracted repository. `python reproduce.py` regenerates all outputs and the PDF. The setup also runs the analysis if its outputs are absent.'),
      nb.v4.new_code_cell(setup),
      nb.v4.new_markdown_cell('## Data checks\n\nI preserve fractional-year exposure, supplied average-population weights and all observations with positive homicide rates.'),
      nb.v4.new_code_cell("print(json.dumps(summary['data'], indent=2))\nprint(castle.groupby('sid').effyear.first().value_counts(dropna=False).sort_index())"),
      nb.v4.new_markdown_cell('## Direct replication\n\nI fit state-and-year effects, state-and-region-year effects, and the region-year model with the supplied controls. Standard errors cluster by state with the documented absorbed-effects small-sample convention.'),
      nb.v4.new_code_cell("for name, region, controls in [('SY',False,False),('RY',True,False),('RYX',True,True)]:\n    result, fitted, data_used, design = fit_model(castle, region=region, controls=controls)\n    print(name, json.dumps(result, indent=2))"),
      nb.v4.new_code_cell("headline = pd.read_csv(ROOT / 'output/headline_table.csv')\nprint(headline[['model','paper_beta','replication_beta','paper_se','replication_se','coefficient_gap']].to_string(index=False))"),
      nb.v4.new_markdown_cell('## My discrepancy diagnosis\n\nThe coefficient and corrected standard error reproduce at published precision. I checked sample balance, log outcomes, fractional exposure and the weights. Default statsmodels clustering counts the state fixed effects differently in its small-sample factor; the supplied correction excludes effects nested in the state clusters. I retain both standard errors in the output rather than conceal that choice.\n\nMy coefficient is in log units. The exact rate change is `100 * (exp(beta) - 1)`, not a change in homicide counts or percentage points. Source benchmarks are transcribed from the paper, not copied from my fitted results.')]
    second=[nb.v4.new_markdown_cell('# Castle Doctrine and Homicide\n\n## Robustness and Assessment\n\nI report five extensions and retain every specification. I distinguish unconditional cohort-time comparisons from the full conditional Callaway–Sant’Anna estimator, and I do not attribute every numerical change to forbidden comparisons.'),nb.v4.new_code_cell(setup)]
    sections=[
      ('1. Clean treatment comparisons','estimator_comparison.csv','The positive direction survives without already-treated controls. The exposure coding, aggregation and regional controls also change, so the comparison does not isolate only estimator choice.'),
      ('2. Cohort-balanced event study','balanced_event_study.csv','Using the same cohorts at every event time removes changing cohort composition from the plotted dynamics. Reference-year sensitivity qualifies the magnitude; non-rejection of pre-trends does not establish parallel trends.'),
      ('3. Prespecified specification curve','specification_curve.csv','All points are retained. Changing weights and samples changes the target population; significance across correlated models is not a probability that the claim is true.'),
      ('4. Leave-one-state-out influence','leave_one_state_out.csv','The positive pooled result does not depend on Florida alone. The state-deletion difference is not an identified state-specific causal effect.'),
      ('5. Restricted wild cluster inference','inference.csv','The positive region-year coefficient survives a different finite-sample reference distribution. Resampling does not repair a violation of parallel trends.'),
      ('Additional outcome diagnostics','placebo_outcomes.csv','These original-style falsification checks are not counted as a novel extension. A non-rejection is not proof that the design is valid.')]
    for title,csv,interpretation in sections:
        second.extend([nb.v4.new_markdown_cell('## '+title),nb.v4.new_code_cell(f"print(pd.read_csv(ROOT / 'output/{csv}').to_string(index=False))"),nb.v4.new_markdown_cell('**My interpretation.** '+interpretation)])
        image={'balanced_event_study.csv':'event_study.png','specification_curve.csv':'specification_curve.png','leave_one_state_out.csv':'state_influence.png'}.get(csv)
        if image:
            second.append(nb.v4.new_code_cell("from IPython.display import Image, display\ndisplay(Image(filename=str(ROOT / 'output/"+image+"')))"))
    second.append(nb.v4.new_markdown_cell('## My overall judgment\n\nThe positive pooled relationship survives these exercises, while its exact magnitude remains conditional on comparisons, weights and the reference year. I have not established a common effect in every state or identified whether additional deaths were legally justified. The report and references explain those limits.\n\n## Peer audit\n\nI am assigned to audit Roman Carrubba’s Card (1995) replication, and Julia Clark is assigned to audit my Cheng–Hoekstra repository. Roman’s repository URL is still needed. The project deadline is Thursday 19 November at 11:59 pm; the audit issue is due Sunday 22 November at 11:59 pm. I will run the final version from a clean checkout, file an approximately 300-word issue and add its URL as a Canvas submission comment. No peer run or filed issue has been completed yet.'))
    previous=Path.cwd();os.chdir(root)
    try:
        for filename,cells in [('01_positioning_and_replication.ipynb',first),('02_robustness.ipynb',second)]:
            notebook=nb.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}})
            count=0
            for cell in notebook.cells:
                if cell.cell_type!='code':continue
                count+=1
                with capture_output() as captured:
                    result=shell.run_cell(cell.source,store_history=True)
                if result.error_in_exec or result.error_before_exec:
                    raise RuntimeError(captured.stdout) from (result.error_in_exec or result.error_before_exec)
                cell.execution_count=count;cell.outputs=[]
                if captured.stdout:cell.outputs.append(nb.v4.new_output('stream',name='stdout',text=captured.stdout))
                if captured.stderr:cell.outputs.append(nb.v4.new_output('stream',name='stderr',text=captured.stderr))
                for output in captured.outputs:
                    cell.outputs.append(nb.v4.new_output('display_data',data=output.data,metadata=output.metadata))
            nb.validate(notebook)
            nb.write(notebook,root/'notebooks'/filename)
    finally:os.chdir(previous)

```
