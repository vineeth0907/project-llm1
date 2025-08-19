# Conversational LLM Web App (Streamlit + Google Gemini) - ChatGPT Style UI

import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ChatGPT-like styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .stChatMessage {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        margin: 8px 0;
        padding: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stChatMessage[data-testid="chatMessage"] {
        background: rgba(255, 255, 255, 0.95);
    }
    
    .stChatInput {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        border: 2px solid #e0e0e0;
        padding: 12px 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stChatInput:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .chat-header {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 0 0 20px 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 20px;
        margin: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        margin: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Google Gemini API Key
GEMINI_API_KEY = "AIzaSyDY7hbsK8pVPSG-i08-eed21m5bmxYPzQU"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main chat interface
def main():
    # Header
    with st.container():
        st.markdown("""
        <div class="chat-header">
            <h1 style="color: #333; margin: 0; font-size: 2.5em;">🤖 AI Chat Assistant</h1>
            <p style="color: #666; margin: 10px 0 0 0; font-size: 1.1em;">Powered by Google Gemini 1.5 Flash</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat container
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # User input
    user_prompt = st.chat_input("Type your message here...")
    
    # Handle user message
    if user_prompt:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response = model.generate_content(user_prompt)
                    ai_response = response.text
                    st.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                except Exception as e:
                    error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Sidebar with controls
    with st.sidebar:
        st.markdown('<div class="sidebar .sidebar-content">', unsafe_allow_html=True)
        
        st.header("🎛️ Chat Controls")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Export chat
        if st.session_state.messages:
            chat_export = ""
            for msg in st.session_state.messages:
                role_emoji = "👤" if msg["role"] == "user" else "🤖"
                chat_export += f"{role_emoji} {msg['role'].capitalize()}: {msg['content']}\n\n"
            
            st.download_button(
                "📥 Export Chat",
                chat_export,
                file_name="chat_history.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        st.markdown("---")
        
        # Model info
        st.subheader("🤖 Model Info")
        st.info("**Gemini 1.5 Flash**\n\n- Fast & efficient responses\n- Advanced reasoning\n- Real-time chat")
        
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 