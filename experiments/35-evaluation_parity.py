# %%

import numpy as np
import tqdm
import subset2evaluate.utils as utils
import subset2evaluate.utils
import subset2evaluate.evaluate
import subset2evaluate.select_subset
import multiprocessing

data_old_all = list(utils.load_data_wmt_test().items())

# %%
with multiprocessing.Pool(len(data_old_all)) as pool:
    spa_precomputed_values = pool.starmap(
        subset2evaluate.evaluate.precompute_spa_randnorm,
        [(x[1], 10, "human", 2) for x in data_old_all]
    )
spa_precomputed = dict(zip([x[0] for x in data_old_all], spa_precomputed_values))

# %%
for method_kwargs in [
    dict(method="metric_avg", metric="MetricX-23-c"),
    dict(method="metric_var", metric="MetricX-23-c"),
    dict(method="metric_cons", metric="MetricX-23-c"),
    dict(method="pyirt_diffdisc", metric="MetricX-23-c", retry_on_error=True),
    dict(method="diversity", metric="lm"),
    dict(method="precomet_avg"),
    dict(method="precomet_var"),
    dict(method="precomet_cons"),
    dict(method="precomet_diversity"),
    dict(method="precomet_diffdisc_direct"),
]:
    par_spa_all = []
    for data_name, data_old in tqdm.tqdm(data_old_all):
        par_spa = subset2evaluate.evaluate.eval_spa_par_randnorm(
            subset2evaluate.select_subset.basic(data_old, **method_kwargs),
            data_old,
            spa_precomputed=spa_precomputed[data_name],
        )
        par_spa_all.append(np.average(par_spa))
    print(f'{method_kwargs["method"]:<15}', f"SPA: {np.average(par_spa_all):.1%}")

# %%
par_spa_all = []
for repetitions in range(10):
    for data_name, data_old in tqdm.tqdm(data_old_all):
        par_spa = subset2evaluate.evaluate.eval_spa_par_randnorm(
            subset2evaluate.select_subset.basic(data_old, method="random"),
            data_old,
            spa_precomputed=spa_precomputed[data_name],
        )
        par_spa_all.append(par_spa)



# %%

import subset2evaluate.utils

spa_all_random_arr = np.array(par_spa_all).reshape(-1, 10).mean(axis=1)
conf = subset2evaluate.utils.confidence_interval(spa_all_random_arr, confidence=0.90,)
print(f"{(conf[1]-conf[0])/2:.2%}")