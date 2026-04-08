import streamlit as st
from episode_puller_v2 import TvShow
from episode_puller_v2 import Episode
from episode_puller_v2 import fuzzy_search_result


st.title("Random Episodes", text_alignment="center")


# Block of if statements below add necessary values to session state so they are tacked each rerun
if "show" not in st.session_state:
    st.session_state["show"] = ""
    
if "show_name" not in st.session_state:   
    st.session_state["show_name"] = ""
if "episode_generated" not in st.session_state:
    st.session_state["episode_generated"] = False
if "episode" not in st.session_state:
    st.session_state["episode"] = ""
if "rating" not in st.session_state:
    st.session_state["rating"] = None
if "seasons" not in st.session_state:
    st.session_state["seasons"] = []
if "valid_episodes" not in st.session_state:
    st.session_state["valid_episodes"] = []
if "episode_error" not in st.session_state:
    st.session_state["episode_error"] = None
if "disabled" not in st.session_state:
    st.session_state["disabled"] = False
if ["user_agent"] not in st.session_state:
    st.session_state["user_agent"] = st.context.headers.get("User-Agent")


if st.session_state["episode_generated"] == False:
    # textbox for user to input show name
    show_name = st.text_input("Name of Tv Show", help="Type name of show", placeholder=st.session_state["show_name"])
   
  




# create instance of tv show using user input
    # If a user has typed a show name that is different from the show that was previously loaded
    if show_name != "" and st.session_state["show_name"] != show_name :
        try:
            st.session_state["show"] = TvShow(show_name)
            st.session_state["show_name"] = show_name
            st.rerun()
        # If loading a show creates an error, suggests a name that will work 
        # If no suggestion found, tell user could not find a show with that name
        except Exception as e:     
            try:
                st.write(f" Did you mean {fuzzy_search_result(show_name)}")
                st.session_state["show"] = ""
                st.session_state["show_name"] = show_name
            except:
                st.write("Couldn't find a show with that name")
                st.session_state["show"] = ""
                st.session_state["show_name"] = show_name
        


    # Verify that show is properly loaded
    if isinstance(st.session_state["show"], TvShow):
        st.image(st.session_state["show"].picture)         
        rating = st.number_input("Lowest rating", min_value=0.0, max_value=10.0, value=st.session_state["rating"],format="%0.1f", help="Type the lowest rated episode you'd watch", step=0.5) 
        seasons = st.multiselect("Seasons", options=st.session_state["show"].season_list, default=st.session_state["seasons"], help="Select seasons to choose from", placeholder="Choose seasons")
        # A list of episodes satisfying the user's requirements is created, then an episode is chosen from it randomly
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
# After an episode has been generated a page with the episode and other information is generated for the user
else:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back") == True:
            st.session_state["episode"] = ""
            st.session_state["valid_episodes"] = []
            st.session_state["episode_generated"] = False
            st.session_state["episode_error"] = None
            st.session_state["disabled"] = False
            st.rerun()
    st.markdown(f"# {st.session_state["episode"].name}")
    if "Firefox" in st.session_state["user_agent"]:
        if "Mobile" in st.session_state["user_agent"]:
            st.components.v1.html(f'<iframe src="https://vidsrc-embed.su/embed/tv/{st.session_state["episode"].imdb_id}/{st.session_state["episode"].season}-{st.session_state["episode"].number}" style="width: 100%; height: 220px;" frameborder="0" referrerpolicy="origin" sandbox="allow-scripts allow-same-origin allow-forms" allowfullscreen></iframe>', height=220)
        else:
            st.components.v1.html(f'<iframe src="https://vidsrc-embed.su/embed/tv/{st.session_state["episode"].imdb_id}/{st.session_state["episode"].season}-{st.session_state["episode"].number}" width="100%" height=520 sandbox="allow-scripts allow-same-origin allow-forms" allowfullscreen></iframe>', height=520)
    else:
        if "Mobile" in st.session_state["user_agent"]:
            st.components.v1.html(f'<iframe src="https://vidsrc.cc/v2/embed/tv/{st.session_state["episode"].imdb_id}/{st.session_state["episode"].season}/{st.session_state["episode"].number}" style="width: 100%; height: 220px;" frameborder="0" referrerpolicy="origin" sandbox="allow-scripts allow-same-origin allow-forms" allowfullscreen></iframe>', height=220)
        else:
            st.components.v1.html(f'<iframe src="https://vidsrc.cc/v2/embed/tv/{st.session_state["episode"].imdb_id}/{st.session_state["episode"].season}/{st.session_state["episode"].number}" style="width: 100%; height: 520px;" frameborder="0" referrerpolicy="origin" sandbox="allow-scripts allow-same-origin allow-forms" allowfullscreen></iframe>', height=520)
            # Below is another possible link to use to embed in case this one breaks.
            #st.components.v1.html(f'<iframe src="https://www.2embed.cc/embedtv/{st.session_state["episode"].imdb_id}&s={st.session_state["episode"].season}&e={st.session_state["episode"].number}" width="100%" height="520" allowfullscreen></iframe>', height=520)"https://vidsrc-embed.ru/embed/tv/{st.session_state["episode"].imdb_id}/{st.session_state["episode"].season}-{st.session_state["episode"].number}" width="100%" height="520" allowfullscreen></iframe>', height=520)
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
        
    