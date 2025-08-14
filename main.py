import streamlit as st
from llama_rag import scrape_urls, generate_response


st.set_page_config(page_title="Cybersecurity Threat Q&A", layout="centered")
st.title("🔐 Cybersecurity Threat Intelligence Q&A")
st.markdown("Ask questions about the latest cybersecurity vulnerabilities and advisories.")

# Step 1: Number of URLs
num_urls = st.number_input("How many URLs do you want to process?", min_value=1, max_value=10, step=1)

# Step 2: URL inputs
urls = []
for i in range(num_urls):
    url = st.text_input(f"Enter URL {i+1}")
    if url:
        urls.append(url)

# Step 3: Question input
query = st.text_area("What do you want to know?")

# Step 4: Button
if st.button("🔍 Generate Cybersecurity Insights"):
    if not urls or not query.strip():
        st.error("Please enter at least one URL and a question.")
    else:
        index = scrape_urls(urls)
        answer = generate_response(index, query)

        st.subheader("Answer")
        st.write(answer)

