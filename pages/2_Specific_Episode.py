import streamlit as st
from episode_puller_v2 import TvShow
from episode_puller_v2 import Episode
from episode_puller_v2 import fuzzy_search_result


st.title("Specific Episodes", text_alignment="center")
#st.popover("Help", type="tertiary")


if "show" not in st.session_state:
    st.session_state["show"] = ""
    
if "show_name" not in st.session_state:   
    st.session_state["show_name"] = ""
if "episode_generated" not in st.session_state:
    st.session_state["episode_generated"] = False
if "episode" not in st.session_state:
    st.session_state["episode"] = ""
if "seasons" not in st.session_state:
    st.session_state["seasons"] = []
if "season_choice" not in st.session_state:
    st.session_state["season_choice"] = None
if "disabled" not in st.session_state:
    st.session_state["disabled"] = False

if st.session_state["episode_generated"] == False:
    # textbox for user to input show name
    show_name = st.text_input("Name of Tv Show", help="Type name of show", placeholder=st.session_state["show_name"])

    




    # create instance of tv show using user input
    if show_name != "" and st.session_state["show_name"] != show_name :
        try:
            st.session_state["show"] = TvShow(show_name)
            st.session_state["show_name"] = show_name
            st.session_state["seasons"] = st.session_state["show"].season_list
            st.rerun()
        except Exception as e:     
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
        col1, col2 = st.columns(2)
        with col1:    
            season_choice = st.selectbox("What season", options=st.session_state["show"].season_list, help="Select seasons to choose from", placeholder="Choose seasons")
            if st.session_state["season_choice"] != season_choice:
                st.session_state["season_choice"] = season_choice
                st.rerun()
        if st.session_state["season_choice"] != None:
            with col2:
                episode_choice = st.selectbox("What episode", options=st.session_state["show"].season_episode_dict[st.session_state["season_choice"]])

        if st.button("Generate episode!") == True:
            try:
                st.session_state["valid_episodes"] = st.session_state["show"].valid_episodes(rating, seasons)
                episode = st.session_state["show"].random_episode(st.session_state["valid_episodes"])
                if isinstance(episode, Episode):
                    st.session_state["episode"] = episode
                    st.session_state["rating"] = rating
                    st.session_state["seasons"] = seasons
                    st.session_state["episode_generated"] = True
                    st.session_state["valid_episodes"].remove(episode)
                    st.rerun()
            except Exception as e:
                st.write("Could not generate episode, is your rating too high?")

else:
    col10, col11 = st.columns(2)
    with col10:
        if st.button("Back") == True:
            st.session_state["episode"] = ""
            st.session_state["valid_episodes"] = []
            st.session_state["episode_generated"] = False
            st.session_state["episode_error"] = None
            st.session_state["disabled"] = False
            st.rerun()
    st.markdown(f"# {st.session_state["episode"].name}")
    st.components.v1.html(f'<iframe src="https://vidsrc-embed.ru/embed/tv/{st.session_state["episode"].imdb_id}/{st.session_state["episode"].season}-{st.session_state["episode"].number}" width="100%" height="520" allowfullscreen></iframe>', height=520)
    col3, col4 = st.columns([.69, .31])
    with col3:
        st.markdown(f"{st.session_state["episode"].season_and_number}")
        if st.session_state["episode"].rating != 0: 
            st.markdown(f"{st.session_state["episode"].rating}:star:")
    with col4:
        if st.button("Generate another episode!", disabled=st.session_state["disabled"]) == True:
                try:
                    episode = st.session_state["show"].random_episode(st.session_state["valid_episodes"])
                    if isinstance(episode, Episode):
                        st.session_state["episode"] = episode
                        st.session_state["episode_generated"] = True
                        st.session_state["valid_episodes"].remove(episode)
                        st.rerun()
                except Exception as e:
                    st.session_state["disabled"] = True
                    st.session_state["episode_error"] = e
                    st.rerun()
                    
    if st.session_state["episode_error"] != None:
        with col4:
            st.write("No more random episodes")
    col5, col6 = st.columns(2)
    col5.image(st.session_state["episode"].image)  
    col6.markdown(st.session_state["episode"].summary)      
        
    