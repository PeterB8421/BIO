import glob
import json
import os.path
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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
    sns.boxplot(result_df, x='category', y='similarity')
    plt.ylim(bottom=0)
    plt.gca().set_title(sys.argv[3])
    plt.savefig(sys.argv[2])


if __name__ == '__main__':
    main()
