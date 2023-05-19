import networkx as nx
import os
import pickle
import stanza
from stanza.server import CoreNLPClient

os.environ["$CORENLP_HOME"] = "/home/rain/.stanfordnlp_resources/stanford-corenlp-4.1.0"
client = CoreNLPClient(timeout=150000000, be_quiet=True, annotators=['openie'], endpoint='http://localhost:1234')
client.start()

with open("./data/nonpsychotic_posts.pickle", "rb") as p:
    nonpsychotic_posts = pickle.load(p)

i = 0
for username, post_info in nonpsychotic_posts.items():
    for post in post_info:
        post_text = post["text"].lower()
        doc = client.annotate(post_text, output_format="json")
        triples = []
        for sentence in doc['sentences']:
            for triple in sentence['openie']:
                triples.append({
                    'subject': triple['subject'],
                    'relation': triple['relation'],
                    'object': triple['object']
                })
        g = nx.DiGraph()
        for triplet in triples:
            g.add_edge(triplet["subject"], triplet["object"], relation=triplet["relation"])
        nx.write_gml(g, "./data/nonpsychotic_graphs/nonpsychotic_post" + str(i) + ".gml")
        print("Nonpsychotic graph ", i, " completed successfully!")
        i += 1
        if i == 4938:
            break
    if i == 4938:
        break

with open("./data/psychotic_posts.pickle", "rb") as p:
    psychotic_posts = pickle.load(p)

i = 0
for username, post_info in psychotic_posts.items():
    for post in post_info:
        post_text = post["text"].lower()
        doc = client.annotate(post_text, output_format="json")
        triples = []
        for sentence in doc['sentences']:
            for triple in sentence['openie']:
                triples.append({
                    'subject': triple['subject'],
                    'relation': triple['relation'],
                    'object': triple['object']
                })
        g = nx.DiGraph()
        for triplet in triples:
            g.add_edge(triplet["subject"], triplet["object"], relation=triplet["relation"])
        nx.write_gml(g, "./data/psychotic_graphs/psychotic_post" + str(i) + ".gml")
        print("Psychotic graph ", i, " completed successfully!")
        i += 1

client.stop()