import os
import replicate
import streamlit as st
from duckduckgo_search import DDGS

# 🔐 Replicate API Token (Recommended: use st.secrets or environment variable)
REPLICATE_API_TOKEN = "r8_68cVwq3RphFx77wOOLXYwuqcC32FlYt117MhC"  # Replace with your token
client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# 🧠 IBM Granite Model ID
GRANITE_MODEL = "ibm-granite/granite-3.3-8b-instruct"

# 🔎 DuckDuckGo Search
def search_duckduckgo(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(
                f"{query} site:gov OR site:org OR site:nationalgeographic.com OR site:carbontrust.com OR site:greenpeace.org",
                max_results=3
            )
            return "\n".join([f"- {r['title']}: {r['href']}" for r in results])
    except Exception as e:
        return "- No external sources found or error during search."

# 🤖 Call IBM Granite via Replicate
def query_replicate(prompt):
    try:
        output = client.run(GRANITE_MODEL, input={"prompt": prompt, "max_new_tokens": 350})
        return "".join(output)
    except Exception as e:
        return f"❌ Error from Replicate: {str(e)}"

# 🌱 Agent 1: Recipe generator
def eco_lifestyle_agent(user_prompt, location, category):
    search_query = f"{user_prompt} {category} in {location}" if location else f"{user_prompt} {category}"
    sources = search_duckduckgo(search_query) or "- No sources found."
    system_prompt = (
        f"You are Recipe generator AI, helping users prepare meals.\n"
        f"Focus: personalized sustainable recipe advice, ingredient tips, and care to be taken.\n"
        f"User Location: {location or 'unspecified'} | Topic: {category}\n"
        f"User Query: {user_prompt}\n\nSources:\n{sources}\n\nAnswer:"
    )
    return query_replicate(system_prompt)

# 🛍️ Agent 2: Ingredient Finder
def eco_product_agent(user_prompt, location):
    search_query = f"{user_prompt} recipe {location}"
    sources = search_duckduckgo(search_query) or "- No product results found."
    system_prompt = (
        f"You are Ingredient Finder. Recommend ingredients for the recipe or alternatives.\n"
        f"Location: {location or 'global'} | Query: {user_prompt}\n"
        f"Sources:\n{sources}\n\nSuggest useful and sustainable alternatives with brief explanation."
    )
    return query_replicate(system_prompt)

# 🔄 Agent 3: Recipe Fixer
def recycling_rules_agent(user_prompt, location):
    search_query = f"{user_prompt} recipe fix in {location}"
    sources = search_duckduckgo(search_query) or "- No fix found."
    system_prompt = (
        f"You are Recipe Fixer Bot. Help users understand what changes can be made to the recipe.\n"
        f"Location: {location or 'not specified'} | Query: {user_prompt}\n"
        f"Sources:\n{sources}\n\nAnswer:"
    )
    return query_replicate(system_prompt)


# 🎨 Streamlit App
st.set_page_config(page_title="🌿 Multi-Agent Recipe Assistant", layout="wide")
st.title("🌿 Multi-Agent Recipe Generator Assistant")
st.markdown("Powered by IBM Granite + RAG | Get recipe tips, suggestions, and fixing current food items.")

# Sidebar for navigation
st.sidebar.title("Navigation")
tab = st.sidebar.radio("Choose Agent", ["🌱 Recipe Agent", "🛍️ Recipe Finder", "🔄 Recipe Fixer"])

# 🌱 Tab 1 - Recipe Agent
if tab == "🌱 Recipe Agent":
    st.subheader("🌱 Recipe Agent")
    q1 = st.text_input("Ask what food item you can create")
    l1 = st.text_input("Your location", placeholder="e.g., Mumbai")
    c1 = st.selectbox("Topic", ["Home", "Travel", "Shopping", "fixing current recipe", "healthy recipe", "Diet", "General"], index=6)
    if st.button("Get Advice"):
        if q1.strip():
            response = eco_lifestyle_agent(q1, l1, c1)
            st.text_area("Response", value=response, height=250)

# 🛍️ Tab 2 - Recipe Finder
elif tab == "🛍️ Recipe Finder":
    st.subheader("🛍️ Recipe Finder")
    q2 = st.text_input("Any query related to recipe (e.g., I have paneer, tomato, bread)")
    l2 = st.text_input("Your location", placeholder="e.g., India")
    if st.button("Find Recipes / Ingredients"):
        if q2.strip():
            response = eco_product_agent(q2, l2)
            st.text_area("Recipe Suggestions / Ingredient Alternatives", value=response, height=250)

# 🔄 Tab 3 - Recipe Fixer
elif tab == "🔄 Recipe Fixer":
    st.subheader("🔄 Recipe Fixer Bot")
    q3 = st.text_input("Fixing current recipe (e.g., Can I fix my current recipe?)")
    l3 = st.text_input("Your location", placeholder="e.g., Delhi")
    if st.button("Fix Recipe"):
        if q3.strip():
            response = recycling_rules_agent(q3, l3)
            st.text_area("Fixing Guidance", value=response, height=250)
