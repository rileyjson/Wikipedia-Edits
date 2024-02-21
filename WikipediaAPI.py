import tkinter as tk
import json
import ssl
from urllib.request import urlopen

def get_wikipedia_url(article_name):
    formatted_name = article_name.replace(' ', '%20')
    return f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles={formatted_name}&rvprop=timestamp|user&rvlimit=30&redirects"

def fetch_wikipedia_data(url):
    context = ssl._create_unverified_context()
    try:
        response = urlopen(url, context=context)
        return json.loads(response.read())
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def parse_wikipedia_data(data, article_name):
    if not data:
        return "Network error occurred."

    pages = data.get("query", {}).get("pages", {})
    for _, page_info in pages.items():
        if 'revisions' not in page_info:
            return f"No Wikipedia page found for {article_name}."

        revisions = page_info.get("revisions", [])
        result_lines = [f'{rev["timestamp"]} {rev["user"]}' for rev in revisions]

        if 'redirects' in data['query']:
            result_lines.insert(0, f"Redirected to {page_info['title']}")
            

        return '\n'.join(result_lines)

    return f"No Wikipedia data found for {article_name}"  

def create_gui():
    def search_callback():
        article_name = entry.get().strip()
        if not article_name:
            result_label["text"] = "You must provide an article name."
            return

        url = get_wikipedia_url(article_name)
        data = fetch_wikipedia_data(url)
        result_text = parse_wikipedia_data(data, article_name)
        result_label["text"] = result_text

    window = tk.Tk()
    window.title("Wikipedia Recent Changes Viewer")
    window.geometry("800x600")

    prompt_label = tk.Label(window, text="Enter a Wikipedia article name:")
    entry = tk.Entry(window)
    search_button = tk.Button(window, text="Search", command=search_callback)
    result_label = tk.Label(window, text="", wraplength=800)

    prompt_label.pack(pady=10)
    entry.pack(pady=10, padx=20, fill=tk.X)
    search_button.pack(pady=10)
    result_label.pack(pady=10, padx=20)

    window.mainloop()

def main():
    while True:
        print("\nChoose an option:")
        print("1) Search Through Command Line")
        print("2) Search Through GUI")
        print("3) Quit")
        option = input("Enter option: ")

        if option == "1":
            article_name = input("\nEnter the Wikipedia article name: ").strip()
            if not article_name:
                print("You must provide an article name.")
                continue

            url = get_wikipedia_url(article_name)
            data = fetch_wikipedia_data(url)
            result_text = parse_wikipedia_data(data, article_name)
            print("\n" + result_text if result_text else "No result.")

        elif option == "2":
            create_gui()
            break  # Exit loop after closing GUI

        elif option == "3":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
