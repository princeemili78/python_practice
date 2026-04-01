import streamlit as st
from episode_puller_v2 import TvShow
from episode_puller_v2 import fuzzy_search_result


st.title("Tv Show Randomizer")
#st.popover("Help", type="tertiary")


if "show" not in st.session_state:
    st.session_state["show"] = ""
    
if "show_name" not in st.session_state:   
    st.session_state["show_name"] = ""


# textbox for user to input show name
show_name = st.text_input("Name of Tv Show", help="Type name of show")




# create instance of tv show using user input
if show_name != "" and st.session_state["show_name"] != show_name :
    try:
        st.session_state["show"] = TvShow(show_name)
        st.session_state["show_name"] = show_name
    except Exception as e:

        st.write(e) 
        
        try:
            st.write(f" Did you mean {fuzzy_search_result(show_name)}")
            st.session_state["show"] = ""
            st.session_state["show_name"] = show_name
        except:
            st.write("Couldn't find a show with that name")
            st.session_state["show"] = ""
            st.session_state["show_name"] = show_name
      



if isinstance(st.session_state["show"], TvShow):
    st.image(st.session_state["show"].picture)         
    rating = st.number_input("Lowest rating", min_value=0.0, max_value=10.0, value="min",format="%0.1f", help="Type the lowest rated episode you'd watch", placeholder="") 
    seasons = st.multiselect("Seasons", options=range(1, 1 + st.session_state["show"].num_seasons), default=[], help="Select seasons to choose from", placeholder="Choose seasons")
    if st.button("Generate episode!") == True:
        try:
            episode = st.session_state["show"].random_episode(rating, seasons)
            st.image(episode.image)        
            st.write(f"{episode.season_and_number} {episode.name}")
            st.write(episode.summary)
        except Exception as e:
            st.write(e)

