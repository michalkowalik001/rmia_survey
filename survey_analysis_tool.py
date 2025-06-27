import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_excel():
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Data preview:")
            st.dataframe(df.head(10))
            return df
        except Exception as e:
            st.error(f"Error loading file: {e}")
    return None

def get_inputs():
    question = st.number_input("Question number (e.g. 1 means Question1)", min_value=1, value=1)
    split = st.checkbox("Split the chart by another question?")
    split_q = None
    if split:
        split_q = st.number_input("Question number for split (e.g. 2 means Question2)", min_value=1, value=2)
    title = st.text_input("Chart title", "My chart")
    x_label = st.text_input("X-axis label", "Category")
    y_label = st.text_input("Y-axis label", "Number of responses")

    st.markdown("### Appearance settings")
    font_size = st.slider("Font size", min_value=8, max_value=24, value=12)
    fig_width = st.slider("Chart width", min_value=4, max_value=12, value=6)
    fig_height = st.slider("Chart height", min_value=3, max_value=10, value=3)

    fixed_y = st.checkbox("Set fixed Y-axis range?")
    y_max = None
    if fixed_y:
        y_max = st.number_input("Fixed Y-axis max value", min_value=1, value=10)

    return question, split, split_q, title, x_label, y_label, y_max, font_size, fig_width, fig_height


def plot_chart(data, title, x_label, y_label, y_max, font_size, fig_width, fig_height, all_categories=None):
    counts = data.value_counts().reindex(all_categories).fillna(0).sort_index()
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    bars = ax.bar(counts.index.astype(str), counts.values, color="skyblue", edgecolor="black")

    ax.set_title(title, fontsize=font_size + 2)
    ax.set_ylabel(y_label, fontsize=font_size)
    ax.set_xlabel(x_label, fontsize=font_size)
    ax.tick_params(axis='both', labelsize=font_size)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.05, str(int(height)),
                ha='center', va='bottom', fontsize=font_size)

    if y_max is not None:
        ax.set_ylim(0, y_max)

    plt.tight_layout()
    st.pyplot(fig)

def plot_split_chart(data, group, title, x_label, y_label, y_max, font_size, fig_width, fig_height, all_categories=None):
    df = pd.DataFrame({'value': data, 'group': group})
    groups = df['group'].dropna().unique()
    groups.sort()

    for g in groups:
        group_data = df[df['group'] == g]['value']
        st.subheader(f"{title} - Group: {g}")
        plot_chart(group_data, f"{title} - Group {g}", x_label, y_label,
                   y_max, font_size, fig_width, fig_height, all_categories)
        
def show_summary_table(data, group=None):
    st.markdown("### Summary statistics")

    if group is not None:
        df = pd.DataFrame({'value': data, 'group': group})
        groups = df['group'].dropna().unique()
        groups.sort()
        summary_tables = []

        for g in groups:
            group_data = df[df['group'] == g]['value']
            if pd.api.types.is_numeric_dtype(group_data):
                summary = group_data.describe()[['count', 'mean', 'std', 'min', 'max']].to_frame().T
                summary[['mean', 'std']] = summary[['mean', 'std']].round(2)
            else:
                summary = group_data.describe()[['count', 'unique', 'top', 'freq']].to_frame().T
            summary.index = [f"Group {g}"]
            summary_tables.append(summary)

        full_summary = pd.concat(summary_tables)
        st.dataframe(full_summary)

    else:
        if pd.api.types.is_numeric_dtype(data):
            summary = data.describe()[['count', 'mean', 'std', 'min', 'max']]
        else:
            summary = data.describe()[['count', 'unique', 'top', 'freq']]
        st.dataframe(summary.to_frame().T)



def main():
    st.title("Survey Chart Generator")

    df = load_excel()
    if df is None:
        return

    question, split, split_q, title, x_label, y_label, y_max, font_size, fig_width, fig_height = get_inputs()

    data_col = f"Question{question}"
    if data_col not in df.columns:
        st.error(f"Column '{data_col}' not found in the dataset")
        return

    data = df[data_col].dropna()
    all_categories = sorted(df[data_col].dropna().unique())

    if split:
        split_col = f"Question{split_q}"
        if split_col not in df.columns:
            st.error(f"Column '{split_col}' not found in the dataset")
            return

        group = df[split_col].dropna()
        min_len = min(len(data), len(group))
        data = data.iloc[:min_len]
        group = group.iloc[:min_len]

        show_summary_table(data, group)
        plot_split_chart(data, group, title, x_label, y_label,
                         y_max, font_size, fig_width, fig_height, all_categories)
    else:
        show_summary_table(data)
        plot_chart(data, title, x_label, y_label,
                   y_max, font_size, fig_width, fig_height, all_categories)



if __name__ == "__main__":
    main()
