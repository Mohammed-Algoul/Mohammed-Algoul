"""All profile copy lives here, separate from the drawing code.

Everything below is sourced from Mohammed's public GitHub profile, the public
README files of his repositories, or information he provided directly.
Edit this file and run `python scripts/build.py` to regenerate the visuals.
"""

NAME_FIRST = "Mohammed"
NAME_LAST = "Algoul"
LOGIN = "Mohammed-Algoul"

HERO_LABEL = "INTELLIGENT SYSTEMS & COMPUTER ENGINEERING"
HERO_HEADLINE = ["Machine learning", "Data analytics", "Intelligent systems"]
HERO_SUB = ["From CNNs on medical images to data-driven", "apps built with Python and Flutter."]
HERO_META = ["AL-AQSA UNIVERSITY", "GAZA, PALESTINE"]

# (accent, short code, group title, [(label, simple-icon slug or None)])
STACK = [
    ("cyan", "LANG", "Languages", [
        ("Python", "python"), ("JavaScript", "javascript"), ("HTML5", "html5"), ("CSS", "css"),
    ]),
    ("violet", "AI/ML", "AI & Machine Learning", [
        ("TensorFlow", "tensorflow"), ("Keras", "keras"), ("scikit-learn", "scikitlearn"),
        ("CNNs", None), ("Classification", None), ("Clustering", None), ("Dimensionality Reduction", None),
    ]),
    ("blue", "DATA", "Data Analysis", [
        ("pandas", "pandas"), ("NumPy", "numpy"), ("Matplotlib", None), ("Seaborn", None),
        ("Jupyter", "jupyter"), ("EDA", None), ("Feature Engineering", None),
    ]),
    ("sky", "MOBILE", "Mobile Development", [
        ("Flutter", "flutter"), ("Dart", "dart"),
    ]),
    ("indigo", "TOOLS", "Frameworks & Tools", [
        ("FastAPI", "fastapi"), ("Web Scraping", None), ("Google Colab", "googlecolab"), ("Kaggle", "kaggle"),
        ("Git", "git"), ("GitHub", "github"), ("WPLSoft · PLC", None),
    ]),
    ("magenta", "COURSES", "Also studying", [
        ("IoT", None), ("Embedded Systems", None), ("Robotics", None), ("Cyber Security", None),
        ("Wireless Communications", None), ("Pattern Recognition", None),
    ]),
]

# Featured repositories — names, descriptions, stacks and figures come from
# each repository's own public README.
PROJECTS = [
    dict(slug="lung-cancer", repo="lung-cancer-detection-deep-learning", accent="cyan",
         label="Deep learning · Medical imaging", title="Lung Cancer Detection",
         desc="CNN that classifies lung CT scans as Normal, Benign or Malignant, trained on the IQ-OTH/NCCD dataset.",
         tags=["Python", "TensorFlow", "Keras", "Google Colab"],
         stat="97.7%", stat_label="REPORTED ACCURACY", stat_sub="1,190 CT scans · 3 classes", visual="scan"),
    dict(slug="churn", repo="Customer-Churn-Prediction", accent="blue",
         label="Machine learning · Business analytics", title="Customer Churn Prediction",
         desc="Predicts telecom customer churn end to end: cleaning, EDA, feature engineering, model comparison and business insights.",
         tags=["pandas", "scikit-learn", "Seaborn", "Matplotlib"],
         stat="3", stat_label="MODELS COMPARED", stat_sub="LogReg · Random Forest · SVM", visual="curve"),
    dict(slug="personality", repo="ML-Customer-Personality-Analysis", accent="violet",
         label="Machine learning · Segmentation", title="Customer Personality Analysis",
         desc="Regression, classification and clustering on the Customer Personality Analysis dataset, after full EDA and preprocessing.",
         tags=["pandas", "NumPy", "scikit-learn", "Seaborn"],
         stat="3", stat_label="ML TASKS", stat_sub="Regression · Classification · Clustering", visual="clusters"),
    dict(slug="research", repo="Ai-research", accent="magenta",
         label="Research · Pattern recognition", title="AI Research",
         desc="Research reports, including the failure modes of dimensionality reduction: when PCA, LDA, Kernel PCA, t-SNE and UMAP break, and why.",
         tags=["Pattern Recognition", "Machine Learning", "Python"],
         stat="5", stat_label="TECHNIQUES ANALYZED", stat_sub="PCA · LDA · KPCA · t-SNE · UMAP", visual="pca"),
]

SECTIONS = [
    ("01", "About", "~/whoami"),
    ("02", "Toolkit", "~/stack"),
    ("03", "Featured work", "~/projects"),
    ("04", "GitHub activity", "~/activity"),
    ("05", "Connect", "~/contact"),
]

CONNECT_TITLE = "Let's build something intelligent."
CONNECT_SUB = "Open to AI/ML internships, research collaborations and learning opportunities."

BUTTONS = [
    ("linkedin", "LinkedIn", "https://www.linkedin.com/in/eng-mohammed-algoul/"),
    ("github", "Follow on GitHub", "https://github.com/Mohammed-Algoul"),
    ("repos", "All repositories", "https://github.com/Mohammed-Algoul?tab=repositories"),
]
