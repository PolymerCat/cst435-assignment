import xmlrpc.client
import time

def read_file(path):
    with open(path, "r", encoding="utf8") as f:
        return f.read()

if __name__ == "__main__":
    server = xmlrpc.client.ServerProxy("http://localhost:9000/")

    text = read_file("large.txt")

    print("\n--- Starting RPC Processing ---")

    overall_start = time.time()

    # Word count
    start = time.time()
    wc = server.word_count(text)
    wc_time = time.time() - start

    # Sentence count
    start = time.time()
    sc = server.sentence_count(text)
    sc_time = time.time() - start

    # Longest word
    start = time.time()
    mw = server.max_letter_in_word(text)
    mw_time = time.time() - start

    # Shortest word
    start = time.time()
    sw = server.min_letter_in_word(text)
    sw_time = time.time() - start

    overall_time = time.time() - overall_start

    print("\n===== RESULTS =====")
    print(f"Word Count: {wc}   (Time: {wc_time:.6f} sec)")
    print(f"Sentence Count: {sc}   (Time: {sc_time:.6f} sec)")
    print(f"Longest Word: {mw}   (Time: {mw_time:.6f} sec)")
    print(f"Shortest Word: {sw}   (Time: {sw_time:.6f} sec)")

    print("\n===== OVERALL EXECUTION TIME =====")
    print(f"{overall_time:.6f} seconds\n")
