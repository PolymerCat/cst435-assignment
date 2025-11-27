from xmlrpc.server import SimpleXMLRPCServer
import re

def word_count(text):
    return len(text.split())

def sentence_count(text):
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences)

def max_letter_in_word(text):
    words = text.split()
    return max(words, key=len) if words else ""

def min_letter_in_word(text):
    words = text.split()
    return min(words, key=len) if words else ""

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("0.0.0.0", 9000), allow_none=True)
    print("RPC Server running on port 9000...")

    server.register_function(word_count)
    server.register_function(sentence_count)
    server.register_function(max_letter_in_word)
    server.register_function(min_letter_in_word)

    server.serve_forever()
