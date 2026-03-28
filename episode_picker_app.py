import streamlit as st
from episode_puller_v2 import TvShow


st.title("Tv Show Randomizer")



if "show" not in st.session_state:
    st.session_state["show"] = ""
    
if "show_name" not in st.session_state:   
    st.session_state["show_name"] = ""


# textbox for user to input show name
show_name = st.text_input("Name of Tv Show")


# create instance of tv show using user input
if show_name != "" and "show" not in st.session_state or st.session_state["show_name"] != show_name :
    st.session_state["show"] = TvShow(show_name)
    st.session_state["last_input"] = show_name
        # number input for ratings you wanna watch

if isinstance(st.session_state["show"], TvShow):         
    rating = st.number_input("Lowest rated episode you want to watch", min_value=0.0, max_value=10.0, value=None, format="%0.1f")
    seasons = st.multiselect("Which seasons do you want to choose from", options=range(1, 1 + st.session_state["show"].num_seasons))
    if st.button("Generate episode!") == True:
        st.write(st.session_state["show"].random_episode(rating, seasons))
