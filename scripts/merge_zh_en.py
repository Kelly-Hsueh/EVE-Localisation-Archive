"""
merge_zh_en.py – Original reference implementation for merging zh + en pickles.

This file is kept as-is from the original reference.
The production merge logic lives in merge.py which extends this approach
to support all EVE localization languages.
"""

import pickle
import json


def load_pickle(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)


def merge_zh_en(zh_file, en_file, output_file):
    zh_data_tuple = load_pickle(zh_file)
    zh_data = zh_data_tuple[1]
    en_data_tuple = load_pickle(en_file)
    en_data = en_data_tuple[1]

    merged = {}
    all_ids = set(zh_data.keys()) | set(en_data.keys())
    for msg_id in sorted(all_ids):
        zh_text = zh_data.get(msg_id, "")
        en_text = en_data.get(msg_id, "")
        if isinstance(zh_text, tuple):
            zh_text = zh_text[0] if zh_text and zh_text[0] is not None else ""
        if isinstance(en_text, tuple):
            en_text = en_text[0] if en_text and en_text[0] is not None else ""
        merged[str(msg_id)] = {"zh": zh_text, "en": en_text}

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=4)
    print(f"Merged zh and en data saved to {output_file}")


if __name__ == "__main__":
    merge_zh_en("localization_fsd_zh.pickle",
                "localization_fsd_en-us.pickle", "merged_zh_en.json")
