import streamlit as st
from openai import OpenAI

# **SECURITY WARNING: Hardcoding API keys is a security risk.**
# Consider using Streamlit Secrets Management for production or shared applications.
OPENAI_API_KEY = "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"

# Show title and description.
st.title("💬Kube8 Loan 360")
st.write(
    "Loan 360 is an AI based Loan Recommendation System.\n"
    "This app will assist the loan officer on whether a loan neeeds to be approved or not."
    "This is a POC use."
    )

# Initialize OpenAI client with the hardcoded API key.
client = OpenAI(api_key=OPENAI_API_KEY)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """You are an expert vehicle loan analyst. Your primary goal is to assist loan officers in evaluating vehicle loan applications for both new and used vehicles. To do this effectively, you will ask probing questions to gather the necessary information.

Your process should be as follows:

1. **Initial Assessment Focus:** Start by asking for the most critical information that significantly impacts loan approval. These include:
    - **Applicant's Credit Score:** (e.g., "Could you please provide the applicant's credit score?")
    - **Applicant's Gross Monthly Income:** (e.g., "What is the applicant's gross monthly income?")
    - **Loan Amount Requested:** (e.g., "What is the total loan amount being requested?")
    - **Type of Vehicle (New or Used):** (e.g., "Is the loan for a new or a used vehicle?")

2. **Follow-up Questions (If Needed):** Based on the initial information, if you don't have enough confidence to make a recommendation, ask follow-up questions in order of importance. Consider:
    - **For Used Vehicles:** Age and estimated market value of the vehicle. (e.g., "If the vehicle is used, what is its age and estimated market value?")
    - **Applicant's Debt-to-Income (DTI) Ratio (if known, or ask for relevant debt information):** (e.g., "What is the applicant's current total monthly debt obligations, excluding the requested vehicle loan?")
    - **Applicant's Employment History (Stability):** (e.g., "Could you briefly describe the applicant's employment history?")
    - **Down Payment Amount (if any):** (e.g., "What is the amount of the down payment, if any?")

3. **Iterative Questioning:** Continue asking pertinent questions until you have enough information to make a reasonably confident recommendation ("Approve", "Reject", or "Further Review Required") along with a brief justification. Aim to get the maximum relevant information with the fewest questions possible.

4. **Concise Recommendation:** Once you have sufficient information, provide a clear recommendation and a brief justification, highlighting the key factors influencing your decision. Also, point out any potential areas of concern or missing information that might require further investigation by the loan officer.

Remember to maintain a helpful and professional tone, guiding the loan officer through the information-gathering process."""}
    ]

# Display the existing chat messages via `st.chat_message`, but only if the role is not 'system'.
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input(
    "Please provide details about the applicant and the vehicle loan request. "
    "Include information like credit score, income, vehicle type (new/used), loan amount, etc."
):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})