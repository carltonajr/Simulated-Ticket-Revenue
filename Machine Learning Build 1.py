import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split
from IPython.display import display
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
import random
from sklearn.ensemble import IsolationForest
from statsmodels.formula.api import ols
import re


def change_for_machine_learning(df):
    new_df = df.copy()
    for column in df.columns:
        if df[column].dtype != int and df[column].dtype != float:
            new_df[column] = new_df[column].astype('category')
            new_df[column] = new_df[column].cat.codes
    return new_df


def new_maps(df1, value1, df2, value2):
    codes = df1[value1]
    names = df2[value2]
    code_name_map = dict(zip(codes, names))
    return code_name_map


def has_docstring(func):
    """Check to see if the function  has a docstring.

    Args:
      func (callable): A function.

    Returns:
      bool
    """
    return func.__doc__ is not None


has_dc = has_docstring(has_docstring)

if not has_dc:
    display("has_docstring() doesn't have a docstring!")
else:
    display("has_docstring() looks ok")
    

def opponent_search(value):
    display(all_seasons.opp_id.sort_values().unique())
    results = all_seasons[all_seasons['opp_id'].str.contains(value, case=False)].drop('stand_dev_talons', axis=1)
    if len(results) == 0:
        raise ValueError("No team IDs found. Please choose from the list above.")
    else:
        results=results
    return results


def create_dict(range_num, key_data, key_column, value_data, value_column):
    """Create a dictionary containing a number of 'key: value' pairs.

  Args:
    range_num (int): Range the loop will run over
    key_data (variable): Dataset the keys will be pulled from.
    key_column (variable): Dataset column the keys will be pulled from.
    value_data (variable): Dataset the values will be pulled from.
    value_column (variable): Dataset column the values will be pulled from.

  Returns:
    dict
  """
    new_dict = {}
    for i in range(range_num):
        new_dict[key_data[key_column][i]] = value_data[value_column][i]
    return new_dict


def sample_append(range_num, append_to, data, column):
    """Create a list of average values based on the dataset.

  Args:
    range_num (int): Range the loop will run over.
    append_to (list): Empty list that data will be appended to.
    data (Dataframe): Dataset to be sampled from.
    column (Series): Dataframe column used in the sample.

  Returns:
    list
  """
    for i in range(range_num):
        append_to.append(
        np.mean(data.sample(frac=1, replace=True)[column])
    )
    return append_to

for dirname, _, filenames in os.walk('/work/complete_dataset'):
    """
    For loop that merges the data from the two teams into one full dataset with the option of saving to a csv file.

    Args:
      folder / folder path to pull readable csv files from

    Returns:
      dataframe
    """
    rows_list = []
    for filename in filenames:
        # View the files found in the folder/path given
        # print(os.path.join(dirname, filename))
        df = pd.read_csv(f"/work/complete_dataset/{filename}")
        # Create a list with each row of the dataframe
        for index, row in df.iterrows():
            rows_list.append(row)
# The new dataframe is indexed by the game_id column as the unique identifier.
# Sorted by the season being shown then the game to ensure easier game-by-game viewing.
    data = pd.DataFrame(rows_list).set_index("game_id").sort_values(['season', 'game'])

# os.makedirs('/work/complete_dataset', exist_ok=True) 
# data.to_csv("/work/complete_dataset/all_seasons_complete.csv", index=True)

pd.set_option('display.max_rows', None)


data['team_z_score'] = (data.team_score - data.team_score.mean()) / data.team_score.std()
data['opp_z_score'] = (data.opp_score - data.opp_score.mean()) / data.opp_score.std()


plt.figure(figsize=(15, 5))
sns.set_style('whitegrid')
sns.regplot(data=data, x=np.arange(start=1, stop=len(data)+1), y='team_score', ci=0.1, scatter_kws={'alpha': 0.5})


sns.displot(data=data, x='team_score', bins=35, col='conference')

