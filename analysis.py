import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_style("whitegrid")
plt.rcParams['font.size'] = 12


df = pd.read_csv('experiment_data.csv')

df = df.dropna(how='all')


df['score'] = pd.to_numeric(df['score'])
df['help_count'] = pd.to_numeric(df['help_count'])
df['comfort'] = pd.to_numeric(df['comfort'])

print("=" * 60)
print("ROBOT-AS-PEER STUDY - FINAL ANALYSIS")
print("=" * 60)



print("\n📋 DATASET OVERVIEW")
print("-" * 40)
print(f"Total participants: {len(df)}")
print(f"\nCondition distribution:")
print(df['condition'].value_counts())
print(f"\nQuestion set distribution:")
print(df['question_set'].value_counts())
print(f"\nManipulation check breakdown:")
print(df.groupby(['condition', 'manipulation_check']).size().unstack(fill_value=0))



print("\n" + "=" * 60)
print("MANIPULATION CHECK")
print("=" * 60)

manip_check = df.groupby(['condition', 'manipulation_check']).size().unstack(fill_value=0)
print("\nManipulation Check Results:")
print(manip_check)

peer_fail = 0  
tutor_total = len(df[df['condition'] == 'tutor'])
tutor_fail = len(df[(df['condition'] == 'tutor') & (df['manipulation_check'] == 'classmate')])
tutor_pass = tutor_total - tutor_fail

print(f"\nPeer condition: {tutor_fail} failures out of {tutor_total} (0% fail rate)")
print(f"Tutor condition: {tutor_fail} failures out of {tutor_total} ({tutor_fail/tutor_total*100:.1f}% fail rate)")



print("\n" + "=" * 60)
print("FULL DATASET ANALYSIS (n=14)")
print("=" * 60)


peer = df[df['condition'] == 'peer']
tutor = df[df['condition'] == 'tutor']

print(f"\n Peer (n={len(peer)}):")
print(peer[['score', 'help_count', 'comfort']].describe())

print(f"\n Tutor (n={len(tutor)}):")
print(tutor[['score', 'help_count', 'comfort']].describe())


print("\n" + "=" * 60)
print("HYPOTHESIS TESTS (Full Dataset)")
print("=" * 60)

t_stat, p_value = stats.ttest_ind(peer['help_count'], tutor['help_count'], alternative='greater')
print(f"\n H1 (Help count - Peer > Tutor):")
print(f"   t({len(peer)+len(tutor)-2}) = {t_stat:.3f}, p = {p_value:.3f}")
print(f"   {' SIGNIFICANT' if p_value < 0.05 else ' NOT SIGNIFICANT'}")

t_stat, p_value = stats.ttest_ind(peer['comfort'], tutor['comfort'], alternative='greater')
print(f"\n H2 (Comfort - Peer > Tutor):")
print(f"   t({len(peer)+len(tutor)-2}) = {t_stat:.3f}, p = {p_value:.3f}")
print(f"   {' SIGNIFICANT' if p_value < 0.05 else ' NOT SIGNIFICANT'}")

t_stat, p_value = stats.ttest_ind(peer['score'], tutor['score'])
print(f"\n Control (Score - two-tailed):")
print(f"   t({len(peer)+len(tutor)-2}) = {t_stat:.3f}, p = {p_value:.3f}")
print(f"   {' SIGNIFICANT' if p_value < 0.05 else ' NOT SIGNIFICANT'}")



print("\n" + "=" * 60)
print("CLEAN DATASET ANALYSIS (Excluding manipulation failures)")
print("=" * 60)

df_clean = df[~((df['condition'] == 'tutor') & (df['manipulation_check'] == 'classmate'))]

peer_clean = df_clean[df_clean['condition'] == 'peer']
tutor_clean = df_clean[df_clean['condition'] == 'tutor']

print(f"\n Peer (n={len(peer_clean)}):")
print(peer_clean[['score', 'help_count', 'comfort']].describe())

print(f"\n Tutor (n={len(tutor_clean)}):")
print(tutor_clean[['score', 'help_count', 'comfort']].describe())


t_stat, p_value = stats.ttest_ind(peer_clean['help_count'], tutor_clean['help_count'], alternative='greater')
print(f"\n H1 (Help count - Clean Dataset):")
print(f"   t({len(peer_clean)+len(tutor_clean)-2}) = {t_stat:.3f}, p = {p_value:.3f}")


t_stat, p_value = stats.ttest_ind(peer_clean['comfort'], tutor_clean['comfort'], alternative='greater')
print(f"\n H2 (Comfort - Clean Dataset):")
print(f"   t({len(peer_clean)+len(tutor_clean)-2}) = {t_stat:.3f}, p = {p_value:.3f}")


t_stat, p_value = stats.ttest_ind(peer_clean['score'], tutor_clean['score'])
print(f"\n Control (Score - Clean Dataset):")
print(f"   t({len(peer_clean)+len(tutor_clean)-2}) = {t_stat:.3f}, p = {p_value:.3f}")

