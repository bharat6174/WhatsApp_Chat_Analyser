import streamlit as st
import timeline as timeline
import seaborn as sns
import preprocessor, helper, wordcloud
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    # fetching unique users for group analysis
    user_list = df['User_Name'].unique().tolist()
    user_list.remove('Group_Notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis w.r.t", user_list)

    if st.sidebar.button("Show Analysis"):

        # Statistics
        num_messages, words,num_media, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Number of media")
            st.title(num_media)

        with col4:
            st.header("Number of Links")
            st.title(num_links)

        #Monthly Timeline
        st.header("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['Time'], timeline['Message'], 'o--', color='orangered')
        plt.xticks(rotation='vertical')
        ax.set_ylabel("Number of Messages")
        st.pyplot(fig)

        #Daily Timeline
        st.header("Daily Timeline")
        timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['only_date'], timeline['Message'], '-', color='black')
        plt.xticks(rotation='vertical')
        ax.set_ylabel("Number of Messages")
        st.pyplot(fig)

        #Activity Map:

        st.title("Activity Maps")

        col1, col2 = st.columns(2)

        with col1:
            st.header("Weekly Activity")
            busy_day = helper.weekly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(busy_day.index, busy_day.values, color='orange')
            ax.set_xlabel("Number of Messages")
            st.pyplot(fig)

        with col2:
            st.header("Monthly Activity")
            busy_month = helper.monthly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(busy_month.index, busy_month.values, color='red')
            ax.set_xlabel("Number of Messages")
            st.pyplot(fig)

        #Heatmap
        st.header("Activity heatmap")

        activity = helper.daily_activity(selected_user, df)

        fig, ax = plt.subplots()
        ax = sns.heatmap(activity)
        st.pyplot(fig)



        # Busy Users plots
        if selected_user == 'Overall':

            num_busy, pct_busy = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.header("Most busy users (Barplot)")
                ax.bar(num_busy.index, num_busy.values, color = 'orangered')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most busy users (Percentage)")
                st.dataframe(pct_busy)

        #Word Cloud

        st.title("Word Cloud")
        wc_df = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc_df)
        st.pyplot(fig)

        #Most Common Words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1], color = 'orangered')
        plt.xticks(rotation = 'vertical')

        st.header("Most frequently repeated words:")
        st.pyplot(fig)

        #Emoji Dataframe

        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.header('Emoji Repeatition')
            emoji_df = helper.num_emoji(selected_user, df)
            st.dataframe(emoji_df)

        with col2:
            st.header('Emoji Repeatition (Pie - Chart)')
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(8), labels = emoji_df[0].head(8), autopct = '%0.2f')
            st.pyplot(fig)

