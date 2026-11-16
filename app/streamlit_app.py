
import os

import requests
import streamlit as st


API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000"
)

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Research Agent")
st.write(
    "Research any topic using Tavily web search "
    "and Google Gemini."
)

st.divider()

query = st.text_area(
    "What would you like to research?",
    placeholder="Example: Latest developments in Generative AI in 2026",
    height=120
)

if st.button("Generate Research Report", type="primary"):
    if not query.strip():
        st.warning("Please enter a research topic.")

    elif len(query.strip()) < 5:
        st.warning("Your research topic must contain at least 5 characters.")

    else:
        try:
            with st.spinner("Searching the web and generating your report..."):
                response = requests.post(
                    f"{API_URL}/research",
                    json={"query": query.strip()},
                    timeout=180
                )

            if response.status_code == 200:
                result = response.json()

                st.success("Research report generated!")

                st.subheader("Research Report")
                st.markdown(result["report"])

                st.divider()

                st.subheader("Sources")

                for index, source in enumerate(
                    result.get("sources", []),
                    start=1
                ):
                    st.markdown(
                        f"{index}. [{source['title']}]({source['url']})"
                    )

                st.download_button(
                    label="Download Report",
                    data=result["report"],
                    file_name="research_report.md",
                    mime="text/markdown"
                )

            else:
                try:
                    error_detail = response.json().get(
                        "detail",
                        "Research request failed."
                    )
                except ValueError:
                    error_detail = "Research request failed."

                st.error(f"API Error: {error_detail}")

        except requests.exceptions.Timeout:
            st.error(
                "The research request timed out. "
                "Please try again."
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the FastAPI backend. "
                "Check whether the backend is running."
            )

        except requests.exceptions.RequestException as exc:
            st.error(f"Request failed: {exc}")
