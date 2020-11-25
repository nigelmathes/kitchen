"""
This serves a custom window display, showing off the input ingredients for this Dish.

i.e. A Streamlit app, based heavily on the Streamlit self-driving demo:
     https://github.com/streamlit/demo-self-driving
"""
import os
import requests

import cv2

import altair as alt
import streamlit as st
import numpy as np
import pandas as pd


# Path to the Streamlit public S3 bucket
DATA_URL_ROOT = "https://streamlit-self-driving.s3-us-west-2.amazonaws.com/"


def create_window_display():
    """
    Create a window display from image data to advertise your dish

    i.e. Create an automatic EDA report for image data which will be viewable
         through the web API

    Returns:
        None, but serves a Streamlit-based display at the default port of 80
    """

    @st.cache
    def load_metadata(url):
        return pd.read_csv(url)

    # This function uses some Pandas magic to summarize the metadata Dataframe.
    @st.cache
    def create_summary(metadata: pd.DataFrame):
        one_hot_encoded = pd.get_dummies(
            metadata[["frame", "label"]], columns=["label"]
        )
        summary = (
            one_hot_encoded.groupby(["frame"])
            .sum()
            .rename(
                columns={
                    "label_biker": "biker",
                    "label_car": "car",
                    "label_pedestrian": "pedestrian",
                    "label_trafficLight": "traffic light",
                    "label_truck": "truck",
                }
            )
        )
        return summary

    image_metadata = load_metadata(os.path.join(DATA_URL_ROOT, "labels.csv.gz"))
    data_summary = create_summary(metadata=image_metadata)

    # Show the metadata DataFrame as a table
    st.write("## Metadata", image_metadata[:1000], "## Summary", data_summary[:1000])

    # Draw the UI elements to search for objects (pedestrians, cars, etc.)
    selected_frame_index, selected_frame = frame_selector_ui(data_summary)
    if selected_frame_index is None:
        st.error("No frames fit the criteria. Please select different label or number.")
        return

    # Load the image from S3.
    image_url = os.path.join(DATA_URL_ROOT, selected_frame)
    image = load_image(image_url)

    # Add boxes for objects on the image. These are the boxes for the ground image.
    boxes = image_metadata[image_metadata.frame == selected_frame].drop(
        columns=["frame"]
    )
    draw_image_with_boxes(
        image,
        boxes,
        "Ground Truth",
        "**Human-annotated data** (frame `%i`)" % selected_frame_index,
    )


def frame_selector_ui(summary):
    st.sidebar.markdown("# Frame")

    # The user can pick which type of object to search for.
    object_type = st.sidebar.selectbox("Search for which objects?", summary.columns, 2)

    # The user can select a range for how many of the selected object should be present.
    min_elts, max_elts = st.sidebar.slider(
        "How many %ss (select a range)?" % object_type, 0, 25, [10, 20]
    )
    selected_frames = get_selected_frames(summary, object_type, min_elts, max_elts)
    if len(selected_frames) < 1:
        return None, None

    # Choose a frame out of the selected frames.
    selected_frame_index = st.sidebar.slider(
        "Choose a frame (index)", 0, len(selected_frames) - 1, 0
    )

    # Draw an altair chart in the sidebar with information on the frame.
    objects_per_frame = (
        summary.loc[selected_frames, object_type].reset_index(drop=True).reset_index()
    )
    chart = (
        alt.Chart(objects_per_frame, height=120)
        .mark_area()
        .encode(
            alt.X("index:Q", scale=alt.Scale(nice=False)), alt.Y("%s:Q" % object_type)
        )
    )
    selected_frame_df = pd.DataFrame({"selected_frame": [selected_frame_index]})
    vline = (
        alt.Chart(selected_frame_df).mark_rule(color="red").encode(x="selected_frame")
    )
    st.sidebar.altair_chart(alt.layer(chart, vline))

    selected_frame = selected_frames[selected_frame_index]
    return selected_frame_index, selected_frame


def draw_image_with_boxes(image, boxes, header, description):
    label_colors = {
        "car": [255, 0, 0],
        "pedestrian": [0, 255, 0],
        "truck": [0, 0, 255],
        "trafficLight": [255, 255, 0],
        "biker": [255, 0, 255],
    }
    image_with_boxes = image.astype(np.float64)
    for _, (xmin, ymin, xmax, ymax, label) in boxes.iterrows():
        image_with_boxes[
            int(ymin) : int(ymax), int(xmin) : int(xmax), :
        ] += label_colors[label]
        image_with_boxes[int(ymin) : int(ymax), int(xmin) : int(xmax), :] /= 2

    # Draw the header and image.
    st.subheader(header)
    st.markdown(description)
    st.image(image_with_boxes.astype(np.uint8), use_column_width=True)


@st.cache(hash_funcs={np.ufunc: str})
def get_selected_frames(summary, label, min_elts, max_elts):
    return summary[
        np.logical_and(summary[label] >= min_elts, summary[label] <= max_elts)
    ].index


@st.cache(show_spinner=False)
def load_image(url: str) -> np.array:
    response = requests.get(url=url, stream=True).raw
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = image[:, :, [2, 1, 0]]  # BGR -> RGB

    return image


if __name__ == "__main__":
    create_window_display()
