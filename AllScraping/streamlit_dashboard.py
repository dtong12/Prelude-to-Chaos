import streamlit as st


import sofascoreParser as sofascoreParser
import masterClass as masterClass

st.title("""
Visualization for alarm dashboard
""")



sofascore_data = sofascoreParser.ingest_softscore_data()
col1, col2, col3 = st.columns(3)
with col1: 
    st.header("Sofascore")
    for item in sorted(sofascore_data.keys()):
        st.markdown(f"\t - {item}")
with col2: 
    st.header("Caesars")
    for item in sorted(sofascore_data.keys()):
        st.markdown(f"\t - {item}")

with col3: 
    st.header("Draftkings")
    for item in sorted(sofascore_data.keys()):
        st.markdown(f"\t - {item}")

sofascore_display =  []
for key in sofascore_data:
    pretty_print = vars(sofascore_data[key])
    sub_item = {}
    for thing in pretty_print:
        try:
            if thing != 'input': 
                sub_item[thing] = pretty_print[thing]
        except Exception as e:
            print(e)
        pass
    sofascore_display.append(sub_item)


st.header("All current sofascore games")
st.write(sofascore_display)


#masterClass.main()
