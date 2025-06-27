import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = [1,2,3,4,2,1,2,3,4,2,1,3,3,2,3,4,1,2,3,4,2,3,4,5,2,1,2,3,5]
divide_by= [1,1,2,1,2,1,2,3,2,2,1,2,1,3,2,1,1,2,1,1,2,2,2,2,2,1,2,1,1]

question = st.number_input("Select question number", min_value=1, max_value=20, value=1, step=1)
n_categories= st.number_input("How many possible categories are in this question", value=5, min_value=1 , max_value=10)
y_axis= st.text_input("How do you want to call your y-axis?", "(name of your y-axis)")
x_axis= st.text_input("How do you want to call your x-axis?", "(name of your x-axis)")
title= st.text_input("How do you want to title your graphs?", "(name of your graph)")
split = st.checkbox("Split chart by some question?")
split_q = st.number_input("By which question do you want to split your chart", min_value=1, max_value=20, value=1, step=1)
chart_type = st.selectbox("Select chart type", options=["Bar chart", "Pie chart"])

full_index = pd.Index(range(1, n_categories + 1))

if split:
    df = pd.DataFrame({'category': data, 'group': divide_by})
    groups = df['group'].unique()
    groups.sort()
    counts_dict = {}
    for g in groups:
        counts = df[df['group'] == g]['category'].value_counts().reindex(full_index, fill_value=0)
        counts_dict[g] = counts

    if chart_type == "Bar chart":
        max_y = max(count.max() for count in counts_dict.values()) + 1
        fig, axes = plt.subplots(len(groups), 1, figsize=(8, 4*len(groups)), sharey=True)
        if len(groups) == 1:
            axes = [axes]
        colors = plt.cm.get_cmap('tab10', len(groups))

        for i, g in enumerate(groups):
            counts = counts_dict[g]
            counts.plot(kind='bar', ax=axes[i], color=colors(i))
            axes[i].set_title(f"{title} - Group {g}")
            axes[i].set_ylabel(y_axis)
            axes[i].set_xlabel(x_axis)
            axes[i].set_ylim(0, max_y)
            for idx, v in enumerate(counts):
                axes[i].text(idx, v + 0.1, str(v), ha='center')
        plt.tight_layout()
        st.pyplot(fig)

    else:  # Pie chart
        fig, axes = plt.subplots(len(groups), 1, figsize=(6, 5*len(groups)))
        if len(groups) == 1:
            axes = [axes]

        # Generate distinct colors for categories
        category_colors = plt.cm.tab20(np.linspace(0, 1, n_categories))

        for i, g in enumerate(groups):
            counts = counts_dict[g]
            colors = category_colors[:len(counts)]
            counts.plot(kind='pie', ax=axes[i], autopct='%1.1f%%', startangle=90, colors=colors)
            axes[i].set_title(f"{title} - Group {g}")
            axes[i].set_ylabel("")
        plt.tight_layout()
        st.pyplot(fig)

else:
    counts = pd.Series(data).value_counts().reindex(full_index, fill_value=0)
    if chart_type == "Bar chart":
        fig, ax = plt.subplots(figsize=(8,4))
        counts.plot(kind='bar', ax=ax, color='blue')
        ax.set_title(title)
        ax.set_ylabel(y_axis)
        ax.set_xlabel(x_axis)
        for i, v in enumerate(counts):
            ax.text(i, v + 0.1, str(v), ha='center')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        fig, ax = plt.subplots(figsize=(6,6))
        category_colors = plt.cm.tab20(np.linspace(0, 1, n_categories))
        counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, colors=category_colors)
        ax.set_ylabel("")
        ax.set_title(title)
        plt.tight_layout()
        st.pyplot(fig)
