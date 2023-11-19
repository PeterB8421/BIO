import glob
import json
import os.path
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def get_category(filename : str):
    cat = filename.split('_')[2]
    if cat == 'ref.jpg':
        cat = 'cross'
    return cat.replace('.jpg', '')


def main():
    # sys.argv [0] = Script pathname, [1] = path, [2] = output filename, [3] = graph title
    if len(sys.argv) != 4:
        print('Usage: python plot_results.py <dir> <name> <label>\n'
              '<dir> = Directory containing dataset with json subdirectories\n'
              '<name> = Name of the output file with its extension.\n'
              '<label> = Label for the graph.', file=sys.stderr)
        exit(1)
    path = sys.argv[1]
    results_json = glob.glob(os.path.join(path, '*/json/*.json'))
    results_json += glob.glob(os.path.join(path, '*/cross*.json'))
    dfs = []
    for file in results_json:
        with open(file, 'r') as f:
            data = json.load(f)
            result_data = [
                {
                    'src'       : item['src'],
                    'target'    : item['target'],
                    'similarity': item['result'][0]['face_matches'][0]['similarity'],
                    'category': get_category(os.path.basename(item['target']))
                }
                for item in data
            ]
            df = pd.DataFrame(result_data)
            dfs.append(df)
    result_df = pd.concat(dfs, ignore_index=True)
    # result_df.to_csv('results_women_deepfakes.csv')
    if (result_df['target'].str.contains('_result.jpg')).any():
        cols = ['obscure', 'glasses', 'hair', 'ref']
        result_df = result_df[result_df['category'] != 'cross']
    else:
        cols = ['obscure', 'glasses', 'hair', 'cross']
    sns.boxplot(result_df, x='category', y='similarity', order=cols)
    plt.ylim(bottom=0)
    plt.gca().set_title(sys.argv[3])
    plt.savefig(sys.argv[2])


if __name__ == '__main__':
    main()
