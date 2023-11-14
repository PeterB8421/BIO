import glob
import json
import os.path
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print('Usage: python plot_results.py <dir>\n'
              '<dir> = Directory containing dataset with json subdirectories', file=sys.stderr)
        exit(1)
    path = sys.argv[1]
    results_json = glob.glob(os.path.join(path, '*/json/*.json'))
    dfs = []
    for file in results_json:
        with open(file, 'r') as f:
            data = json.load(f)
            result_data = [
                {
                    'src'       : item['src'],
                    'target'    : item['target'],
                    'similarity': item['result'][0]['face_matches'][0]['similarity'],
                    'category': os.path.basename(item['target']).split('_')[2].replace('.jpg', '')
                }
                for item in data
            ]
            df = pd.DataFrame(result_data)
            dfs.append(df)
    result_df = pd.concat(dfs, ignore_index=True)
    print(result_df['similarity'], result_df['src'], result_df['target'])
    sns.boxplot(result_df, x='category', y='similarity')
    name = 'graph.png'
    if len(sys.argv) == 3:
        name = sys.argv[2]
    plt.savefig(name)
    plt.show()


if __name__ == '__main__':
    main()
