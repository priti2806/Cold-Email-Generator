import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Set up page configuration
st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

# ---------- Custom CSS for Styling ----------
st.markdown("""
    <style>
        .stApp {
            background-color: #87CEFA; /* Alice Blue */
        }

        .title-text {
            font-size: 40px;
            font-weight: 700;
            color: #2c3e50;
            text-align: center;
            margin: 20px 0 10px 0;
        }

        .subtitle-text {
            font-size: 16px;
            color: #34495e;
            text-align: center;
            margin-bottom: 20px;
        }

        .content-box {
            background-color: white;
            padding: 20px 30px;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
            max-width: 800px;
            margin: 0 auto;
        }

        .email-box {
            background-color: #fcfcfc;
            color: #2d2d2d;
            font-family: 'Courier New', Courier, monospace;
            padding: 15px 20px;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
            white-space: pre-wrap;
            margin-top: 10px;
            font-size: 14px;
            line-height: 1.4;
        }

        input {
            color: black !important;
        }

        .success-message {
            color: green;
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 5px;
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Main App ----------
def create_streamlit_app(llm, portfolio, clean_text):
    # Title Section
    st.markdown('<div class="title-text">📧 Cold Mail Generator</div>', unsafe_allow_html=True)
    #st.markdown('<div class="subtitle-text">Paste the job URL and instantly generate a professional cold email</div>', unsafe_allow_html=True)

    # Content Box
    #st.markdown('<div class="content-box">', unsafe_allow_html=True)

    url_input = st.text_input("🔗 Enter the Job URL:", value="https://www.google.com/about/careers/applications/jobs/results/74939955737961158-software-engineer-iii-google-cloud")
    submit_button = st.button("✨ Generate Cold Email")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            raw_data = loader.load().pop().page_content
            data = clean_text(raw_data)

            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            if not jobs:
                st.warning("⚠️ No jobs found on this page.")
                return

            # Only use the first job
            job = jobs[0]
            skills = job.get('skills', [])
            links = portfolio.query_links(skills)
            email = llm.write_mail(job, links)

            st.markdown('<div class="success-message">✅ Cold email generated successfully!</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="email-box">{email}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ An Error Occurred: {e}")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------- App Entry Point ----------
if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
