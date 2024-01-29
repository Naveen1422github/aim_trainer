import pandas as pd
import streamlit as st
    # streamlit functioning
        
st.set_page_config(layout="wide")

stats = st.empty()

st.write("---")

df = pd.read_csv(r'Output\pink_circle_coordinates.csv')

          
with stats:
    tab, video, image1, image2 = st.columns(4)
    
    with tab:
        st.table(df)

    with video:
        for index, row in df.iterrows():
            video_path = f"Output/path_visualization_{index}.mp4"
            button_label = f"Play Video {index + 1}"

            if st.button(button_label, key=f"button_{index}"):
                # Store the selected video path in a SessionState variable
                st.session_state.selected_video_path = video_path

    with image1:
        # Display the selected video in the image1 column
        selected_video_path = getattr(st.session_state, 'selected_video_path', None)
        if selected_video_path:
            st.video(selected_video_path)
        else:
            st.image('Output/series_shots.png')
    
    with image2:
      st.image('Output/series_shots.png')




        
