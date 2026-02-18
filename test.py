from sentence_transformers import SentenceTransformer

# Load a pre-trained sentence embedding model
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# Convert a sentence to vector
vector = model.encode("The movie was fantastic!")
print(vector.shape)  # Check embedding dimensions
