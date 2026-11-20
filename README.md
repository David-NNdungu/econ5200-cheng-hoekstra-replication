# Castle Doctrine and Homicide: Replication and Robustness Checks

## Objective

I replicate Cheng and Hoekstra (2013) and examine whether their finding that castle-doctrine expansions increased homicide holds under other reasonable choices.

**Paper:** Cheng, C., and Hoekstra, M. (2013). “Does Strengthening Self-Defense Law Deter Crime or Escalate Violence? Evidence from Expansions to Castle Doctrine.” *Journal of Human Resources*, 48(3), 821–854.

## Data

I use `castle.dta`, which contains 550 state-year observations for 50 states from 2000 to 2010. There are 21 adopting states and 29 never-adopting states.

I keep the supplied `cdl` variable, which records the share of each year that the law was in effect, and the supplied population weights. The data and licence notice are included in `data/`. The download script checks that the data match the version used in this project.

Source: [Scott Cunningham’s Mixtape repository](https://github.com/scunning1975/mixtape).

## Direct Replication

I reproduce Table 5, Panel A, columns 1–3.

| Specification | Paper estimate | My estimate | Paper SE | My SE |
|---|---:|---:|---:|---:|
| State and year fixed effects | 0.0801 | 0.08006351 | 0.0342 | 0.03422469 |
| State and region-by-year fixed effects | 0.0946 | 0.09458774 | 0.0279 | 0.02786513 |
| Region-by-year effects and time-varying controls | 0.0937 | 0.09367518 | 0.0290 | 0.02898593 |

My headline coefficient corresponds to an **8.336% increase** in the homicide rate using `100 * (exp(beta) - 1)`. It is a change in a log rate, not a change in homicide counts or percentage points.

I investigated the sample, treatment coding, weights and standard-error correction. The estimates and corrected standard errors match the paper at its displayed precision. The report explains why statsmodels’ default clustered standard errors differ.

## Robustness Checks

1. **Treatment comparisons:** I compare TWFE with cohort-time estimates using never-treated and not-yet-treated controls.
2. **Event study:** I use the same adoption cohorts at each event time and check a different pre-treatment reference year.
3. **Specification curve:** I estimate 24 combinations of samples, weights, fixed effects and controls.
4. **State influence:** I remove one state at a time and re-estimate the model.
5. **Inference:** I use a null-imposed wild cluster bootstrap with 1,999 draws.

All 24 specification-curve estimates are positive, but only eight reject zero at the 5% level. Excluding Florida gives a coefficient of 0.0832 in the region-year model. The wild cluster bootstrap p-value is 0.0035.

My conclusion is that the positive pooled result survives these checks, while its size and precision depend on the choices made. The cohort-time comparison also changes treatment coding and aggregation, so I do not interpret its entire difference from TWFE as the effect of removing forbidden comparisons.

## Reproduce My Results

Python 3.12 was tested. From the repository folder:

```bash
python -m venv .venv
```

Activate the environment with `source .venv/bin/activate` on macOS/Linux or `.venv\Scripts\activate` on Windows. Then run:

```bash
python -m pip install -r requirements.txt
python reproduce.py
```

**The one reproduction command is `python reproduce.py`.** It checks the data, reruns the analysis and regenerates the tables, figures, PDF report and executed notebooks.

The clean-checkout test took about eight seconds after installing dependencies. Runtime will vary by computer. No API key is needed. The included data allow an offline run after installation.

Standard errors are clustered by state. The report and code document the absorbed-effects correction used to match the paper. Confidence intervals use a t reference with one fewer degree of freedom than the number of state clusters.

## Files

| File or folder | Contents |
|---|---|
| `reproduce.py` | Runs the complete project |
| `download_data.py` | Downloads and checks the dataset if needed |
| `requirements.txt` | Pinned Python packages |
| `notebooks/01_positioning_and_replication.ipynb` | Data checks and direct replication |
| `notebooks/02_robustness.ipynb` | Robustness results, figures and explanations |
| `src/` | Estimation, report and notebook code |
| `data/` | Dataset, provenance and licence |
| `output/` | Results, figures and bootstrap draws |
| `report/Castle_Doctrine_Replication.pdf` | Written report |
| `report/report.md` | Editable report text |
| `references.md` | References |
| `ai-appendix.md` | P.R.I.M.E. review record |
| `ai-response-record.md` | Supporting response and source record |
| `AUDIT.md` | Peer-audit instructions and assignment |
| `verification.json` | Reproduction checks |

## Acknowledgments

I follow the [course replication template](https://github.com/RyanPiao/econ5200-replication-template) and use the Cheng–Hoekstra starter as a guide. My questions, checks and decisions are recorded in the appendix.