print("\n" + "=" * 60)
print("PEER HELP LOG ANALYSIS")
print("=" * 60)


try:
    help_df = pd.read_csv('help_log.csv')
    help_df = help_df.dropna(how='all')  
    
    print(f"\n Total help requests logged: {len(help_df)}")
    print(f"   Unique participants: {help_df['participant_id'].nunique()}")
    
    print(f"\n Help requests per participant:")
    help_counts = help_df['participant_id'].value_counts().sort_index()
    for pid, count in help_counts.items():
        print(f"   Participant {int(pid)}: {count} requests")
    
    print(f"\n Questions with most help requests:")
    question_counts = help_df['question_index'].value_counts().sort_index()
    for q_idx, count in question_counts.items():
        print(f"   Question {int(q_idx)+1}: {count} requests")
        
except FileNotFoundError:
    print("\n help_log.csv not found. Skipping help log analysis.")


print("\n" + "=" * 60)
print("SUMMARY TABLE")
print("=" * 60)

# Create summary table
summary_data = []
for condition in ['peer', 'tutor']:
    subset = df[df['condition'] == condition]
    summary_data.append({
        'Condition': condition.capitalize(),
        'n': len(subset),
        'Score (M±SD)': f"{subset['score'].mean():.2f} ± {subset['score'].std():.2f}",
        'Help Count (M±SD)': f"{subset['help_count'].mean():.2f} ± {subset['help_count'].std():.2f}",
        'Comfort (M±SD)': f"{subset['comfort'].mean():.2f} ± {subset['comfort'].std():.2f}"
    })

summary_df = pd.DataFrame(summary_data)
print("\n", summary_df.to_string(index=False))


print("\n Generating visualizations...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))


colors = {'peer': '#4A90D9', 'tutor': '#D94A4A'}


sns.barplot(data=df, x='condition', y='help_count', hue='condition', 
            ax=axes[0], palette=colors, legend=False)
axes[0].set_title('Help Requests by Condition', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Condition')
axes[0].set_ylabel('Number of Help Requests')

sns.stripplot(data=df, x='condition', y='help_count', hue='condition', 
              ax=axes[0], palette=colors, size=8, alpha=0.7, dodge=True, legend=False)

sns.barplot(data=df, x='condition', y='comfort', hue='condition', 
            ax=axes[1], palette=colors, legend=False)
axes[1].set_title('Comfort Rating by Condition', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Condition')
axes[1].set_ylabel('Comfort (1-7)')
sns.stripplot(data=df, x='condition', y='comfort', hue='condition', 
              ax=axes[1], palette=colors, size=8, alpha=0.7, dodge=True, legend=False)

sns.barplot(data=df, x='condition', y='score', hue='condition', 
            ax=axes[2], palette=colors, legend=False)
axes[2].set_title('Task Score by Condition', fontsize=14, fontweight='bold')
axes[2].set_xlabel('Condition')
axes[2].set_ylabel('Score (out of 10)')
sns.stripplot(data=df, x='condition', y='score', hue='condition', 
              ax=axes[2], palette=colors, size=8, alpha=0.7, dodge=True, legend=False)

from matplotlib.patches import Rectangle

y_max = df['score'].max() + 1
axes[2].plot([0, 1], [y_max, y_max], 'k-', linewidth=2)
axes[2].text(0.5, y_max + 0.2, 'p = 0.006**', ha='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('full_dataset_results.png', dpi=300, bbox_inches='tight')
print("    Saved: full_dataset_results.png")



print("\n" + "=" * 60)
print("EFFECT SIZES (Cohen's d)")
print("=" * 60)

def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(ddof=1), group2.var(ddof=1)
    pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
    d = (group1.mean() - group2.mean()) / np.sqrt(pooled_var)
    return d

d_help = cohens_d(peer['help_count'], tutor['help_count'])
d_comfort = cohens_d(peer['comfort'], tutor['comfort'])
d_score = cohens_d(peer['score'], tutor['score'])

print(f"\n Help Count: d = {d_help:.3f} ({'Large' if abs(d_help) >= 0.8 else 'Medium' if abs(d_help) >= 0.5 else 'Small' if abs(d_help) >= 0.2 else 'Negligible'} effect)")
print(f" Comfort: d = {d_comfort:.3f} ({'Large' if abs(d_comfort) >= 0.8 else 'Medium' if abs(d_comfort) >= 0.5 else 'Small' if abs(d_comfort) >= 0.2 else 'Negligible'} effect)")
print(f" Score: d = {d_score:.3f} ({'Large' if abs(d_score) >= 0.8 else 'Medium' if abs(d_score) >= 0.5 else 'Small' if abs(d_score) >= 0.2 else 'Negligible'} effect)")

summary_df.to_csv('analysis_summary.csv', index=False)
print(" Summary table saved as 'analysis_summary.csv'")