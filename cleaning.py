import json

def mask_email(email):
    if not email or '@' not in email:
        return email
    parts = email.split('@')
    return parts[0][0] + "***@" + parts[1]


def clean_data(input_file, output_file):
    # Load the toxic data
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {input_file}.")
        return

    seen_ids = set()
    sanitized_data = []

    for item in data:
        item_id = item.get('id')
        if item_id is None or item_id in seen_ids:
            continue
        
        price = item.get('price')
        if price is None:
            continue
            
        try:
            price = float(price)
        except (ValueError, TypeError):
            continue

        if price > 5000:
            continue
            
        if price < 0:
            continue

        if 'name' in item:
            del item['name']
            
        if 'email' in item:
            item['email'] = mask_email(item['email'])
        sanitized_data.append(item)
        seen_ids.add(item_id)

    # Save the sanitized data
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sanitized_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving file: {e}")
        return
    print(f"Successfully sanitized data. Output saved to {output_file}")
    print(f"Original records: {len(data)}")
    print(f"Sanitized records: {len(sanitized_data)}")

if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    INPUT_PATH = os.path.join(script_dir, "toxic_sample.json")
    OUTPUT_PATH = os.path.join(script_dir, "sanitized_sample.json")
    clean_data(INPUT_PATH, OUTPUT_PATH)
