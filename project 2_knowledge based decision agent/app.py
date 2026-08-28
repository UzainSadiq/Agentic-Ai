import streamlit as st
from agent import run_agent
st.set_page_config(page_title='Edu Agent',page_icon='🎓',layout='wide')
st.title('🎓 Edu Agent')
st.caption('Knowledge-Based Decision Agent • OpenRouter Free LLM • Local Embeddings • Chroma • LangGraph')
with st.sidebar:
    st.header('Project'); st.write('Ask questions about the educational knowledge base.'); st.divider(); st.write('Query Analysis → Retrieval → Agent Reasoning → Answer')
if 'messages' not in st.session_state: st.session_state.messages=[]
for m in st.session_state.messages:
    with st.chat_message(m['role']): st.markdown(m['content'])
if prompt:=st.chat_input('Ask about admission, courses, scholarships, attendance...'):
    st.session_state.messages.append({'role':'user','content':prompt})
    with st.chat_message('user'): st.markdown(prompt)
    with st.chat_message('assistant'):
        with st.status('Searching knowledge base and reasoning...',expanded=False): result=run_agent(prompt)
        st.markdown(result['answer'])
        if result.get('sources'):
            with st.expander('📚 Retrieved sources'):
                for s in result['sources']: st.markdown(f"**{s['source']}** — chunk {s['chunk']}  \n{s['preview']}")
    st.session_state.messages.append({'role':'assistant','content':result['answer']})
