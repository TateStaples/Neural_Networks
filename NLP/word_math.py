import gensim

model = gensim.models.KeyedVectors.load("/Users/22staples/PycharmProjects/Neural_Networks/NLP/google_embedding_keyedvec_300")# load_word2vec_format('GoogleNews-vectors-negative300.bin', binary = True)
# model.init_sims(True)
# model.save(fname_or_handle="google_embedding_keyedvec_300")
amount_answers = 5


if __name__ == '__main__':
    print("model loaded")
    while True:
        response = input("Enter equation or type done:  ").lower()
        if response == "done":
            break
        words = response.split()
        postive = []
        negative = []
        pos = True
        for word in words:
            if word == "+":
                pos = True
            elif word == "-":
                pos = False
            elif word not in model.vocab:
                print(f"{word} not found")
                continue
            elif pos:
                postive.append(word)
            else:
                negative.append(word)
        print("calculating...")
        if len(postive) == 0 and len(negative) == 0:
            print("Error: invalid equation\n")
            continue
        for i, result in enumerate(model.most_similar(positive=postive, negative=negative, topn=amount_answers)):
            word, relation = result
            print(f"{i+1}: {word} - {relation}")
        print()  # buffer
    print("Goodbye!")