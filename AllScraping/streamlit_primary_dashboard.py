import streamlit as st
from streamlit_autorefresh import st_autorefresh


import json
from datetime import datetime
import pytz
import sys


st_autorefresh(interval= 0.03 * 60 * 1000, key="dataframerefresh")

def streamlit_main():
    print()

    last_streamlit_refresh = timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")
    st.title("Prelude to Chaos 2.0")

    #f = open(sys.path[0] + '/../data.yml') #latest_streamlit_json_payload.json
    with open('latest_streamlit_json_payload.json') as json_file:
        payload = json.load(json_file)
    
    #title games

    sofa_game_json = payload['game_names']['sofa_games']
    caesars_game_json = payload['game_names']['caesars_games']
    draftkings_game_json = payload['game_names']['draftkings_games']
    fanduel_game_json = payload['game_names']['fanduel_games']

    st.write(f"Payload last updated:   {payload['timestamp']}")
    st.write(f"Streamlit last updated:   {last_streamlit_refresh}")

    st.markdown(f'<h1 style="color:#33ff33;font-size:14px;"> Glitches </h1>', unsafe_allow_html=True)
    st.write(payload['global_glitches'])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.header(f"Sofascore")
        st.markdown(f'<h1 style="color:#FFFFFF;font-size:14px;"> {len(sofa_game_json)} Games </h1>', unsafe_allow_html=True)
        with st.expander(f"Sofa Games"):
            for item in sorted(sofa_game_json):
                st.markdown(f"\t - {item}")
    with col2:
        st.header(f"Caesars")
        st.markdown(f'<h1 style="color:#FFFFFF;font-size:14px;"> {len(caesars_game_json)} Games </h1>', unsafe_allow_html=True)
        with st.expander(f"Caesars Games"):
            for item in sorted(caesars_game_json):
                st.markdown(f"\t - {item}")
        st.text("Anchored Games")
        st.write(payload['intersection']['caesars_games'])
    with col3:
        st.header(f"Draftkings")
        st.markdown(f'<h1 style="color:#FFFFFF;font-size:14px;"> {len(draftkings_game_json)} Games </h1>', unsafe_allow_html=True)
        with st.expander(f"Draftkings Games"):
            for item in sorted(draftkings_game_json):
                st.markdown(f"\t - {item}")
        st.text("Anchored Games")
        st.write(list(payload['intersection']['draftkings_games']))
    with col4:
        st.header(f"Fanduel")
        st.markdown(f'<h1 style="color:#FFFFFF;font-size:14px;"> {len(fanduel_game_json)} Games </h1>', unsafe_allow_html=True)
        with st.expander(f"Fanduel Games"):
            for item in sorted(fanduel_game_json):
                st.markdown(f"\t - {item}")
        st.text("Anchored Games")
        st.write(list(payload['intersection']['fanduel_games']))

    st.header("Game Analysis Lines")
    col1a, col2a, col3a = st.columns(3)

    def generate_analysis(sportsbook):
        with st.expander(f"{sportsbook}"):
            st.header(sportsbook.capitalize())
            for game_name in payload['analysis'][sportsbook]:
                # with st.expander(f"{game_name}"):
                st.markdown("""---""")
                st.markdown(f'<h1 style="color:#FFA500;font-size:22px;">{game_name}</h1>', unsafe_allow_html=True)
                
                for line_name in payload['analysis'][sportsbook][game_name]:
                    set_matching = payload['analysis'][sportsbook][game_name][line_name]['set_matching']
                    game_matching = payload['analysis'][sportsbook][game_name][line_name]['game_matching']
                    point_matching = payload['analysis'][sportsbook][game_name][line_name]['point_matching']
                    glitch = payload['analysis'][sportsbook][game_name][line_name]['glitches']
                    st.markdown(f'<h1 style="color:#FFFFFF;font-size:16px;">{line_name}</h1>', unsafe_allow_html=True)
                    if set_matching:
                        st.markdown(f'<h1 style="color:#33ff33;font-size:14px;">{set_matching}</h1>', unsafe_allow_html=True)
                    if game_matching:
                        st.markdown(f'<h1 style="color:#33ff33;font-size:14px;">{game_matching}</h1>', unsafe_allow_html=True)
                    if point_matching:
                        st.markdown(f'<h1 style="color:#33ff33;font-size:14px;">{point_matching}</h1>', unsafe_allow_html=True)
                    st.markdown(f'<h1 style="color:#ff6961;font-size:10px;">Glitches: {glitch}</h1>', unsafe_allow_html=True)            
    
    
    with col1a: generate_analysis("caesars")
    with col2a: generate_analysis("draftkings")
    with col3a: generate_analysis("fanduel")
        

    #Displaying no analysis lines
    st.header("No analysis lines")
    col1b, col2b, col3b = st.columns(3)
    with col1b: 
        st.header('Caesars')
        for game_name in payload['no_analysis']['caesars']:
            with st.expander(game_name):
                for gameline in payload['no_analysis']['caesars'][game_name]:
                    st.markdown(f"\t{gameline}")
    with col2b: 
        st.header('Draftkings')
        for game_name in payload['no_analysis']['draftkings']:
            with st.expander(game_name):
                for gameline in payload['no_analysis']['draftkings'][game_name]:
                    st.markdown(f"\t{gameline}")

    with col3b: 
        st.header('Fanduel')
        for game_name in payload['no_analysis']['fanduel']:
            with st.expander(game_name):
                for gameline in payload['no_analysis']['fanduel'][game_name]:
                    st.markdown(f"\t{gameline}")

    print(f"Payload successfully processed at: {payload['timestamp']}")
if __name__ == "__main__":
    streamlit_main()