from pprint import pprint
import time
import streamlit as st
from graph_creator import GraphCreator
from load_data_source import LoadDataSource
from vectorstore_creator import VectorStoreCreator

st.title("CalmAcademia")
#Creating VectorStore:
urls=LoadDataSource("web_urls.txt")
if "vectorstore_path" not in st.session_state:
    st.session_state.vectorstore_path=VectorStoreCreator(urls)

#Graph Creation
if "app" not in st.session_state:
    st.session_state.app=GraphCreator()

if "ind" not in st.session_state:
    st.session_state.ind=1

if "thread_id" not in st.session_state:
    st.session_state.thread_id=1

if "fun_game_initializer" not in st.session_state:
    st.session_state.fun_game_initializer=False

if "fun_game_type" not in st.session_state:
    st.session_state.fun_game_type=None

if "fun_game_question" not in st.session_state:
    st.session_state.fun_game_question=None

if "fun_game_phase" not in st.session_state:
    st.session_state.fun_game_phase=False

if "i_spy_replayer" not in st.session_state:
    st.session_state.i_spy_replayer=False

if "activity_phase" not in st.session_state:
    st.session_state.activity_phase=False

if "interactions" not in st.session_state:
    st.session_state.interactions=[]

if "problem" not in st.session_state:
    st.session_state.problem=None

if "messages" not in st.session_state:
    st.session_state.messages=[]

user_response=st.text_input("You:",key="user_response",placeholder="Type your message here..")

if user_response:
    st.session_state.messages.append({"role":"user","content":user_response})
    if st.session_state.ind%7==0:
        st.session_state.thread_id+=1
        st.session_state.interactions=[]

    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    inputs={"key":{
        "user_response":user_response,
        "vectorstore_path":st.session_state.vectorstore_path,
        "user_problem":st.session_state.problem,
        "fun_game_initializer":st.session_state.fun_game_initializer,
        "activity_phase":st.session_state.activity_phase,
        "fun_game_phase":st.session_state.fun_game_phase,
        "i_spy_replayer":st.session_state.i_spy_replayer,
        "fun_game":{
            'type':st.session_state.fun_game_type,
            'question':st.session_state.fun_game_question
        },
        "interaction":st.session_state.interactions
    },
    "history":[("user",user_response)],
    "num_questions_asked":st.session_state.ind
    }


    for output in st.session_state.app.stream(inputs,config):
        for key,value in output.items():
            if key in ["generation","fallback"]:
                st.session_state.interactions.append(value["history"])
                st.session_state.problem=value["key"]["problem"]
                st.session_state.ind+=1

            if key in ["generation","fallback","activity_suggestor","joke_generator","motivation_generator","external_help","i_spy_replayer","service_initiator"]:
                st.session_state.messages.append({"role":"ai","content":value['key']['ai_response']})
                pprint(f"AI:{value['key']['ai_response']}")


            if key=="activity_suggestor":
                st.session_state.activity_phase=True

            if key=="fun_game_generator":
                st.session_state.messages.append({"role":"ai","content":value['key']['fun_game_generator']})
                pprint(f"AI:{value['key']['fun_game_generator']}")
                st.session_state.fun_game_initializer=True
                st.session_state.activity_phase=False

            if key=="fun_game_manager":
                fun_game_state=value["key"]["fun_game_state"]
                if fun_game_state=="Exit":
                    st.session_state.fun_game_phase=False

            if key=="i_spy_manager":
                user_answer=value["key"]["i_spy_user_answer"]
                if user_answer=="guessed":
                    st.session_state.i_spy_replayer=True

            if key=="i_spy_replay_decider":
                decider=value["key"]["i_spy_replay_decider"]
                if decider=="not_replay":
                    st.session_state.i_spy_replayer=False

            if key=="would_you_rather_question_generator":
                st.session_state.fun_game_initializer=False
                st.session_state.fun_game_phase=True
                st.session_state.fun_game_type="Would_you_rather"
                st.session_state.fun_game_question=value["key"]["would_you_rather_question"]
                st.session_state.messages.append({"role":"ai","content":value['key']['would_you_rather_question']})
                pprint(f"AI:{value['key']['would_you_rather_question']}")

            elif key=="i_spy_question_generator":
                st.session_state.fun_game_initializer=False
                st.session_state.fun_game_phase=True
                st.session_state.fun_game_type="I_spy"
                word=value["key"]["i_spy_word"]
                asked_question=value["key"]["i_spy_question"]
                question=f"""
                The word to be guessed is: {word}.
                And the asked question is: {asked_question}
                         """
                st.session_state.fun_game_question=question
                st.session_state.messages.append({"role":"ai","content":asked_question})
                pprint(f"AI:{asked_question}")


            time.sleep(3)

    # user_response=st.text_input("You:",value="",key="user_response2",placeholder="Type your message here..")


for message in st.session_state.messages:
    if message["role"]=="user":
        st.write(f"You:{message['content']}")

    else:
        st.write(f"AI:{message['content']}")