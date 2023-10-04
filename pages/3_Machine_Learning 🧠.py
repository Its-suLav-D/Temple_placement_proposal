import streamlit as st

st.title("Machine Learning 🧠")


st.image("https://auto.gluon.ai/stable/_static/autogluon-w.png", caption='AutoGluon Logo')
st.subheader("AutoGluon")

st.write("""
We planned to use AutoGluon to train a model to predict the best locations for new temples. AutoGluon Tabular automates machine learning tasks for structured data, handling data preprocessing, feature engineering, model selection, tuning, and ensembling. With just a few lines of code, we can easily train models for classification or regression problems. 
""")

st.subheader('Visualization Interpretation for Feature Engineering:')

st.markdown("""
    1. LDS Visitor Ratio Analysis in Counties with and Without Temples:

    > This visualization is quite potent. From a feature engineering perspective, the ratio of visitor counts to LDS buildings to the overall population of each Census Block Group can serve as an input feature because it's an indicator of the density of potential visitors to a temple. High ratios might suggest areas with an active LDS population or significant interest in visiting LDS sites.
    Scaling this by different geographic levels (tract, county, city, or state) can allow for additional granularity or abstraction depending on the model's needs. For instance, if we're trying to predict temple placements on a city or county scale, we might want to aggregate these ratios up to that level.
            
    2. Geo Distribution of Churches and Temples Visualization in Idaho
        
    > This visualization offers insights into the current distribution of LDS temples and churches. If there's a clustering of churches but no temple nearby, that could be a potential area of interest.
            
    > Distance features can be engineered from this data. For instance, the average distance of an area to the nearest temple or the density of churches within a certain radius.
            
""")

st.title("How AutoGluon can Aid us:")

st.markdown(
    """
AutoGluon automates many aspects of the machine learning process. Here's how it can be beneficial for this task:

1. Automated Feature Engineering: AutoGluon can potentially discover and engineer additional valuable features from the raw data. This can save time and potentially improve model performance.

2. Model Selection and Hyperparameter Tuning: Instead of manually picking a machine learning algorithm and tuning it, AutoGluon tries out multiple algorithms and hyperparameter combinations to find the best model for our dataset.

3. Handling Missing Data: AutoGluon can automatically handle missing data, which can be common in datasets like this. This can save time in the preprocessing stage.

4. Evaluation: AutoGluon provides easy-to-read performance metrics, helping you understand how well the model is doing and where it might be going wrong.

"""
)

st.title("Thank You! 🙏")