mean_score_by_season = data.groupby('season')['team_score'].mean().round(1)
mean_score_by_season

samples = data.sample(frac=1/10, replace=False)

list_of_sampled = list(samples.index)
training = data[~data.index.isin(list_of_sampled)]
len(training)

team_model = ols('team_score ~ margin', data=samples).fit()

opps_model = ols('opp_score ~ margin', data=samples).fit()
team_model.params, opps_model.params

explanatory_data = pd.DataFrame({'score_diff': np.arange(0 , 82, 2)})

prediction_data = explanatory_data.assign(team_score = team_model.predict(explanatory_data))
display(prediction_data.info())
display(data[['margin','team_score']].info())


fig = plt.figure()
plt.figure(figsize=(15, 4))
sns.set_style('whitegrid')
sns.regplot(x="margin",  y="talons_score", data=training, color='green')

sns.scatterplot(x="margin",  y="talons_score",  data=prediction_data, color='red')

sns.scatterplot(x="margin",  y="talons_score",  data=samples, color='yellow')

plt.show()

bootstrap_1 = data.sample(frac=1/5, replace=True)

mean_z_score = np.mean(bootstrap_1['team_z_score'])

z_score_35 = []
for i in range(35):
    z_score_35.append(
        np.mean(data.sample(frac=1, replace=True)['team_z_score'])
    )

plt.hist(z_score_35, bins=15)
plt.show()


pop = data.sample(n=150, random_state=3456543)

# Calculate the mean duration in mins from population
mean_pop = data.team_score.mean() 

# Calculate the mean duration in mins from sample
mean_samp = pop.team_score.mean()
[mean_pop, mean_samp]


pop.team_score.hist(bins=np.arange(pop.team_score.min(), pop.talons_score.max(), 1))
plt.title('Sample Population  - Team Scoring')
plt.show()

uniforms = np.random.uniform(low=pop.team_score.min(), high=pop.team_score.max(), size=pop.team_score.max())
plt.hist(uniforms, bins=np.arange(pop.team_score.min(), pop.team_score.max(), 1))
plt.show()


# Set the sample size to 70
sample_size = 70

# Calculate the population size from attrition_pop
pop_size = len(data)

# Calculate the interval
interval = pop_size // sample_size
new_samp = data.iloc[::interval]

new_samp.plot(x='stand_dev_talons', y='score_diff', kind='scatter')
ids = list(data['opp_id'].unique())
choose_randoms = random.sample(ids, k=5)

condition = data['opp_id'].isin(choose_randoms)
use_condition = data[condition]


# result_samp = (data['game_ending'] == 'one_score win').mean()
# result_hypothesis = 0.05

mean_team_score_full = sample_append(len(bootstrap_1), mean_team_score_full, bootstrap_1, 'team_score')
mean_opp_score_full = sample_append(len(bootstrap_1), mean_opp_score_full, bootstrap_1, 'opp_score')

lower = np.quantile(bootstrap_1.talons_score, 0.025)
upper = np.quantile(bootstrap_1.talons_score, 0.975)


plt.figure(figsize=(15, 10))
sns.scatterplot(x='game_id', y='team_score', data=bootstrap_1, hue='season', palette='coolwarm')

random_stats = data.sample(41, replace=False)


calculations = change_for_machine_learning(random_stats)
calculations['game_ending_cat'] = random_stats['game_ending']


# Hypothesize that the proportion of one score wins
p_0 = 0.04

# Calculate the sample proportion of one score wins
p_hat = (random_stats['game_ending'] == "one_score win").mean()


# Calculate the sample size
n = len(random_stats)

# Calculate the numerator and denominator of the test statistic
numerator = p_hat - p_0
denominator = np.sqrt(p_0 * (1 - p_0) / n)

# Calculate the test statistic
z_score = numerator / denominator

# Calculate the p-value from the z-score
p_value = 1 - norm.cdf(z_score)
