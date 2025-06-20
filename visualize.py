import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

def visualize_data(csv_path='products.csv'):
    # Read with correct encoding
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

    # Clean Price column
    df['Price'] = df['Price'].astype(str).apply(lambda x: re.sub(r'[^\d.]', '', x))
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Convert rating text to number
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['Rating'] = df['Rating'].map(rating_map)

    # Make plots folder
    os.makedirs('static/plots', exist_ok=True)

    ### Plot 1: Price Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Price'].dropna(), bins=10, kde=True)
    plt.title('Book Price Distribution')
    plt.xlabel('Price (£)')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('static/plots/price_distribution.png')
    plt.close()

    ### Plot 2: Rating Count
    plt.figure(figsize=(6, 4))
    sns.countplot(x='Rating', data=df)
    plt.title('Book Rating Count')
    plt.xlabel('Rating (Stars)')
    plt.ylabel('Number of Books')
    plt.tight_layout()
    plt.savefig('static/plots/rating_count.png')
    plt.close()

    ### Plot 3: Average Price per Rating
    plt.figure(figsize=(6, 4))
    avg_price = df.groupby('Rating')['Price'].mean().reset_index()
    sns.barplot(data=avg_price, x='Rating', y='Price')
    plt.title('Average Book Price by Rating')
    plt.xlabel('Rating (Stars)')
    plt.ylabel('Average Price (£)')
    plt.tight_layout()
    plt.savefig('static/plots/avg_price_by_rating.png')
    plt.close()

    ### Plot 4: Top 10 Most Expensive Books
    top10 = df.nlargest(10, 'Price')[['Title', 'Price']]
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top10, x='Price', y='Title', palette='magma')
    plt.title('Top 10 Most Expensive Books')
    plt.xlabel('Price (£)')
    plt.ylabel('Book Title')
    plt.tight_layout()
    plt.savefig('static/plots/top10_expensive_books.png')
    plt.close()

    ### Plot 5: Boxplot - Price Distribution per Rating
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x='Rating', y='Price')
    plt.title('Price Distribution by Rating')
    plt.xlabel('Rating (Stars)')
    plt.ylabel('Price (£)')
    plt.tight_layout()
    plt.savefig('static/plots/boxplot_price_rating.png')
    plt.close()

    print("✅ All visualizations generated successfully!")

# Run this file to generate all plots
if __name__ == "__main__":
    visualize_data()
