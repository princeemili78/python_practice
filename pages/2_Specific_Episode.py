import streamlit as st
from episode_puller_v2 import TvShow
from episode_puller_v2 import Episode
from episode_puller_v2 import fuzzy_search_result


st.title("Specific Episodes", text_alignment="center")


if "page_2_show" not in st.session_state:
    st.session_state["page_2_show"] = ""
    
if "page_2_show_name" not in st.session_state:   
    st.session_state["page_2_show_name"] = ""
if "page_2_episode_generated" not in st.session_state:
    st.session_state["page_2_episode_generated"] = False
if "page_2_episode" not in st.session_state:
    st.session_state["page_2_episode"] = ""
if "page_2_seasons" not in st.session_state:
    st.session_state["page_2_seasons"] = []
if "season_choice" not in st.session_state:
    st.session_state["season_choice"] = None

if "previous_episode_error" not in st.session_state:
    st.session_state["previous_episode_error"] = None

if "next_episode_error" not in st.session_state:
    st.session_state["next_episode_error"] = None

if ["user_agent"] not in st.session_state:
    st.session_state["user_agent"] = st.context.headers.get("User-Agent")

if st.session_state["page_2_episode_generated"] == False:
    # textbox for user to input show name
    show_name = st.text_input("Name of Tv Show", help="Type name of show", placeholder=st.session_state["page_2_show_name"])






    # create instance of tv show using user input
    if show_name != "" and st.session_state["page_2_show_name"] != show_name :
        try:
            st.session_state["page_2_show"] = TvShow(show_name)
            st.session_state["page_2_show_name"] = show_name
            st.session_state["page_2_seasons"] = st.session_state["page_2_show"].season_list
            st.rerun()
        except Exception as e:     
            try:
                st.write(f" Did you mean {fuzzy_search_result(show_name)}")
                st.session_state["page_2_show"] = ""
                st.session_state["page_2_show_name"] = show_name
            except:
                st.write("Couldn't find a show with that name")
                st.session_state["page_2_show"] = ""
                st.session_state["page_2_show_name"] = show_name
        



    if isinstance(st.session_state["page_2_show"], TvShow):
        st.image(st.session_state["page_2_show"].picture)       
        col1, col2 = st.columns(2)
        with col1:    
            season_choice = st.selectbox("What season", options=st.session_state["page_2_show"].season_list, help="Select seasons to choose from", placeholder="Choose seasons")
            if st.session_state["season_choice"] != season_choice:
                st.session_state["season_choice"] = season_choice
                st.rerun()
        if st.session_state["season_choice"] != None:
            with col2:
                episode_number = st.selectbox("What episode", options=[episode.number for episode in st.session_state["page_2_show"].season_episode_dict[st.session_state["season_choice"]]])
                episode_list = st.session_state["page_2_show"].season_episode_dict[st.session_state["season_choice"]]
                episode = [e for e in episode_list if e.number == episode_number][0]
                if st.session_state["page_2_episode"] != episode:
                    st.session_state["page_2_episode"] = episode
                    st.rerun()
        col3,col4 = st.columns(2)
        with col3:
            st.image(st.session_state["page_2_episode"].image)
        with col4:
            st.markdown(f"# {st.session_state["page_2_episode"].name}")
            st.markdown(st.session_state["page_2_episode"].summary)  

        if st.button("Watch Epiosde!") == True:
            st.session_state["page_2_episode_generated"] = True
            st.rerun()

else:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back") == True:
            st.session_state["page_2_episode"] = ""
            st.session_state["page_2_episode_generated"] = False
            st.session_state["next_episode_error"] = None
            st.session_state["previous_episode_error"] = None
            st.rerun()
    st.markdown(f"# {st.session_state["page_2_episode"].name}")
    st.markdown(f"{st.session_state["page_2_episode"].summary}")
    # Send users to either streaming site depending on what browser they are using
    if "Firefox" in st.session_state["user_agent"]:
        if "Mobile" in st.session_state["user_agent"]:
            st.components.v1.html(f'<iframe src="https://vidsrc-embed.su/embed/tv/{st.session_state["page_2_episode"].imdb_id}/{st.session_state["page_2_episode"].season}-{st.session_state["page_2_episode"].number}" style="width: 100%; height: 220px;" frameborder="0" referrerpolicy="origin" allowfullscreen></iframe>', height=220)
        else:
            st.components.v1.html(f'<iframe src="https://vidsrc-embed.su/embed/tv/{st.session_state["page_2_episode"].imdb_id}/{st.session_state["page_2_episode"].season}-{st.session_state["page_2_episode"].number}" width="100%" height=520 allowfullscreen></iframe>', height=520)
    else:
        if "Mobile" in st.session_state["user_agent"]:
            st.components.v1.html(f'<iframe src="https://vidsrc.cc/v2/embed/tv/{st.session_state["page_2_episode"].imdb_id}/{st.session_state["page_2_episode"].season}/{st.session_state["page_2_episode"].number}" style="width: 100%; height: 220px;" frameborder="0" referrerpolicy="origin" allowfullscreen></iframe>', height=220)
        else:
            st.components.v1.html(f'<iframe src="https://vidsrc.cc/v2/embed/tv/{st.session_state["page_2_episode"].imdb_id}/{st.session_state["page_2_episode"].season}/{st.session_state["page_2_episode"].number}" style="width: 100%; height: 520px;" frameborder="0" referrerpolicy="origin" sandbox="allow-scripts allow-same-origin allow-forms"  allowfullscreen ></iframe>', height=520)
            # Below is another possible link to use to embed in case this one breaks.
            #st.components.v1.html(f'<iframe src="https://www.2embed.cc/embedtv/{st.session_state["page_2_episode"].imdb_id}&s={st.session_state["page_2_episode"].season}&e={st.session_state["page_2_episode"].number}" width="100%" height="520" allowfullscreen></iframe>', height=520)
    col4, col5 = st.columns([.85, .15])
    with col5:
        if st.button("Next Episode") == True:
                try:
                    episode = st.session_state["page_2_show"].next_episode(st.session_state["page_2_episode"])
                    if isinstance(episode, Episode):
                        st.session_state["page_2_episode"] = episode
                        st.session_state["page_2_episode_generated"] = True
                        st.session_state["previous_episode_error"] = None
                        st.rerun()
                except Exception as e:
                    st.session_state["next_episode_error"] = e
                    st.rerun()
    if st.session_state["next_episode_error"] != None:
        with col5:
            st.write("This is the last episode")
    with col4:
        if st.button("Previous Episode") == True:
                try:
                    episode = st.session_state["page_2_show"].previous_episode(st.session_state["page_2_episode"])
                    if isinstance(episode, Episode):
                        st.session_state["page_2_episode"] = episode
                        st.session_state["page_2_episode_generated"] = True
                        st.session_state["next_episode_error"] = None
                        st.rerun()
                except Exception as e:
                    st.session_state["previous_episode_error"] = e
                    st.rerun()
    if st.session_state["previous_episode_error"] != None:
        with col4:
            st.write("This is the first episode")
      
        
    