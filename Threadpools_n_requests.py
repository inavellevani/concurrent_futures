import concurrent.futures
import requests
import json

def get_url(url):
    try:
        response = requests.get(url)
        product_data = response.json()
        return product_data

    except Exception:
        return None

def process_group(urlss):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(get_url, urlss))
    return results

def main():
    base_url = "https://dummyjson.com/products/"
    urls = [f"{base_url}{i}" for i in range(1, 101)]
    url_grouping = [urls[i:i + 20] for i in range(0, len(urls), 20)]

    all_results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as thread_executor:
        futures = [thread_executor.submit(process_group, group) for group in url_grouping]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            all_results.extend(result)

    with open('output_data.json', 'w') as json_file:
        json.dump(all_results, json_file, indent=2)

    print("Done")

if __name__ == '__main__':
    main()